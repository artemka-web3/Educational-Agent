import os
from pytube import YouTube
from moviepy.editor import VideoFileClip
import speech_recognition as sr
from pydub import AudioSegment
import yt_dlp

def download_youtube_video(url, output_path='video'):
    ydl_opts = {
        'outtmpl': f'{output_path}.mp4'
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return output_path + '.mp4'

def extract_audio_from_video(video_path, audio_path='audio.wav'):
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path)
    return audio_path

def chunk_audio_and_save(audio_path, chunk_length=60000):  # chunk_length in milliseconds
    audio = AudioSegment.from_wav(audio_path)
    length_audio = len(audio)
    chunk_paths = []
    for i, chunk in enumerate(range(0, length_audio, chunk_length)):
        chunk_audio = audio[chunk:chunk + chunk_length]
        chunk_path = f"temp_chunk_{i}.wav"
        chunk_audio.export(chunk_path, format="wav")
        chunk_paths.append(chunk_path)
    return chunk_paths

def recognize_speech_from_audio(audio_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data, language='ru-RU')  # Используйте 'en-US' для английского языка
    return text

def main(url):
    video_path = download_youtube_video(url)
    audio_path = extract_audio_from_video(video_path)
    chunks = chunk_audio_and_save(audio_path)
    full_transcript = []
    for i, file_path in enumerate(chunks):
        print(f"Transcribing chunk {i+1}/{len(chunks)}...")
        transcript = recognize_speech_from_audio(file_path)
        full_transcript.append(transcript)
        os.remove(file_path)  # Clean up chunk file
    os.remove(video_path)  # Удалить видеофайл после обработки, если это необходимо
    os.remove(audio_path)  # Удалить аудиофайл после обработки, если это необходимо
    return full_transcript

def write_text_from_video(link):
    youtube_url = link
    transcribed_text = main(youtube_url)
    full_text = ''.join(transcribed_text)

    with open('video.txt', 'w', encoding='utf-8') as f:
        f.write(full_text)

def read_from_file():
    file = open('video.txt', 'r')
    text = file.read()
    file.close()
    return text
