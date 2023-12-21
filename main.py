import streamlit as st
import locale
import os
from functions import cleanup_temp_files, get_video_details, get_playlist_details, file_rename
from pytube import YouTube
from pytube import Playlist
from zipfile import ZipFile
import tempfile




def zip_musics_func():
    # Diretório dos downloads
    download_folder = temp_dir

    # Criar o arquivo ZIP temporário
    zip_file_path = 'temp_download.zip'

    # Compactar todos os arquivos no diretório usando os.walk
    with ZipFile(zip_file_path, 'w') as zipf:
        for root, _, files in os.walk(download_folder):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, download_folder)
                zipf.write(file_path, arcname=arcname)

    return zip_file_path

# Adicionar estilos CSS de um arquivo externo (substitua 'styles.css' pelo caminho do seu arquivo)


# Função para inicializar variáveis de estado
def initialize_session_state():
    st.session_state.enter_message = None
    st.session_state.btn_down = None
    st.session_state.selected_bitrate = None

# Inicializar variáveis de estado ao iniciar o aplicativo
initialize_session_state()

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

st.set_page_config(page_title='YouTube MP3 Downloader')

# Adicione o código CSS diretamente usando st.markdown


# Use st.markdown para criar um contêiner com classes personalizadas
st.markdown("<h1 class='titulo-youtube'><span class='titulo-you'>You</span><span class='titulo-tube'>Tube</span><span class='titulo-youtube'>MP3 Downloader</span></h1>", unsafe_allow_html=True)

with open("styles.css") as f:
    css = f.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


# Diretório temporário para armazenar os arquivos baixados temporariamente
temp_dir = tempfile.mkdtemp()

# Criar diretório temporário se não existir
if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)

# Limpar arquivos temporários ao iniciar o aplicativo
#cleanup_temp_files(temp_dir)



# ===========================
# Sidebar 
# ===========================

st.markdown(
    """
    <style>
        @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css');
    </style>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown("# Entre em Contato! 😉")
st.sidebar.markdown('---')

name_icon = '<svg xmlns="http://www.w3.org/2000/svg" height="48" width="60" viewBox="0 0 700 512"><!--!Font Awesome Free 6.5.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2023 Fonticons, Inc.--><path fill="#ffffff" d="M64 96c0-35.3 28.7-64 64-64H512c35.3 0 64 28.7 64 64V352H512V96H128V352H64V96zM0 403.2C0 392.6 8.6 384 19.2 384H620.8c10.6 0 19.2 8.6 19.2 19.2c0 42.4-34.4 76.8-76.8 76.8H76.8C34.4 480 0 445.6 0 403.2zM281 209l-31 31 31 31c9.4 9.4 9.4 24.6 0 33.9s-24.6 9.4-33.9 0l-48-48c-9.4-9.4-9.4-24.6 0-33.9l48-48c9.4-9.4 24.6-9.4 33.9 0s9.4 24.6 0 33.9zM393 175l48 48c9.4 9.4 9.4 24.6 0 33.9l-48 48c-9.4 9.4-24.6 9.4-33.9 0s-9.4-24.6 0-33.9l31-31-31-31c-9.4-9.4-9.4-24.6 0-33.9s24.6-9.4 33.9 0z"/></svg>'
email_icon = '<svg xmlns="http://www.w3.org/2000/svg" height="48" width="60" viewBox="0 0 700 512"><!--!Font Awesome Free 6.5.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2023 Fonticons, Inc.--><path fill="#ffffff" d="M256 64C150 64 64 150 64 256s86 192 192 192c17.7 0 32 14.3 32 32s-14.3 32-32 32C114.6 512 0 397.4 0 256S114.6 0 256 0S512 114.6 512 256v32c0 53-43 96-96 96c-29.3 0-55.6-13.2-73.2-33.9C320 371.1 289.5 384 256 384c-70.7 0-128-57.3-128-128s57.3-128 128-128c27.9 0 53.7 8.9 74.7 24.1c5.7-5 13.1-8.1 21.3-8.1c17.7 0 32 14.3 32 32v80 32c0 17.7 14.3 32 32 32s32-14.3 32-32V256c0-106-86-192-192-192zm64 192a64 64 0 1 0 -128 0 64 64 0 1 0 128 0z"/></svg>'
linkedin_icon = '<svg xmlns="http://www.w3.org/2000/svg" height="48" width="60" viewBox="0 0 700 512"><!--!Font Awesome Free 6.5.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2023 Fonticons, Inc.--><path fill="#ffffff" d="M416 32H31.9C14.3 32 0 46.5 0 64.3v383.4C0 465.5 14.3 480 31.9 480H416c17.6 0 32-14.5 32-32.3V64.3c0-17.8-14.4-32.3-32-32.3zM135.4 416H69V202.2h66.5V416zm-33.2-243c-21.3 0-38.5-17.3-38.5-38.5S80.9 96 102.2 96c21.2 0 38.5 17.3 38.5 38.5 0 21.3-17.2 38.5-38.5 38.5zm282.1 243h-66.4V312c0-24.8-.5-56.7-34.5-56.7-34.6 0-39.9 27-39.9 54.9V416h-66.4V202.2h63.7v29.2h.9c8.9-16.8 30.6-34.5 62.9-34.5 67.2 0 79.7 44.3 79.7 101.9V416z"/></svg>'
github_icon = '<svg xmlns="http://www.w3.org/2000/svg" height="48" width="60" viewBox="0 0 700 512"><!--!Font Awesome Free 6.5.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2023 Fonticons, Inc.--><path fill="#ffffff" d="M165.9 397.4c0 2-2.3 3.6-5.2 3.6-3.3 .3-5.6-1.3-5.6-3.6 0-2 2.3-3.6 5.2-3.6 3-.3 5.6 1.3 5.6 3.6zm-31.1-4.5c-.7 2 1.3 4.3 4.3 4.9 2.6 1 5.6 0 6.2-2s-1.3-4.3-4.3-5.2c-2.6-.7-5.5 .3-6.2 2.3zm44.2-1.7c-2.9 .7-4.9 2.6-4.6 4.9 .3 2 2.9 3.3 5.9 2.6 2.9-.7 4.9-2.6 4.6-4.6-.3-1.9-3-3.2-5.9-2.9zM244.8 8C106.1 8 0 113.3 0 252c0 110.9 69.8 205.8 169.5 239.2 12.8 2.3 17.3-5.6 17.3-12.1 0-6.2-.3-40.4-.3-61.4 0 0-70 15-84.7-29.8 0 0-11.4-29.1-27.8-36.6 0 0-22.9-15.7 1.6-15.4 0 0 24.9 2 38.6 25.8 21.9 38.6 58.6 27.5 72.9 20.9 2.3-16 8.8-27.1 16-33.7-55.9-6.2-112.3-14.3-112.3-110.5 0-27.5 7.6-41.3 23.6-58.9-2.6-6.5-11.1-33.3 2.6-67.9 20.9-6.5 69 27 69 27 20-5.6 41.5-8.5 62.8-8.5s42.8 2.9 62.8 8.5c0 0 48.1-33.6 69-27 13.7 34.7 5.2 61.4 2.6 67.9 16 17.7 25.8 31.5 25.8 58.9 0 96.5-58.9 104.2-114.8 110.5 9.2 7.9 17 22.9 17 46.4 0 33.7-.3 75.4-.3 83.6 0 6.5 4.6 14.4 17.3 12.1C428.2 457.8 496 362.9 496 252 496 113.3 383.5 8 244.8 8zM97.2 352.9c-1.3 1-1 3.3 .7 5.2 1.6 1.6 3.9 2.3 5.2 1 1.3-1 1-3.3-.7-5.2-1.6-1.6-3.9-2.3-5.2-1zm-10.8-8.1c-.7 1.3 .3 2.9 2.3 3.9 1.6 1 3.6 .7 4.3-.7 .7-1.3-.3-2.9-2.3-3.9-2-.6-3.6-.3-4.3 .7zm32.4 35.6c-1.6 1.3-1 4.3 1.3 6.2 2.3 2.3 5.2 2.6 6.5 1 1.3-1.3 .7-4.3-1.3-6.2-2.2-2.3-5.2-2.6-6.5-1zm-11.4-14.7c-1.6 1-1.6 3.6 0 5.9 1.6 2.3 4.3 3.3 5.6 2.3 1.6-1.3 1.6-3.9 0-6.2-1.4-2.3-4-3.3-5.6-2z"/></svg>'

st.sidebar.markdown(f'### {name_icon} Caio Fernando', unsafe_allow_html=True)
st.sidebar.markdown(f'##### Engenheiro e Analista de Dados', unsafe_allow_html=True)
st.sidebar.markdown(f'##### Desenvolvedor Python', unsafe_allow_html=True)
st.sidebar.markdown('---')

st.sidebar.markdown(f'### {email_icon} caiofernandobs@gmail.com', unsafe_allow_html=True)
st.sidebar.markdown(f'### [{linkedin_icon}](https://www.linkedin.com/in/caiofernandobs/) /caiofernandobs', unsafe_allow_html=True)
st.sidebar.markdown(f'### [{github_icon}](https://github.com/C41m/) /C41m', unsafe_allow_html=True)
st.sidebar.markdown('---')

# ===========================
# Sidebar Final 
# ===========================

with st.container():
    with st.container():
        link_video = st.text_input('Insira o link do vídeo do YouTube:', placeholder='Cole o link aqui') 
        pesq_btn_video = st.button("Pesquisar", key='pesqBtnVideo')
        #st.session_state.btn_down = st.markdown('')

    try:
        if link_video or pesq_btn_video:
            title, duration, thumbnail_url, abr_list, audio_streams  = get_video_details(link_video)
            
            with st.container():
                st.image(thumbnail_url, width=450, use_column_width=True)
                st.markdown(f'### {title}')
                st.markdown(f'Duração: {duration}')
                
                # Seleção da qualidade de áudio
                #st.radio('Escolha a qualidade de áudio (Taxa de Bits):', abr_list)

                # Armazena o estado da sessão
                #st.session_state.selected_bitrate = selected_bitrate_radio

            with st.container():
                # st.session_state.selected_bitrate_radio = None
                # st.session_state.selected_bitrate = None
                selected_bitrate_radio = st.radio('Escolha a qualidade de áudio (Taxa de Bits):', abr_list)

                # Encontra a stream de áudio correspondente à taxa de bits escolhida
                selected_stream = None
                for stream in audio_streams:
                    if stream.abr == selected_bitrate_radio:
                        selected_stream = stream
                        break

                conv_btn = st.button("Converter", key='convBtnVideo')
                if conv_btn:
                    st.session_state.info_video = st.info('Baixando...')
                    progress_bar = st.progress(0)
                    # Realizar o download da stream de áudio escolhida
                    if selected_stream:
                        progress_bar.progress(15)
                        file_download = selected_stream.download(output_path=temp_dir)
                        progress_bar.progress(50)
                        file_ok = file_rename(file_download, title)
                        progress_bar.progress(100)
                        st.session_state.info_video.success('Conversão concluída!')

                        # Adicionar um botão para baixar o arquivo
                        with open(file_ok, 'rb') as file:
                            download_btn = st.download_button(label='Download', data=file.read(), key='download_button', file_name=os.path.basename(file_ok))
                        
                        if download_btn:
                            st.session_state.enter_message

                        # Limpar arquivos temporários após o download
                        cleanup_temp_files(temp_dir)

                    else:
                        st.error('Erro: Stream não encontrada')
    except:
        st.warning('Digite um link de vídeo válido!')

st.markdown('---')
with st.container():

    with st.container():
        link = st.text_input('Insira o link da playlist do YouTube:', placeholder='Cole o link aqui') 
        conv_btn_playlist = st.button("Converter!", key='convBtnPlaylist')
        st.session_state.btn_down = st.markdown('')

    try:
        if link and conv_btn_playlist:

            st.session_state.enter_message = st.info('Carregando...')
            progress_bar1 = st.progress(0)
            video_ids, video_titles, video_thumbs, playlist_title, duration, playlist_urls, progress_bar1 = get_playlist_details(link, progress_bar1)
            
            progress_bar = st.progress(0)
            st.session_state.enter_message.info('Convertendo...')
            
            st.markdown(f'# {playlist_title}')
            for i, (video_name, video_id, video_thumb, duration, video_url) in enumerate(zip(video_titles, video_ids, video_thumbs, duration, playlist_urls), 1):

                progress_bar.progress(i / len(video_titles))
                st.session_state.enter_message.info(f'Convertendo: {i}/{len(video_titles)} videos')

                with st.container():
                    col1, col2 = st.columns(2)   
                    with col1:
                        if video_thumb:
                            st.image(video_thumb, width=450, use_column_width=True)
                    with col2:
                        st.markdown(f'#### {video_name}')
                        st.markdown(f'##### Duração: {duration}')

                        video = YouTube(video_url)
                        # Obter a primeira stream de áudio disponível
                        audio_stream = video.streams.filter(only_audio=True).order_by('abr').last()
                        if audio_stream:
                            try:
                                file_download = audio_stream.download(output_path=temp_dir)
                                file_ok = file_rename(file_download, video_name)
                                #cleanup_temp_files(temp_dir)
                                st.success(f'Conversão do vídeo {i}/{len(video_titles)} concluído!')
                            except Exception:
                                st.warning(f"Erro ao baixar o vídeo - Restrições")

                st.markdown('---')

            # Adicionar o botão de download após o progresso
            with st.container():
                # Compactar todas as músicas
                zip_file_path = zip_musics_func()
                # Exibir o link para download do arquivo ZIP
                st.info("Clique abaixo para baixar todos os arquivos compactados:")
                with open(zip_file_path, "rb") as zip_file:
                    st.session_state.btn_down.download_button(label="Download", data=zip_file, key="download_button1", file_name="download.zip")
                
                #
                st.session_state.enter_message.success('Concluído! Aperte em Download!')

                # Remover o arquivo ZIP temporário após o download
                os.remove(zip_file_path)

                # # Limpar arquivos temporários após o download
                cleanup_temp_files(temp_dir)
    except:
        st.warning('Digite um link de Playlist válido!')









