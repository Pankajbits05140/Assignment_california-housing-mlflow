

import numpy as np 

from sklearn.model_selection import train_test_split    
# scripts/preprocess.py

from sklearn.datasets import fetch_california_housing
import pandas as pd
import os

def load_and_save_data():
    data = fetch_california_housing(as_frame=True)
    df = pd.concat([data.data, data.target.rename("target")], axis=1)

    os.makedirs("data/raw", exist_ok=True)
    df.to_csv("data/raw/california_housing.csv", index=False)

if __name__ == "__main__":
    load_and_save_data()
