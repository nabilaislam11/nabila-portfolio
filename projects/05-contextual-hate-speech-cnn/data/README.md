# CNN Dataset Format

Use a CSV with three fields:

| Column | Description |
| --- | --- |
| `text` | Input sentence or social-media post |
| `context` | Optional conversational context associated with the text |
| `label` | Category for supervised classification |

Keep training, validation and test samples separated when comparing experiments. See the [main academic research repository](https://github.com/nabilaislam11/contextual-hate-speech-detection-cnn) for the final paper, methodology and CNN training pipeline.
