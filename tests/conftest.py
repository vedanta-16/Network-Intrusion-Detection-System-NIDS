"""
Ensures the project root is importable as `src.*` regardless of where
pytest is invoked from. The existing tests already do `from src.predict
import predict_traffic`, but without this, running `pytest` from a
different working directory would fail with ModuleNotFoundError.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
