import random
import csv
from pathlib import Path

# Ruta a la carpeta data/ on hi ha els CSVs
DATA_DIR = Path(__file__).resolve().parent.parent / "api" / "data"


def _load_csv(filename):
    path = DATA_DIR / filename
    if not path.exists():
        return []
    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return [row for row in reader]


def _get_random_row(filename, field):
    rows = _load_csv(filename)
    if not rows:
        return "?"
    return random.choice(rows).get(field, "?") or "?"


def _resolve_placeholders(body, placeholders_used, players):
    if not body:
        return body

    if players:
        shuffled = players[:]
        random.shuffle(shuffled)
        body = body.replace("{player}", shuffled[0])
        body = body.replace("{player2}", shuffled[1] if len(shuffled) > 1 else shuffled[0])
        body = body.replace("{chosen_player}", random.choice(players))
        body = body.replace("{most_voted}", random.choice(players))

    body = body.replace("{number_1_3}", str(random.randint(1, 3)))
    body = body.replace("{number_1_5}", str(random.randint(1, 5)))
    body = body.replace("{timer_10}", "10 segons")
    body = body.replace("{timer_30}", "30 segons")

    if "{word}" in body:
        body = body.replace("{word}", _get_random_row("word.csv", "object"))
    if "{theme}" in body:
        body = body.replace("{theme}", _get_random_row("theme.csv", "theme"))
    if "{random_place}" in body:
        body = body.replace("{random_place}", _get_random_row("place.csv", "place"))
    if "{random_likely_to}" in body:
        body = body.replace("{random_likely_to}", _get_random_row("likely_to.csv", "most_likely_to"))
    if "{random_red_flag}" in body:
        body = body.replace("{random_red_flag}", _get_random_row("red_flag.csv", "red_flag"))
    if "{random_object}" in body:
        body = body.replace("{random_object}", _get_random_row("word.csv", "object"))
    if "{spicy_question}" in body:
        body = body.replace("{spicy_question}", _get_random_row("spicy_questions.csv", "spicy_questions"))
    if "{random_question}" in body:
        body = body.replace("{random_question}", _get_random_row("random_questions.csv", "random_questions"))

    return body


def get_random_game(players):
    try:
        # 60% jocs normals, 20% preguntes random, 20% preguntes picants
        rand = random.random()

        if rand < 0.6:
            games = _load_csv("games.csv")
            if games:
                game = random.choice(games)
                title = game.get("title") or "Pregunta"
                body = game.get("body") or ""
                placeholders_used = game.get("placeholders_used") or ""
                body = _resolve_placeholders(body, placeholders_used, players)
                return {"title": title, "body": body}

        elif rand < 0.8:
            questions = _load_csv("random_questions.csv")
            if questions:
                q = random.choice(questions)
                return {"title": "Pregunta", "body": q.get("random_questions", "")}

        else:
            spicy = _load_csv("spicy_questions.csv")
            if spicy:
                q = random.choice(spicy)
                return {"title": "Pregunta Picant 🌶️", "body": q.get("spicy_questions", "")}

        return {
            "title": "Pregunta",
            "body": "🔥 Quin és el teu gènere musical per escalfar la prèvia?"
        }

    except Exception:
        return {
            "title": "Pregunta",
            "body": "🔥 Quin és el teu gènere musical per escalfar la prèvia?"
        }