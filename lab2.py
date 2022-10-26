import requests
city = "Bryansk,RU"
appid = "297f42939b1d804959707682cf0c5fb8"
res = requests.get("http://api.openweathermap.org/data/2.5/weather",
params={'q': city, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
data = res.json()
print("скорость ветра сегодня:",data['wind']['speed'])
print('видимость сегодня',data['visibility'])

res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
params={'q': city, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
data = res.json()
print("Ветер:")
for i in data['list']:
    print("Дата <", i['dt_txt'], "> \r\n скорость <",
i['wind']['speed'],'>\r\n влажность<',
i['visibility'])
print("____________________________")
