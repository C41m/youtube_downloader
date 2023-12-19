import os
import streamlit as st
import google.oauth2.credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Função para limpar arquivos temporários
def cleanup_temp_files(directory):
    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            st.warning(f"Não foi possível excluir o arquivo {file_path}. Erro: {e}")


def authenticate_youtube():
    # Obtenha o caminho absoluto do diretório atual onde o script está sendo executado
    script_directory = os.path.dirname(os.path.abspath(__file__))

    # Combine o caminho do diretório com o nome do arquivo
    CLIENT_SECRETS_FILE = os.path.join(script_directory, "client_secret_999265794631-98539690rmnr37pm89ikd4rdknuomma5.apps.googleusercontent.com.json")

    # Substitua 'path/to/client_secrets.json' pelo caminho real do seu arquivo JSON de credenciais
    SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]

    # Configurar o fluxo de autenticação
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_local_server(port=0)

    # Criar um objeto de serviço do YouTube autenticado
    youtube = build("youtube", "v3", credentials=credentials)
    return youtube, script_directory