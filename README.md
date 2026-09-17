# Network Intrusion Detection System (NIDS)

A compact educational ML-based Network Intrusion Detection System using Python, Pandas, Scikit-learn and Streamlit.

## Architecture

Network Flow CSV -> Data Cleaning -> Feature Selection -> Random Forest -> BENIGN/ATTACK -> Security Dashboard

## Project structure

- `data/raw/traffic.csv` — training/input network-flow CSV
- `models/nids_model.pkl` — trained Random Forest model
- `src/generate_sample_data.py` — creates a synthetic dataset for testing
- `src/train.py` — trains and evaluates the model
- `src/predict.py` — loads the model and classifies uploaded traffic
- `src/feature_extraction.py` — defines the 12 numeric model features
- `dashboard/app.py` — Streamlit detection dashboard
- `dashboard/pages/1_Alert_History.py` — alert-history page
- `tests/` — basic automated tests

## Clean setup on Kali Linux

Run these commands from the project root:

```bash
cd ~/Desktop/nids_project
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Verify the important dependencies:

```bash
python -c "import pandas, numpy, sklearn, joblib, streamlit; print('Dependencies OK')"
```

## Option A — step-by-step (recommended for learning)

### 1. Generate demo data

```bash
python -m src.generate_sample_data --rows 10000 --attack-ratio 0.20
```

This creates:

```text
data/raw/traffic.csv
```

### 2. Inspect the dataset

```bash
python -m src.data_collection
```

### 3. Train the model

```bash
python -m src.train
```

A successful run creates:

```text
models/nids_model.pkl
```

The training command also prints accuracy, precision, recall, F1-score and a confusion matrix.

### 4. Start the dashboard

```bash
python -m streamlit run dashboard/app.py
```

Then open the local Streamlit address shown in the terminal, normally `http://localhost:8501`.

Upload a CSV containing the same 12 model features. `Source IP`, `Destination IP` and `Protocol` are optional display columns; the model itself uses the 12 numeric flow features listed in `src/feature_extraction.py`.

## Option B — one command

After dependencies are installed:

```bash
python run.py
```

`run.py` automatically generates the demo dataset if it is missing, trains the model if it is missing, and then launches Streamlit.

## Important: real NIDS data

The included generator creates **synthetic educational data**. It is useful for proving that the software pipeline works, but the resulting 100% accuracy is not evidence of real-world intrusion-detection performance.

For realistic evaluation, replace `data/raw/traffic.csv` with a labeled network-flow dataset such as a CICIDS/CSE-CIC-IDS-style CSV, provided it contains the required feature columns and `Label`.

The training code converts `BENIGN` to `BENIGN` and every other label to `ATTACK` for binary classification.

## Troubleshooting

### `ModuleNotFoundError: No module named 'sklearn'`

Activate the virtual environment and install dependencies:

```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
```

### `FileNotFoundError: Train the model first.`

This means `models/nids_model.pkl` does not exist. Run:

```bash
python -m src.generate_sample_data
python -m src.train
```

or simply:

```bash
python run.py
```

### `Dataset not found: data/raw/traffic.csv`

Generate the demo dataset:

```bash
python -m src.generate_sample_data
```

### Run tests

```bash
pytest -v
```
