import speech_recognition as sr
import time 
import webbrowser
import playsound
import os
import random
from gtts import gTTS
from time import ctime
from googleapiclient.discovery import build

r = sr.Recognizer()

DEVELOPER_KEY = 'AIzaSyAKxi709HFgAHcLZIaRDg9dB_qQPaVPuns' 
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

prefix = ['IMG ', 'IMG_', 'IMG-', 'DSC ']
postfix = [' MOV', '.MOV', ' .MOV']

def record_audio(ask = False):
    with sr.Microphone() as source:
        if ask:
            print(ask)
        audio = r.listen(source)
        voice_data = ''
        try: 
            voice_data = r.recognize_google(audio)

        except sr.UnknownValueError:
            alexa_speak('Sorry, I do not understand')
        except sr.RequestError:
            alexa_speak('Sorry, connection error')
        return voice_data

def alexa_speak(audio_string):
    tts = gTTS(text=audio_string, lang='en')
    r = random.randint(1, 10000)
    audio_file = 'audio-' + str(r) + '.mp3'
    tts.save(audio_file)
    playsound.playsound(audio_file)
    print(audio_string)
    os.remove(audio_file)

def youtube_search():
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

  search_response = youtube.search().list(
    q=random.choice(prefix) + str(random.randint(999, 9999)) + random.choice(postfix),
    part='snippet',
    maxResults=5
  ).execute()

  videos = []

  for search_result in search_response.get('items', []):
    if search_result['id']['kind'] == 'youtube#video':
      videos.append('%s' % (search_result['id']['videoId']))
  return (videos[random.randint(0, 2)])

def respond(voice_data):
    if 'what is your name' in voice_data:
        alexa_speak('My name is Hana')
    if 'what time is it' in voice_data:
        alexa_speak(ctime())
    if 'what can you do' in voice_data:
        alexa_speak('I can recommend you random youtube videos, you just have to say: Random Video')
    if 'what is your favorite video' in voice_data:
        alexa_speak('My favorite video is Cat Cant Handle Flower')
        url = 'https://www.youtube.com/watch?v=-Z4jx5VMw8M'
        webbrowser.get().open(url)
    if 'random video' in voice_data:
        video = youtube_search()
        url = 'https://www.youtube.com/watch?v=' + video
        webbrowser.get().open(url)
        alexa_speak('This is what I found')
    if 'finish' in voice_data:
        exit()

time.sleep(1)
alexa_speak('can I help you?')
while 1:
    voice_data = record_audio()
    respond(voice_data)