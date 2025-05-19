import os
import torch
from transformers import (
    GPT2TokenizerFast,
    GPT2LMHeadModel,
    Trainer,
    TrainingArguments,
    DataCollatorForLanguageModeling
)
from torch.utils.data import Dataset
import pandas as pd

class StoryDataset(Dataset):
    def __init__(self, path, tokenizer, max_input=50, max_target=150):
        df = pd.read_csv(path)
        self.inputs = df["input_text"].tolist()
        self.targets = df["target_text"].tolist()
        self.tokenizer = tokenizer
        self.max_input = max_input
        self.max_target = max_target

    def __len__(self):
        return len(self.inputs)

    def __getitem__(self, idx):
        enc_in = self.tokenizer(
            self.inputs[idx],
            truncation=True,
            padding="max_length",
            max_length=self.max_input,
        )
        enc_tgt = self.tokenizer(
            self.targets[idx],
            truncation=True,
            padding="max_length",
            max_length=self.max_target,
        )

        input_ids = enc_in["input_ids"] + enc_tgt["input_ids"]
        attention_mask = enc_in["attention_mask"] + enc_tgt["attention_mask"]
        labels = [-100] * self.max_input + enc_tgt["input_ids"]

        return {
            "input_ids": torch.tensor(input_ids, dtype=torch.long),
            "attention_mask": torch.tensor(attention_mask, dtype=torch.long),
            "labels": torch.tensor(labels, dtype=torch.long),
        }

def main():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"🏎️ Training on: {device}")

    # Tokenizer & Model
    tokenizer = GPT2TokenizerFast.from_pretrained("gpt2-medium")
    tokenizer.pad_token = tokenizer.eos_token

    model = GPT2LMHeadModel.from_pretrained("gpt2-medium")
    model.resize_token_embeddings(len(tokenizer))
    model = model.to(device)

    # Dataset’ler
    train_dataset = StoryDataset("data/processed/rocstories_train.csv", tokenizer)
    valid_dataset = StoryDataset("data/processed/rocstories_valid.csv", tokenizer)

    # Data collator
    data_collator = DataCollatorForLanguageModeling(tokenizer, mlm=False)

    args = TrainingArguments(
    output_dir="out-storygen",
    num_train_epochs=8,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    learning_rate=3e-5,
    warmup_steps=500,
    weight_decay=0.01,
    gradient_accumulation_steps=4,
    do_eval=True,
    eval_steps=500,
    save_steps=1000,
    save_total_limit=3,
    logging_steps=200,
    logging_dir="logs",
    fp16=torch.cuda.is_available(),
    dataloader_num_workers=os.cpu_count() // 2,
)




    # Trainer
    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=train_dataset,
        eval_dataset=valid_dataset,
        data_collator=data_collator,
    )

    # Eğitim
    trainer.train()
    trainer.save_model("out-storygen/final")
    print("✅ Model eğitimi tamamlandı ve kaydedildi: out-storygen/final2")

if __name__ == "__main__":
    main()
