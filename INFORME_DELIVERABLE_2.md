# Informe del projecte — FotLiYa (Lliurament 2)

**Autors:** Agustí Prat Creus, Clara Escuer Roure, Maxim Nicolaev Popovici i Anna Morón Rauret

---

## 1. Adreça pública del repositori

https://github.com/AgustiPrat/FotLiYa.git

---

## 2. Resum del lliurament

Aquest segon lliurament amplia FotLiYa amb funcionalitats pròpies d'una aplicació web més completa, dinàmica i orientada a la participació dels usuaris. A diferència de la primera entrega, centrada en la base funcional del joc, aquesta segona fase incorpora:

- Un sistema de propostes de preguntes pels usuaris
- Moderació administrativa
- Una integració real amb una API externa
- Una base de dades més madura i preparada per escalar

L'objectiu principal ha estat transformar l'aplicació en un sistema web més interactiu, on els usuaris no només consumeixen contingut, sinó que també poden proposar preguntes pròpies i gestionar-les des del seu espai personal.

---

## 3. Noves funcionalitats

### Sistema de propostes de preguntes (`ProposedQuestion`)

S'ha incorporat el model `ProposedQuestion`, que permet als usuaris registrats proposar preguntes pròpies amb un estat de validació. El sistema inclou funcionalitats completes de CRUD:

- **Crear** preguntes noves
- **Editar** preguntes pròpies (només en estat pendent)
- **Eliminar** preguntes pròpies (només en estat pendent)

Tot amb control d'accés mitjançant autenticació, garantint la coherència del flux de moderació.

### Panell d'administració propi

S'ha desenvolupat una vista d'administració pròpia dins de l'aplicació, pensada per a usuaris amb permisos d'*staff*. Des d'aquest panell, l'administrador pot:

- Veure les preguntes pendents de revisió
- Aprovar-les (es converteixen en preguntes reals del sistema via el model `Question`)
- Rebutjar-les amb una nota explicativa

Un *context processor* mostra dinàmicament el nombre de preguntes pendents per facilitar la gestió.

### Integració amb l'API externa (FastAPI)

S'ha integrat una API externa separada mitjançant un microservei FastAPI. Aquesta API:

- Llegeix dades des de fitxers CSV
- Exposa endpoints per retornar contingut aleatori (paraules, temes, llocs, preguntes picants, dinàmiques de joc)

Des de Django, es consumeix a través del fitxer `api_client.py`, que genera partides aleatòries i substitueix els placeholders del contingut (`{player}`, `{number_1_5}`, `{random_place}`...) amb dades reals o noms dels jugadors.

---

## 4. Model de dades

### Canvis respecte al Deliverable 1

#### `GameSession`
S'han afegit els camps següents:

| Camp | Tipus | Descripció |
|------|-------|------------|
| `duration_seconds` | `IntegerField` (nullable) | Durada total de la partida en segons |
| `ended` | `BooleanField` | Indica si la partida ha finalitzat |
| `game_type` | `CharField(50)` | Tipus de joc (per defecte `"classic"`) |
| `notes` | `TextField` | Notes lliures associades a la sessió |

#### `Player`
S'han afegit els camps següents:

| Camp | Tipus | Descripció |
|------|-------|------------|
| `avatar` | `CharField(50)` | Identificador de l'avatar del jugador |
| `color` | `CharField(20)` | Color associat al jugador per a la UI |

#### `Question`
S'ha canviat `text` de `CharField(255)` a `TextField` per suportar preguntes més llargues. S'ha afegit:

| Camp | Tipus | Descripció |
|------|-------|------------|
| `source` | `CharField(20)` | Origen de la pregunta: `manual`, `api` o `proposed` |

#### `Answer`
S'ha afegit el camp:

| Camp | Tipus | Descripció |
|------|-------|------------|
| `created_at` | `DateTimeField` | Marca de temps de quan es va respondre |

### Model nou: `ProposedQuestion`

Gestiona el cicle de vida de les preguntes proposades pels usuaris fins a la seva aprovació o rebuig.

| Camp | Tipus | Descripció |
|------|-------|------------|
| `text` | `TextField` | Text de la pregunta proposada |
| `category` | `CharField(100)` | Categoria de la pregunta (indexat) |
| `mechanics` | `CharField(100)` | Mecànica de joc associada (opcional) |
| `created_by` | `ForeignKey(User)` | Usuari que ha proposat la pregunta |
| `created_at` | `DateTimeField` | Data de creació (indexat) |
| `status` | `CharField(10)` | Estat: `pending`, `approved` o `rejected` (indexat) |
| `admin_note` | `TextField` | Nota de l'administrador en cas de rebuig |

---

## 5. Millores visuals i estructurals

Totes les noves vistes s'integren amb la mateixa base visual del projecte, mantenint coherència en l'estètica i en l'experiència d'usuari:

- Les pàgines de gestió de preguntes, l'administració i el joc comparteixen una estructura comuna
- S'utilitza una plantilla base comuna per mantenir un disseny homogeni
- El disseny segueix sent minimalista i adaptat a mòbil (fons fosc, cards, chips per als jugadors)

---

## 6. Decisions de disseny

### Arquitectura general

L'arquitectura continua basant-se en dos serveis orquestrats amb Docker Compose:

- **API** (FastAPI): serveix les dades aleatòries del joc a partir de fitxers CSV. Servei independent i sense estat.
- **Web** (Django): gestiona la interfície d'usuari, l'autenticació, les sessions de joc, la moderació i la base de dades.

Aquesta separació fa el projecte més modular i escalable, permetent que cada servei evolucioni de forma independent.

### Flux de moderació de preguntes

El model `ProposedQuestion` implementa un sistema d'estats (`pending` → `approved` / `rejected`) que garanteix la qualitat del contingut del joc:

- Quan un usuari crea una pregunta, queda en estat `pending`.
- L'administrador pot **aprovar-la**: es crea automàticament una entrada al model `Question` amb `source="proposed"` i la pregunta entra al joc.
- L'administrador pot **rebutjar-la**: s'emmagatzema el motiu al camp `admin_note` per informar l'usuari.
- Un usuari només pot **editar o eliminar** les seves pròpies preguntes i únicament si encara estan en estat `pending`. Intentar fer-ho sobre una pregunta d'un altre usuari retorna un `404`.

### Control d'accés

S'han seguit dos mecanismes diferenciats:

- **Vistes d'usuari** (`question_create`, `question_edit`, `question_delete`, `question_list`): protegides amb el decorator `@login_required` de Django.
- **Vistes d'administrador** (`admin_question_list`, `approve_question`, `reject_question`): protegides amb comprovació manual de `request.user.is_staff`, retornant un redirect al login si no es compleix. Es va optar per comprovació manual en lloc de `@staff_member_required` per tenir control total sobre el comportament del redirect.

### Suggeriments de categoria amb jQuery (sense API externa)

El formulari de creació/edició de preguntes incorpora un sistema de suggeriments de categories implementat amb **jQuery**. Quan l'usuari escriu al camp de categoria, es filtren en temps real les coincidències d'una llista predefinida de categories i es mostren com a *chips* clicables. Es va optar per una llista local en lloc de cridar una API externa (com Datamuse) per garantir la disponibilitat sense dependre de serveis de tercers i evitar latència innecessària.

### 12factor

Es mantenen les decisions del primer lliurament i s'hi afegeix:

- **Processos sense estat**: cap vista guarda estat en memòria; tot el flux de joc passa per `request.session` o la base de dades.
- **Logs**: els serveis continuen escrivint per stdout/stderr, recollits per Docker.

---

## 7. Divisió de la feina

Les notes haurien de ser iguals entre tots els membres del grup. La feina s'ha repartit de la manera següent:

| Membre  | Àrea | Tasques principals |
|---------|------|--------------------|
| Agustí  | Backend Django — CRUD | Model `ProposedQuestion`, vistes crear/editar/eliminar, seguretat d'accés |
| Maxim   | Backend Django — Admin + Tests | Vista d'administrador, tests E2E amb Behave+Splinter, millores als models |
| Clara   | Frontend + AJAX | Templates del CRUD, integració jQuery amb API externa, millores visuals |
| Anna    | Base de dades + Frontend | Revisió i millora de la BD, templates del panell admin, estils generals i document d'entrega |

---

## 8. Com executar l'aplicació

### Requisits

- Docker
- Docker Compose

### Passos

```bash
# 1. Clonar el repositori
git clone https://github.com/AgustiPrat/FotLiYa
cd FotLiYa

# 2. Aixecar els contenidors
docker-compose up --build

# 3. Accedir a l'aplicació
# http://localhost:8080
```

### Accés

| Recurs | URL |
|--------|-----|
| Aplicació web | http://localhost:8080 |
| Panell d'administració de preguntes | http://localhost:8080/admin-panel/questions/ |
| Panell d'administració Django | http://localhost:8080/admin/ |

### Credencials dels usuaris de prova

La base de dades `db.sqlite3` està inclosa al repositori per facilitar les proves sense necessitat de configuració addicional.

| Usuari | Contrasenya | Rol |
|--------|-------------|-----|
| `admin` | `admin-fotliya4` | Administrador (accés al panell d'admin i moderació) |
| `Test` | `1234test1234` | Usuari registrat (pot proposar i gestionar preguntes pròpies) |
| `Test1` | `1234test11234` | Usuari registrat (pot proposar i gestionar preguntes pròpies) |
