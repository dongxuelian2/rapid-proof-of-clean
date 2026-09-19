$ErrorActionPreference = "Stop"

$repositoryRoot = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $repositoryRoot

function Invoke-Checked {
    param(
        [Parameter(Mandatory = $true)]
        [string]$FilePath,
        [Parameter(Mandatory = $false)]
        [string[]]$Arguments = @()
    )

    & $FilePath @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Command failed with exit code $LASTEXITCODE`: $FilePath $($Arguments -join ' ')"
    }
}

$virtualEnvironmentPath = Join-Path $repositoryRoot ".venv"
$virtualEnvironmentPython = Join-Path $virtualEnvironmentPath "Scripts\python.exe"
$uvCommand = Get-Command uv -ErrorAction SilentlyContinue

if ($null -ne $uvCommand) {
    $uvPath = $uvCommand.Source
    $cachePath = Join-Path $repositoryRoot ".uv-cache"

    if (-not (Test-Path -LiteralPath $virtualEnvironmentPython)) {
        Write-Host "Creating the project virtual environment with uv..."
        Invoke-Checked $uvPath @("--cache-dir", $cachePath, "venv", ".venv", "--python", "3.12")
    }

    $syncArguments = @("--cache-dir", $cachePath, "sync", "--extra", "dev")
    if (Test-Path -LiteralPath (Join-Path $repositoryRoot "uv.lock")) {
        $syncArguments += "--locked"
    }
    Write-Host "Installing the project and development dependencies with uv..."
    Invoke-Checked $uvPath $syncArguments
} else {
    $pythonCommand = Get-Command python -ErrorAction SilentlyContinue
    if ($null -eq $pythonCommand) {
        throw "Neither uv nor a usable python command was found. Install one project-local tool and rerun this script."
    }

    try {
        & $pythonCommand.Source --version *> $null
    } catch {
        throw "The python command is present but could not be executed. Install a usable Python or uv and rerun this script."
    }
    if ($LASTEXITCODE -ne 0) {
        throw "The python command is present but could not be executed. Install a usable Python or uv and rerun this script."
    }

    if (-not (Test-Path -LiteralPath $virtualEnvironmentPython)) {
        Write-Host "Creating the project virtual environment with python -m venv..."
        Invoke-Checked $pythonCommand.Source @("-m", "venv", ".venv")
    }
    Write-Host "Installing the project and development dependencies with pip..."
    Invoke-Checked $virtualEnvironmentPython @("-m", "pip", "install", "-e", ".[dev]")
}

if (-not (Test-Path -LiteralPath $virtualEnvironmentPython)) {
    throw "The project virtual environment was not created at $virtualEnvironmentPython"
}

Write-Host "Python version:"
Invoke-Checked $virtualEnvironmentPython @("--version")

$ruffPath = Join-Path $virtualEnvironmentPath "Scripts\ruff.exe"
if (Test-Path -LiteralPath $ruffPath) {
    Write-Host "Running Ruff..."
    Invoke-Checked $ruffPath @("check", ".")
} else {
    Write-Host "Running Ruff through Python..."
    Invoke-Checked $virtualEnvironmentPython @("-m", "ruff", "check", ".")
}

Write-Host "Running smoke tests..."
Invoke-Checked $virtualEnvironmentPython @("-m", "pytest")
Write-Host "Bootstrap completed successfully."
