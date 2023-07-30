import re
import asyncio
import aiohttp


# 1. Создадим класс Weather, который будет хранить параметры погоды:

class Weather:
    def __init__(self, city, temperature, description):
        self.city = city
        self.temperature = temperature
        self.description = description

    def __str__(self):
        return f"{self.city}: {self.temperature}°C, {self.description}"


# 2. Для запроса погоды используем функцию get_weather, которая будет принимать название города и возвращать объект класса Weather:


async def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        async with session.get(url) as response:
            data = await response.json()
            temperature = data["main"]["temp"]
            description = data["weather"][0]["description"]
            return Weather(city, temperature, description)


# 3. Создадим асинхронную функцию main, которая будет запускать запросы на получение погоды для каждого города и выводить результат:

async def main(cities):
    tasks = [asyncio.create_task(get_weather(city)) for city in cities]
    weathers = await asyncio.gather(*tasks)
    for weather in weathers:
        print(weather)

if __name__ == "__main__":
    file = open('cities.txt', 'r')

    strings = file.readlines()

    pattern = r'\)\s(.+?)(?=\s[-\s\d])'

    cities = []

    for string in strings:
        match = re.search(pattern, string)
        if match:
            cities.append(match.group(1))

    API_KEY = "0fb610dab7456bc44dbdde2ddba9be71"
    asyncio.run(main(cities))


