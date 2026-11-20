"""CNN training and evaluation for context-aware text classification."""
import argparse, json, os, random
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras import layers, Model

SEED = 42
random.seed(SEED)
np.random.seed(SEED)
tf.random.set_seed(SEED)

def build_model(vocab_size, max_len, class_count, embedding_dim=128):
    tokens = layers.Input(shape=(max_len,), name="token_ids")
    embedded = layers.Embedding(vocab_size, embedding_dim)(tokens)
    pooled = []
    for kernel in (2, 3, 4):
        conv = layers.Conv1D(128, kernel, activation="relu", padding="same")(embedded)
        pooled.append(layers.GlobalMaxPooling1D()(conv))
    x = layers.Concatenate()(pooled)
    x = layers.Dropout(0.4)(x)
    x = layers.Dense(128, activation="relu")(x)
    x = layers.Dropout(0.3)(x)
    output = layers.Dense(class_count, activation="softmax")(x)
    model = Model(tokens, output)
    model.compile(optimizer="adam", loss="sparse_categorical_crossentropy",
                  metrics=["accuracy"])
    return model

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", required=True)
    parser.add_argument("--output", default="artifacts")
    parser.add_argument("--epochs", type=int, default=8)
    parser.add_argument("--max-words", type=int, default=30000)
    parser.add_argument("--max-len", type=int, default=160)
    args = parser.parse_args()
    df = pd.read_csv(args.csv)
    required = {"text", "context", "label"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing CSV columns: {sorted(missing)}")
    df = df.dropna(subset=["text", "label"]).copy()
    df["context"] = df["context"].fillna("")
    if df["label"].nunique() < 2:
        raise ValueError("At least two distinct classes are required.")
    combined = [
        f"[POST] {str(t)} [CONTEXT] {str(c)}"
        for t, c in zip(df["text"], df["context"])
    ]
    encoder = LabelEncoder()
    y = encoder.fit_transform(df["label"].astype(str))
    x_train, x_test, y_train, y_test = train_test_split(
        combined, y, test_size=0.2, random_state=SEED, stratify=y)
    tokenizer = Tokenizer(num_words=args.max_words, oov_token="<OOV>")
    tokenizer.fit_on_texts(x_train)
    train_x = pad_sequences(tokenizer.texts_to_sequences(x_train), maxlen=args.max_len)
    test_x = pad_sequences(tokenizer.texts_to_sequences(x_test), maxlen=args.max_len)
    model = build_model(args.max_words, args.max_len, len(encoder.classes_))
    model.fit(train_x, y_train, validation_split=0.15, epochs=args.epochs,
              batch_size=32, callbacks=[tf.keras.callbacks.EarlyStopping(
                  monitor="val_loss", patience=2, restore_best_weights=True)])
    predictions = model.predict(test_x, verbose=0).argmax(axis=1)
    os.makedirs(args.output, exist_ok=True)
    model.save(os.path.join(args.output, "context_cnn.keras"))
    with open(os.path.join(args.output, "tokenizer.json"), "w", encoding="utf-8") as f:
        f.write(tokenizer.to_json())
    with open(os.path.join(args.output, "labels.json"), "w", encoding="utf-8") as f:
        json.dump(encoder.classes_.tolist(), f, ensure_ascii=False, indent=2)
    report = classification_report(y_test, predictions,
        target_names=encoder.classes_, output_dict=True, zero_division=0)
    with open(os.path.join(args.output, "evaluation.json"), "w", encoding="utf-8") as f:
        json.dump({"classification_report": report,
                   "confusion_matrix": confusion_matrix(y_test, predictions).tolist(),
                   "test_samples": int(len(y_test)), "seed": SEED},
                  f, ensure_ascii=False, indent=2)
    print("Artifacts saved to", args.output)

if __name__ == "__main__":
    main()
