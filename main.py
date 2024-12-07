# main.py

from github_manager import download_repo
from embedding_generator import generate_embedding
from mongo_manager import insert_embedding
import os
from code_chat import chat_with_code

# Datos del repositorio privado
repo_owner = 'jfgg'
repo_name = 'sql-ragapp'

# Descargar el repositorio privado de GitHub
repo_dir = download_repo(repo_owner, repo_name)

if repo_dir:
    # Recorrer los archivos descargados del repositorio
    for root, _, files in os.walk(repo_dir):
        for file in files:
            if file.endswith('.sql'):  # Filtrar solo archivos de código Python
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    code_content = f.read()

                # Generar el embedding para el archivo de código y guardarlo en MongoDB
                embedding = generate_embedding(code_content)
                insert_embedding(file_path, embedding)

    print("Embeddings generados e insertados en MongoDB exitosamente.")
else:
    print("No se pudo descargar el repositorio.")

# Pregunta del usuario
user_query = "Analisa el archivo estadisticasUsuario.sql (This script returns information on each user-created statistics object, along with the DROP STATISTICS object to run if appropriate.) y dame recomendaciones para mejorarlo"

# Obtener respuesta del modelo
response = chat_with_code(user_query)
print(f"Respuesta del modelo: {response}")
