Sphinx site for pyS_LinkChecker

This folder contains an independent Sphinx project configured to use autodoc
and autosummary. It is intentionally independent from the repository's main
`docs/` folder so you can build/release Sphinx docs separately.

Quick start (PowerShell):

```powershell
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
python -m pip install -r sphinx_site\requirements-sphinx.txt
# optionally install runtime deps if you want real module imports
# python -m pip install aiohttp rich orjson pendulum
sphinx_site\generate_apidoc.ps1 -Force
cd sphinx_site
.\\make.bat
```

Notes:
- The Sphinx config mocks runtime-only imports via ``autodoc_mock_imports`` so
  the build works without installing aiohttp/rich/orjson/pendulum.
- The `generate_apidoc.ps1` helper will create `sphinx_site/source/generated`.
