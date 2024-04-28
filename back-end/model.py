from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

checkpoint = "mr4/phobert-base-vi-sentiment-analysis"
tokenizer = AutoTokenizer.from_pretrained(checkpoint)
model = AutoModelForSequenceClassification.from_pretrained(checkpoint)

BAD = model.config.id2label[0]
GOOD = model.config.id2label[1]
NOMAL = model.config.id2label[2]

def detect_sentiment(input):
    raw_inputs = [input]
    inputs = tokenizer(raw_inputs, padding=True, truncation=True, return_tensors="pt")
    outputs = model(**inputs)
    prediction = torch.nn.functional.softmax(outputs.logits, dim=-1)[0]
    index_result = int(torch.argmax(prediction).numpy())
    return model.config.id2label[index_result]
    