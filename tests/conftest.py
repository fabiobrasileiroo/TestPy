import os
import sys

# Ensure the project root is on sys.path so tests can import the `app` package
# This makes `from app.matematica import Matematica` work when pytest runs from the repo
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
