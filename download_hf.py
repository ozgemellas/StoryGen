# scripts/download_hf.py

import pandas as pd
import os
from datasets import load_dataset

def main():
    # 1. HF’den veri kümesini indir (train + test split’leri)
    ds = load_dataset("mintujupally/ROCStories")
    
    # 2. Pandas DataFrame’e çevir
    df_train = ds["train"].to_pandas()
    df_test  = ds["test"].to_pandas()
    
    # 3. Birleştir ve CSV’ye kaydet
    df_all = pd.concat([df_train, df_test], ignore_index=True)
    os.makedirs("data", exist_ok=True)
    df_all.to_csv("data/rocstories.csv", index=False)
    print(f"✅ data/rocstories.csv oluşturuldu ({len(df_all)} örnek).")

if __name__ == "__main__":
    main()
