# scripts/preprocess.py

import pandas as pd
import re
import os

def main():
    # 1. Ham CSV’i oku
    df = pd.read_csv("data/rocstories.csv")
    cols = list(df.columns)
    print("🔍 Found columns:", cols)

    # 2. 'text' sütununu hikâye olarak işleme al
    sents_list = []
    if 'text' in df.columns:
        for story in df['text']:
            # Nokta/ünlem/soru işaretinden sonra böl
            sents = re.split(r'(?<=[.!?])\s+', str(story).strip())
            sents_list.append(sents)
    else:
        raise RuntimeError(
            "CSV’de 'text' sütunu bulunmuyor. Kolonlar: {}".format(cols)
        )

    # 3. input/target çiftlerini oluştur
    inputs, targets = [], []
    for sents in sents_list:
        if len(sents) >= 5:
            inputs.append(sents[0].strip())
            targets.append(" ".join(sents[1:5]).strip())

    # 4. DataFrame’e dönüştür ve %90 train – %10 valid ayır
    proc = pd.DataFrame({"input_text": inputs, "target_text": targets})
    split_idx = int(len(proc) * 0.1)
    valid_df = proc.iloc[:split_idx].reset_index(drop=True)
    train_df = proc.iloc[split_idx:].reset_index(drop=True)

    # 5. Kaydet
    os.makedirs("data/processed", exist_ok=True)
    train_df.to_csv("data/processed/rocstories_train.csv", index=False)
    valid_df.to_csv("data/processed/rocstories_valid.csv", index=False)
    print(f"✅ Hazır! Train: {len(train_df)} örnek, Valid: {len(valid_df)} örnek.")

if __name__ == "__main__":
    main()


