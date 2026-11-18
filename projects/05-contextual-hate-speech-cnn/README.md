# CNN-based Approaches for Contextual Hate Speech Detection

A reconstructed machine-learning baseline inspired by the academic project title **CNN-based Approaches for Contextual Hate Speech Detection**.

## Reference pipeline
- CSV input with post text, conversational context and label
- Context-marked text concatenation
- Tokenization and sequence padding
- Embedding layer
- Parallel 1D CNN branches with kernel sizes 2, 3 and 4
- Dropout and softmax classification
- Early stopping, classification report and confusion matrix export
- Separate prediction script

## Scope and provenance
This is a newly authored reference pipeline, not a verified reproduction of the original academic implementation. No dataset, model weights, benchmark scores or experimental findings are fabricated or included.

## Evaluation cautions
A credible study should use author- or conversation-grouped splits to reduce leakage, report macro-F1 and per-class metrics, compare suitable baselines, and inspect context-sensitive errors. Predictions require human review and should not be used as the sole basis for punitive decisions.

## Validation status
Python syntax compilation passed. Training and inference have not been run because no dataset or trained model was supplied.

## Original academic project: source and attribution

The original CSE438 group submission includes a final paper and presentation titled “Unlocking the Potential of NLP: CNN based Approaches for Contextual Hate Speech Detection” and identifies Nabila Islam Borno as a group member. This repository's TensorFlow code is a later reference pipeline, not the original experiment.

Original group materials: https://github.com/Khandaker-Atik/cse438/tree/main/submission6

This was collaborative academic work. Specific individual implementation responsibilities are pending confirmation. The implementation and tests documented in this directory describe a later independently reconstructed reference build, not a copy of the historical submission. No original group files have been imported into this repository.
