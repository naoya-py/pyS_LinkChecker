# pyS_LinkChecker (MkDocs)

This site is generated with MkDocs and mkdocstrings. It provides a Markdown-centric documentation site.

## Build

Install the requirements and run the local server:

```powershell
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
python -m pip install -r requirements-mkdocs.txt
mkdocs serve
```

## Production build

```powershell
mkdocs build -d site
```
