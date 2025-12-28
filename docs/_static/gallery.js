/* Gallery search + tag filter for the experiments gallery.
 *
 * This is intentionally dependency-free and compatible with static Sphinx builds.
 */
(function () {
  "use strict";

  function uniq(arr) {
    return Array.from(new Set(arr));
  }

  function parseTagsFromCard(card) {
    const raw = (card.dataset.tags || "").trim();
    if (raw) {
      return raw.split(",").map((t) => t.trim()).filter(Boolean);
    }
    const spans = Array.from(card.querySelectorAll(".gallery-tags .tag"));
    return spans.map((s) => (s.textContent || "").trim()).filter(Boolean);
  }

  function normalize(s) {
    return (s || "").toLowerCase().trim();
  }

  function buildIndex(cards) {
    return cards.map((card) => {
      const title = card.dataset.title || (card.querySelector("h3")?.textContent || "");
      const desc = card.dataset.desc || (card.querySelector("p")?.textContent || "");
      const tags = parseTagsFromCard(card);
      const haystack = normalize([title, desc, tags.join(" ")].join(" "));
      return { card, title, desc, tags, haystack };
    });
  }

  function getToolbarEls() {
    return {
      input: document.getElementById("gallery-search"),
      clearBtn: document.getElementById("gallery-clear"),
      tagCloud: document.getElementById("gallery-tag-cloud"),
      count: document.getElementById("gallery-count"),
    };
  }

  function readInitialState() {
    const params = new URLSearchParams(window.location.search);
    const q = params.get("q") || "";
    const tagsParam = params.get("tags") || "";
    const tags = tagsParam
      ? tagsParam.split(",").map((t) => t.trim()).filter(Boolean)
      : [];
    return { q, tags: uniq(tags) };
  }

  function writeStateToUrl(q, selectedTags) {
    const url = new URL(window.location.href);
    const params = url.searchParams;

    if (q) {
      params.set("q", q);
    } else {
      params.delete("q");
    }

    if (selectedTags.length) {
      params.set("tags", selectedTags.join(","));
    } else {
      params.delete("tags");
    }

    // Preserve current hash (if any).
    url.search = params.toString();
    window.history.replaceState({}, "", url.toString());
  }

  function renderTagCloud(tagCloudEl, tagCounts, selectedTagsSet, onToggle) {
    tagCloudEl.innerHTML = "";
    const items = Array.from(tagCounts.entries());

    // sort: most frequent first, then alphabetical
    items.sort((a, b) => {
      if (b[1] !== a[1]) return b[1] - a[1];
      return a[0].localeCompare(b[0]);
    });

    for (const [tag, count] of items) {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "gallery-tag-chip" + (selectedTagsSet.has(tag) ? " is-active" : "");
      btn.setAttribute("data-tag", tag);
      btn.setAttribute("aria-pressed", selectedTagsSet.has(tag) ? "true" : "false");
      btn.title = `${tag} (${count})`;

      const label = document.createElement("span");
      label.className = "chip-label";
      label.textContent = tag;

      const badge = document.createElement("span");
      badge.className = "chip-count";
      badge.textContent = String(count);

      btn.appendChild(label);
      btn.appendChild(badge);

      btn.addEventListener("click", () => onToggle(tag));
      tagCloudEl.appendChild(btn);
    }
  }

  function applyFilters(index, q, selectedTagsSet) {
    const qn = normalize(q);
    let visible = 0;

    for (const item of index) {
      const matchesQuery = !qn || item.haystack.indexOf(qn) !== -1;
      const matchesTags =
        selectedTagsSet.size === 0 ||
        Array.from(selectedTagsSet.values()).every((t) => item.tags.includes(t));

      const ok = matchesQuery && matchesTags;
      item.card.classList.toggle("is-hidden", !ok);
      if (ok) visible += 1;
    }
    return visible;
  }

  function main() {
    const grid = document.querySelector('.gallery-grid[data-gallery="experiments"]') || document.querySelector(".gallery-grid");
    if (!grid) return;

    const cards = Array.from(grid.querySelectorAll("a.gallery-card"));
    if (!cards.length) return;

    const els = getToolbarEls();
    if (!els.input || !els.clearBtn || !els.tagCloud || !els.count) return;

    const index = buildIndex(cards);

    // Tag histogram
    const tagCounts = new Map();
    for (const item of index) {
      for (const t of item.tags) {
        tagCounts.set(t, (tagCounts.get(t) || 0) + 1);
      }
    }

    // Initial state from URL
    const init = readInitialState();
    const selected = new Set(init.tags);

    if (init.q) {
      els.input.value = init.q;
    }

    function update() {
      const q = els.input.value || "";
      const visible = applyFilters(index, q, selected);
      els.count.textContent = `Showing ${visible} of ${index.length} experiments`;
      renderTagCloud(els.tagCloud, tagCounts, selected, toggleTag);
      writeStateToUrl(q, Array.from(selected.values()));
    }

    function toggleTag(tag) {
      if (selected.has(tag)) selected.delete(tag);
      else selected.add(tag);
      update();
    }

    function clearAll() {
      els.input.value = "";
      selected.clear();
      update();
      els.input.focus();
    }

    // Debounce typing a little
    let tId = null;
    els.input.addEventListener("input", () => {
      if (tId) window.clearTimeout(tId);
      tId = window.setTimeout(update, 80);
    });

    els.clearBtn.addEventListener("click", clearAll);

    // Allow ESC to clear search quickly
    els.input.addEventListener("keydown", (ev) => {
      if (ev.key === "Escape") {
        ev.preventDefault();
        clearAll();
      }
    });

    update();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", main);
  } else {
    main();
  }
})();
