from telebot import TeleBot, types
import requests
from bs4 import BeautifulSoup
import threading
import time

TOKEN = ""

stop_sending = False
sending_thread = None

bot = TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "ку✌️\nвведи /button")

@bot.message_handler(commands=['button'])
def button_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("БИТКОИН К РУБЛЮ")
    button2 = types.KeyboardButton("БИТКОИН К ДОЛЛАРУ") 
    button3 = types.KeyboardButton("ПОГОДА В КОПЕЙСКЕ КАЖДЫЕ 10 МИНУТ") 
    button4 = types.KeyboardButton("ПОГОДА В КОПЕЙСКЕ") 
    markup.add(button1, button2, button3, button4)

    bot.send_message(message.chat.id, "Выбери что тебе нужно", reply_markup=markup)

@bot.message_handler(content_types='text')
def message_reply(message):
    global stop_sending, sending_thread
    if message.text == "ПОГОДА В КОПЕЙСКЕ КАЖДЫЕ 10 МИНУТ":

        bot.send_message(message.chat.id, "Если хочешь остановиться напиши стоп.")
        url = 'https://yandex.ru/pogoda/ru/11207?lat=55.188533&lon=61.624168&from=yabro_ntp_clock&win=694'
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        temp = soup.find("span", class_="AppFactTemperature_sign__1MeN4").text
        temp2 = soup.find("span", class_="AppFactTemperature_value__2qhsG").text
        temp3 = soup.find("span", class_="AppFactTemperature_degree__LL_2v").text
        pogoda = soup.find("p", class_="AppFact_warning__8kUUn").text
        pogoda = temp + temp2 + temp3 + " " + pogoda
        bot.send_message(message.chat.id, pogoda)
        if sending_thread is None or not sending_thread.is_alive():
            stop_sending = False
            def send_messages():
                chat_id = message.chat.id
                while not stop_sending:
                    bot.send_message(chat_id, pogoda)
                    time.sleep(10*60)
            sending_thread = threading.Thread(target=send_messages)
            sending_thread.start()
    elif message.text.lower() == "стоп":
        stop_sending = True
        bot.send_message(message.chat.id, "Остановка отправки сообщений.")
    elif message.text=="БИТКОИН К РУБЛЮ":
        url = 'https://api.binance.com/api/v3/ticker/price'
        response = requests.get(url, params={'symbol': 'BTCUSDT'})
        price_object = response.json()
        price_usd = float(price_object['price'])
        newprice_usd = int(price_usd)
        usd_amount = price_usd
        response = requests.get('https://api.exchangerate-api.com/v4/latest/USD')
        data = response.json()
        rate = data['rates']['RUB']
        price_rub = int(usd_amount * rate)
        bot.send_message(message.chat.id,price_rub)
    elif message.text=="БИТКОИН К ДОЛЛАРУ":
        url = 'https://api.binance.com/api/v3/ticker/price'
        response = requests.get(url, params={'symbol': 'BTCUSDT'})
        price_object = response.json()
        price_usd = float(price_object['price'])
        newprice_usd = int(price_usd)
        bot.send_message(message.chat.id,newprice_usd)
    elif message.text == "ПОГОДА В КОПЕЙСКЕ":
        url = 'https://yandex.ru/pogoda/ru/11207?lat=55.188533&lon=61.624168&from=yabro_ntp_clock&win=694'
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        temp = soup.find("span", class_="AppFactTemperature_sign__1MeN4").text
        temp2 = soup.find("span", class_="AppFactTemperature_value__2qhsG").text
        temp3 = soup.find("span", class_="AppFactTemperature_degree__LL_2v").text
        pogoda = soup.find("p", class_="AppFact_warning__8kUUn").text
        pogoda = temp + temp2 + temp3 + " " + pogoda
        bot.send_message(message.chat.id, pogoda)

bot.infinity_polling()
