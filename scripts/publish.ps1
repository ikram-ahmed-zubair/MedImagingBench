
$ErrorActionPreference = "Stop"

# Always run from the root of this project.
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $repoRoot

Write-Host "`n=== MedImagingBench Publish ===" -ForegroundColor Cyan

# Verify the Git repository.
$gitRootOutput = & git rev-parse --show-toplevel
if ($LASTEXITCODE -ne 0) {
    throw "This directory is not inside a Git repository."
}

$gitRoot = (Resolve-Path "$gitRootOutput").Path
if ($gitRoot -ne $repoRoot) {
    throw "The Git root does not match the project root. Stopping."
}

$branch = (& git branch --show-current).Trim()
if ([string]::IsNullOrWhiteSpace($branch)) {
    throw "No Git branch is checked out."
}

$originUrl = & git remote get-url origin 2>$null
if ($LASTEXITCODE -ne 0 -or
    [string]::IsNullOrWhiteSpace(($originUrl -join ""))) {
    throw "Git remote 'origin' is not configured."
}

Write-Host "Branch: $branch"
Write-Host "Remote: origin"

# Do not mix previously staged changes into this operation.
& git diff --cached --quiet
$stagedExitCode = $LASTEXITCODE

if ($stagedExitCode -eq 1) {
    throw "Staged changes already exist. Review them before using this script."
}
if ($stagedExitCode -ne 0) {
    throw "Could not inspect the Git staging area."
}

# Run the existing tests, lint, and formatting checks.
$checkScript = Join-Path $PSScriptRoot "check.ps1"
if (-not (Test-Path $checkScript)) {
    throw "scripts/check.ps1 was not found."
}

Write-Host "`n=== Running project checks ===" -ForegroundColor Cyan
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File $checkScript

if ($LASTEXITCODE -ne 0) {
    throw "Checks failed. Nothing was committed or pushed."
}

# Show current changes.
Write-Host "`n=== Current changes ===" -ForegroundColor Cyan
& git status --short

$changes = @(& git status --short)
if ($LASTEXITCODE -ne 0) {
    throw "Could not read Git status."
}
if ($changes.Count -eq 0) {
    Write-Host "No changes to publish." -ForegroundColor Yellow
    return
}

Write-Host "`nEnter only the file paths you want to publish."
Write-Host "Separate paths with commas."
Write-Host "Example: src/medbench/arrays.py,tests/test_smoke.py"

$pathInput = Read-Host "Approved file paths"
$selectedPaths = @(
    $pathInput -split "," |
        ForEach-Object { $_.Trim() } |
        Where-Object { $_ -ne "" }
)

if ($selectedPaths.Count -eq 0) {
    Write-Host "Cancelled. No files were staged." -ForegroundColor Yellow
    return
}

# Explicitly block the unrelated JDK and Jupyter notebooks.
$unsafePaths = @(
    $selectedPaths | Where-Object {
        $_ -match '(^|[\\/])oracleJdk-27([\\/]|$)' -or
        $_ -match '\.ipynb$'
    }
)

if ($unsafePaths.Count -gt 0) {
    throw "The Java JDK and Jupyter notebooks cannot be selected for publishing."
}

# Stage only the exact paths that you entered.
& git add -- $selectedPaths
if ($LASTEXITCODE -ne 0) {
    throw "Git could not stage the selected paths."
}

# Verify that the selected paths produced staged changes.
& git diff --cached --quiet
$diffExitCode = $LASTEXITCODE

if ($diffExitCode -eq 0) {
    Write-Host "No changes were staged from those paths." -ForegroundColor Yellow
    return
}
if ($diffExitCode -ne 1) {
    throw "Could not inspect the staged changes."
}

# Check and display the exact changes before committing.
& git diff --cached --check
if ($LASTEXITCODE -ne 0) {
    & git reset
    throw "Staged changes have whitespace errors. Changes were unstaged."
}

Write-Host "`n=== Files staged for publishing ===" -ForegroundColor Cyan
& git diff --cached --name-status
& git --no-pager diff --cached --stat

Write-Host "`n=== Review the staged diff ===" -ForegroundColor Cyan
& git --no-pager diff --cached

$commitMessage = Read-Host "`nEnter a commit message"
if ([string]::IsNullOrWhiteSpace($commitMessage)) {
    & git reset
    Write-Host "Cancelled. Your file edits were preserved." -ForegroundColor Yellow
    return
}

$confirmation = Read-Host "Type PUBLISH to commit and push these changes"
if ($confirmation -cne "PUBLISH") {
    & git reset
    Write-Host "Cancelled. Changes were unstaged; file edits were preserved." -ForegroundColor Yellow
    return
}

# Commit locally.
& git commit -m $commitMessage
if ($LASTEXITCODE -ne 0) {
    throw "Commit failed. No push was attempted."
}

# Push the current branch without force-pushing.
& git push -u origin $branch
if ($LASTEXITCODE -ne 0) {
    throw "Push failed. The commit remains local; inspect the Git error."
}

Write-Host "`nPush completed. Check GitHub Actions for the remote CI result." -ForegroundColor Green
