# query_model.py

import requests
from embedding_generator import generate_embedding
from database_manager import search_similar_embeddings

# Configuración del modelo Llama8B en Azure
AZURE_ENDPOINT = 'URL EP'
AZURE_API_KEY = 'API Key'

def query_llm(query):
    """
    Realiza una consulta al modelo LLM y obtiene una respuesta.
    
    Args:
        query (str): La consulta para el modelo.

    Returns:
        str: La respuesta del modelo.
    """
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {AZURE_API_KEY}'
    }

    # Crea la estructura de la solicitud
    data = {
        "messages": [{
            "role": "system", 
            "content": "You are a DBA expert who reviews SQL Server scripts to analyze their complexity, potential security issues, performance, and potential problems. You must respond with your findings, prioritized by level of danger, and provide a solution. This solution can be in code or with an explanation of how to solve each problem.\nAlways answer as helpfully as possible, while being safe.\nYour answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content.\nPlease ensure that your responses are socially unbiased and positive in nature.\nIf you don't know the answer to a question, please don't share false information.\nFeel free to use Markdown for formatting.\n"
            },
            {
                "role": "user", 
                "content": query
            }],
        "model": "llama3B",  # O el modelo que estés usando
        "max_tokens": 500,  # Ajusta según tus necesidades
        "temperature": 0.7,
    }

    # Envía la solicitud al modelo
    response = requests.post(AZURE_ENDPOINT, headers=headers, json=data)

    # Maneja la respuesta
    if response.status_code == 200:
        response_data = response.json()
        return response_data.get("choices")[0].get("message").get("content")
    else:
        raise Exception(f"Error al consultar el modelo: {response.status_code} - {response.text}")
