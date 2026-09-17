import pandas as pd
from src.preprocessing import clean_data

def test_clean_data_removes_duplicates_and_nan():
    df = pd.DataFrame({"A": [1, 1, None], "Label": ["BENIGN", "BENIGN", "ATTACK"]})
    result = clean_data(df)
    assert len(result) == 1
