**Aplikasi dibuat oleh:** ImNotDanish05 💻✨
**Dibantu dan didukung penuh oleh:** Aria, asisten virtual~

---

### 🎯 Deskripsi:

Program ini digunakan untuk **mengambil data komentar & overview dari sebuah tempat di Google Maps**, lalu menyimpannya ke file `.txt`.

---

### ✅ Persiapan Sebelum Menjalankan:

#### 1. **Install semua package Python yang dibutuhkan**

Jalankan perintah ini di terminal atau CMD:

```bash
pip install selenium beautifulsoup4 pynput pyautogui
```

Kalau kamu belum install `pip`, pastikan Python kamu udah versi 3.8 ke atas dan aktif di PATH.

---

#### 2. **Download ChromeDriver**

* Kunjungi: [https://googlechromelabs.github.io/chrome-for-testing/](https://googlechromelabs.github.io/chrome-for-testing/)
* Sesuaikan versi ChromeDriver dengan versi Chrome di komputermu.
* Ekstrak `chromedriver.exe` ke folder bernama `chromedriver-win64/`

Contoh struktur folder:

```
📁 proyek-scraper/
├── chromedriver-win64/
│   └── chromedriver.exe
├── app.py
└── hasil/
```

---

### 🧪 Cara Pakai:

1. **Jalankan file `app.py`**

   * Klik dua kali atau jalankan via terminal:

     ```bash
     python app.py
     ```

2. **Masukkan link Google Maps dari tempat yang ingin kamu ambil datanya**
   Contoh:

   ```
   [https://www.google.com/maps/place/Politeknik+Negeri+Semarang/@-7.0536...](https://www.google.com/maps/place/Gedung+Direktorat+POLINES/@-7.0536732,110.4319025,21z/data=!4m10!1m2!2m1!1sPOLINES!3m6!1s0x2e708c0374ca46c1:0x2b0b2f7472560a54!8m2!3d-7.0520893!4d110.4355963!15sCgdQT0xJTkVTWgkiB3BvbGluZXOSAQdjb2xsZWdlmgEjQ2haRFNVaE5NRzluUzBWSlEwRm5TVU55YTBscWJHRm5FQUWqATwKCy9nLzEyMzJqMHFyEAEyHhABIhqf0CVgSRdciVhEk8ma_n1pddkBBmIj7Uhi1zILEAIiB3BvbGluZXPgAQD6AQQIVxBJ!16s%2Fg%2F11c5b17v1k?entry=ttu&g_ep=EgoyMDI1MDcyMy4wIKXMDSoASAFQAw%3D%3D)
   ```

3. **Tunggu proses scraping berjalan**
   Program akan membuka Chrome, klik tab "Overview" dan "Review", lalu scroll otomatis sambil ngecek perubahan warna layar (dengan grayscale detection supaya ringan banget 😎)

4. **Cek hasilnya di folder `hasil/`**

   * `overview.txt`: berisi nama, alamat, rating, dan nomor telepon tempat
   * `review.txt`: kumpulan komentar user dari Google Maps

---

### 💡 Tips Tambahan:

* Pastikan **Chrome kamu tidak dalam mode zoom**, biar scraping warna-nya pas!
  Jika perlu, Aria udah set zoom otomatis di kode:

  ```python
  driver.execute_script("document.body.style.zoom='100%'")
  ```

* Kalau halaman gagal diakses karena CAPTCHA/login, cukup login dan tekan `ENTER` di terminal seperti instruksi 😇

---

### 📽️ Video Tutorial Lengkap:

[YouTube: Google Maps Review Scraper - by ImNotDanish05](https://www.youtube.com/watch?v=2d75pATkC9M)

