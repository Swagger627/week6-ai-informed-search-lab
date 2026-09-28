"""Completed modular version of the supplied Streamlit template.

Run with:
    streamlit run streamlit_app_solution_template2.py
"""

# The completed interface is kept in app.py so Streamlit Community Cloud has a
# conventional entry point. Reload it on Streamlit reruns so the page is drawn
# every time this alternative entry point executes.
import importlib
import sys

if "app" in sys.modules:
    importlib.reload(sys.modules["app"])
else:
    import app  # noqa: F401

