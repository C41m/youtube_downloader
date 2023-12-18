import streamlit as st
import tkinter as tk
from tkinter import filedialog
from functions import select_folder
import locale
import os
from pytube import YouTube
import base64




def file_rename(file_path):
    base, ext = os.path.splitext(file_path)
    new_file = base + '.mp3'

    if os.path.exists(new_file):
        os.remove(new_file)

    os.rename(file_path, new_file)
    return new_file



locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

st.set_page_config(page_title='Youtube Downloader')

st.title('Youtube Downloader')

with st.container():
    link = st.text_input(' ', placeholder='Link do Youtube')
    
    # Adiciona uma mensagem para pressionar Enter
    st.info("Pressione Enter para continuar.")




selected_folder_path = st.session_state.get("folder_path", None)
folder_select_button = st.button("Selecione Diretorio")
if folder_select_button:
    selected_folder_path = select_folder()
    st.session_state.folder_path = selected_folder_path
    if selected_folder_path:
        st.write('Selected folder path:', selected_folder_path)



if link:
    try:
        # Obter informações do vídeo
        video = YouTube(link)

        # Filtrar apenas as streams de áudio
        audio_streams = video.streams.filter(only_audio=True)

        # Extrair as taxas de bits disponíveis para as streams de áudio
        available_bitrates = [stream.abr for stream in audio_streams]

        # Remover o "kbps" e converter para inteiros (ignorando valores que não podem ser convertidos)
        int_bitrates = [int(b.replace('kbps', '')) for b in available_bitrates if b.replace('kbps', '').isdigit()]

        # Reverter a lista para exibir de maior para menor
        reversed_bitrates = sorted(int_bitrates, reverse=True)

        # Converter novamente para strings para exibir no seletor
        reversed_bitrates_str = [f"{b}kbps" for b in reversed_bitrates]

        # Exibir um seletor para escolher a taxa de bits
        selected_bitrate = st.radio("Escolha a qualidade de áudio (Taxa de Bits):", reversed_bitrates_str)

        # Inicializar a variável para armazenar a stream selecionada
        selected_stream = None

        # Encontrar a stream de áudio correspondente à taxa de bits escolhida
        for stream in audio_streams:
            if stream.abr == selected_bitrate:
                selected_stream = stream
                break

        # Verificar se o botão de download foi pressionado
        if st.button("Selecionar"):
            # Realizar o download da stream de áudio escolhida
            if selected_stream:


                file_download = selected_stream.download()
                file_ok = file_rename(file_download)
                st.success("Download concluído com sucesso!")
                
                # with open(file_ok, 'rb') as file:
                #     btn = st.download_button(label='Downloaddd', data=file.read(), file_name=file_ok, key='mp3')
                #     st.success("Download concluído com sucesso!")



    except Exception as e:
        st.error(f"Ocorreu um erro: {e}")