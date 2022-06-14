
## DEVOPS - TP2 - DOCKER
## ARTHUR ALLIE - EFREI - M1 BDIA APP

### Rappel des objectifs de ce TP : 
- Configurer un workflow Github Action
- Transformer un wrapper en API
- Publier automatiquement a chaque push sur Docker Hub
- Mettre à disposition son image (format API) sur DockerHub
- Mettre à disposition son code dans un repository Github

---

-- Repository GitHub associé à mon TP : 
https://github.com/ArthurA14/docker-devops-td1 (JE REUTILISE LE REPOSITORY DE LA SESSION PRECEDENTE)
-- Image sur DockerHub associé à mon TP : 
https://hub.docker.com/r/antoinearthur/efrei-devops-tp2

---

### Solutions techniques employées : 
Pour réaliser ce travail, j'ai utilisé le langage de programmation ***Python***. 
Afin de requêter une API, j'ai utilisé en plus de Python le micro framework dédié ***Flask***.
L'OS que j'utilise est ***Windows 10***, avec le CLI ***WSL2***, de manière à bénéficier de certaines commandes Unix.

---

### Travail réalisé étape par étape : 

### 1.  Installations préliminaires : 
- #### Je commence par créer un répertoire de projet en local, que je nomme *docker-devops-tp2*:
````bash
$ cd ../..
$ cd Users/arthu/Efrei/DEVOPS
$ mkdir docker-devops-tp2
$ cd docker-devops-tp2
````

- *Je crée ensuite un environnement virtuel *myvenv* au sein de ce répertoire projet; cela me permettra d'installer toutes les librairies dont j'aurai besoin ultérieurement, tout en isolant mon application d'un point de vue code. En effet, en procédédant ainsi, les versions des librairies que j'installerai dans mon environnement virtuel seront toujours disponibles au sein de cet environnement, ce qui m'assurera que mon code fonctionnera toujours correctement en son sein :* 
````bash
$ python3 -m venv myvenv
````

- #### Activation de l'environnement virtuel *myvenv* : 
````bash
$ source myvenv/bin/activate
````
-> *Ce qui donne :* 
````bash
(myvenv) toto@DESKTOP-OBTCMJQ:/mnt/c/Users/arthu/Efrei/DEVOPS/docker-devops-tp2$
````
*A présent, je lancerai toujours de nouvelles commandes à partir de cet environnement virtuel.*

---

### 2 . Création de compte sur openweathermap.org
#### *(Cette étape a déjà été réalisée lors d'une session précédente.)*
- #### Je crée un compte sur openweathermap.org.
- #### J'y récupère mon API KEY dans mon espace personnel.
*Pour les besoins de la démonstration, mon API KEY est : ***68e3a32**********

---

### 3.  Test de la Weather API en ligne de commandes : 
#### *(Cette étape a déjà été réalisée lors d'une session précédente.)*
- #### Sous WSL2, dans *myvenv*, je tape : 
````bash
$ export APIKEY=68e3a32******
````

- #### Test de l'API KEY à partir de la console : 
#### *(Cette étape a déjà été réalisée lors d'une session précédente.)*
````bash
$ curl "http://api.openweathermap.org/data/2.5/weather?q=palermo&appid=$APIKEY"
````

````bash
{"coord":{"lon":13.5833,"lat":37.8167},"weather":[{"id":800,"main":"Clear","description":"clear sky","icon":"01d"}],"base":"stations","main":{"temp":307.34,"feels_like":304.89,"temp_min":301.13,"temp_max":310.26,"pressure":1018,"humidity":14,"sea_level":1018,"grnd_level":960},"visibility":10000,"wind":{"speed":2.69,"deg":357,"gust":3.27},"clouds":{"all":10},"dt":1654422181,"sys":{"type":2,"id":2007649,"country":"IT","sunrise":1654400659,"sunset":1654453456},"timezone":7200,"id":2523918,"name":"Province of Palermo","cod":200}
````
-> *Cette commande me retourne les informations météorologiques de la ville de "Palerme"*.

---

### 4.  Utilisation de la Weather API avec Python et Flask : 
- #### Installation des dépendances nécessaires dans mon environnement virtuel : 
````bash
$ pip install flask
$ pip install python-dotenv
````
Puis, dans myapi.py : 
````python
from dotenv import load_dotenv
````

- #### Création d'un fichier *config.py* et d'un fichier *myapi.py* : 
````bash
$ touch config.py
$ touch myapi.py
````
- #### Ecriture du code au sein du fichier *config.py*:
*-> Ce fichier se charge de récupérer les variables d'environnements : clé API, Latitute, Longitude.*
````bash
from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    """Base config class."""
    APIKEY = os.environ.get('APIKEY')
    LAT = os.environ.get('LAT') 
    LONG = os.environ.get('LONG')
````
- #### Ecriture du code au sein du fichier *myapi.py*:
````python
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
            <p><b> Description du temps </b> : """+ str(descri) +""" </p>
            <p><b> Force du vent </b> : """+ str(wind) +""" </p>"""
            
    return html

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8081)
# app.run(host='0.0.0.0')  # accept connection from every host
````
*-> Ce code me permet de paramétrer l'url que je requête, avec le nom d'une ville à renseigner.* 

- #### Compilation et exécution de mon code : 
````bash
$ python3 myapi.py
````

````bash
 * Serving Flask app 'myapi' (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on all addresses (0.0.0.0)
   WARNING: This is a development server. Do not use it in a production deployment.
 * Running on http://127.0.0.1:8081
 * Running on http://172.17.154.251:8081 (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 348-274-305
````
*-> Cette commande, en exécutant le code contenu dans le fichier **myapi.py**, me permet d'accéder à mon server local http://127.0.0.1:8081 .*
*Dans l'URL, je tape :* 
-> http://127.0.0.1:8081/api/prova/astana
*puis :*
-> http://127.0.0.1:8081/api/daylight/astana

*J'obtiens :*
````bash
{
  "city": "astana", 
  "sunrise": 1, 
  "sunset": 2
}
````
*puis :*
````bash
{
  "city": "astana", 
  "daylight": 59298, 
  "sunrise": 1654815573, 
  "sunset": 1654874871
}
````

---

### 5. Dockerization :
- #### Création d'un fichier *"requirements.txt"* dans le répertoire de projet : 
````bash
$ touch requirements.txt
````
-> *J'y inscris les dépendances nécessaires :* 
````python
flask==2.1.2
requests==2.22.0
click==8.1.3
importlib-metadata==4.11.4
itsdangerous==2.1.2
Jinja2==3.1.2
MarkupSafe==2.1.1
Werkzeug==2.1.2
zipp==3.8.0
python-dotenv
````

- #### Création du fichier ***Dockerfile*** : 
-> *Ce fichier me permet d'exécuter les différentes commandes, associées à différents fichiers, dont j'ai besoin pour créer mon conteneur Docker. Dans ce fichier, j'écris donc les lignes de commandes suivantes :*
````docker
FROM  python:3.8-buster

WORKDIR /docker-devops-tp2  # répertoire de projet à partir duquel je travaille  

COPY  requirements.txt  .  # utilisation des dépendances dont j'aurai éventuellement besoin

RUN  pip  install  -r  requirements.txt  # exécution de ce fichier

COPY myapi.py .  # import du fichier python contenant mon code

EXPOSE 8081  # numéro du port que je vais utiliser sur mon réseau pour créer mon image

CMD ["python", "myapi.py"]  # langage et fichier que je vais utiliser dans mon image Docker 
````

-> *Pour la suite de mon travail, j'ai déjà installé lors d'une session précédente ***Docker Desktop***. Je dois le démarrer afin de pouvoir utiliser la commande *docker* dans WSL2.*

- #### Construction de l'image Docker : 
#### *(Cette étape a déjà été réalisée lors d'une session précédente.)*
````bash
$ docker build --tag myapi .
````

-> *Cette ligne de commande permet de créer l'image **"myapi"** que je vais utiliser par la suite.*

````bash
[+] Building 3.2s (11/11) FINISHED
 => [internal] load build definition from Dockerfile                                                               0.1s
 => => transferring dockerfile: 329B                                                                               0.0s
 => [internal] load .dockerignore                                                                                  0.1s
 => => transferring context: 2B                                                                                    0.0s
 => [internal] load metadata for docker.io/library/python:3.8-buster                                               2.7s
 => [auth] library/python:pull token for registry-1.docker.io                                                      0.0s
 => [1/5] FROM docker.io/library/python:3.8-buster@sha256:458c39bbb8187420ae4e9bd4d1a889511f5fb5463b7969b47fb4441  0.0s
 => [internal] load build context                                                                                  0.0s
 => => transferring context: 3.77kB                                                                                0.0s
 => CACHED [2/5] WORKDIR /docker-devops-tp2                                                                        0.0s
 => CACHED [3/5] COPY requirements.txt .                                                                           0.0s
 => CACHED [4/5] RUN pip install -r requirements.txt                                                               0.0s
 => [5/5] COPY myapi.py .                                                                                          0.1s
 => exporting to image                                                                                             0.2s
 => => exporting layers                                                                                            0.1s
 => => writing image sha256:cb967dd1b0d7d997ba6be87ff9ef593a6ceaa6df6cfa3dd1483a28ba0aba263e                       0.0s
 => => naming to docker.io/library/myapi                                                                           0.0s
````

- #### Exécution du conteneur associé : 
````bash
$ docker run -p 8081:8081 --env APIKEY=$APIKEY --rm myapi
````
*ou :*
````bash
$ docker run -p 8081:8081 --env APIKEY=68e3a32****** --rm myapi
````

````bash
 * Serving Flask app 'myapi' (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on all addresses (0.0.0.0)
   WARNING: This is a development server. Do not use it in a production deployment.
 * Running on http://127.0.0.1:8081
 * Running on http://172.17.0.2:8081 (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 415-332-724
````
*Dans l'URL, je tape :* 
-> http://127.0.0.1:8081/api/prova/astana
*puis :*
-> http://127.0.0.1:8081/api/daylight/astana
-> *J'obtiens alors, en local, comme précédemment :* 

````bash
{
  "city": "astana", 
  "sunrise": 1, 
  "sunset": 2
}
````
*puis :*
````bash
{
  "city": "astana", 
  "daylight": 59298, 
  "sunrise": 1654815573, 
  "sunset": 1654874871
}
````

---

### 6. Utilisation de GitHub Actions afin de publier mon image sur DockerHub :

- #### Ajout de son ID Docker comme secret sur GitHub : 
	##### - Se rendre sur https://hub.docker.com/settings/security : 
	##### - Aller dans : *"Account settings"* -> *"Security"* -> *"New Access Token"* -> *"Access Token Description"* 
	*-> Ici, je choisis d'entrer la chaîne de caractères "mytoken"*

- #### Ajout de ses identifiants Docker comme secrets dans l'interface utilisateur des secrets de GitHub :
	##### - Se rendre sur https://github.com/ArthurA14/docker-devops-td1 : 
	##### - Aller dans : *"Settings"* -> *"Secrets"* -> *"Actions"* -> *"New repository secret"*
	##### *-> Ici, je renseigne deux "secrets" :* 
	*-> Name : "USERNAME", Value : "a*t****" (username DockerHub)
	*-> Name : "PASSWORD", Value : "********" (password DockerHub)*
	*-> Pour chacun des deux champs, je termine en cliquant sur **"Add secret".***

- #### Configurer le GitHub Actions workflow :
	##### - Se rendre sur https://github.com/ArthurA14/docker-devops-td1 : 
	##### - Enable GitHub Container Registry : *Cliquer sur "Profile"* -> *"Feature Preview"* -> *"Improved Container Support"* -> *"Enable"*
  ##### - Retourner sur le repository du projet : https://github.com/ArthurA14/docker-devops-td1
	##### - Aller dans l'onglet *"Actions"* du menu principal, -> *"New workflow"* -> *"Docker image"* -> *"Configure"*
  *-> cela me permet de modifier le contenu du fichier *"docker-image.yml"* : https://github.com/ArthurA14/docker-devops-td1/tree/main/.github/workflows*
  ##### - Dans ce fichier, j'inscris le code suivant : 
````bash
name: ci

on:
  push:
    branches:
      - 'main'

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      -
        name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2
      -
        name: Login to DockerHub
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.USERNAME }}
          password: ${{ secrets.PASSWORD }}
      -
        name: Build and push
        uses: docker/build-push-action@v3
        with:
          push: true
          tags: ${{ secrets.USERNAME }}/efrei-devops-tp2:latest 
````

##### - Cliquer sur *"Start commit"* puis *"Commit new file"*

-> *Mon image a bien été envoyée sur DockerHub, à l'adresse suivante : https://hub.docker.com/r/antoinearthur/efrei-devops-tp2*
-> *Les différentes étapes de ce processus d'envoi sont :*
- Set up job
- Set up Docker Buildx
- Login to DockerHub
- Build and Push
- Post Build and Push
- Post Login to DockerHub 
- Post Setup Docker Buildx
- Complete job

----

### 7. Récupération de mon image sur Docker Hub :
*Dans un premier terminal, je lance :*
````bash
$ docker run --network host --env LAT="5.902785" --env LONG="102.754175" --env APIKEY=68e3a32****** antoinearthur/efrei-devops-tp2
````
*En allant à l'adresse http://127.0.0.1:8081 ou http://192.168.65.3:8081, j'obtiens :*
````bash
    API TP DEVOPS - Arthur ALLIE
    Latitude : 5.9028 °
    Longitude : 102.7542 °
    Pays : MY 
    Ville : Jertih
    Température :299.81
    Température ressentie : 299.81
    Temps : Clouds
    Description du temps : overcast
    Force du vent : 3.44
````


*Puis dans un second terminal, je lance :*
````bash
curl "http://localhost:8081/?lat=5.902785&lon=102.754175"
````
*J'obtiens :*
````bash
    <h1>API TP DEVOPS - Arthur ALLIE </h1>
    <p><b> Latitude </b> : 5.9028 °</p>
    <p><b> Longitude </b> : 102.7542 °</p>
    <p><b> Pays </b> : MY </p>
    <p><b> Ville </b> : Jertih </p>
    <p><b> Température </b> :299.81 </p>
    <p><b> Température ressentie </b> : 299.81 </p>
    <p><b> Temps </b> : Clouds </p>
    <p><b> Description du temps </b> : overcast </p>
    <p><b> Force du vent </b> : 3.44 </p>
````
