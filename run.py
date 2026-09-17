"""One-command local launcher for the NIDS demo."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "raw" / "traffic.csv"
MODEL = ROOT / "models" / "nids_model.pkl"


def run_module(module, *args):
    subprocess.run([sys.executable, "-m", module, *args], cwd=ROOT, check=True)


def main():
    if not DATA.exists():
        print("[1/3] No dataset found. Generating the 10,000-row demo dataset...")
        run_module("src.generate_sample_data", "--rows", "10000", "--attack-ratio", "0.20")
    else:
        print(f"[1/3] Dataset found: {DATA}")

    if not MODEL.exists():
        print("[2/3] No trained model found. Training the model...")
        run_module("src.train")
    else:
        print(f"[2/3] Model found: {MODEL}")

    try:
        __import__("streamlit")
    except ImportError:
        print("\nStreamlit is not installed in the active Python environment.")
        print("Install project dependencies with:")
        print("  python -m pip install -r requirements.txt")
        print("Then run: python run.py")
        return

    print("[3/3] Starting the Streamlit dashboard...")
    subprocess.run(
        [sys.executable, "-m", "streamlit", "run", "dashboard/app.py"],
        cwd=ROOT,
        check=True,
    )


if __name__ == "__main__":
    main()
