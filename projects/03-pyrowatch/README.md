# PyroWatch — Fire & Smoke Image Analysis

A Python/Flask application connecting media submission, analysis history, and a configurable computer-vision model adapter.

## Components

- Authenticated image and video submission records
- File-type checks and upload-size controls
- Analysis records and history pages
- Optional YOLO image-inference adapter
- Annotated output for successful image inference

## Technology

Python · Flask · Ultralytics YOLO adapter · OpenCV

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"
flask --app run.py create-admin
python run.py
```

For model-based image analysis, configure compatible model weights and optional dependencies:

```bash
pip install ultralytics opencv-python-headless
export MODEL_PATH=/absolute/path/to/verified-model.pt
```

The web application handles analysis records independently of model configuration.

## Automated tests

Three GitHub Actions tests cover authentication/dashboard rendering, unsupported-file rejection, and analysis-detail pages. Model inference is activated through the optional adapter and externally configured weights.
