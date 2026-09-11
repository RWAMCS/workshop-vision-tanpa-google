from pathlib import Path
from ultralytics import YOLO
from PIL import Image, ImageDraw, ImageFont

MODEL_NAME = "yolo11s.pt"

# Parameter inference — mudah diubah jika diperlukan.
# conf=0.30 dipilih sebagai titik seimbang: menekan false positive
# tanpa menghilangkan objek valid (jangan naikkan ke ~0.70).
CONF_THRESHOLD = 0.30
IOU_THRESHOLD = 0.50
IMG_SIZE = 1280
MAX_DET = 100
USE_AUGMENT = True  # Test-Time Augmentation agar robust thd ukuran/posisi/kondisi gambar.


def _predict(model, source):
    """Jalankan inference dengan fallback aman jika `augment` tidak didukung."""
    params = dict(source=source, conf=CONF_THRESHOLD, iou=IOU_THRESHOLD,
                  imgsz=IMG_SIZE, max_det=MAX_DET, verbose=False)
    if USE_AUGMENT:
        try:
            return model.predict(augment=True, **params)
        except TypeError:
            # Versi Ultralytics lama tidak mengenal argumen `augment`.
            # Fallback: inference normal tanpa TTA.
            return model.predict(**params)
    return model.predict(**params)


def _gambar_hasil_pillow(input_path, output_path, detections):
    """Gambar bounding box YOLO memakai Pillow. Koordinat di-clamp agar di dalam gambar."""
    image = Image.open(input_path).convert("RGB")
    w, h = image.size
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.truetype("arial.ttf", 18)
    except OSError:
        font = ImageFont.load_default()

    for item in detections:
        x1, y1, x2, y2 = item["box_pixel"]
        # Clamp agar box tidak keluar dari ukuran gambar.
        x1 = min(max(0.0, x1), w - 1)
        y1 = min(max(0.0, y1), h - 1)
        x2 = min(max(0.0, x2), w - 1)
        y2 = min(max(0.0, y2), h - 1)
        if x2 <= x1 or y2 <= y1:
            continue
        label = f'{item["name"]} {item["confidence"]:.1f}%'
        draw.rectangle((x1, y1, x2, y2), outline="red", width=4)
        ty = max(0, y1 - 28)
        bbox = draw.textbbox((x1, ty), label, font=font)
        draw.rectangle(bbox, fill="red")
        draw.text((x1 + 4, ty + 1), label, fill="white", font=font)
    image.save(output_path)


def uji_deteksi_objek(nama_file_gambar):
    gambar = Path(nama_file_gambar)
    if not gambar.exists():
        print(f"ERROR: File gambar tidak ditemukan: {gambar}")
        return

    try:
        with Image.open(gambar) as im:
            im.verify()
        with Image.open(gambar) as im2:
            img_w, img_h = im2.convert("RGB").size
    except Exception as e:
        print(f"ERROR: Format gambar tidak valid / gagal dibuka: {gambar} ({e})")
        return

    try:
        print("Memuat model YOLO...")
        model = YOLO(MODEL_NAME)
    except Exception as e:
        print(f"ERROR: Model gagal dimuat ({MODEL_NAME}): {e}")
        return

    print(f"Menganalisis gambar: {gambar}")
    try:
        hasil = _predict(model, str(gambar))
    except Exception as e:
        print(f"ERROR: Inference gagal: {e}")
        return
    result = hasil[0]

    print("\n=== HASIL DETEKSI OBJEK ===")
    if result.boxes is None or len(result.boxes) == 0:
        print("Tidak ada objek yang terdeteksi.")
        return

    detections = []
    for box in result.boxes:
        # NMS sudah ditangani Ultralytics (iou + max_det di atas),
        # jadi tidak dibuat NMS manual di sini.
        class_id = int(box.cls[0])
        nama_objek = result.names[class_id]  # anti-hallucination: nama HANYA dari model
        confidence = float(box.conf[0]) * 100
        # Post-processing general: saring sisa deteksi di bawah threshold utama.
        # Satu threshold untuk semua class agar tetap universal.
        if (confidence / 100.0) < CONF_THRESHOLD:
            continue
        x1, y1, x2, y2 = [float(v) for v in box.xyxy[0].tolist()]
        # Normalized 0-1 berdasarkan ukuran asli gambar.
        nx1 = min(max(x1 / img_w, 0.0), 1.0)
        ny1 = min(max(y1 / img_h, 0.0), 1.0)
        nx2 = min(max(x2 / img_w, 0.0), 1.0)
        ny2 = min(max(y2 / img_h, 0.0), 1.0)
        detections.append({
            "name": nama_objek,
            "confidence": confidence,
            "box_pixel": [x1, y1, x2, y2],
            "box_norm": [nx1, ny1, nx2, ny2],
        })

    if not detections:
        print("Tidak ada objek yang terdeteksi.")
        return

    for i, d in enumerate(detections, start=1):
        x1, y1, x2, y2 = d["box_pixel"]
        nx1, ny1, nx2, ny2 = d["box_norm"]
        print(f"\nObjek {i}")
        print(f"Nama       : {d['name']}")
        print(f"Confidence : {d['confidence']:.2f}%")
        print(f"Bounding Box (pixel): x1={x1:.1f}, y1={y1:.1f}, x2={x2:.1f}, y2={y2:.1f}")
        print("Bounding Box (normalized): "
              f"x1={nx1:.4f}, y1={ny1:.4f}, x2={nx2:.4f}, y2={ny2:.4f}")

    try:
        output = Path("hasil_deteksi_cli.jpg")
        _gambar_hasil_pillow(str(gambar), str(output), detections)
        print(f"\nGambar hasil disimpan sebagai: {output.resolve()}")
    except Exception as e:
        print(f"ERROR: Gagal menyimpan gambar hasil: {e}")

if __name__ == "__main__":
    uji_deteksi_objek("tes_gambar.jpeg")
