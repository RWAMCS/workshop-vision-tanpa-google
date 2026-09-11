from pathlib import Path
from uuid import uuid4
from flask import Flask, render_template, request
from PIL import Image, ImageDraw, ImageFont
from ultralytics import YOLO

app = Flask(__name__)
BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "static/uploads"
RESULT_DIR = BASE_DIR / "static/results"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
RESULT_DIR.mkdir(parents=True, exist_ok=True)
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}

MODEL_NAME = "yolo11s.pt"

# Parameter inference — mudah diubah jika diperlukan.
# conf=0.30 = titik seimbang (menekan false positive tanpa menghapus objek valid).
CONF_THRESHOLD = 0.30
IOU_THRESHOLD = 0.50
IMG_SIZE = 1280
MAX_DET = 100
USE_AUGMENT = True  # Test-Time Augmentation; ada fallback aman bila tidak didukung.

print("Memuat model YOLO...")
try:
    model = YOLO(MODEL_NAME)
except Exception as e:
    print(f"ERROR: Model gagal dimuat ({MODEL_NAME}): {e}")
    raise
print("Model YOLO siap digunakan.")

def predict_with_fallback(source):
    """Inference dengan fallback aman jika `augment` tidak didukung versi Ultralytics."""
    params = dict(source=source, conf=CONF_THRESHOLD, iou=IOU_THRESHOLD,
                  imgsz=IMG_SIZE, max_det=MAX_DET, verbose=False)
    if USE_AUGMENT:
        try:
            return model.predict(augment=True, **params)
        except TypeError:
            # Versi lama tidak mengenal `augment` -> inference normal.
            return model.predict(**params)
    return model.predict(**params)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def buat_gambar_hasil(input_path, output_path, detections):
    image = Image.open(input_path).convert("RGB")
    w, h = image.size
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.truetype("arial.ttf", 18)
    except OSError:
        font = ImageFont.load_default()

    for item in detections:
        x1, y1, x2, y2 = item["box"]
        # Clamp agar box jelas & tidak keluar dari ukuran gambar.
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
    image.save(output_path, quality=95)

@app.route("/", methods=["GET", "POST"])
def index():
    error = None
    detections = []
    image_url = None

    if request.method == "POST":
        if "file" not in request.files:
            error = "File gambar belum dipilih."
            return render_template("index.html", error=error)
        file = request.files["file"]
        if not file.filename:
            error = "File gambar belum dipilih."
            return render_template("index.html", error=error)
        if not allowed_file(file.filename):
            error = "Format file harus JPG, JPEG, PNG, atau WEBP."
            return render_template("index.html", error=error)

        extension = file.filename.rsplit(".", 1)[1].lower()
        unique_name = f"{uuid4().hex}.{extension}"
        upload_path = UPLOAD_DIR / unique_name
        result_path = RESULT_DIR / f"hasil_{unique_name}"
        try:
            file.save(upload_path)
        except Exception as e:
            error = f"Gagal menyimpan file upload: {e}"
            return render_template("index.html", error=error)

        # Validasi gambar bisa dibuka + ambil ukuran asli untuk normalized coords.
        try:
            with Image.open(upload_path) as im:
                im.verify()
            with Image.open(upload_path) as im2:
                img_w, img_h = im2.convert("RGB").size
        except Exception:
            try:
                upload_path.unlink(missing_ok=True)
            except OSError:
                pass
            error = "File gambar tidak valid atau gagal dibuka."
            return render_template("index.html", error=error)

        try:
            results = predict_with_fallback(str(upload_path))
        except Exception as e:
            error = f"Inference YOLO gagal: {e}"
            return render_template("index.html", error=error)
        result = results[0]

        if result.boxes is not None:
            for box in result.boxes:
                # NMS sudah ditangani Ultralytics (iou + max_det);
                # tidak dibuat NMS manual.
                class_id = int(box.cls[0])
                confidence = float(box.conf[0]) * 100
                # Filter general satu threshold untuk semua class.
                if (confidence / 100.0) < CONF_THRESHOLD:
                    continue
                x1, y1, x2, y2 = [float(v) for v in box.xyxy[0].tolist()]
                nx1 = min(max(x1 / img_w, 0.0), 1.0)
                ny1 = min(max(y1 / img_h, 0.0), 1.0)
                nx2 = min(max(x2 / img_w, 0.0), 1.0)
                ny2 = min(max(y2 / img_h, 0.0), 1.0)
                detections.append({
                    "name": result.names[class_id],  # anti-hallucination: nama HANYA dari model
                    "confidence": confidence,
                    "box": [x1, y1, x2, y2],
                    "box_norm": [nx1, ny1, nx2, ny2],
                })

        try:
            buat_gambar_hasil(upload_path, result_path, detections)
        except Exception as e:
            error = f"Gagal membuat gambar hasil: {e}"
            return render_template("index.html", error=error, detections=detections)
        image_url = f"/static/results/hasil_{unique_name}"

    return render_template("index.html", error=error, detections=detections, image_url=image_url)

if __name__ == "__main__":
    app.run(debug=True)
