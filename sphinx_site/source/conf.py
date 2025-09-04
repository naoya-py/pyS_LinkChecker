import os
import sys
from datetime import datetime

# Add project root to sys.path so autodoc can import modules (use Docstrings)
sys.path.insert(0, os.path.abspath('../../'))

project = 'pyS_LinkChecker (sphinx_site)'
author = 'naoya-py'
release = '0.0.0'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
]

autosummary_generate = True
autodoc_member_order = 'bysource'
autodoc_typehints = 'description'

# Mock runtime-only imports so the docs can build without installing deps
autodoc_mock_imports = ['aiohttp', 'orjson', 'pendulum', 'rich']

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# Theme: prefer sphinx_rtd_theme, fallback to 'alabaster'
try:
    import sphinx_rtd_theme  # type: ignore
    html_theme = 'sphinx_rtd_theme'
except Exception:
    html_theme = 'alabaster'

html_static_path = ['_static']

html_context = {
    'generated_on': datetime.utcnow().isoformat() + 'Z'
}
