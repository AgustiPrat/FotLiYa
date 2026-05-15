import os
import random
import requests

API_URL = os.environ.get("API_URL", "http://localhost:8000")

def _fetch(endpoint):
    r = requests.get(f"{API_URL}{endpoint}", timeout=3)
    r.raise_for_status()
    return r.json()

def _placeholder_resolvers(players):
    shuffled = players[:]
    random.shuffle(shuffled)

    return {
        "{player}":            lambda: shuffled[0] if shuffled else "?",
        "{player2}":           lambda: shuffled[1] if len(shuffled) > 1 else "?",
        "{chosen_player}":     lambda: random.choice(players) if players else "?",
        "{most_voted}":        lambda: random.choice(players) if players else "?",
        "{number_1_3}":        lambda: str(random.randint(1, 3)),
        "{number_1_5}":        lambda: str(random.randint(1, 5)),
        "{timer_10}":          lambda: "10 segons",
        "{timer_30}":          lambda: "30 segons",
        "{word}":              lambda: _fetch("/word/random").get("object", "?"),
        "{theme}":             lambda: _fetch("/theme/random").get("theme", "?"),
        "{random_place}":      lambda: _fetch("/place/random").get("place", "?"),
        "{random_likely_to}":  lambda: _fetch("/likely_to/random").get("most_likely_to", "?"),
        "{random_red_flag}":   lambda: _fetch("/red_flag/random").get("red_flag", "?"),
        "{random_object}":     lambda: _fetch("/word/random").get("object", "?"),
        "{spicy_question}":    lambda: _fetch("/spicy_question/random").get("spicy_questions", "?"),
        "{random_question}":   lambda: _fetch("/question/random").get("random_questions", "?"),
    }

def get_random_game(players):
    try:
        game = _fetch("/games/random")
        body = game.get("body", "")
        placeholders_used = game.get("placeholders_used") or ""
        resolvers = _placeholder_resolvers(players)

        for placeholder in placeholders_used.split(","):
            placeholder = placeholder.strip()
            if placeholder in resolvers:
                body = body.replace(placeholder, resolvers[placeholder]())

        return {"title": game.get("title", ""), "body": body}

    except Exception as e:
        return {"title": "Error", "body": f"No s'ha pogut connectar amb l'API: {e}"}