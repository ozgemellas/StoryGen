import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import argparse

# GPU varsa kullan
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Model yolu (senin dizinine göre ayarlanmış)
MODEL_PATH = "out-storygen/final"

# Model ve tokenizer yükle
tokenizer = GPT2Tokenizer.from_pretrained(MODEL_PATH)
model = GPT2LMHeadModel.from_pretrained(MODEL_PATH)
model.to(device)
model.eval()

def generate_story(prompt, max_length=150, temperature=0.8, top_p=0.95):
    # Prompt'u tokenlara çevir
    inputs = tokenizer(prompt, return_tensors="pt").to(device)

    # Hikâye üretimi
    output = model.generate(
        **inputs,
        max_length=max_length,
        do_sample=True,
        temperature=temperature,
        top_p=top_p,
        pad_token_id=tokenizer.eos_token_id
    )

    # Tokenları metne çevir
    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)

    return generated_text

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="StoryGen: Hikâye Tamamlayıcı")
    parser.add_argument("--prompt", type=str, required=True, help="Başlangıç cümlesi")
    parser.add_argument("--length", type=int, default=150, help="Maksimum uzunluk")
    args = parser.parse_args()

    story = generate_story(args.prompt, max_length=args.length)
    print("\n📝 Oluşturulan Hikâye:\n")
    print(story)
