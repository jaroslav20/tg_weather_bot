import requests
import datetime
from weather_bot_tg.config import tg_bot_token, open_weather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor


bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)



@dp.message_handler(commands=["start"])
async  def start_command(message: types.Message):
    await message.reply("Привет! Я бот прогноза погоды.\nДай мне название города и я расскажу о погоде")



@dp.message_handler()
async def get_weather(message: types.Message):

    '''                 Dict smile weather             '''
    code_to_smile = {
        "Clear": "Ясно \U0001f31e",
        "Clouds": "Облачно \U0001f324\uFE0F",
        "Rain": "Дождь \U0001f327\uFE0F",
        "Drizzle": "Морось \U0001f326\uFE0F",
        "Trunderstorm": "Гроза \u26C8\uFE0F",
        "Show": "Снег \U0001f328\uFE0F",
        "Mist": "Туман \U0001F32B"
    }

    '''                 Time of year calculation             '''
    season = int(datetime.datetime.now().strftime('%m'))
    if season == 1 or season == 2 or season == 12:
        season_m = 'Зима \u2603\uFE0F'
    elif season == 3 or season == 4 or season == 5:
        season_m = "Весна \U0001f331"
    elif season == 6 or season == 7 or season == 8:
        season_m = "Лето \u2600\uFE0F️"
    elif season == 9 or season == 10 or season == 11:
        season_m = "Осень \U0001f342"
    else:
        season_m = "Mount is not correct"

    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
        )
        data = r.json()

        '''                 Data Extraction             '''
        city_name = data["name"]
        cur_weather = data["main"]["temp"]
        temp_max = data["main"]["temp_max"]
        temp_min = data["main"]["temp_min"]
        humidity = data["main"]["humidity"]  # Влажность
        feels_like = data["main"]["feels_like"]  # Ощущается
        pressure = data["main"]["pressure"]  # Давление
        cur_wind = data["wind"]["speed"]  # Скорость ветра
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        lenght_of_the_day = sunset_timestamp - sunrise_timestamp

        '''                 Weather description             '''
        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Нестандартная погода"

        weather_str = f"""Сейчас: {datetime.datetime.now().strftime(f'%H:%M')}
{datetime.datetime.now().strftime(f'%Y-%m-%d')}\n{season_m}\n
Погода в городе: {city_name} {wd}\n\nТемпература: {cur_weather}С°
Min t:  {temp_min}С°
Max t: {temp_max}С°\n\
Ощущается как: {feels_like}\n\nСкорость ветра: {cur_wind}метр/сек
Время восхода солнца: {sunrise_timestamp.strftime(f'%H:%M')}  \U0001f305
Время заката: {sunset_timestamp.strftime(f'%H:%M')}  \U0001f307
Продолжительность светового дня: {lenght_of_the_day}\n
Влажность: {humidity}%  \U0001f4a7
Давление: {pressure}мм.рт.ст"""


        '''                 Output weather forecast             '''

        await message.reply(weather_str)

    except:
        await message.reply("Проверьте название города")



if __name__ == '__main__':
    executor.start_polling(dp)