# Documentació del projecte — FotLiYa

## 1. Adreça pública del repositori

https://github.com/AgustiPrat/FotLiYa

---

## 2. Decisions de disseny

### Arquitectura general

El projecte està dividit en dos serveis orquestrats amb Docker Compose:

- **API** (FastAPI): serveix les dades del joc (preguntes, paraules, llocs, red flags...) a partir de fitxers CSV. És un servei independent i sense estat.
- **Web** (Django): gestiona la interfície d'usuari, l'autenticació, les sessions de joc i la base de dades.

Aquesta separació segueix el principi de responsabilitat única i permet que cada servei evolucioni de forma independent.

### Model de dades

El model Django conté 4 entitats relacionades:

- `GameSession`: representa una partida. Pot estar associada a un usuari autenticat o ser anònima.
- `Player`: jugador dins d'una sessió. Relacionat amb `GameSession` mitjançant clau forana.
- `Question`: pregunta emmagatzemada a la base de dades Django (independent de l'API).
- `Answer`: resposta d'un jugador a una pregunta dins d'una sessió.

### Connexió amb l'API

La vista `game` de Django crida l'API FastAPI per obtenir una pregunta aleatòria (`/games/random`). Els placeholders de la pregunta (com `{player}`, `{number_1_5}`, `{random_place}`...) s'omplen dinàmicament al mòdul `api_client.py`, que utilitza el camp `placeholders_used` de cada joc per saber exactament quins endpoints cal cridar.

### Autenticació

S'utilitza el sistema d'autenticació integrat de Django (`django.contrib.auth`). Les partides poden ser jugades tant per usuaris autenticats com anònims.

### Interfície d'usuari

El disseny és minimalista i adaptat a un joc de festa (fons fosc, cards, chips per als jugadors). S'ha prioritzat la usabilitat en mòbil.

### 12factor

- **Configuració per variables d'entorn**: la URL de l'API s'injecta via `API_URL` al `docker-compose.yml`.
- **Serveis com a recursos adjunts**: l'API és un servei extern consumit per la web via HTTP.
- **Processos sense estat**: Django no guarda estat en memòria; tot passa per la sessió o la base de dades.
- **Logs**: els serveis escriuen per stdout/stderr, recollits per Docker.

---

## 3. Divisió de la feina i notes de qualificació

Les notes haurien de ser iguals entre tots els membres del grup. La feina s'ha repartit de la següent manera:

| Membre  | Rol principal |
|---------|--------------|
| Anna    | Frontend (templates HTML, CSS, disseny UI) i lògica Django (vistes, formularis) |
| Clara   | Frontend (templates HTML, CSS, disseny UI) i lògica Django (vistes, formularis) |
| Nico    | Backend (API FastAPI, model de dades, base de dades) i dockerització |
| Agustí  | Backend (API FastAPI, model de dades, base de dades) i dockerització |

---

## 4. Com executar l'aplicació

### Requisits

- Docker
- Docker Compose

### Passos

```bash
# 1. Clonar el repositori
git clone https://github.com/AgustiPrat/FotLiYa.git
cd FotLiYa

# 2. Aixecar els contenidors
docker compose up --build

# 3. Aplicar les migracions (primer cop)
docker compose exec web uv run manage.py migrate

# 4. (Opcional) Crear un superusuari per accedir a l'admin
docker compose exec web uv run manage.py createsuperuser
```

### Accés

- Aplicació web: http://localhost:8080
- API: http://localhost:8000
- Admin Django: http://localhost:8080/admin
