# embedding_generator.py

from transformers import AutoTokenizer, AutoModel
import torch
import numpy as np

# Cargar el modelo y el tokenizador de Hugging Face
tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
model = AutoModel.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')

def generate_embedding(text):
    """
    Genera un embedding a partir de un texto dado utilizando el modelo de Hugging Face.
    
    Args:
        text (str): Texto para el cual se generará el embedding.
    
    Returns:
        numpy.ndarray: El embedding generado como un vector.
    """
    inputs = tokenizer(text, return_tensors='pt', padding=True, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
    # Usar la representación del [CLS] token como embedding
    embedding = outputs.last_hidden_state[:, 0, :].numpy()
    return embedding.flatten()  # Asegúrate de devolver un vector 1-D
