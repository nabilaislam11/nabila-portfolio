from pathlib import Path
from uuid import uuid4
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, send_from_directory
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app import db
from app.models import DetectionRecord
from app.services.detector import FireSmokeDetector, DetectorUnavailable

main_bp = Blueprint("main", __name__)

def _extension(filename):
    return filename.rsplit(".", 1)[-1].lower() if "." in filename else ""

@main_bp.get("/")
@login_required
def dashboard():
    total = DetectionRecord.query.count()
    completed = DetectionRecord.query.filter_by(status="completed").count()
    recent = DetectionRecord.query.order_by(DetectionRecord.created_at.desc()).limit(8).all()
    model_path = current_app.config.get("MODEL_PATH", "")
    ready = bool(model_path and Path(model_path).is_file())
    return render_template("dashboard.html", total=total, completed=completed,
        recent=recent, model_ready=ready)

@main_bp.route("/analyze", methods=["GET", "POST"])
@login_required
def analyze():
    if request.method == "POST":
        file = request.files.get("media")
        if not file or not file.filename:
            flash("Select an image or video first.", "error")
            return redirect(url_for("main.analyze"))
        ext = _extension(file.filename)
        image_ext = current_app.config["ALLOWED_IMAGE_EXTENSIONS"]
        video_ext = current_app.config["ALLOWED_VIDEO_EXTENSIONS"]
        if ext not in image_ext | video_ext:
            flash("Unsupported file type. Upload JPG, PNG, WEBP, MP4, AVI, MOV or MKV.", "error")
            return redirect(url_for("main.analyze"))
        upload_dir = Path(current_app.config["UPLOAD_FOLDER"])
        upload_dir.mkdir(parents=True, exist_ok=True)
        safe = secure_filename(file.filename) or "upload"
        stored = f"{uuid4().hex}_{safe}"
        source = upload_dir / stored
        file.save(source)
        record = DetectionRecord(original_filename=safe,
            media_type="image" if ext in image_ext else "video",
            status="processing", created_by=current_user.id)
        db.session.add(record)
        db.session.commit()
        if ext in video_ext:
            record.status = "not_processed"
            record.error_message = "Video inference is not implemented in this reference build."
            db.session.commit()
            flash("Video stored as a record; video inference is not implemented yet.", "warning")
            return redirect(url_for("main.record_detail", record_id=record.id))
        output = f"annotated_{uuid4().hex}.jpg"
        try:
            detector = FireSmokeDetector(current_app.config.get("MODEL_PATH", ""))
            detections = detector.predict_image(source, upload_dir / output)
            record.status = "completed"
            record.detection_count = len(detections)
            record.result_filename = output
            if detections:
                record.confidence_summary = ", ".join(
                    f"{d['label']}: {d['confidence']:.2f}" for d in detections[:5])
            else:
                record.confidence_summary = "No detections returned by the configured model."
            db.session.commit()
        except DetectorUnavailable as exc:
            record.status = "model_unavailable"
            record.error_message = str(exc)
            db.session.commit()
        except Exception as exc:
            record.status = "failed"
            record.error_message = str(exc)[:500]
            db.session.commit()
        return redirect(url_for("main.record_detail", record_id=record.id))
    return render_template("analyze.html")

@main_bp.get("/records/<int:record_id>")
@login_required
def record_detail(record_id):
    record = db.get_or_404(DetectionRecord, record_id)
    return render_template("record_detail.html", record=record)

@main_bp.get("/media/<path:filename>")
@login_required
def media(filename):
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], filename, as_attachment=False)
