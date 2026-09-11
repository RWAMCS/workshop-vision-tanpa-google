# Laporan Praktikum — Object Localization Tanpa Google Cloud

## Tujuan
Mendeteksi objek pada gambar dan menampilkan nama objek, confidence score, serta bounding box.

## Teknologi
Python, Ultralytics YOLO, Pillow, Flask, HTML/CSS.

## Alur Sistem
1. Pengguna memilih gambar.
2. YOLO lokal mendeteksi objek.
3. Sistem mengambil nama objek, confidence, dan koordinat bounding box.
4. Pillow menggambar bounding box dan label.
5. Flask menampilkan hasil di browser.

## Eksperimen 1
File `percobaan1.py` menjalankan deteksi melalui terminal.

## Eksperimen 2
File `app.py` menyediakan antarmuka web untuk upload dan deteksi.

## Perbedaan
Implementasi ini tidak menggunakan Google Cloud Vision API, Google Cloud Billing, Service Account, API key, atau `kredensial.json`.

## Kesimpulan
Object localization dapat dijalankan secara lokal tanpa layanan cloud. YOLO menghasilkan informasi objek, confidence score, dan bounding box yang kemudian divisualisasikan menggunakan Pillow dan ditampilkan melalui Flask.

Catatan: bila dosen secara khusus mewajibkan Google Cloud Vision API, implementasi ini harus disebut sebagai alternatif lokal.
