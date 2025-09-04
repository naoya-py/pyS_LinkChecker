MkDocs site for pyS_LinkChecker

This folder contains a minimal MkDocs + mkdocstrings site.

Quick start:

1. Create and activate a virtualenv

   ```powershell
   python -m venv .venv
   .\\.venv\\Scripts\\Activate.ps1
   ```

2. Install dependencies

   ```powershell
   python -m pip install -r requirements-mkdocs.txt
   ```

3. Run the dev server

   ```powershell
   mkdocs serve
   ```

Notes:
- mkdocstrings will import your package to extract docstrings. If your package has runtime dependencies (aiohttp, rich, etc.), install them in the same environment or use mocking strategies.
- The MkDocs config (`mkdocs.yml`) already inserts the project root into `sys.path` for mkdocstrings via `setup_commands`.
