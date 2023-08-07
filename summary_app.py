from transformers import pipeline

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")