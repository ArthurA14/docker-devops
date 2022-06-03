
https://mldv.it/home/posts/lectures/restapi-python-docker-2020/ :
https://pypi.org/project/python-dotenv/
https://lucasvidelaine.wordpress.com/2018/01/29/utilisation-de-dockerhub/


> cd ../..
toto@DESKTOP-OBTCMJQ:/mnt/c$
Linux : 
> cd Users/arthu/Efrei/DEVOPS/docker-devops-td1

Powershell :
> cd Users\arthu\Efrei\DEVOPS\docker-devops-td1

Créer environnement virtuel : 
> py -3 -m venv myvenv (Windows)
> python3 -m venv myvenv (Linux)

Activer l'environnement virtuel : 
> myvenv\Scripts\activate (Windows)
> source myvenv/bin/activate (Linux)

Set the environment variable for the key :
$ export APIKEY=68e3a32a2b52669bdab1c00876332096

Test the API from the console :
$ curl "http://api.openweathermap.org/data/2.5/weather?q=brescia&appid=$APIKEY"

Use the API with python : 
Créer fichier prova_api.py : 
$ touch prova_api.py
$ python3 prova_api.py

My API with Flask :
$ sudo apt install python3-flask / pip install flask

Créer fichier myapi.py : 
$ touch myapi.py

And run it with the command :
$ python3 myapi.py

> http://127.0.0.1:5000/

Try it by connecting to http://localhost:5000/ from the web browser.

............................................................................

Let's add a new entry-point named /api/prova and return a JSON for testing.

> http://127.0.0.1:5000/api/prova

............................................................................

Reading parameters :
Do " pip install python-dotenv "

Puis, dans myapi.py : 
from dotenv import load_dotenv

Alternative, arguably more elegant, way :
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

............................................................................

Alternative way : 
Dans myapi.py : 
    app.config.from_object('config.Config')

............................................................................

Retrieve data from REST API, elaborate it and return it :

@app.route('/api/daylight/<city>', methods=['GET'])
def api_daylight(city):
    output = {}
    uri = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={APIKEY}"
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

............................................................................

Dockerization : 

app.run(host='0.0.0.0')  # accept connection from every host

File requirements.txt :
    flask==1.1.1
    requests==2.22.0

File Dockerfile :

    FROM python:3.8-buster

    WORKDIR /docker-devops-td1

    COPY requirements.txt .

    RUN pip install -r requirements.txt

    COPY myapi.py .

    EXPOSE 5000

    CMD ["python", "myapi.py"]

Build the image with :
$ docker build --tag myapi .
$ docker build --tag prova_api .

Run the container with :
$ docker run -p 5000:5000 --env APIKEY=$APIKEY --rm myapi
$ docker run -p 5000:5000 --env APIKEY=$APIKEY --rm prova_api
Ou : 
$ docker run -p 5000:5000 --env APIKEY=240aa650f4db4e154a07d0459c30a347 --rm prova_api
$ docker run --env LAT="5.902785" --env LONG="102.754175" --env APIKEY=240aa650f4db4e154a07d0459c30a347 --rm prova_api

-> https://openweathermap.org/current
"https://api.openweathermap.org/data/2.5/weather?lat="+LAT+"&lon="+LONG+"&appid="+APIKEY

............................................................................

Utilisation de Docker Hub : 
$ docker images
$ docker login --username=antoinearthur
-> mp Docker Hub à entrer
tag IMAGE ID de prova_api : e0050a5233b7
$ docker tag e0050a5233b7 antoinearthur/docker-devops-td1 
$ docker images   
$ docker push antoinearthur/docker-devops-td1 
$ docker run --env LAT="5.902785" --env LONG="102.754175" --env APIKEY=240aa650f4db4e154a07d0459c30a347 antoinearthur/docker-devops-td1 
