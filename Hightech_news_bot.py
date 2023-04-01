import telebot
import requests
from bs4 import BeautifulSoup
import random

# инициализируем токен телеграм-бота
TOKEN = 'YOUR TOKEN HERE'
bot = telebot.TeleBot(TOKEN)

from telebot import types

# команда для обработки нажатия на кнопку /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # создаем клавиатуру
    keyboard = types.ReplyKeyboardMarkup()
    # добавляем кнопки
    keyboard.add(types.KeyboardButton('Свежая новость 🆕'), 
                 types.KeyboardButton('Последние 3 новости 📰'))
    # отправляем сообщение с приветствием и клавиатурой
    bot.reply_to(message, "Привет! Я бот, который выдаёт новости с сайта 3dnews.ru Нажми одну из кнопок, чтобы получить новости.", reply_markup=keyboard)

# функция для получения новостей с сайта
def get_news():
    url = 'https://3dnews.ru/news'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    news_list = soup.find_all('div', class_='cntPrevWrapper')
    news = []
    for item in news_list:
        title = item.find('h1').text.strip()
        description = item.find('p').text.strip()
        url = "https://3dnews.ru"+item.find('a', class_='entry-header').get('href')
        news.append({'title':title, 'description': description, 'url': url})
    return news

# функция для форматирования новостей в текстовый вид
def format_news(news):
    if not news:
        return "Новостей пока нет."
    text = ''
    for item in news:
        text += f"{item['title']}\n\n{item['description']}\n\n{item['url']}\n\n"
    return text

# команда для обработки нажатия на кнопку "Свежая новость"
@bot.message_handler(func=lambda message: message.text == 'Свежая новость 🆕')
def send_latest_news(message):
        news = get_news()
        random_news = random.choice(news)
        text = f"{random_news['url']}"
        bot.send_message(message.chat.id, text)

# команда для обработки нажатия на кнопку "Последние 3 новости"
@bot.message_handler(func=lambda message: message.text == 'Последние 3 новости 📰')
def send_last_3_news(message):
        news = get_news()
        latest_3_news = news[:3]
        text = format_news(latest_3_news)
        bot.send_message(message.chat.id, text)

# запускаем бота
bot.polling()
