# chat_with_code.py

import numpy as np
from mongo_manager import collection
from query_model import query_llm, generate_embedding  # Actualizamos la importación al archivo y método correctos
from sklearn.metrics.pairwise import cosine_similarity

def find_relevant_code_snippets(query_embedding, top_k=3):
    """
    Encuentra los fragmentos de código más relevantes basados en la similitud de embeddings.
    """
    # Convertimos el embedding a una matriz 2D para usar con cosine_similarity
    query_vector = np.array(query_embedding).reshape(1, -1)

    # Recuperamos todos los documentos desde MongoDB
    documents = list(collection.find({}))

    # Calcular las similitudes del coseno en Python
    similarities = []
    for doc in documents:
        code_embedding = np.array(doc['embedding']).reshape(1, -1)
        similarity = cosine_similarity(query_vector, code_embedding)[0][0]
        similarities.append((doc, similarity))

    # Ordenar los documentos por similitud en orden descendente
    similarities = sorted(similarities, key=lambda x: x[1], reverse=True)

    # Devolver los top_k fragmentos más relevantes
    relevant_snippets = [item[0] for item in similarities[:top_k]]

    return relevant_snippets

def chat_with_code(user_query):
    """
    Procesa la consulta del usuario y devuelve una respuesta del modelo Llama8B.
    """
    # Generar el embedding de la consulta del usuario
    query_embedding = generate_embedding(user_query)

    # Encontrar los fragmentos de código más relevantes
    relevant_code_snippets = find_relevant_code_snippets(query_embedding)

    # Construir el contexto con los fragmentos de código más relevantes
    code_context = "\n\n".join([snippet['file_path'] + ":\n" + str(snippet['embedding']) for snippet in relevant_code_snippets])

    # Preparar el prompt para el modelo LLM
    prompt = f"Contexto del código:\n{code_context}\n\nPregunta del usuario: {user_query}\n\nResponde de manera detallada:"

    # Obtener la respuesta del modelo usando query_llm desde query_model.py
    response = query_llm(prompt)

    return response
