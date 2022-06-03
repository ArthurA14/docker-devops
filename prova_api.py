import requests
import os

APIKEY = os.environ['APIKEY']  # reads the environment variable
LAT = os.environ['LAT']
LONG = os.environ['LONG']

# response = requests.get("http://api.openweathermap.org/data/2.5/weather?q=brescia&appid="+APIKEY)
url="https://api.openweathermap.org/data/2.5/weather?lat="+LAT+"&lon="+LONG+"appid="+APIKEY
# print(url)
response = requests.get("https://api.openweathermap.org/data/2.5/weather?lat="+LAT+"&lon="+LONG+"&appid="+APIKEY)
                         
print(response.status_code)
print(response.json())