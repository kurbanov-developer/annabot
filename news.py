from cmath import pi
from secrets import choice
from bs4 import BeautifulSoup
import requests
import random

url = 'https://lenta.ru/'

page = requests.get(url)

   
filteredNews = []
allNews = []

soup = BeautifulSoup(page.content, "html.parser")
card = soup.select('a.card-big._longgrid')

n = random.choice(card)

title = n.find('h3', class_='card-big__title')
image = n.find('img', class_='card-big__image').attrs.get('src')
span = n.find('span', class_='card-big__rightcol')

info = title.text + '\n' + span.text

    

