# Context-Aware Hate Speech Detection with CNN

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
