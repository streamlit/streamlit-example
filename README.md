
GitHub üzerinde **GitHub Actions (Workflow)** kullanarak Python/Kivy tabanlı uygulamanızı (`iddaa_mobile_app_v11.py`) herhangi bir bilgisayar kurulumu yapmadan tamamen otomatik olarak **Android `.apk`** dosyasına dönüştürebilirsiniz.

İşte GitHub üzerinde tek tıkla (`Run workflow`) APK derlemenizi sağlayan adım adım rehber:

---

### 📂 GitHub Reposunda Bulunması Gereken Dosyalar

GitHub reponuzun ana dizininde şu 3 dosyanın olması yeterlidir:

1. **`main.py`**: Uygulama kodunuz (`iddaa_mobile_app_v11.py` dosyasının adını `main.py` yapıp yükleyin).
2. **`buildozer.spec`**: Buildozer yapılandırma ayar dosyası.
3. **`.github/workflows/build.yml`**: GitHub Actions otomasyon betiği.

---

### 🚀 1. Adım: GitHub Actions Workflow Dosyasını Oluşturun

GitHub reponuzda **`.github/workflows/`** klasörü açın ve içerisine **`build.yml`** adında bir dosya oluşturup aşağıdaki kodu yapıştırın:

```yaml
name: Build Android APK

on:
  workflow_dispatch: # GitHub arayüzünden manuel "Run workflow" butonu ile başlatma
  push:
    branches: [ main, master ] # Kod push edildiğinde otomatik tetikleme

jobs:
  build:
    runs-on: ubuntu-22.04

    steps:
      - name: Repoyu Klonla (Checkout)
        uses: actions/checkout@v3

      - name: Python Ortamını Hazırla
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Buildozer İle APK Derle
        uses: ArtemisAxe/buildozer-action@v1
        with:
          save_buildozer_cache: true

      - name: Üretilen APK Dosyasını Yükle (Artifacts)
        uses: actions/upload-artifact@v3
        with:
          name: Iddaa-Analiz-Robotu-APK
          path: bin/*.apk
```

---

### ⚙️ 2. Adım: `buildozer.spec` Ayarlarını Düzenleyin

Ana dizindeki `buildozer.spec` dosyanızda şu satırların tanımlı olduğundan emin olun:

```ini
[app]
title = Iddaa Analiz Robotu
package.name = iddaarobot
package.domain = org.analiz
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

# Gerekli Kütüphaneler:
requirements = python3,kivy,numpy,pandas,scipy

orientation = portrait
fullscreen = 0
android.permissions = INTERNET
android.api = 33
android.minapi = 21
```

---

### 📲 3. Adım: GitHub'da APK'yı Derleyin ve İndirin

1. Dosyaları GitHub reponuza yükleyin (`git push` yapın).
2. GitHub reponuzda üst menüde bulunan **Actions** sekmesine tıklayın.
3. Sol taraftaki menüden **Build Android APK** başlığını seçin.
4. Sağ tarafta beliren **Run workflow** butonuna tıklayıp derlemeyi başlatın.
5. İşlem bulut sunucularında yaklaşık **5-8 dakika** sürer.
6. Derleme bittiğinde ilgili çalışmanın üzerine tıklayın; sayfanın en altında **Artifacts** bölümünde **`Iddaa-Analiz-Robotu-APK.zip`** indirme bağlantısını göreceksiniz.
7. İndirdiğiniz zip dosyasını açıp içindeki `.apk` dosyasını telefonunuza yükleyebilirsiniz.

---

💡 Ayrıntılı yerel kurulum veya Colab alternatifleri için reponuzda bulunan **`apk_derleme_rehberi_v11.md`** belgesini de inceleyebilirsiniz.
