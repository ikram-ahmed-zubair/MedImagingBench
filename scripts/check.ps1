[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"
$projectRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot ".."))
$python = Join-Path $projectRoot ".venv\Scripts\python.exe"
$ruff = Join-Path $projectRoot ".venv\Scripts\ruff.exe"

foreach ($tool in @($python, $ruff)) {
    if (-not (Test-Path -LiteralPath $tool -PathType Leaf)) {
        Write-Host "FAIL: Required project tool not found: $tool" -ForegroundColor Red
        exit 1
    }
}

$checks = @(
    [pscustomobject]@{
        Name = "Tests"
        Executable = $python
        Arguments = @("-m", "pytest", "-q")
    },
    [pscustomobject]@{
        Name = "Lint"
        Executable = $ruff
        Arguments = @("check", ".")
    },
    [pscustomobject]@{
        Name = "Formatting"
        Executable = $ruff
        Arguments = @("format", "--check", ".")
    }
)

$results = @()
Push-Location $projectRoot
try {
    foreach ($check in $checks) {
        Write-Host "`nRunning $($check.Name)..." -ForegroundColor Cyan
        & $check.Executable @($check.Arguments)
        $exitCode = $LASTEXITCODE

        if ($exitCode -eq 0) {
            Write-Host "PASS: $($check.Name)" -ForegroundColor Green
            $results += [pscustomobject]@{ Name = $check.Name; Passed = $true }
        }
        else {
            Write-Host "FAIL: $($check.Name) (exit code $exitCode)" -ForegroundColor Red
            $results += [pscustomobject]@{ Name = $check.Name; Passed = $false }
        }
    }
}
finally {
    Pop-Location
}

Write-Host "`nCheck summary:"
$results | ForEach-Object {
    $status = if ($_.Passed) { "PASS" } else { "FAIL" }
    Write-Host "  $status - $($_.Name)"
}

if ($results.Where({ -not $_.Passed }).Count -gt 0) {
    exit 1
}

exit 0
