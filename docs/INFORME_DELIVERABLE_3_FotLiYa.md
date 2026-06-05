# Informe del projecte — FotLiYa (Lliurament 3)

**Autors:** Agustí Prat Creus, Clara Escuer Roure, Maxim Nicolaev Popovici i Anna Morón Rauret

---

## 1. Adreça pública del repositori

https://github.com/AgustiPrat/FotLiYa.git

---

## 2. Resum del lliurament

Aquest tercer i últim lliurament converteix FotLiYa en una aplicació Web 3.0 mitjançant la incorporació de marcat semàntic RDFa amb schema.org. A més, s'ha aprofitat per polir l'aspecte visual, millorar la base de dades de preguntes i afegir millores generals al projecte.

Les millores principals d'aquesta entrega són:

- Marcat semàntic RDFa amb schema.org a la pàgina de detall de pregunta
- Millora del flux del joc i la base de dades de preguntes
- Poliment visual general: pàgina de joc, home i responsive
- Millores generals: pàgina 404 personalitzada, perfil d'usuari i navbar millorat

---

## 3. RDFa implementat — Per què `Question` de schema.org

S'ha triat el tipus `Question` de schema.org per marcar semànticament les pàgines de detall de les preguntes proposades (`ProposedQuestion`), ja que és el tipus que millor s'ajusta a la naturalesa del contingut: textos en forma de pregunta creats per usuaris, amb categoria, autor i data de creació.

Els camps marcats amb RDFa són:

| Propietat RDFa | Camp del model | Descripció |
|----------------|----------------|------------|
| `name` | `question.text` | Text de la pregunta |
| `about` | `question.category` | Categoria de la pregunta |
| `author` → `Person` → `name` | `question.created_by.username` | Autor de la pregunta |
| `dateCreated` | `question.created_at` | Data de creació |

Exemple del marcat aplicat a la template:

```html
<div class="card" vocab="https://schema.org/" typeof="Question">
  <h2 property="name">{{ question.text }}</h2>
  <span property="about">{{ question.category }}</span>
  <div property="author" typeof="Person">
    <span property="name">{{ question.created_by.username }}</span>
  </div>
  <p property="dateCreated">{{ question.created_at|date:"Y-m-d" }}</p>
</div>
```

---

## 4. Captura del validator schema.org

> ⚠️ **Nota:** Cal afegir aquí la captura de pantalla de https://validator.schema.org amb el resultat correcte del marcat RDFa de la pàgina de detall.

---

## 5. Noves funcionalitats

### Pàgina de detall de pregunta amb RDFa (Agustí)

S'ha creat una pàgina de detall per a cada `ProposedQuestion` accessible des de la llista de preguntes de l'usuari. La pàgina inclou marcat semàntic RDFa complet amb schema.org, verificat amb el validator oficial.

### Millores al joc i base de dades de preguntes (Maxim)

- S'han afegit més de 20 preguntes noves als CSVs de preguntes aleatòries i picants
- S'ha millorat el flux del joc mostrant de forma destacada el jugador actiu a cada ronda
- S'ha afegit un comptador de rondes visible durant la partida
- S'ha creat la pàgina d'estadístiques (`/stats/`) per a usuaris autenticats, que mostra les partides jugades, els jugadors i la data de cada partida

### Poliment visual i UX (Clara)

- S'ha millorat el disseny de la targeta de pregunta a `game.html`
- S'ha afegit una animació CSS en canviar de pregunta
- S'han millorat els botons de "Següent" i "Finalitzar"
- S'ha afegit una secció d'explicació del joc amb les regles bàsiques a `home.html`
- S'han revisat totes les pàgines per garantir la correcta visualització en mòbil
- S'ha assegurat la coherència visual entre totes les pàgines, incloent la nova pàgina de detall

### Millores generals (Anna)

- **Pàgina 404 personalitzada**: s'ha creat `404.html` amb el disseny propi de FotLiYa i s'ha configurat el `handler404` al `settings.py`
- **Pàgina de perfil d'usuari** (`/profile/`): mostra el nom d'usuari, les preguntes proposades (total, aprovades i pendents) i l'historial de partides jugades amb els jugadors de cada sessió
- **Navbar millorat**: el nom d'usuari ara és un enllaç directe al perfil, s'ha afegit un botó "Jugar" i s'han revisat tots els enllaços
- **Fix `api_client.py`**: s'ha corregit la integració amb l'API de joc per llegir correctament els CSVs locals quan el servidor FastAPI no està disponible

---

## 6. Canvis al model respecte al Deliverable 2

En aquest lliurament no s'han fet canvis al model de dades. Els models `GameSession`, `Player`, `Question`, `Answer` i `ProposedQuestion` es mantenen igual que al Deliverable 2. Les millores s'han centrat en la capa de presentació, la semàntica web i l'experiència d'usuari.

---

## 7. Decisions de disseny

### Elecció de `Question` com a tipus schema.org

Es va valorar usar `CreativeWork` o `Comment`, però `Question` és el tipus més específic i semànticament correcte per a preguntes de text creades per usuaris. A més, schema.org defineix `Question` com a subclasse de `CreativeWork`, la qual cosa permet heretar propietats com `author` i `dateCreated` de forma estàndard.

### Pàgina de perfil com a punt central de l'usuari

Es va decidir fer que el nom d'usuari al navbar fos directament clicable i portés al perfil, en lloc d'afegir un enllaç separat. Això redueix la sobrecàrrega visual del navbar i és el patró esperat pels usuaris en aplicacions web modernes.

### Pàgina 404 integrada amb el disseny general

La pàgina 404 hereta de `base.html` i manté el mateix fons, tipografia i estil visual que la resta de l'aplicació. Això reforça la identitat de marca fins i tot en situacions d'error, a diferència de les pàgines d'error genèriques de Django.

### Fix de l'`api_client.py`

L'arquitectura original depenia d'un servidor FastAPI extern que havia d'estar arrencat per separat. Per garantir que el joc funcioni en qualsevol entorn sense configuració addicional, s'ha reescrit l'`api_client.py` per llegir els CSVs directament des del sistema de fitxers, mantenint tota la lògica de substitució de placeholders (`{player}`, `{number_1_3}`, `{word}`, etc.).

### 12factor

Es mantenen les decisions dels lliuraments anteriors. Les noves vistes (`profile`, `error_404`) no guarden estat en memòria i segueixen el patró de la resta de l'aplicació.

---

## 8. Divisió de la feina

Les notes haurien de ser iguals entre tots els membres del grup. La feina s'ha repartit de la manera següent:

| Membre | Àrea | Tasques principals |
|--------|------|--------------------|
| Agustí | Web 3.0 — RDFa | Pàgina de detall de `ProposedQuestion`, marcat semàntic schema.org, verificació amb validator |
| Maxim | Joc + BD preguntes | Millora del flux del joc, afegir preguntes als CSVs, pàgina d'estadístiques |
| Clara | Visual i UX | Polir `game.html` i `home.html`, animacions CSS, responsive i coherència visual |
| Anna | Millores generals | Pàgina 404, pàgina de perfil d'usuari, millores al navbar, fix `api_client.py`, document d'entrega |

---

## 9. Com executar l'aplicació

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
| Perfil d'usuari | http://localhost:8080/profile/ |
| Estadístiques | http://localhost:8080/stats/ |
| Detall de pregunta | http://localhost:8080/questions/\<id\>/ |
| Panell d'administració de preguntes | http://localhost:8080/admin-panel/questions/ |
| Panell d'administració Django | http://localhost:8080/admin/ |

### Credencials dels usuaris de prova

La base de dades `db.sqlite3` està inclosa al repositori per facilitar les proves sense necessitat de configuració addicional.

| Usuari | Contrasenya | Rol |
|--------|-------------|-----|
| `admin` | `admin-fotliya4` | Administrador (accés al panell d'admin i moderació) |
| `Test` | `1234test1234` | Usuari registrat (pot proposar i gestionar preguntes pròpies) |
| `Test1` | `1234test11234` | Usuari registrat (pot proposar i gestionar preguntes pròpies) |
