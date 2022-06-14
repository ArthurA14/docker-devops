import flask
from flask import request, jsonify
import os
import requests
from datetime import datetime, timedelta
import config
from config import Config

app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config.from_object('config.Config')

# APIKEY = os.environ.get('APIKEY')
# LAT = os.environ.get('LAT') 
# LONG = os.environ.get('LONG')

@app.route('/', methods=['GET'])
def home():
    html = """
           <h1>Sunrise-sunset API</h1>
           <p>Example RESTful API for the course Lab. of Cloud Computing, Big Data and security @ UniCatt</p>
           """
    return html


@app.route('/api/prova/<city>', methods=['GET'])
def api_prova(city):
    output = {}
    if city:
        output = {
            'sunrise': 1,
            'sunset': 2,
            'city': city
        }
    return jsonify(output)


@app.route('/api/daylight/<city>', methods=['GET'])
def api_daylight(city):
    output = {}
    uri = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={config.Config.APIKEY}"
    # uri = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={APIKEY}"
    print(uri)
    res = requests.get(uri)
    if res.status_code == 200:
        data = res.json()
        sunrise = data['sys']['sunrise']
        sunset = data['sys']['sunset']
        output = {
            'sunrise': sunrise,
            'sunset': sunset,
            'daylight': sunset-sunrise,
            'city': city            
        }
    return output


@app.route('/', methods=['GET'])
def api_daylight2():
    output = {}
    uri = f"https://api.openweathermap.org/data/2.5/weather?lat={config.Config.LAT}&lon={config.Config.LONG}&appid={config.Config.APIKEY}"
    # uri = f"https://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LONG}&appid={APIKEY}"
    print(uri)
    res = requests.get(uri)
    if res.status_code == 200:
        data = res.json()
        sunrise = data['sys']['sunrise']
        sunset = data['sys']['sunset']
        latitude = data['coord']['lat']
        longitude = data['coord']['lon']
        city = data['name']
        daylight = sunset-sunrise
        meteo = data['weather'][0]['main']
        descri = data['weather'][0]['description']
        temp = data['main']['temp']
        feels = data['main']['feels_like']
        wind = data['wind']['speed']
        country = data['sys']['country']

        html = """
            <h1>API TP DEVOPS - Arthur ALLIE </h1>
            <p><b> Latitude </b> : """+ str(latitude) +""" °</p>
            <p><b> Longitude </b> : """+ str(longitude) +""" °</p>
            <p><b> Pays </b> : """+ str(country) +""" </p>
            <p><b> Ville </b> : """+ str(city) +""" </p>
            <p><b> Température </b> :"""+ str(temp) +""" </p>
            <p><b> Température ressentie </b> : """+ str(feels) +""" </p>
            <p><b> Temps </b> : """+ str(meteo) +""" </p>
            <p><b> Description du temps </b> : """+ str(description) +""" </p>
            <p><b> Force du vent </b> : """+ str(wind) +""" </p>"""
            
    return html

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8081)
# app.run(host='0.0.0.0')  # accept connection from every host
