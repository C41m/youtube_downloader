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
cleanup_temp_files(temp_dir)


with st.container():
    with st.container():
        link_video = st.text_input('Insira o link do vídeo do YouTube:', placeholder='Cole o link aqui') 
        pesq_btn_video = st.button("Pesquisar", key='pesqBtnVideo')
        #st.session_state.btn_down = st.markdown('')

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
            st.session_state.selected_bitrate_radio = None
            st.session_state.selected_bitrate = None
            selected_bitrate_radio = st.radio('Escolha a qualidade de áudio (Taxa de Bits):', abr_list, index=abr_list.index(st.session_state.selected_bitrate))

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


st.markdown('---')
with st.container():

    with st.container():
        link = st.text_input('Insira o link da playlist do YouTube:', placeholder='Cole o link aqui') 
        conv_btn_playlist = st.button("Converter!", key='convBtnPlaylist')
        st.session_state.btn_down = st.markdown('')

    
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

