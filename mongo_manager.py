# mongo_manager.py
import pymongo
import sys
from pymongo import MongoClient
import numpy as np
import ssl
import certifi

ca = certifi.where()

# Conectar a MongoDB
client = pymongo.MongoClient('url mongo db')
#client = MongoClient('mongodb+srv://ragapp.5h0ff.mongodb.net/" --apiVersion 1 --username ragapp --password gGl78MsaCmEXkupo')  # Cambia la URL según tu configuración de MongoDB
db = client.ragapp
#db = client['ragapp']
collection = db['code_embeddings']

def insert_embedding(file_path, embedding):
    """
    Inserta un embedding en la colección de MongoDB.
    """
    # Asegúrate de que el embedding sea 1-D
    if isinstance(embedding, np.ndarray):
        embedding = embedding.flatten().tolist()  # Convierte a lista 1-D

    document = {
        "file_path": file_path,
        "embedding": embedding
    }
    collection.insert_one(document)
    print(f"Embedding insertado para el archivo: {file_path}")
