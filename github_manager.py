# github_manager.py

import requests
import os
from zipfile import ZipFile

# Configuración del token y la URL base de GitHub
GITHUB_TOKEN = 'token de usuario'
GITHUB_API_URL = 'https://api.github.com'

def download_repo(repo_owner, repo_name, output_dir='repos'):
    """
    Descarga un repositorio privado de GitHub como un archivo ZIP.

    Args:
        repo_owner (str): El nombre del propietario del repositorio.
        repo_name (str): El nombre del repositorio.
        output_dir (str): El directorio donde se guardarán los archivos del repositorio.

    Returns:
        str: La ruta del directorio donde se extrajeron los archivos del repositorio.
    """
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json',
    }
    repo_url = f'{GITHUB_API_URL}/repos/{repo_owner}/{repo_name}/zipball'

    response = requests.get(repo_url, headers=headers, stream=True)

    if response.status_code == 200:
        zip_path = f'{output_dir}/{repo_name}.zip'
        os.makedirs(output_dir, exist_ok=True)

        with open(zip_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=128):
                f.write(chunk)

        with ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(output_dir)

        print(f'Repositorio descargado y extraído en {output_dir}')
        return output_dir
    else:
        print(f'Error al descargar el repositorio: {response.status_code}')
        return None
