# PowerShell helper to run sphinx-apidoc for sphinx_site
param(
    [switch]$Force
)

if (-not (Get-Command sphinx-apidoc -ErrorAction SilentlyContinue)) {
    Write-Error "sphinx-apidoc not found. Install requirements: python -m pip install -r sphinx_site\requirements-sphinx.txt"
    exit 1
}

$generated = Join-Path -Path $PSScriptRoot -ChildPath "source\generated"
if ((Test-Path $generated) -and (-not $Force)) {
    Write-Host "Directory 'source/generated' already exists. Use -Force to overwrite."
}
else {
    if (Test-Path $generated) { Remove-Item -Recurse -Force $generated }
    New-Item -ItemType Directory -Path $generated | Out-Null
    Push-Location $PSScriptRoot
    sphinx-apidoc -o .\source\generated ..\
    Pop-Location
    Write-Host "sphinx-apidoc finished. Generated files are in sphinx_site\source\generated"
}
