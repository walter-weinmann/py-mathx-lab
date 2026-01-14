# Copyright (c) 2022-2025 IO-Swiss Aero GmbH. All rights reserved.
# Use of this source code is governed by the IO-Swiss Aero GmbH
# License, that can be found in the LICENSE.md file.

"""Sphinx extension providing an ``eval-rst`` directive for MyST Markdown.

The documentation in this repository is primarily written in MyST Markdown.
Some pages embed reStructuredText (reST) blocks using a directive-like block
such as::

    :::{eval-rst}
    .. autoclass:: mathxlab.exp.cli.ExperimentArgs
       :members:
    :::

Modern ``myst-parser`` versions do not support ``eval-rst`` as a MyST extension
name, and they do not ship a built-in directive of that name. Without a working
``eval-rst`` directive, embedded autodoc markup can render literally (e.g.
showing ``.. py:class::`` blocks in the output).

This extension registers a docutils directive called ``eval-rst``. The directive
parses its body as reStructuredText within the *current* Sphinx document, so all
Sphinx directives (autodoc, autosummary, references, etc.) behave as expected.
"""

from __future__ import annotations

from docutils import nodes
from docutils.parsers.rst import Directive
from docutils.statemachine import ViewList
from sphinx.util.nodes import nested_parse_with_titles


class EvalRstDirective(Directive):
    """Directive that parses its content as reStructuredText."""

    has_content = True

    def run(self) -> list[nodes.Node]:
        """Parse directive content as reST and return the resulting nodes.

        Returns:
            A list of docutils nodes produced by parsing the directive body.
        """
        container = nodes.container()

        # Build a ViewList with proper source/line information to get readable
        # warnings and correct backlinks in the rendered output.
        view = ViewList()
        source = self.state.document.current_source or "eval-rst"
        base_line = max(self.lineno - 1, 0)
        for i, line in enumerate(self.content):
            view.append(line, source, base_line + i)

        nested_parse_with_titles(self.state, view, container)
        return list(container.children)


def setup(app):  # type: ignore[no-untyped-def]
    """Register the directive with Sphinx."""
    app.add_directive("eval-rst", EvalRstDirective)
    return {
        "version": "0.2",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
