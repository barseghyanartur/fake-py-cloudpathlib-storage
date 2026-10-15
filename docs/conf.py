# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
import sys
from pathlib import Path

PARENT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PARENT_DIR))

# fake.py ships `fakepy` as a regular (non-namespace) package. Expose this
# checkout's `fakepy/cloudpathlib_storage` beneath it.
try:
    import fakepy

    fakepy.__path__.insert(0, str(PARENT_DIR / "fakepy"))
except ImportError:
    pass

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

try:
    from fakepy import cloudpathlib_storage

    version = cloudpathlib_storage.__version__
    project = cloudpathlib_storage.__title__
    copyright = cloudpathlib_storage.__copyright__
    author = cloudpathlib_storage.__author__
except ImportError:
    version = "0.1"
    project = "fake-py-cloudpathlib-storage"
    copyright = "2024-2026, Artur Barseghyan <artur.barseghyan@gmail.com>"
    author = "Artur Barseghyan <artur.barseghyan@gmail.com>"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.todo",
    "sphinx_no_pragma",
    "sphinx_llms_txt_link",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

language = "en"

release = version

# The suffix of source filenames.
source_suffix = {
    ".rst": "restructuredtext",
}

pygments_style = "sphinx"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
# html_extra_path = ["examples"]

prismjs_base = "//cdnjs.cloudflare.com/ajax/libs/prism/1.29.0"

html_css_files = [
    f"{prismjs_base}/themes/prism.min.css",
    f"{prismjs_base}/plugins/toolbar/prism-toolbar.min.css",
    "https://cdn.jsdelivr.net/gh/barseghyanartur/jsphinx@1.3.4/src/css/sphinx_rtd_theme.css",  # noqa
]

html_js_files = [
    f"{prismjs_base}/prism.min.js",
    f"{prismjs_base}/plugins/autoloader/prism-autoloader.min.js",
    f"{prismjs_base}/plugins/toolbar/prism-toolbar.min.js",
    f"{prismjs_base}/plugins/copy-to-clipboard/prism-copy-to-clipboard.min.js",
    "https://cdn.jsdelivr.net/gh/barseghyanartur/jsphinx@1.3.4/src/js/download_adapter.js",  # noqa
]

# -- Options for todo extension ----------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/todo.html#configuration

todo_include_todos = True

# -- Options for Epub output  ----------------------------------------------
epub_title = project
epub_author = author
epub_publisher = "GitHub"
epub_copyright = copyright
# URL or ISBN
epub_identifier = "https://github.com/barseghyanartur/fake-py-cloudpathlib-storage"  # noqa
epub_scheme = "URL"  # or "ISBN"
epub_uid = "https://github.com/barseghyanartur/fake-py-cloudpathlib-storage"



# -- Autodoc -----------------------------------------------------------------

# `parametrize` replaces parametrized test methods with placeholders that
# raise on any attribute access, which breaks autodoc introspection. Allow
# dunder lookups (docs build only), then skip them and the generated
# `test_name[...]` variants (their names embed machine-specific values).
try:
    from parametrize.parametrize import UnparametrizedMethod

    _getattribute = UnparametrizedMethod.__getattribute__

    def _safe_getattribute(self, name):
        if name.startswith("__"):
            return object.__getattribute__(self, name)
        return _getattribute(self, name)

    UnparametrizedMethod.__getattribute__ = _safe_getattribute
except ImportError:
    UnparametrizedMethod = None


def skip_parametrized(app, what, name, obj, skip, options):
    """Skip `parametrize` placeholders and generated test variants."""
    if "[" in name:
        return True
    if UnparametrizedMethod and type(obj) is UnparametrizedMethod:
        return True
    return None


def setup(app):
    app.connect("autodoc-skip-member", skip_parametrized)
