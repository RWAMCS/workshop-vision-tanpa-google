# Workshop Vision Tanpa Google

Implementasi **Object Localization** yang berjalan **100% lokal** di komputer sendiri — tanpa Google Cloud Vision API, tanpa billing, tanpa Service Account, tanpa `kredensial.json`, tanpa API key apa pun.

Cara kerja: Gambar → YOLO lokal (Ultralytics) → nama objek + confidence + bounding box → Pillow menggambar box → Flask menampilkan di browser.

## 1. Deskripsi Project

Project praktikum computer vision untuk mendeteksi objek dalam gambar beserta tingkat keyakinan (confidence) dan lokasinya (bounding box, pixel + normalized 0–1). Ada dua percobaan:

- **Percobaan 1** (`percobaan1.py`) — deteksi via terminal (CLI). Input `tes_gambar.jpeg`, output `hasil_deteksi_cli.jpg`.
- **Percobaan 2** (`app.py`) — deteksi via web Flask. Upload gambar di browser, hasil + tabel tampil langsung. (Tidak ada file `percobaan2.py` — Percobaan 2 memang menggunakan `app.py`.)

## 2. Teknologi

- Python 3.13
- Flask (web interface)
- Ultralytics YOLO — model `yolo11s.pt` (otomatis diunduh saat pertama dijalankan)
- Pillow (menggambar bounding box + label)
- HTML / CSS / Vanilla JavaScript (tanpa framework, tanpa CDN)

## 3. Struktur Project

```
workshop_vision_tanpa_google/
├── app.py                  ← Percobaan 2 (web Flask)
├── percobaan1.py           ← Percobaan 1 (CLI)
├── requirements.txt        ← ultralytics, Flask, Pillow
├── README.md               ← file ini
├── README_LANGKAH.md       ← panduan langkah versi lama
├── LAPORAN_ALTERNATIF.md   ← bahan laporan praktikum
├── setup_windows.bat       ← setup otomatis Windows
├── .gitignore
├── tes_gambar.jpeg         ← gambar contoh untuk testing
├── hasil_deteksi_cli.jpg   ← output Percobaan 1
├── yolo11s.pt              ← model YOLO (tidak ikut push, auto-download)
├── yolo11n.pt              ← model lama (tidak ikut push)
├── templates/
│   └── index.html          ← UI web
└── static/
    ├── uploads/            ← gambar upload (diabaikan Git)
    └── results/            ← gambar hasil (diabaikan Git)
```

Catatan: file `*.pt`, isi `static/uploads/`, isi `static/results/`, `__pycache__/`, dan `.venv/` sengaja **tidak** masuk Git (lihat `.gitignore`). Model YOLO diunduh otomatis oleh Ultralytics saat pertama dijalankan.

## 4. Prasyarat

- Windows 10/11
- Python 3.13 (centang "Add python.exe to PATH" saat instalasi) — cek: `python --version`
- pip — cek: `pip --version`
- Git — cek: `git --version`
- VS Code (disarankan)
- Koneksi internet (hanya untuk instalasi dependency + download model pertama kali)

## 5. Setup Windows

Buka PowerShell **di folder project**, lalu jalankan perintah berikut satu per satu:

```powershell
cd "F:\belajar mandiri\skpi\day 1\workshop_vision_tanpa_google"

python -m venv .venv --without-pip

.\.venv\Scripts\python.exe -m ensurepip --upgrade

.\.venv\Scripts\python.exe -m pip install --upgrade pip

.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Atau klik dua kali `setup_windows.bat` untuk menjalankan langkah yang sama secara otomatis.

Jika PowerShell menolak `Activate.ps1` (execution policy), cukup **jangan** pakai `Activate` — panggil Python venv secara langsung seperti contoh di bawah (`.\.venv\Scripts\python.exe ...`). Itu cara yang dipakai di seluruh panduan ini dan sudah terbukti berjalan.

## 6. Menjalankan Percobaan 1

```powershell
cd "F:\belajar mandiri\skpi\day 1\workshop_vision_tanpa_google"

.\.venv\Scripts\python.exe percobaan1.py
```

- **Input:** `tes_gambar.jpeg` (sudah tersedia di folder project).
- **Model:** `yolo11s.pt` — conf 0.30, IoU 0.50, imgsz 1280, max_det 100, augment True. File `.pt` diunduh otomatis bila belum ada.
- **Proses YOLO:** membaca gambar → deteksi objek (NMS bawaan Ultralytics) → saring di bawah conf 0.30 → nama objek murni dari model → hitung koordinat pixel + normalized.
- **Output:** daftar objek di terminal + file `hasil_deteksi_cli.jpg` (gambar + bounding box Pillow) di folder project. Buka file tersebut untuk melihat hasilnya.
- **Hasil yang diharapkan:** ±11 objek (cup, laptop, cat, potted plant, tv, book, ...) dengan confidence 30–94%.

## 7. Menjalankan Percobaan 2

Percobaan 2 = aplikasi web Flask (`app.py`). Langkah pengujian:

```powershell
cd "F:\belajar mandiri\skpi\day 1\workshop_vision_tanpa_google"

.\.venv\Scripts\python.exe app.py
```

1. Tunggu tulisan `Model YOLO siap digunakan` dan `Running on http://127.0.0.1:5000`.
2. Buka `http://127.0.0.1:5000` di browser.
3. Klik area upload / drag & drop `tes_gambar.jpeg` → preview muncul + tombol **Analyze Image** aktif.
4. Klik **Analyze Image** → scanning + progress bar + % berjalan (0→95%, 100% saat respons diterima).
5. Hasil tampil: gambar bounding box, 3 kartu ringkasan (jumlah, tertinggi, rata-rata), daftar objek terurut confidence + koordinat (klik "View coordinates").
6. Klik **Analyze Another Image** untuk menguji gambar lain.
7. Hentikan server dengan `Ctrl+C` di terminal.

## 8. Bukti Pengujian

Screenshot yang disarankan:

- **Percobaan 1:** jendela terminal yang menampilkan `=== HASIL DETEKSI OBJEK ===` + beberapa objek, **dan** file `hasil_deteksi_cli.jpg` yang terbuka (terlihat bounding box + label).
- **Percobaan 2:** halaman browser pada section **Detection Results** — terlihat gambar hasil, kartu summary, dan daftar objek.

Tidak perlu screenshot terminal yang terlalu panjang; cukup bukti hasil yang jelas.

## 9. Troubleshooting

| Masalah | Solusi |
|---|---|
| `python` tidak dikenali | Instal ulang Python, centang "Add python.exe to PATH"; tutup-buka PowerShell |
| `pip` tidak dikenali | `python -m ensurepip --upgrade`, lalu `python -m pip install --upgrade pip` |
| `ModuleNotFoundError` (ultralytics/flask/PIL) | Pastikan perintah dijalankan via `.\.venv\Scripts\python.exe` dan `pip install -r requirements.txt` sudah sukses |
| Model `.pt` tidak ditemukan | Dibiarkan — Ultralytics mengunduh otomatis saat pertama dijalankan (butuh internet) |
| `tes_gambar.jpeg` tidak ditemukan | Jalankan perintah dari folder project (`cd ...` dulu) |
| Port 5000 dipakai | Hentikan proses lama (`Ctrl+C`) atau jalankan ulang; Flask default `http://127.0.0.1:5000` |
| `Activate.ps1` ditolak PowerShell | Jangan pakai Activate; gunakan `.\.venv\Scripts\python.exe` langsung |
| `git` tidak dikenali | Instal Git for Windows, tutup-buka PowerShell |
| Git authentication gagal | Jangan pakai password — buat **Personal Access Token** di GitHub (Settings → Developer settings → Tokens), gunakan sebagai password saat push |
| `remote origin already exists` | `git remote set-url origin https://github.com/RWAMCS/workshop-vision-tanpa-google.git` (jangan add remote kedua) |

## 10. GitHub

Repository: https://github.com/RWAMCS/workshop-vision-tanpa-google

```powershell
cd "F:\belajar mandiri\skpi\day 1\workshop_vision_tanpa_google"

git init -b main

git remote add origin https://github.com/RWAMCS/workshop-vision-tanpa-google.git

git remote -v

git add .

git status

git commit -m "Initial commit - workshop vision tanpa Google"

git push -u origin main
```

Jika remote sudah ada tetapi URL-nya salah, ganti dengan:

```powershell
git remote set-url origin https://github.com/RWAMCS/workshop-vision-tanpa-google.git
```
