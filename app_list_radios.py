from fastapi import FastAPI, BackgroundTasks, Query
from fastapi.middleware.cors import CORSMiddleware
import requests
import urllib.request
from typing import Optional, Tuple, Dict
import asyncio

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

RADIO_STREAMS = {
    "fabian": "https://sonic-us.streaming-chile.com/8072/stream",
    "radioarmeria": "https://c19.radioboss.fm:8114/stream",
    "foramontanos": "https://foramontanos.fm:8443/live",
    "foramonta2": "https://foramontanos.fm:8443/ODC",
    "soyradioinc": "https://streamlky.alsolnet.com/soyradiotvaudio",
    # Adicione mais rádios aqui, no formato "nome_radio": "url_radio"
}

SONG_HISTORY_LIMIT = 8

radio_data = {}
for radio_name in RADIO_STREAMS:
    radio_data[radio_name] = {
        "song_history": [],
        "current_song": {"artist": "", "song": ""},
        "monitoring_started": False,
    }



def get_album_art(artist: str, song: str) -> Optional[str]:
    try:
        response = requests.get(
            f"https://itunes.apple.com/search?term={artist}+{song}&media=music&limit=1"
        )
        response.raise_for_status()
        data = response.json()
        if data["resultCount"] > 0:
            return data["results"][0]["artworkUrl100"].replace("100x100bb", "512x512bb")
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar capa do álbum: {e}")
        return None

def get_mp3_stream_title(streaming_url: str, interval: int) -> Optional[str]:
    needle = b'StreamTitle='
    ua = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.110 Safari/537.36'

    headers = {
        'Icy-MetaData': '1',
        'User-Agent': ua
    }

    req = urllib.request.Request(streaming_url, headers=headers)
    response = urllib.request.urlopen(req)

    meta_data_interval = None
    for key, value in response.headers.items():
        if key.lower() == 'icy-metaint':
            meta_data_interval = int(value)
            break

    if meta_data_interval is None:
        return None

    offset = 0
    while True:
        response.read(meta_data_interval)
        buffer = response.read(interval)
        title_index = buffer.find(needle)
        if title_index != -1:
            title = buffer[title_index + len(needle):].split(b';')[0].decode('utf-8')
            return title
        offset += meta_data_interval + interval

def extract_artist_and_song(title: str) -> Tuple[str, str]:
    # Remove as aspas simples extras
    title = title.strip("'")
    
    if '-' in title:
        artist, song = title.split('-', 1)
        return artist.strip(), song.strip()
    else:
        return '', title.strip()
    


async def monitor_radio(radio_name: str, background_tasks: BackgroundTasks):
    global radio_data
    radio = radio_data[radio_name]
    if not radio["monitoring_started"]:
        radio["monitoring_started"] = True
        while True:
            title = get_mp3_stream_title(RADIO_STREAMS[radio_name], 19200)
            if title:
                artist, song = extract_artist_and_song(title)
                if artist != radio["current_song"]["artist"] or song != radio["current_song"]["song"]:
                    if radio["current_song"]["artist"] and radio["current_song"]["song"]:
                        radio["song_history"].insert(0, radio["current_song"])
                        radio["song_history"] = radio["song_history"][:SONG_HISTORY_LIMIT]
                    radio["current_song"] = {"artist": artist, "song": song}
            await asyncio.sleep(10)

@app.get("/")
async def root():
    return {
        "message": "Bienvenido",
        "now_playing": "Use /get_stream_title/?url=https://example.com/stream",
        "contact": "+51975959016",
        "free_use": "Contact us for free use of history."        
    }

@app.get("/get_stream_title/")
async def get_stream_title(url: str, interval: Optional[int] = 19200):
    title = get_mp3_stream_title(url, interval)
    if title:
        artist, song = extract_artist_and_song(title)
        art_url = get_album_art(artist, song)  # Busca a capa do álbum
        return {"artist": artist, "song": song, "art": art_url}  # Retorna a URL da capa junto com as informações da música
    else:
        return {"error": "Failed to retrieve stream title"}



@app.get("/radio_info/")
async def get_radio_info(background_tasks: BackgroundTasks, radio_url: Optional[str] = Query(None)):
    if radio_url:
        radio_name = next((name for name, url in RADIO_STREAMS.items() if url == radio_url), None)
        if radio_name is None:
            return {
                "currentSong": "Api Desabilitada",
                "currentArtist": "Contactame para su uso +51975959016"
            }
    else:
        radio_name = None  # Para indicar que no se proporcionó ningún nombre de radio

    if radio_name is None or radio_name not in RADIO_STREAMS:
        return {
            "currentSong": "Api Desabilitada",
            "currentArtist": "Contactame para su uso +51975959016"
        }

    background_tasks.add_task(monitor_radio, radio_name, background_tasks)
    return {
        "currentSong": radio_data[radio_name]["current_song"]["song"],
        "currentArtist": radio_data[radio_name]["current_song"]["artist"],
        "songHistory": radio_data[radio_name]["song_history"],
    }
