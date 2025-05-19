##  📖 StoryGen 
ROCStories veri setine dayalı olarak başlangıç cümlesi girildiğinde dinamik olarak kısa hikâye oluşturan bir Python projesidir. Projenin odağında modüler yapı, temiz mimari ve kullanıcı dostu arayüz bulunmaktadır.

---

## Proje Adımları

1. **Veri İndirme (download\_hf.py)**

   * `scripts/download_hf.py` betiği Hugging Face’den `mintujupally/ROCStories` veri setini indirir.
   * Eğitim ve test split’lerini birleştirerek tek bir CSV dosyası (`data/rocstories.csv`) oluşturur.

2. **Veri Ön İşleme (preprocess.py)**

   * `scripts/preprocess.py` ham CSV’yi (`data/rocstories.csv`) okuyup cümle temelli parçalama yapar.
   * İlk cümleyi `input_text`, sonraki dört cümleyi `target_text` olarak ayarlar.
   * Oluşan veri çifti `%90 train`, `%10 valid` oranıyla `data/processed/` altına kaydedilir.

3. **Model Eğitimi**

   * `train.py` üzerinden hiperparametreler (epok sayısı, batch size vb.) tanımlanır.
   * PyTorch eğitim döngüsü ve checkpoint mekanizması ile model ağırlıkları `out-storygen/model/` altında saklanır.

4. **Hikâye Üretimi**

   * `generate.py` betiği komut satırından başlangıç cümlesi alır ve eğitilmiş modeli kullanarak hikâyeyi üretir.

5. **Web Arayüzü**

   * Gradio tabanlı `frontend/app.py` ile etkileşimli bir uygulama sunulur.
   * Kullanıcı, tarayıcı üzerinden başlangıç cümlesini girer ve anında hikâye metnini görüntüler.

6. **Sonuç ve İzleme**

   * **logs/** dizininde eğitim ve üretim süreçlerinin log kayıtları yer alır.
   * **out-storygen/** dizininde model ağırlıkları, üretilen hikâye örnekleri ve performans metrikleri bulunur.

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
