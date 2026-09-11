# Workshop Vision — Versi Tanpa Google Cloud

Versi ini menjalankan Object Localization secara lokal menggunakan YOLO. Tidak membutuhkan Google Cloud, billing, Service Account, atau `kredensial.json`.

## Alur
Gambar → YOLO lokal → Nama objek + confidence + bounding box → Pillow → Flask → Browser

## Instalasi
Buka PowerShell di folder project:

```powershell
python -m venv .venv --without-pip
.\.venv\Scripts\python.exe -m ensurepip --upgrade
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Eksperimen 1
Letakkan `tes_gambar.jpeg` di folder project, lalu:

```powershell
.\.venv\Scripts\python.exe percobaan1.py
```

Pertama kali dijalankan, model `yolo11n.pt` akan diunduh otomatis.

## Eksperimen 2
Jalankan:

```powershell
.\.venv\Scripts\python.exe app.py
```

Buka `http://127.0.0.1:5000` di browser, upload gambar, lalu klik Deteksi Objek.

## Catatan laporan
Jika tugas asli mewajibkan Google Cloud Vision API, tuliskan bahwa YOLO adalah alternatif lokal untuk demonstrasi Object Localization karena Cloud Vision memerlukan billing. Jangan menyebut YOLO sebagai Google Cloud Vision API.
