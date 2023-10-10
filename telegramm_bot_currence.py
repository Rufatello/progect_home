import os
import requests
import telebot
bot = telebot.TeleBot('token_telegram')
CURRENCY_RATES_FILE = "currency_rates.json"
API_KEY = os.getenv('API_KEY_USD')

def get_currency_rate(currency):
    url = f"https://api.apilayer.com/exchangerates_data/latest?base={currency}"
    response = requests.get(url, headers={'apikey': API_KEY}).json()
    rate = response["rates"]["RUB"]
    return rate

@bot.message_handler(commands=['start'])
def start(message):

    bot.send_message(message.chat.id, "Привет! Введи /USD или /EUR, чтобы получить к RUB.")

@bot.message_handler(commands=['USD'])
@bot.message_handler(commands=['EUR'])
def get_currency_rate_message(message):
    currency = message.text[1:]
    if currency not in ['USD', 'EUR']:
        bot.send_message(message.chat.id, 'Некорректная валюта. Введите /USD или /EUR.')
        return

    rate = get_currency_rate(currency)
    bot.send_message(message.chat.id, f"Курс {currency} к рублю: {rate:.2f}")




if __name__ == "__main__":
    bot.polling(none_stop=True, interval=0)
