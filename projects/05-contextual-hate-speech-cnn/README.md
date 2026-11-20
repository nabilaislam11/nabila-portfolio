# Context-Aware Hate Speech Detection — CNN Pipeline

A Python/TensorFlow implementation exploring context-aware text classification using one-dimensional convolutional neural networks.

**Related academic research:** [Contextual Hate Speech Detection with CNNs](https://github.com/nabilaislam11/contextual-hate-speech-detection-cnn), including the final research paper, methodology, and reported results.

## Pipeline

- CSV input for post text, conversational context, and category
- Context markers, tokenization, and sequence padding
- Embedding layer and parallel Conv1D branches
- Dropout and softmax classification
- Training script with early stopping and evaluation exports
- Separate prediction script

## Technology

Python · TensorFlow/Keras · NumPy · Pandas · scikit-learn

## Source

- `src/train.py` — model definition, training, and evaluation workflow
- `src/predict.py` — inference from saved model artifacts
- `requirements.txt` — dependencies
- `data/README.md` — input format

The [academic research repository](https://github.com/nabilaislam11/contextual-hate-speech-detection-cnn) brings together the final paper, experimental analysis, and a companion CNN training and evaluation pipeline. This portfolio implementation demonstrates a context-column classification workflow.

## Verification

The GitHub Actions workflow checks Python source compilation. Training follows the input schema described in `data/README.md`.
