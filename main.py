import streamlit as st
import locale
import os
from functions import cleanup_temp_files
from pytube import YouTube
from pytube import Playlist
from zipfile import ZipFile
import tempfile


def video_info_func():
    # Pegando título do vídeo
    title = video.title
    author = video.author
    full_title = author + ' - ' + title
    
    # Pegando duração do vídeo
    duration_seconds = video.length
    duration_minutes = divmod(duration_seconds, 60)
    duration_formatted = f"{duration_minutes[0]}:{duration_minutes[1]}"
    return full_title, duration_formatted

def file_rename(file_download):
    full_title, duration_formatted = video_info_func()

    # Construir o novo caminho do arquivo com o mesmo diretório
    new_file = os.path.join(os.path.dirname(file_download), f"{full_title}.mp3")

    # Renomear o arquivo
    os.rename(file_download, new_file)

def mp3_converter(file_download):
    base, ext = os.path.splitext(file_download)
    new_file = base + '.mp3'

    if os.path.exists(new_file):
        os.remove(new_file)

    os.rename(file_download, new_file)
    return new_file

def download_playlist_func(video):
    audio_streams = video.streams.filter(only_audio=True)

    # Extrair as taxas de bits disponíveis para as streams de áudio
    available_bitrates = [int(stream.abr.replace('kbps', '')) for stream in audio_streams]

    # Obter a maior taxa de bits disponível
    highest_bitrate = max(available_bitrates)
    
    # Encontrar a stream correspondente à taxa de bits mais alta
    selected_stream = None
    for stream in audio_streams:
        if int(stream.abr.replace('kbps', '')) == highest_bitrate:
            selected_stream = stream
            break

    # Realizar o download da stream de áudio escolhida
    if selected_stream:
        file_download = selected_stream.download(output_path=temp_dir)
        #mp3_converter(file_download)
        file_rename(file_download)
        st.success(f"Download {index} concluído com sucesso!")

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

    # Exibir o link para download do arquivo ZIP
    st.info("Clique abaixo para baixar todos os arquivos compactados:")
    with open(zip_file_path, "rb") as zip_file:
        st.download_button(label="Baixar Arquivos Compactados", data=zip_file, key="download_button", file_name="download.zip")

    # Remover o arquivo ZIP temporário após o download
    os.remove(zip_file_path)


locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

st.set_page_config(page_title='Youtube Downloader')

st.title('Youtube Downloader')

# Diretório temporário para armazenar os arquivos baixados temporariamente
temp_dir = tempfile.mkdtemp()

# Criar diretório temporário se não existir
if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)

# Limpar arquivos temporários ao iniciar o aplicativo
cleanup_temp_files(temp_dir)


with st.container():
    link = st.text_input(' ', placeholder='Link do Youtube')
    
    # Adiciona uma mensagem para pressionar Enter
    enter_message = st.info("Pressione Enter para continuar.")




if link:
    try:
        # Obter informações do vídeo
        video = YouTube(link)

        # Remover a mensagem de "Pressione Enter para continuar."
        enter_message.empty()

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
                file_download = selected_stream.download(output_path=temp_dir)
                file_ok = mp3_converter(file_download)
                st.success("Download concluído com sucesso!")
                
                # Adicionar um botão para baixar o arquivo
                with open(file_ok, 'rb') as file:
                    st.download_button(label='Baixar Vídeo', data=file.read(), key='download_button', file_name=os.path.basename(file_ok))
                
                # Limpar arquivos temporários após o download
                cleanup_temp_files(temp_dir)


    except Exception as e:
        st.error(f"Ocorreu um erro: {e}")

with st.container():
    link = st.text_input('Insira o link da playlist do Youtube:', placeholder='Cole o link aqui')
    
    # Adiciona uma mensagem para pressionar Enter
    enter_message = st.info("Pressione Enter para continuar.")

    # Verificar se o botão de download foi pressionado
    if st.button("Baixar Playlist"):
        # Realizar o download de vídeos da playlist
        playlist = Playlist(link)
        st.header(f'Título da Playlist: {playlist.title}')

        videos = playlist.video_urls

        for index, url in enumerate(videos, start=1):
            video = YouTube(url)
            
            #
            st.write(f'Vídeo {index}/{len(videos)}')
            col1, col2 = st.columns(2)
            with col1:
                st.image(video.thumbnail_url, width=300)
            with col2:
                full_title, duration_formatted = video_info_func()
                st.write(f'Nome do Arquivo: {full_title}')
                st.write(f'Duração: {duration_formatted}')
                st.write(f'Link: {url}')
                
                with st.spinner('Baixando...'):
                    download_playlist = download_playlist_func(video)
                    
            st.write('---')
        
        # Compactar todas as músicas
        zip_musics = zip_musics_func()

        # Limpar arquivos temporários após o download
        cleanup_temp_files(temp_dir)

        # Remover a mensagem de "Pressione Enter para continuar."
        enter_message.empty()

        st.success("Download da playlist concluído com sucesso!")
