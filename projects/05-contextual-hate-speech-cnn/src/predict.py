"""Inference CLI for a trained contextual CNN."""
import argparse
import json
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.text import tokenizer_from_json
from tensorflow.keras.preprocessing.sequence import pad_sequences

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="artifacts/context_cnn.keras")
    parser.add_argument("--tokenizer", default="artifacts/tokenizer.json")
    parser.add_argument("--labels", default="artifacts/labels.json")
    parser.add_argument("--text", required=True)
    parser.add_argument("--context", default="")
    parser.add_argument("--max-len", type=int, default=160)
    args = parser.parse_args()
    model = tf.keras.models.load_model(args.model)
    with open(args.tokenizer, encoding="utf-8") as stream:
        tokenizer = tokenizer_from_json(stream.read())
    with open(args.labels, encoding="utf-8") as stream:
        labels = json.load(stream)
    combined = f"[POST] {args.text} [CONTEXT] {args.context}"
    sequence = pad_sequences(tokenizer.texts_to_sequences([combined]), maxlen=args.max_len)
    scores = model.predict(sequence, verbose=0)[0]
    index = int(np.argmax(scores))
    print(json.dumps({"predicted_label": labels[index],
        "confidence": float(scores[index]),
        "warning": "Model output is a screening signal, not a definitive judgment."},
        ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
