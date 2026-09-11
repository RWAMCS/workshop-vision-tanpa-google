# Workshop Vision Tanpa Google

Implementasi **Object Localization berbasis Computer Vision** yang berjalan secara lokal di komputer tanpa menggunakan Google Cloud Vision API.

Project ini menggunakan **YOLO dari Ultralytics** untuk mendeteksi objek pada gambar, kemudian menampilkan:

- Nama objek
- Confidence
- Bounding box
- Koordinat bounding box dalam pixel
- Koordinat bounding box dalam format normalized 0–1

Hasil deteksi dapat digunakan melalui dua metode:

1. **Percobaan 1 — CLI / Terminal**
2. **Percobaan 2 — Web Application menggunakan Flask**

Tidak membutuhkan:

- Google Cloud Vision API
- Google Cloud Billing
- Google Service Account
- `kredensial.json`
- Google API Key

---

# 1. Cara Kerja

Secara sederhana, sistem bekerja seperti berikut:

```text
                    INPUT
                      │
                      ▼
                Gambar / Foto
                      │
                      ▼
              YOLO Ultralytics
                      │
                      ▼
              Object Detection
                      │
          ┌───────────┴───────────┐
          ▼                       ▼
    Nama Objek               Confidence
          │                       │
          └───────────┬───────────┘
                      ▼
                Bounding Box
                      │
          ┌───────────┴───────────┐
          ▼                       ▼
     Pixel Coordinate       Normalized 0–1
                      │
                      ▼
                Hasil Deteksi
