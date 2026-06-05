import random
import os
import requests

API_URL = os.environ.get("API_URL", "http://api:8000")


def _get(endpoint):
    try:
        response = requests.get(f"{API_URL}{endpoint}", timeout=3)
        response.raise_for_status()
        return response.json()
    except Exception:
        return None


def get_random_game(players):
    try:
        rand = random.random()

        if rand < 0.6:
            data = _get("/games/random")
            if data:
                body = data.get("body") or ""
                body = _resolve_placeholders(body, players)
                return {"title": data.get("title") or "Pregunta", "body": body}

        elif rand < 0.8:
            data = _get("/question/random")
            if data:
                return {"title": "Pregunta", "body": data.get("random_questions", "")}

        else:
            data = _get("/spicy_question/random")
            if data:
                return {"title": "Pregunta Picant 🌶️", "body": data.get("spicy_questions", "")}

        return {
            "title": "Pregunta",
            "body": "🔥 Quin és el teu gènere musical per escalfar la prèvia?"
        }

    except Exception:
        return {
            "title": "Pregunta",
            "body": "🔥 Quin és el teu gènere musical per escalfar la prèvia?"
        }


def _resolve_placeholders(body, players):
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

    # Placeholders que necessiten cridar l'API
    if "{word}" in body:
        data = _get("/word/random")
        body = body.replace("{word}", data.get("object", "?") if data else "?")
    if "{theme}" in body:
        data = _get("/theme/random")
        body = body.replace("{theme}", data.get("theme", "?") if data else "?")
    if "{random_place}" in body:
        data = _get("/place/random")
        body = body.replace("{random_place}", data.get("place", "?") if data else "?")
    if "{random_likely_to}" in body:
        data = _get("/likely_to/random")
        body = body.replace("{random_likely_to}", data.get("most_likely_to", "?") if data else "?")
    if "{random_red_flag}" in body:
        data = _get("/red_flag/random")
        body = body.replace("{random_red_flag}", data.get("red_flag", "?") if data else "?")
    if "{random_object}" in body:
        data = _get("/word/random")
        body = body.replace("{random_object}", data.get("object", "?") if data else "?")
    if "{spicy_question}" in body:
        data = _get("/spicy_question/random")
        body = body.replace("{spicy_question}", data.get("spicy_questions", "?") if data else "?")
    if "{random_question}" in body:
        data = _get("/question/random")
        body = body.replace("{random_question}", data.get("random_questions", "?") if data else "?")

    return body