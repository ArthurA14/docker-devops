
## DEVOPS - TP1 - DOCKER
## ARTHUR ALLIE - EFREI - M1 BDIA APP

### Rappel des objectifs de ce TP : 
- Créer un repository Github
- Créer un wrapper qui retourne la météo d'un lieu donné avec sa latitude et sa longitude (passées en variable d'environnement) en utilisant openweather API dans le langage deprogrammation de votre choix (bash, python, go, nodejs, etc)
- Packager son code dans une image Docker
- Mettre à disposition son image sur DockerHub
- Mettre à disposition son code dans un repository Github

---

-- Repository GitHub associé à mon TP : 
https://github.com/ArthurA14/docker-devops-td1
-- Image sur DockerHub associé à mon TP : 
https://hub.docker.com/r/antoinearthur/docker-devops-td1-test2

---

### Solutions techniques employées : 
Pour réaliser ce travail, j'ai utilisé le langage de programmation ***Python***. Dans un deuxième temps, lorsqu'il s'agira de requêter une API, j'utiliserai en plus de Python le micro framework dédié ***Flask***.
L'OS que j'utilise est ***Windows 10***, avec le CLI ***WSL2***, de manière à bénéficier de certaines commandes Unix.

---

### Travail réalisé étape par étape : 

### 1.  Installations préliminaires : 
- #### Je commence par créer un répertoire de projet en local, que je nomme *docker-devops-td1*:
````bash
$ cd ../..
$ cd Users/arthu/Efrei/DEVOPS
$ mkdir docker-devops-td1
$ cd docker-devops-td1
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
(myvenv) toto@DESKTOP-OBTCMJQ:/mnt/c/Users/arthu/Efrei/DEVOPS/docker-devops-td1$
````
*A présent, je lancerai toujours de nouvelles commandes à partir de cet environnement virtuel.*

---

### 2 . Création de compte sur openweathermap.org
- #### Je crée un compte sur openweathermap.org.
- #### J'y récupère mon API KEY dans mon espace personnel.
*Pour les besoins de la démonstration, mon API KEY est : ***68e3a32**********

---

### 3.  Test de la Weather API en ligne de commandes : 
- #### Sous WSL2, dans *myvenv*, je tape : 
````bash
$ export APIKEY=68e3a32******
````

- #### Test de l'API KEY à partir de la console : 
````bash
$ curl "http://api.openweathermap.org/data/2.5/weather?q=palermo&appid=$APIKEY"
````

````bash
{"coord":{"lon":13.5833,"lat":37.8167},"weather":[{"id":800,"main":"Clear","description":"clear sky","icon":"01d"}],"base":"stations","main":{"temp":307.34,"feels_like":304.89,"temp_min":301.13,"temp_max":310.26,"pressure":1018,"humidity":14,"sea_level":1018,"grnd_level":960},"visibility":10000,"wind":{"speed":2.69,"deg":357,"gust":3.27},"clouds":{"all":10},"dt":1654422181,"sys":{"type":2,"id":2007649,"country":"IT","sunrise":1654400659,"sunset":1654453456},"timezone":7200,"id":2523918,"name":"Province of Palermo","cod":200}
````
-> *Cette commande me retourne les informations météorologiques de la ville de "Palerme"*.

---

### 4.  Utilisation de la Weather API avec Python : 
- #### Création d'un fichier *prova_api.py* : 
````bash
$ touch prova_api.py
````
- #### Ecriture du code au sein de ce fichier *prova_api.py*:
````python
import  requests
import  os

APIKEY = os.environ['APIKEY'] # reads the environment variable

response = requests.get("http://api.openweathermap.org/data/2.5/weather?q=monaco&appid="+APIKEY)

print(response.status_code)
print(response.json())
````
-> *Ce code me permet de paramétrer l'url que je requête, avec le champ "APIKEY"* . 

- #### Compilation et exécution de mon code : 
````bash
$ python3 prova_api.py
````

````bash
{'coord': {'lon': 7.419, 'lat': 43.7314}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'base': 'stations', 'main': {'temp': 298.08, 'feels_like': 298.8, 'temp_min': 296.03, 'temp_max': 301.56, 'pressure': 1015, 'humidity': 83}, 'visibility': 10000, 'wind': {'speed': 1.54, 'deg': 140}, 'clouds': {'all': 0}, 'dt': 1654423514, 'sys': {'type': 2, 'id': 2006345, 'country': 'MC', 'sunrise': 1654400996, 'sunset': 1654456078}, 'timezone': 7200, 'id': 2993457, 'name': 'Monaco', 'cod': 200}
````
-> *Cette commande, en exécutant le code contenu dans le fichier **prova_api.py**, me retourne les informations météorologiques de la ville de "Monaco", de manière analogue à précédemment*.

---

### 5. Dockerization :
- #### Création d'un fichier *"requirements.txt"* dans le répertoire de projet : 
````bash
$ touch requirements.txt
````
-> *J'y inscrits les dépendances nécessaires; cela aura une utilité pour les appels API ultérieurs :* 
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
-> *Ce fichier me permet d'exécuter les différentes commandes, associées à différents  fichiers, dont j'ai besoin pour créer mon conteneur Docker. Dans ce fichier, j'écris donc les lignes de commandes suivantes :*
````docker
FROM  python:3.8-buster

WORKDIR  /docker-devops-td1  # répertoire de projet à partir duquel je travaille  

COPY  requirements.txt  .  # utilisation des dépendances dont j'aurai éventuellement besoin

RUN  pip  install  -r  requirements.txt  # exécution de ce fichier

COPY  prova_api.py  .  # import du fichier python contenant mon code

EXPOSE  5000  # numéro du port que je vais utiliser sur mon réseau pour créer mon image

CMD  ["python",  "prova_api.py"]  # langage et fichier que je vais utiliser dans mon image Docker 
````

-> *Pour la suite de mon travail, je devrai installer ***Docker Desktop*** et démarrer, afin de pouvoir utiliser la commande *docker* dans WSL2.*

- #### Construction de l'image Docker : 
````bash
$ docker build --tag prova_api .
````

-> *Cette ligne de commande permet de créer l'image **"prova_api"** que je vais utiliser par la suite.*

````bash
[+] Building 0.4s (2/3)
[+] Building 10.5s (11/11) FINISHED
 => [internal] load build definition from Dockerfile                                                                              0.1s
 => => transferring dockerfile: 284B                                                                                              0.0s
 => [internal] load .dockerignore                                                                                                 0.1s
 => => transferring context: 2B                                                                                                   0.0s
 => [internal] load metadata for docker.io/library/python:3.8-buster                                                              2.7s
 => [auth] library/python:pull token for registry-1.docker.io                                                                     0.0s
 => [internal] load build context                                                                                                 0.1s
 => => transferring context: 809B                                                                                                 0.0s
 => [1/5] FROM docker.io/library/python:3.8-buster@sha256:458c39bbb8187420ae4e9bd4d1a889511f5fb5463b7969b47fb4441a244a7de8        0.0s
 => CACHED [2/5] WORKDIR /docker-devops-td1                                                                                       0.0s
 => [3/5] COPY requirements.txt .                                                                                                 0.1s
 => [4/5] RUN pip install -r requirements.txt                                                                                     6.9s
 => [5/5] COPY prova_api.py .                                                                                                     0.1s
 => exporting to image                                                                                                            0.4s
 => => exporting layers                                                                                                           0.4s
 => => writing image sha256:e8085f44367ce217860cc794d071095145993469609ead6dfb9ef5dafca05cdf                                      0.0s
 => => naming to docker.io/library/prova_api                                                                                      0.0s
````

- #### Exécution du conteneur associé : 
````bash
$ docker run -p 5000:5000 --env APIKEY=$APIKEY --rm prova_api
````
*Ou :*
````bash
$ docker run -p 5000:5000 --env APIKEY=68e3a32****** --rm prova_api
````

````bash
{'coord': {'lon': 7.419, 'lat': 43.7314}, 'weather': [{'id': 801, 'main': 'Clouds', 'description': 'few clouds', 'icon': '02d'}], 'base': 'stations', 'main': {'temp': 299.03, 'feels_like': 299.68, 'temp_min': 297.27, 'temp_max': 305.93, 'pressure': 1013, 'humidity': 77}, 'visibility': 10000, 'wind': {'speed': 7.72, 'deg': 210}, 'clouds': {'all': 20}, 'dt': 1654442967, 'sys': {'type': 2, 'id': 2006345, 'country': 'MC', 'sunrise': 1654400996, 'sunset': 1654456078}, 'timezone': 7200, 'id': 2993457, 'name': 'Monaco', 'cod': 200}
````

-> *J'obtiens alors, en local, les informations météorologiques de la ville de "Monaco" (comme précédemment)*  :

---

- #### Modification du code de mon fichier *prova_api.py* pour les besoins ci-dessous : 
````python
import  requests
import  os

APIKEY = os.environ['APIKEY'] # reads the environment variable
LAT = os.environ['LAT']
LONG = os.environ['LONG']

url="https://api.openweathermap.org/data/2.5/weather?lat="+LAT+"&lon="+LONG+"appid="+APIKEY
# print(url)
response = requests.get("https://api.openweathermap.org/data/2.5/weather?lat="+LAT+"&lon="+LONG+"&appid="+APIKEY)

print(response.status_code)
print(response.json())
````

-> *J'ajoute deux paramètres à mon url, "LAT" et "LONG", afin de simuler l'exécution du conteneur Docker, avec une API à laquelle on aurait passé ces deux paramètres supplémentaires (voir ci-dessous).
Pour cela, je me suis inspiré de https://openweathermap.org/current, afin de savoir comment réaliser ce type d'appel.*

-> *Puis, je réalise de nouveau les deux étapes précédentes :* 
- #### Construction de l'image Docker : 
````bash
$ docker build --tag prova_api .
````

- #### Exécution du conteneur associé : 
````bash
$ docker run --env LAT="5.902785" --env LONG="102.754175" --env APIKEY=68e3a32****** --rm prova_api
````

````bash
{'coord': {'lon': 102.7542, 'lat': 5.9028}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04n'}], 'base': 'stations', 'main': {'temp': 300.18, 'feels_like': 302.4, 'temp_min': 300.18, 'temp_max': 300.18, 'pressure': 1009, 'humidity': 74, 'sea_level': 1009, 'grnd_level': 982}, 'visibility': 10000, 'wind': {'speed': 3.36, 'deg': 144, 'gust': 3.63}, 'clouds': {'all': 64}, 'dt': 1654443423, 'sys': {'country': 'MY', 'sunrise': 1654383247, 'sunset': 1654428060}, 'timezone': 28800, 'id': 1736405, 'name': 'Jertih', 'cod': 200}
````

-> *J'obtiens alors, en local, les informations météorologiques de la ville de "Jertih", dont les coordonnées GPS ont été passées dans la commande ci-dessus.*

---

### 6. Utilisation de Docker Hub :

- #### Voir les images que j'ai en local sur ma machine : 
````bash
$ docker images
````

````docker
REPOSITORY                        TAG       IMAGE ID       CREATED          SIZE
<none>                            <none>    827e10ad72c3   23 minutes ago   901MB
prova_api                         latest    e8085f44367c   27 minutes ago   901MB
antoinearthur/docker-devops-td1   latest    e0050a5233b7   2 days ago       900MB
<none>                            <none>    0e241ca26b65   2 days ago       900MB
<none>                            <none>    3cf14830e30c   2 days ago       900MB
...
...
<none>                            <none>    a8ecc594b245   2 days ago       900MB
<none>                            <none>    f090edf6daea   2 days ago       900MB
<none>                            <none>    ff051185534c   2 days ago       901MB
myapi                             latest    423e8d18f1a3   2 days ago       900MB
docker101tutorial                 latest    94b1b9060299   10 months ago    28.2MB
alpine/git                        latest    b8f176fa3f0d   12 months ago    25.1MB
````

-> *J'observe notamment la présence de mon image **"prova_api"**, que j'ai créée ci-dessus. Elle possède un champ **"IMAGE ID"** qui lui est associé.*

--- 

- #### Publier une image sur Docker : 
-- **Connection à Docker sur mon serveur  :**
````bash
$ docker login --username=antoinearthur
````
-> *Je dois entrer mon mot de passe Docker Hub en ligne de commandes.*

-- **Récupération de l'ID de mon image, "IMAGE ID" :**
````bash
$ docker images
````

````bash
REPOSITORY                        TAG       IMAGE ID       CREATED          SIZE
<none>                            <none>    827e10ad72c3   23 minutes ago   901MB
prova_api                         latest    e8085f44367c   27 minutes ago   901MB
...
...
````

-> *Je récupère l'**"IMAGE ID"** associée à mon image **"prova_api"** :  *e8085f44367c* .*

-- **J'associe un tag à cet "IMAGE ID", afin de l'identifier plus aisément :**
````bash
$ docker tag e8085f44367c antoinearthur/docker-devops-td1-test2
````

````bash
$ docker images
````

````docker
REPOSITORY                              TAG       IMAGE ID       CREATED          SIZE
<none>                                  <none>    827e10ad72c3   47 minutes ago   901MB
antoinearthur/docker-devops-td1-test2   latest    e8085f44367c   50 minutes ago   901MB
docker101                               0.0.1     e8085f44367c   50 minutes ago   901MB
prova_api                               latest    e8085f44367c   50 minutes ago   901MB
antoinearthur/docker-devops-td1         latest    e0050a5233b7   2 days ago       900MB
<none>                            <none>    0e241ca26b65   2 days ago       900MB
<none>                            <none>    3cf14830e30c   2 days ago       900MB
...
...
<none>                            <none>    a8ecc594b245   2 days ago       900MB
<none>                            <none>    f090edf6daea   2 days ago       900MB
<none>                            <none>    ff051185534c   2 days ago       901MB
myapi                             latest    423e8d18f1a3   2 days ago       900MB
docker101tutorial                 latest    94b1b9060299   10 months ago    28.2MB
alpine/git                        latest    b8f176fa3f0d   12 months ago    25.1MB
````

-> *J'observe notamment la présence de mon tag **"antoinearthur/docker-devops-td1-test2"** associé à mon "IMAGE ID" e8085f44367c, que je viens de créer.*

-- **J'envoie mon image sur Docker Hub :**
````bash
$ docker push antoinearthur/docker-devops-td1-test2
````

````bash
Using default tag: latest
The push refers to repository [docker.io/antoinearthur/docker-devops-td1-test2]
f881c774572b: Pushed
fa1e370b3434: Pushed
d10d11cf02c5: Pushed
d604133a5fd4: Mounted from antoinearthur/docker-devops-td1
02cad1c8915d: Mounted from antoinearthur/docker-devops-td1
9a89b1afab15: Mounted from antoinearthur/docker-devops-td1
f319aadc2fd6: Mounted from antoinearthur/docker-devops-td1
b2870792ee2d: Mounted from antoinearthur/docker-devops-td1
5d1a42aa54a1: Mounted from antoinearthur/docker-devops-td1
80d46995af06: Mounted from antoinearthur/docker-devops-td1
597ea5af36e6: Mounted from antoinearthur/docker-devops-td1
8f534d0617ce: Mounted from antoinearthur/docker-devops-td1
f14da82c36e2: Mounted from antoinearthur/docker-devops-td1
latest: digest: sha256:3413987e3f6d6a4e92571a70bf9a22a9b01b9ff0b4c26177c6e836243bfd28b4 size: 3049
````

-> *Mon image, taguée avec  docker-devops-td1-test2, est uploadée sur Docker Hub, à l'adresse suivante : https://hub.docker.com/r/antoinearthur/docker-devops-td1-test2*
-> *Une fois le transfert terminé, n'importe qui peut réutiliser mon image (voir commande ci-dessous).*

-- **Récupération de mon image sur Docker Hub :**
````bash
$ docker run --env LAT="5.902785" --env LONG="102.754175" --env APIKEY=68e3a32****** antoinearthur/docker-devops-td1-test2 
````

````bash
{'coord': {'lon': 102.7542, 'lat': 5.9028}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04n'}], 'base': 'stations', 'main': {'temp': 300.18, 'feels_like': 302.4, 'temp_min': 300.18, 'temp_max': 300.18, 'pressure': 1009, 'humidity': 74, 'sea_level': 1009, 'grnd_level': 982}, 'visibility': 10000, 'wind': {'speed': 3.36, 'deg': 144, 'gust': 3.63}, 'clouds': {'all': 64}, 'dt': 1654446279, 'sys': {'country': 'MY', 'sunrise': 1654469654, 'sunset': 1654514474}, 'timezone': 28800, 'id': 1736405, 'name': 'Jertih', 'cod': 200}         
````
