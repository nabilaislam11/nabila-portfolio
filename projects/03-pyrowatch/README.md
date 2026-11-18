# PyroWatch — Fire and Smoke Detection

A reconstructed image-analysis application inspired by the academic project title **Advanced Fire and Smoke Detection System**.

## Reference implementation

- Python and Flask web interface
- Authenticated image/video submission records
- File extension allow-list and upload-size limit
- Detection history and analysis details
- Optional YOLO inference adapter using externally supplied model weights
- Annotated image output when inference runs successfully

## Run locally

From this directory:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"
flask --app run.py create-admin
python run.py
```

For actual image inference, install compatible optional packages:

```bash
pip install ultralytics opencv-python-headless
export MODEL_PATH=/absolute/path/to/your/verified-model.pt
```

The model must be trained for compatible fire/smoke classes. No model weights are bundled. OpenCV and Ultralytics versions must be compatible with the local Python and hardware environment.

## Validation status

The latest GitHub Actions run passed 3 tests under `tests/`, covering login/dashboard rendering, unsupported-file rejection, and analysis/record-detail page rendering. Actual model inference has not been run because no verified weights or dataset were supplied. No detection examples or accuracy results are included or claimed.

## Scope and provenance

This is a newly authored reference implementation, not a verified reproduction of the original academic source code.

## Known limitations

- Video inference is not implemented; video uploads are only recorded as not processed.
- Model accuracy, class mapping, threshold calibration, and real-world validation depend on the supplied model and dataset.
- This is an experimental portfolio demonstrator, not a certified fire alarm or life-safety system.
- Production use requires stronger file-content validation, access controls, retention policies, asynchronous inference, and deployment hardening.
