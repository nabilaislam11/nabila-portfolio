"""Optional YOLO inference adapter. No pretrained weights are bundled."""
from pathlib import Path

class DetectorUnavailable(RuntimeError):
    pass

class FireSmokeDetector:
    def __init__(self, model_path):
        self.model_path = model_path
        self.model = None

    def load(self):
        if not self.model_path or not Path(self.model_path).is_file():
            raise DetectorUnavailable(
                "Model weights are not configured. Set MODEL_PATH to a compatible fire/smoke YOLO weights file.")
        try:
            from ultralytics import YOLO
        except ImportError as exc:
            raise DetectorUnavailable(
                "Ultralytics is not installed. Install the optional vision dependencies first.") from exc
        self.model = YOLO(self.model_path)
        return self

    def predict_image(self, image_path, output_path, confidence=0.35):
        if self.model is None:
            self.load()
        results = self.model.predict(source=str(image_path), conf=confidence, save=False, verbose=False)
        result = results[0]
        plotted = result.plot()
        try:
            import cv2
        except ImportError as exc:
            raise DetectorUnavailable("OpenCV is required to save annotated output.") from exc
        if not cv2.imwrite(str(output_path), plotted):
            raise RuntimeError("Could not write annotated image.")
        detections = []
        names = result.names
        if result.boxes is not None:
            for box in result.boxes:
                cls_id = int(box.cls.item())
                conf = float(box.conf.item())
                detections.append({"label": str(names.get(cls_id, cls_id)), "confidence": conf})
        return detections
