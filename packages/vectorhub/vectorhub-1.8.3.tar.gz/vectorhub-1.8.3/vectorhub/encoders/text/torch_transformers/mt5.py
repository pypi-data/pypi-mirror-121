from ..base import BaseText2Vec
from ....base import catch_vector_errors

try:
    import torch
    from transformers import T5Tokenizer, MT5ForConditionalGeneration
except:
    import traceback
    traceback.print_exc()

class MT52Vec(BaseText2Vec):
    def __init__(self, model_name: str='unicamp-dl/mt5-base-multi-msmarco'):
        self.tokenizer  = T5Tokenizer.from_pretrained(model_name)
        self.model      = MT5ForConditionalGeneration.from_pretrained(model_name).eval()
        self.model_name = self.model_name
        self.vector_length = 768
    
    @property
    def urls(self):
        return {"unicamp-dl/mt5-base-multi-msmarco": {"vector_length": 768}}
    
    @property
    def __name__(self):
        return self.model_name

    @catch_vector_errors
    def encode(self, text):
        enc = self.tokenizer(text, return_tensors="pt")
        output = self.model.encoder(
            input_ids=enc["input_ids"], 
            attention_mask=enc["attention_mask"], 
            return_dict=True
        )
        emb = output.last_hidden_state
        return torch.mean(emb, axis=1).tolist()[0]

    def _pad_tensor(self, tensor):
        max_len = max([len(x) for x in tensor])
        return torch.tensor([x + [0] * (max_len - len(x)) for x in tensor])

    def bulk_encode(self, texts: list, pooling_method='mean'):
        tok_output = self.tokenizer(texts)
        if pooling_method != "mean":
            raise ValueError("")
        return torch.mean(self.model.encoder.forward(
            input_ids=self._pad_tensor(
                tok_output['input_ids']), 
                attention_mask=self._pad_tensor(tok_output['attention_mask'])
                )['last_hidden_state'], axis=1).tolist()
