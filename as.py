from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
TOKEN = "5628114893:AAGb7eDbkTYTm_U2B-JQPh4LXMUEUPBcquY"
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(msg: types.Message):
    await msg.reply(f'Я бот. Приятно познакомиться {msg.from_user.first_name}')
                               
@dp.message_handler(content_types=['text'])
async def get_text_messages(msg: types.Message):
   if msg.text.lower() == 'привет':
       await msg.answer('Привет!')
   else:
       await msg.answer('Не понимаю, что это значит.')                               

if __name__ == '__main__':
        executor.start_polling(dp)  