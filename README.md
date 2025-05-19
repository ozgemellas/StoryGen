# StoryGen

**StoryGen**, ROCStories veri setine dayalı olarak başlangıç cümlesi girildiğinde dinamik olarak kısa hikâye oluşturan bir Python projesidir. Projenin odağında modüler yapı, temiz mimari ve kullanıcı dostu arayüz bulunmaktadır.

---

## Proje Adımları

1. **Veri İndirme (download\_hf.py)**

   * Hugging Face’ten `mintujupally/ROCStories` veri setini indirerek `data/rocstories.csv` oluşturur.

2. **Veri Ön İşleme (preprocess.py)**

   * Ham CSV’yi cümlelere bölerek `input_text` ve `target_text` çiftleri oluşturur.
   * %90 eğitim, %10 doğrulama olmak üzere `data/processed/` altına kaydeder.

3. **Model Eğitimi**

   * `train.py` ile hiperparametreleri tanımlayıp PyTorch eğitim döngüsünü çalıştırır.
   * Checkpoint mekanizmasıyla model ağırlıklarını `out-storygen/model/` dizinine kaydeder.

4. **Hikâye Üretimi**

   * `generate.py` komut satırından aldığı başlangıç cümlesini eğitimli modelle genişleterek hikâye üretir.

5. **Veritabanı Yönetimi (init\_db.py)**

   * `scripts/init_db.py` veya `frontend/app.py` başlangıcında; `feedback.db` ve `stories.db` dosyalarını oluşturur.
   * `feedback.db`: kullanıcı beğeni ve geri bildirim kayıtlarını tutar.
   * `stories.db`: prompt, oluşturulma tarihi ve PDF dosya yolunu üç sütunlu tablo şeklinde depolar.

6. **Web Arayüzü**

   * Gradio tabanlı `frontend/app.py` ile tarayıcı üzerinden etkileşimli kullanım sunar.
   * Kullanıcı başlangıç cümlesini girer; anında oluşturulan hikâyeyi ve PDF indirme linkini görüntüler.

7. **Sonuç ve İzleme**

   * **logs/** dizininde eğitim ve üretim süreçlerinin log kayıtları bulunur.
   * **out-storygen/** dizininde model ağırlıkları, üretilen hikâye örnekleri ve performans metrikleri yer alır.

---

## Kullanılan Teknolojiler

* **Python 3.8+**: Proje dili olarak esnek yapısı ve geniş kütüphane desteği.
* **PyTorch**: Derin öğrenme modeli tanımı ve eğitimi için.
* **Pandas & NumPy**: Veri işleme ve analiz adımları için.
* **Datasets (Hugging Face)**: ROCStories veri setinin kolay indirilmesi için.
* **Gradio**: Hızlı ve basit web arayüzü oluşturma.
* **Git & GitHub**: Sürüm kontrolü ve iş birliği.
* **Virtualenv**: İzole Python ortamları.

---

## Klasör Yapısı

```bash
tree -L 3 STORYGEN
```

```text
STORYGEN/
├─ data/
│  ├─ raw/               # Ham CSV dosyası
│  └─ processed/         # Ön işleme sonrası eğitim ve doğrulama CSV'leri
├─ scripts/              # Veri indirme ve ön işleme betikleri
│  ├─ download_hf.py     # HF’den ROCStories indirir
│  └─ preprocess.py      # Ham veriyi train/valid olarak işler
├─ train.py              # Modeli eğitir
├─ generate.py           # Komut satırından hikâye üretir
├─ frontend/             # Gradio arayüzü
│  ├─ app.py             # Uygulama tanımı
│  ├─ database/          # Arayüz veritabanı dosyaları
│  │  ├─ feedback.db     # Kullanıcı beğeni ve geri bildirimler
│  │  └─ stories.db      # Prompt, oluşturulma tarihi, PDF yolu bilgileri
│  └─ saved_pdfs/        # Üretilen PDF dosyaları
│     └─ story571585.pdf # Örnek PDF
├─ logs/                 # Eğitim ve üretim logları
├─ out-storygen/         # Model ağırlıkları ve çıktı örnekleri
├─ examples/             # Örnek kullanım senaryoları
├─ test.py               # Birim testler
└─ requirements.txt      # Python bağımlılıkları

```

Frontend klasöründeki `database/` dizininde:

* `feedback.db`: Kullanıcı beğeni ve geri bildirimlerini saklar.
* `stories.db`: Üretilen PDF’lere ait prompt, oluşturulma tarihi ve dosya yolunu üç sütunlu bir tabloda depolar.

## Hızlı Başlangıç

1. Sanal ortam oluşturun ve aktif edin:

   ```bash
   python -m venv venv
   source venv/bin/activate      # macOS/Linux
   venv\\Scripts\\activate     # Windows
   ```
2. Bağımlılıkları yükleyin:

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
3. Veriyi indirin ve işleyin:

   ```bash
   python scripts/download_hf.py   # HF’den ROCStories indirir
   python scripts/preprocess.py    # Ham veriyi train/valid olarak işler
   ```
4. Modeli eğitin:

   ```bash
   python train.py --config configs/train.yaml
   ```
5. Arayüzü çalıştırın:

   ```bash
   python frontend/app.py
   ```

*Parametre detayları ve ek betikler proje klasörü içindeki dokümantasyonda yer alır.*

---

## Katkıda Bulunma

1. Reposu fork’layın.
2. Yeni bir branch oluşturun (`feature/...`).
3. Değişiklikleri commit edin.
4. Pull request gönderin.

---

## Lisans

MIT © Özge Mellaş 2025
