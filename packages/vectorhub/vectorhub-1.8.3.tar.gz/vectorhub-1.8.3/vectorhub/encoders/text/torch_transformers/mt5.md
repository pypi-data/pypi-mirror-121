---
model_id: "text/mt5"
model_name: "MT5" 
vector_length: "768 (default)"
paper: "https://arxiv.org/abs/2010.02559"
repo: "https://huggingface.co/nlpaueb/legal-bert-base-uncased"
release_date: "2021-06-01"
installation: "pip install vectorhub[encoders-text-torch-transformers]"
category: text
short_description: We propose a systematic investigation of the available strategies when applying BERT in Legal domains.
---

## Description

Multilingual T5 (mT5) is a massively multilingual pretrained text-to-text transformer model, trained following a similar recipe as T5. This repo can be used to reproduce the experiments in the mT5 paper.

## Example

```python
#pip install vectorhub[encoders-text-torch-transformers]
from vectorhub.encoders.text.torch_transformers import MT52Vec
model = MT52Vec()
model.encode("I enjoy taking long walks along the beach with my dog.")
```
