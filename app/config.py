from pathlib import Path
from dotenv import load_dotenv
import os
from typing import Any, Callable

# Resolve project root (one level above the `app/` directory)
ROOT = Path(__file__).resolve().parents[1]
DOTENV_PATH = ROOT / ".env"

# Load .env from project root if present, otherwise use default loader
if DOTENV_PATH.exists():
    load_dotenv(dotenv_path=DOTENV_PATH)
else:
    load_dotenv()


def get_env(key: str, default: Any = None, cast: Callable[[str], Any] | None = None) -> Any:
    """Read an environment variable with an optional cast function.

    Example:
        get_env('PORT', 8000, int)
    """
    val = os.getenv(key, None)
    if val is None:
        return default
    if cast:
        try:
            return cast(val)
        except Exception:
            return val
    return val


# Common variables used across the project/tests
BASE_URL: str = get_env("BASE_URL", "http://fooapi.com")


__all__ = ["get_env", "BASE_URL", "ROOT"]
