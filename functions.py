import os
import streamlit as st

# Função para limpar arquivos temporários
def cleanup_temp_files(directory):
    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            st.warning(f"Não foi possível excluir o arquivo {file_path}. Erro: {e}")
