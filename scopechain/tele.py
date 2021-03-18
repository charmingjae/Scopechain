import telegram
bot = telegram.Bot(token='')
chat_id =

bot.sendMessage(chat_id=chat_id, text='Hello World!')

bot.sendPhoto(chat_id=chat_id, photo=open('./test1.jpg', 'rb'))
