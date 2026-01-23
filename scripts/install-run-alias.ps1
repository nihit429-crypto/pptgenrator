<#
Install a persistent `run` command into the current user's PowerShell profile.
Usage (from repo root):
    powershell -ExecutionPolicy Bypass -File .\scripts\install-run-alias.ps1
This will append a small function to your $PROFILE that changes to the repo folder and runs `run.bat`.
#>

$repo = (Resolve-Path "$PSScriptRoot\..").Path
$profilePath = $PROFILE

if (-not (Test-Path -Path $profilePath)) {
    New-Item -Type File -Force -Path $profilePath -ErrorAction SilentlyContinue | Out-Null
}

$marker = "run alias installed"

if (Test-Path -Path $profilePath) {
    $content = Get-Content -Path $profilePath -Raw
    if ($content -match $marker) {
        Write-Host "'run' already installed"
        exit 0
    }
}

$func = @"

# >>> run alias installed
function run {
    Push-Location '$repo'
    try {
        & .\run.bat `$args
    } finally {
        Pop-Location
    }
}
# <<< run alias installed
"@

Add-Content -Path $profilePath -Value $func
Write-Host "Installed 'run' into $profilePath"
Write-Host "Restart PowerShell or run: . `$PROFILE"
