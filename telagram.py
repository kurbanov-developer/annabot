import logging
import os
from pathlib import Path
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.input_file import InputFile
from dotenv import load_dotenv
import urllib.request
from bot_stt import STT
from bot_tts import TTS
from bs4 import BeautifulSoup
import requests
import random
import weather
import datetime
import mutagen
from mutagen.wave import WAVE
from text_to_num import alpha2digit, text2num

load_dotenv()

TELEGRAM_TOKEN = os.getenv("5628114893:AAGb7eDbkTYTm_U2B-JQPh4LXMUEUPBcquY")

bot = Bot(token="5628114893:AAGb7eDbkTYTm_U2B-JQPh4LXMUEUPBcquY")  # Объект бота
dp = Dispatcher(bot)  # Диспетчер для бота
tts = TTS()
stt = STT()

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    filename="bot.log",
)


# Хэндлер на команду /start , /help
@dp.message_handler(commands=["start", "help"])
async def cmd_start(message: types.Message):
    await message.reply(
        "Привет! Это Бот для конвертации голосового/аудио сообщения в текст"
        " и создания аудио из текста."
    )


# Хэндлер на команду /test
@dp.message_handler(commands="test")
async def cmd_test(message: types.Message):
    
    await message.answer("Test")


def audio_duration(length):
    hours = length // 3600  # calculate in hours
    length %= 3600
    mins = length // 60  # calculate in minutes
    length %= 60
    seconds = length  # calculate in seconds
  
    return hours, mins, seconds



# Хэндлер на получение текста
@dp.message_handler(content_types=[types.ContentType.TEXT])
async def cmd_text(message: types.Message):
    
   
    
    out_filename = tts.text_to_wav(message.text)

    # Отправка голосового сообщения
    path = Path("", out_filename)
    voice = InputFile(path)
    audio = WAVE(path)
    audio_info = audio.info
    length = int(audio_info.length)
    hours, mins, seconds = audio_duration(length)
    await message.answer_voice(voice, duration=seconds)
    if "расскажи новость" in message.text.lower():
        url = 'https://lenta.ru/'
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        card = soup.select('a.card-big._longgrid')
        n = random.choice(card)
        title = n.find('h3', class_='card-big__title')
        image = n.find('img', class_='card-big__image').attrs.get('src')
        span = n.find('span', class_='card-big__rightcol')
        info = title.text + '\n' + span.text
        await message.answer_photo(image, info)
        news = tts.text_to_wav(info, "news.wav")
        path = Path("", news)
        voice = InputFile(path)
        await message.answer_voice(voice)
    if "как дела" in message.text.lower():
        text = ['У меня все отлично.. а у Вас как ?', 'Все супер, а у Вас как ?','Очень даже хорошо..']
        nice = tts.text_to_wav(random.choice(text), "nice.wav")
        path = Path("", nice)
        voice = InputFile(path)
        await message.answer_voice(voice)
    if "отлично" in message.text.lower():
        i_m_glad = ['Я рада', 'Я рада что у Вас отлично', 'Чтобы всегда так было']
        glad = tts.text_to_wav(random.choice(i_m_glad), "i_m_glad.wav")
        path = Path("", glad)
        voice = InputFile(path)
        await message.answer_voice(voice)
    if "привет" in message.text.lower():
        info = ['Привет', 'Хеллоу', 'Приветствую']
        privet = tts.text_to_wav(random.choice(info), "privet.wav")
        path = Path("", privet)
        voice = InputFile(path)
        await message.answer_voice(voice)
    if "что делаешь" in message.text.lower():
        text = ['Сижу, читаю книгу.', 'Сейчас занимаюсь кодингом.']
        what_work = tts.text_to_wav(random.choice(text), "what_work.wav")
        path = Path("", what_work)
        voice = InputFile(path)
        await message.answer_voice(voice)
    if "как настроение" in message.text.lower():
        info = ['Да все нормально', 'Вообще все не плохо', 'у меня все хорошо, надеюсь у Вас тоже']
        sentiment = tts.text_to_wav(random.choice(info), "sentiment.wav")
        path = Path("", sentiment)
        voice = InputFile(path)
        await message.answer_voice(voice)
    if "отправь песни" in message.text.lower():
        name = text.replace('отправь песни', '')
        url = 'https://mp3party.net/search?q='
        page = requests.get(url+name)
        soup = BeautifulSoup(page.content, "html.parser")
        music = soup.find('div', class_='play-btn').attrs.get('href')
        id = soup.find('div', class_='play-btn').attrs.get('data-song-id')
        url = "https://dl1.mp3party.net/online/"
        file = urllib.request.urlretrieve(url+id+".mp3", id+".mp3")
        mp3 = id+".mp3"
        voice = InputFile(mp3)
        await message.answer_audio(voice)
        os.remove(mp3)
    if "сколько время" in message.text.lower():
        now = datetime.datetime.now()
        text = f"Сейчас время {now.hour}:{now.minute}"
        intme = tts.text_to_wav(text, "intime.wav")
        path = Path("", intme)
        voice = InputFile(path)
        await message.answer_voice(voice)   
    if "какая погода" in message.text.lower():
        text = f"Сейчас на улице {int(weather.res.fact.temp)} градуса, Ощущается как {int(weather.res.fact.feels_like)}, {weather.condition}"
        temp = tts.text_to_wav(text, "weather.wav")
        path = Path("", temp)
        voice = InputFile(path)
        await message.answer_voice(voice)
                         

    # Удаление временного файла
    # os.remove(out_filename)


# Хэндлер на получение голосового и аудио сообщения
@dp.message_handler(content_types=[
    types.ContentType.VOICE,
    types.ContentType.AUDIO,
    types.ContentType.DOCUMENT
    ]
)
async def voice_message_handler(message: types.Message):
    
    if message.content_type == types.ContentType.VOICE:
        file_id = message.voice.file_id
    elif message.content_type == types.ContentType.AUDIO:
        file_id = message.audio.file_id
    elif message.content_type == types.ContentType.DOCUMENT:
        file_id = message.document.file_id
    else:
        await message.reply("Формат документа не поддерживается")
        return

    file = await bot.get_file(file_id)
    file_path = file.file_path
    file_on_disk = Path("", f"{file_id}.tmp")
    await bot.download_file(file_path, destination=file_on_disk)

    text = stt.audio_to_text(file_on_disk)

    out_filename = tts.text_to_wav(text)

    # Отправка голосового сообщения
    path = Path("", out_filename)
    voice = InputFile(path)
    audio = WAVE(path)
    audio_info = audio.info
    length = int(audio_info.length)
    hours, mins, seconds = audio_duration(length)    
    await message.answer_voice(voice, duration=seconds)
    if "что ты умеешь" in text.lower():
        info = "Я умею, рассказать новость, ответить на некоторые вопросы, сказать какая погода, отправить песни, сказать время и рассчитать число. спросите меня что нибудь"
        navik = tts.text_to_wav(info, "info.wav")
        path = Path("", navik)
        voice = InputFile(path)
        audio = WAVE(path)
        audio_info = audio.info
        length = int(audio_info.length)
        hours, mins, seconds = audio_duration(length)  
        await message.answer_voice(voice, duration=seconds)
    if "расскажи новость" in text.lower():
        url = 'https://lenta.ru/'
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        card = soup.select('a.card-big._longgrid')
        n = random.choice(card)
        title = n.find('h3', class_='card-big__title')
        image = n.find('img', class_='card-big__image').attrs.get('src')
        span = n.find('span', class_='card-big__rightcol')
        info = title.text + '\n' + span.text
        await message.answer_photo(image, info)
        news = tts.text_to_wav(info, "news.wav")
        path = Path("", news)
        voice = InputFile(path)
        audio = WAVE(path)
        audio_info = audio.info
        length = int(audio_info.length)
        hours, mins, seconds = audio_duration(length)  
        await message.answer_voice(voice, duration=seconds)
    if "как дела" in text.lower():
        text = ['У меня все отлично.. а у Вас как ?', 'Все супер, а у Вас как ?','Очень даже хорошо..']
        nice = tts.text_to_wav(random.choice(text), "nice.wav")
        path = Path("", nice)
        voice = InputFile(path)
        audio = WAVE(path)
        audio_info = audio.info
        length = int(audio_info.length)
        hours, mins, seconds = audio_duration(length) 
        await message.answer_voice(voice, duration=seconds)
    if "отлично" in text.lower():
        i_m_glad = ['Я рада', 'Я рада что у Вас отлично', 'Чтобы всегда так было']
        glad = tts.text_to_wav(random.choice(i_m_glad), "i_m_glad.wav")
        path = Path("", glad)
        voice = InputFile(path)
        audio = WAVE(path)
        audio_info = audio.info
        length = int(audio_info.length)
        hours, mins, seconds = audio_duration(length)
        await message.answer_voice(voice, duration=seconds)
    if "привет" in text.lower():
        info = ['Привет', 'Хеллоу', 'Приветствую']
        privet = tts.text_to_wav(random.choice(info), "privet.wav")
        path = Path("", privet)
        voice = InputFile(path)
        audio = WAVE(path)
        audio_info = audio.info
        length = int(audio_info.length)
        hours, mins, seconds = audio_duration(length)
        await message.answer_voice(voice, duration=seconds)
    if "что делаешь" in text.lower():
        text = ['Сижу, читаю книгу.', 'Сейчас занимаюсь кодингом.']
        what_work = tts.text_to_wav(random.choice(text), "what_work.wav")
        path = Path("", what_work)
        voice = InputFile(path)
        audio = WAVE(path)
        audio_info = audio.info
        length = int(audio_info.length)
        hours, mins, seconds = audio_duration(length)
        await message.answer_voice(voice, duration=seconds)
    if "как настроение" in text.lower():
        info = ['Да все нормально', 'Вообще все не плохо', 'у меня все хорошо, надеюсь у Вас тоже']
        sentiment = tts.text_to_wav(random.choice(info), "sentiment.wav")
        path = Path("", sentiment)
        voice = InputFile(path)
        audio = WAVE(path)
        audio_info = audio.info
        length = int(audio_info.length)
        hours, mins, seconds = audio_duration(length)
        await message.answer_voice(voice, duration=seconds)
    if "отправь песни" in text.lower():
        name = text.replace('отправь песни', '')
        url = 'https://mp3party.net/search?q='
        page = requests.get(url+name)
        soup = BeautifulSoup(page.content, "html.parser")
        music = soup.find('div', class_='play-btn').attrs.get('href')
        id = soup.find('div', class_='play-btn').attrs.get('data-song-id')
        url = "https://dl1.mp3party.net/online/"
        file = urllib.request.urlretrieve(url+id+".mp3", id+".mp3")
        mp3 = id+".mp3"
        voice = InputFile(mp3)
        await message.answer_audio(voice)
        os.remove(mp3)
    if "сколько время" in text.lower():
        now = datetime.datetime.now()
        text = f"Сейчас время {now.hour}:{now.minute}"
        intme = tts.text_to_wav(text, "intime.wav")
        path = Path("", intme)
        voice = InputFile(path)
        audio = WAVE(path)
        audio_info = audio.info
        length = int(audio_info.length)
        hours, mins, seconds = audio_duration(length)
        await message.answer_voice(voice, duration=seconds)
    if "сколько будет" in text.lower():
        intext = text.lower()
        intext = intext.replace("ноль",'0')
        data = ['скажи', 'на', 'сколько будет', 'из','пожалуйста']
        for i in data:
            intext = intext.replace(i, '')
        text = alpha2digit(intext, "ru", ordinal_threshold=0)
        calc = eval(text)
        calc = str(calc).replace('-', 'минус')
        req = tts.text_to_wav("Это будет"+calc, "calc.wav")
        path = Path("", req)
        voice = InputFile(path)
        audio = WAVE(path)
        audio_info = audio.info
        length = int(audio_info.length)
        hours, mins, seconds = audio_duration(length)
        await message.answer_voice(voice, duration=seconds)
    if "какая погода" in text.lower():
        text = f"Сейчас на улице {int(weather.res.fact.temp)} градуса, Ощущается как {int(weather.res.fact.feels_like)}, {weather.condition}"
        temp = tts.text_to_wav(text, "weather.wav")
        path = Path("", temp)
        voice = InputFile(path)
        audio = WAVE(path)
        audio_info = audio.info
        length = int(audio_info.length)
        hours, mins, seconds = audio_duration(length)
        await message.answer_voice(voice, duration=seconds)
        
    

    os.remove(file_on_disk)  # Удаление временного файла


if __name__ == "__main__":
    # Запуск бота
    print("Запуск бота")
    try:
        executor.start_polling(dp, skip_updates=True)
    except (KeyboardInterrupt, SystemExit):
        pass    