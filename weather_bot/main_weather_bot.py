import requests
import datetime
from config import bot_token, open_weather_token
from aiogram import Bot, types, Dispatcher
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor


bot = Bot(token=bot_token)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start_command(message: types.message):
    await message.reply("Hi, there! Just enter the name of the city you want.")

@dp.message_handler()
async def get_weather(message: types.message):
    
    
    code_to_smile = {
        "Clear": "Clear \U00002600",
        "Clouds": "Cloudy \U00002601",
        "Rain": "Rain \U00002614",
        "Drizzle": "Rain \U00002614",
        "Thunderstorm": "Thunderstorm \U000026A1",
        "Snow": "Snow \U0001F328",
        "Mist": "Misty \U0001F32B"
    }
    
    try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
        )
        data = r.json()

        city = data["name"]
        cur_weather = data["main"]["temp"]


        weather_desc = data["weather"][0]["main"]
        if weather_desc in code_to_smile:
            wd = code_to_smile[weather_desc]
        else:
            wd = "Look out the window, I have no info:("




        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestemp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
            data["sys"]["sunrise"])

        await message.reply(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
              f"Weather in: {city}\nTemperature: {cur_weather}C° {wd}\n"
              f"Humidity: {humidity}%\n"
              f"Pressure: {pressure}\n"
              f"Wind speed: {wind} m/s\n"
              f"Sunrise: {sunrise_timestamp}\n"
              f"Sunset: {sunset_timestemp}\n"
              f"Day length: {length_of_the_day}\n"
              f"***Have a nice day***!"
              )
    
    except:
        await message.reply("Please check city name")




if __name__ == '__main__':
    executor.start_polling(dp)
