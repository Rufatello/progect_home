import requests
from datetime import datetime
import os
import telebot

bot = telebot.TeleBot('token_telegramm')
vacancies = []
def get_vacancies(currency):
    """Выгрузка данных по 'HH' по запросам пользователя и возвращается словарь"""
    response = requests.get(f'https://api.hh.ru/vacancies', params={'text': currency, 'per_page': 2})

    data = response.json()
    for vacancy in data['items']:
        published_at = datetime.strptime(vacancy['published_at'], "%Y-%m-%dT%H:%M:%S%z")
        vacancy_info = {
            'id': vacancy['id'],
            'name': vacancy['name'],
            'solary_ot': vacancy['salary']['from'] if vacancy.get('salary') else None,
            'solary_do': vacancy['salary']['to'] if vacancy.get('salary') else None,
            'responsibility': vacancy['snippet']['responsibility'],
            'data': published_at.strftime("%d.%m.%Y")

        }
        vacancies.append(vacancy_info)
    return vacancies

@bot.message_handler(commands=['start'])
def start(message):

    bot.send_message(message.chat.id, "Привет! Введи профессию, которая тебе интересна и тебе выскочит вакансия на hh.ru")


@bot.message_handler(content_types=['text'])
def load_vacancy(message):
    currency = message.text
    data = get_vacancies(currency)
    for i in data:
        bot.send_message(message.chat.id, f"id - {i['id']}\nДолжность - {i['name']}\nЗ.п от - {i['solary_ot']}\nЗ.п до - {i['solary_do']}\nОписание - {i['responsibility']}\nДата - {i['data']}\n")


bot.polling(none_stop=True, interval=0)
