from tkinter import *
import pygame
from playsound import playsound
from random import choice
from bs4 import BeautifulSoup
import requests
import urllib.request
from pathlib import Path


name = "Капкан"

url = 'https://mp3party.net/search?q='

page = requests.get(url+name)

pygame.mixer.init()
pygame.init()

soup = BeautifulSoup(page.content, "html.parser")
p = soup.select('.playlist-btn')
music = soup.find('div', class_='play-btn').attrs.get('href')
id = soup.find('div', class_='play-btn').attrs.get('data-song-id')

url = "https://dl1.mp3party.net/online/"
file = urllib.request.urlretrieve(url+id+".mp3", id+".mp3")

print(music)
print(file[0])
# music = p['href']

# urllib.request.urlretrieve(music, "music/music.mp3")

# MUSIC_LIST=["Antonia - Dinero (feat. Yoss Bones).mp3","Ka-Re - Где то на земле.mp3","Mecano - Hijo De La Luna.mp3", "NЮ - Без тебя фигово.mp3", "Slavik Pogosov - Мама не ругай.mp3"]

# #Play the backgound music
# def Play():
#     song=f'music/music.mp3'
#     pygame.mixer.music.load(song)
#     pygame.mixer.music.play()

# def Pause():
#     pygame.mixer.music.pause()

# def Stop():
#     pygame.mixer.music.stop()
#     pygame.songs_list.selection_clear(ACTIVE)

# #to resume the song

# def Resume():
#     pygame.mixer.music.unpause()

