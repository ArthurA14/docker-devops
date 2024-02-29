import requests
import os

APIKEY = os.environ['APIKEY']  # reads the environment variable
# LAT = os.environ['LAT']
# LONG = os.environ['LONG']
CITY = os.environ['CITY']

# url_1 = "https://api.openweathermap.org/data/2.5/weather?q=monaco&appid="+APIKEY
# url_2 = "https://api.openweathermap.org/data/2.5/weather?lat="+LAT+"&lon="+LONG+"&appid="+APIKEY
# print(url_2)
url_3 = "https://api.openweathermap.org/data/2.5/weather?q="+CITY+"&appid="+APIKEY

# response = requests.get(url_1)
# response = requests.get(url_2)
response = requests.get(url_3)
                         
print(response.status_code)
print(response.json())
# print(os.environ.get('APIKEY'))
