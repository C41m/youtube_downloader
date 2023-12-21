import os
import streamlit as st
from pytube import YouTube, Playlist
from datetime import datetime, timedelta
import re

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

class VideoCache:
    def __init__(self):
        self.cache = {}

    def get_audio_streams_abr(self, video_url):
        if video_url in self.cache:
            print("Usando cache para", video_url)
            return self.cache[video_url]
        else:
            print("Chamando API para", video_url)
            try:
                video = YouTube(video_url)
                # Obter todas as transmissões de áudio disponíveis
                audio_streams = video.streams.filter(only_audio=True).order_by('abr')
                # Obter apenas as informações dentro do campo abr
                abr_list = list([stream.abr for stream in audio_streams])
                # Inverter a lista para melhor qualidade primeiro
                abr_list = list(reversed(abr_list))
                # Armazenar no cache
                self.cache[video_url] = abr_list, audio_streams
                return abr_list, audio_streams
            
            except Exception as e:
                print(f"Erro ao obter transmissões de áudio: {e}")
                return []

video_cache = VideoCache()

# Função para limpar arquivos temporários
def cleanup_temp_files(directory):
    try:
        # Excluir todos os arquivos dentro da pasta
        for file_name in os.listdir(directory):
            file_path = os.path.join(directory, file_name)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                st.warning(f"Não foi possível excluir o arquivo {file_path}. Erro: {e}")

        # Excluir a pasta vazia
        os.rmdir(directory)

    except Exception as e:
        st.warning(f"Não foi possível excluir a pasta {directory}. Erro: {e}")

def get_video_details(video_url):
    video = YouTube(video_url)
    video_id = video.video_id
    youtube = build('youtube', 'v3', developerKey='AIzaSyDFq1AMiBfEfOe2g9vC6FU4tJhzySgJk9A')
    request = youtube.videos().list(part='contentDetails,snippet,statistics,player', id=video_id)
    response = request.execute()

    # Titulo do Vídeo
    title = response['items'][0]['snippet']['title']

    # Duração do Vídeo
    duration_iso = response['items'][0]['contentDetails']['duration']
    duration = format_duration(duration_iso)

    # Thumb do Vídeo
    thumbnail_url = response['items'][0]['snippet']['thumbnails']['maxres']['url']

    # Qualidades do Vídeo
    abr_list, audio_streams = video_cache.get_audio_streams_abr(video_url)

    return title, duration, thumbnail_url, abr_list, audio_streams
    
def format_duration(duration_iso):
    try:
        # Remova os caracteres PT da string
        duration = duration_iso.replace("PT", "")

        # Converta para um objeto timedelta
        delta = timedelta()

        # Iterar sobre as partes da string e adicionar à timedelta
        for part in duration.split("M"):
            if "H" in part:
                delta += timedelta(hours=int(part.split("H")[0]))
                part = part.split("H")[1]
            if "S" in part:
                delta += timedelta(seconds=int(part.split("S")[0]))
                part = part.split("S")[1]
            if part:
                delta += timedelta(minutes=int(part))

        # Formate a timedelta como string no formato HH:MM:SS
        hours, remainder = divmod(delta.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        formatted_duration = "{:02}:{:02}:{:02}".format(hours, minutes, seconds)

        return formatted_duration

    except Exception as e:
        return {"error": str(e)}

def get_video_streams(video_url):
    try:
        video = YouTube(video_url, use_oauth=True, allow_oauth_cache=True)

        # Obter todas as transmissões de vídeo disponíveis
        video_streams = video.streams.filter(file_extension="mp4").order_by('resolution')

        return video_streams

    except Exception as e:
        print(f"Erro ao obter transmissões de vídeo: {e}")
        return []

def mp3_converter(file_download):

    base, ext = os.path.splitext(file_download)
    new_file = base + '.mp3'

    if os.path.exists(new_file):
        os.remove(new_file)

    os.rename(file_download, new_file)
    return new_file

def file_rename(file_download, title):

    title = title.replace('/', '')
    title = title.replace('|', '')
    title = title.replace(':', '')
    title = title.replace('"', '')
    title = title.replace("'", '')
    title = title.replace("*", '')
    title = title.replace("?", '')


    # Construir o novo caminho do arquivo com o mesmo diretório
    new_file = os.path.join(os.path.dirname(file_download), f"{title}.mp3")

    # Renomear o arquivo
    os.rename(file_download, new_file)
    return new_file

def get_playlist_details(playlist_url, progress_bar1):
    playlist = Playlist(playlist_url)
    playlist_id = playlist.playlist_id
    playlist_urls = playlist.video_urls
    youtube = build('youtube', 'v3', developerKey='AIzaSyDFq1AMiBfEfOe2g9vC6FU4tJhzySgJk9A')
    # request = youtube.playlistItems().list(part='contentDetails,id,snippet,status', playlistId=playlist_id)
    # response = request.execute()


    all_playlist_items = []
    def process_items(items):
        for item in items:
            try:
                video_id = item['contentDetails']['videoId']
                privacy_status = item['status']['privacyStatus']

                # Considera apenas vídeos públicos
                if video_id and privacy_status == 'public':
                    all_playlist_items.append(item)
            except (KeyError, TypeError):
                pass  # Ignora itens que não têm os campos necessários

        
    # Sua chamada inicial
    request = youtube.playlistItems().list(part='contentDetails,id,snippet,status', playlistId=playlist_id, maxResults=50)
    response = request.execute()
    process_items(response['items'])
    
    # Verifica se há mais páginas
    while 'nextPageToken' in response:
        request = youtube.playlistItems().list(part='contentDetails,id,snippet,status', playlistId=playlist_id, pageToken=response['nextPageToken'], maxResults=50)
        response = request.execute()
        # Processa os próximos 50 itens
        process_items(response['items'])
        print('Resposta')

    
    request_title = youtube.playlists().list(part='contentDetails,id,snippet,status', id=playlist_id)
    response_title = request_title.execute()

    playlist_title = response_title['items'][0]['snippet']['title']
    
    video_ids = []
    for item in all_playlist_items:
        content_details = item.get('contentDetails', {})
        video_id = content_details.get('videoId', None)
        if video_id:
            video_ids.append(video_id)
        else:
            print('Error')  


    video_titles = [item['snippet']['title'] for item in all_playlist_items]

    # Capturar Thumb
    video_thumbs = []
    for item in all_playlist_items:
        snippet = item.get('snippet', {})
        thumbnails = snippet.get('thumbnails', {})

        # Tentar pegar as resoluções em uma ordem específica
        for resolution in ['maxres', 'standard', 'high', 'medium', 'default']:
            thumbnail_info = thumbnails.get(resolution, {})
            url = thumbnail_info.get('url', None)
            
            if url:
                video_thumbs.append(url)
                break  # Se encontrar uma URL válida, sai do loop
            elif resolution == 'default':
                # Se todas as resoluções falharem, pode adicionar uma URL padrão ou fazer outra manipulação
                video_thumbs.append("Vídeo sem Thumb")

    # Capturar a duração do vídeo
    duration = []
    for i, (video_id) in enumerate(video_ids, 1):
        request = youtube.videos().list(part='contentDetails,snippet,statistics,player', id=video_id)
        response_video = request.execute()
        # print(video_id)
        # print(response_video)

        # Duração do Vídeo
        duration_iso = response_video['items'][0]['contentDetails']['duration']
        duration.append(format_duration(duration_iso))
        
        progress_bar1.progress(i / len(video_ids))
    progress_bar1.empty()

    return video_ids, video_titles, video_thumbs, playlist_title, duration, playlist_urls, progress_bar1


def is_valid_youtube_link(link):
    pattern = re.compile(r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/'
                        '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
    return bool(pattern.match(link))
