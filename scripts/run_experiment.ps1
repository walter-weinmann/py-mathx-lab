# Run an experiment with structured logging (Windows PowerShell 5.1 compatible).
#
# Called from Makefile; can also be run manually:
#   powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_experiment.ps1 -Exp e001 -Uv uv -Args "--seed 1" -VerboseFlag 1
#
# Features:
# - Writes UTF-8 logs (no UTF-16/NUL noise).
# - Captures BOTH: `uv sync --extra dev` output and the experiment output.
# - Shows DEBUG only from your code if your Python logging setup enforces it.

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$Exp,

    [Parameter(Mandatory = $false)]
    [string]$Uv = "uv",

    [Parameter(Mandatory = $false)]
    [string]$Args = "",

    [Parameter(Mandatory = $false)]
    [string]$VerboseFlag = "0",

    [Parameter(Mandatory = $false)]
    [string]$OutRoot = "out"
)

$ErrorActionPreference = "Stop"

function Write-LogLine {
    param(
        [Parameter(Mandatory = $true)][string]$Line,
        [Parameter(Mandatory = $true)][string]$LogPath
    )
    Write-Output $Line
    $Line | Out-File -FilePath $LogPath -Append -Encoding utf8
}

function Run-And-Log {
    param(
        [Parameter(Mandatory = $true)][scriptblock]$Command,
        [Parameter(Mandatory = $true)][string]$LogPath
    )

    & $Command 2>&1 | ForEach-Object {
        $_ | Write-Output
        $_ | Out-File -FilePath $LogPath -Append -Encoding utf8
    }

    return $LASTEXITCODE
}

$outDir = Join-Path $OutRoot $Exp
$logDir = Join-Path $outDir "logs"
New-Item -ItemType Directory -Force -Path $logDir | Out-Null

$ts  = Get-Date -Format "yyyyMMdd_HHmmss"
$log = Join-Path $logDir ("run_{0}_{1}.log" -f $Exp, $ts)

$verboseArg = ""
if ($VerboseFlag -eq "1") {
    $verboseArg = "-v"
}

Write-LogLine ("COMMAND: {0} sync --extra dev" -f $Uv) $log
Write-LogLine (("COMMAND: {0} run --extra dev python -m mathxlab.experiments.{1} --out {2} {3} {4}" -f $Uv, $Exp, $outDir, $verboseArg, $Args).Trim()) $log
Write-LogLine ("START:   {0}" -f (Get-Date -Format o)) $log
Write-LogLine ("PWD:     {0}" -f (Get-Location)) $log
Write-LogLine ("UV:      {0}" -f (& $Uv --version)) $log
Write-LogLine ("PY:      {0}" -f (& $Uv run --extra dev python -V 2>&1)) $log

try {
    Write-LogLine ("GIT:     {0}" -f (& git rev-parse --short HEAD 2>$null)) $log
} catch {
    # ignore
}

Write-LogLine "" $log
Write-Host ("Logging to: " + $log)

Write-LogLine "---- uv sync --extra dev ----" $log
$codeSync = Run-And-Log { & $Uv sync --extra dev } $log
if ($codeSync -ne 0) {
    Write-LogLine ("uv sync failed with exit code: {0}" -f $codeSync) $log
    exit $codeSync
}

Write-LogLine "" $log
Write-LogLine "---- experiment run ----" $log
$codeRun = Run-And-Log { & $Uv run --extra dev python -m ("mathxlab.experiments.{0}" -f $Exp) --out $outDir $verboseArg $Args } $log

Write-LogLine "" $log
Write-LogLine ("END:     {0}" -f (Get-Date -Format o)) $log
Write-LogLine ("EXIT:    {0}" -f $codeRun) $log

exit $codeRun
