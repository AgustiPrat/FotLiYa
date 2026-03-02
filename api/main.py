import pandas as pd 
from fastapi import FastAPI
from typing import List

import models as md
app = FastAPI(title="FotLi Ya!")

games_df = pd.read_csv("data/games.csv")
#categories_df = pd.read_csv("data/categories.csv")
#mechanics_df = pd.read_csv("data/mechanics.csv")
category_df = pd.read_csv("data/category.csv")
random_place_df = pd.read_csv("data/random_place.csv")
likely_to_df = pd.read_csv("data/likely_to.csv")
red_flag_df = pd.read_csv("data/red_flag.csv")
word_df = pd.read_csv("data/word.csv")

@app.get("/")
def get_root():
    return {
        "message" : "Welcome to the FLY API!"
    }

@app.get("/metadata")

@app.get("/place", response_model= List[md.Place])
def get_all_places() -> List[md.Place]:
    return[
        md.Place(**row)
        for _, row in random_place_df.iterrows()
    ]

@app.get("/place/random", response_model = md.Place)
def get_random_place() -> md.Place:
    row = random_place_df.sample(1).iloc[0]
    return md.Place(**row)

@app.get("/category", response_model = List[md.Category])
def get_all_categories() -> List[md.Category]:
    return [md.Category(**row) for _, row in category_df.iterrows()]

@app.get("/category/random", response_model = md.Category)
def get_random_category() -> md.Category:
    return md.Category(**category_df.sample(1).iloc[0])

@app.get("/likely_to", response_model = List[md.LikelyTo])
def get_all_likely_to() -> List[md.LikelyTo]:
    return [md.LikelyTo(**row) for _, row in likely_to_df.iterrows()]

@app.get("/likely_to/random", response_model = md.LikelyTo)
def get_random_likely_to() -> md.LikelyTo:
    return md.LikelyTo(**likely_to_df.sample(1).iloc[0])

@app.get("/red_flag", response_model = List[md.RedFlag])
def get_all_red_flags() -> List[md.RedFlag]:
    return [md.RedFlag(**row) for _, row in red_flag_df.iterrows()]

@app.get("/red_flag/random", response_model = md.RedFlag)
def get_random_red_flag() -> md.RedFlag:
    row = red_flag_df.sample(1).iloc[0]
    return md.RedFlag(**row)

@app.get("/word", response_model = List[md.Word])
def get_all_words() -> List[md.Word]:
    return [md.Word(**row) for _, row in word_df.iterrows()]

@app.get("/word/random", response_model = md.Word)
def get_random_word() -> md.Word:
    return md.Word(**word_df.sample(1).iloc[0])

@app.get("/games", response_model = List[md.Game])
def get_all_games() -> List[md.Game]:
    return [
        md.Game(**row)
        for _, row in games_df.iterrows()
    ]

@app.get("/games/random", response_model = md.Game)
def get_random_game() -> md.Game:
    row = games_df.sample(1).iloc[0]
    id = row["id"]
    title = row["title"] if row["title"] is not pd.NA else None
    body = row["body"] if row["body"] is not pd.NA else None
    category_id = row["category_id"] if row["category_id"] is not pd.NA else None
    mechanic_id = row["mechanic_id"] if row["mechanic_id"] is not pd.NA else None
    uses_player_names = row["uses_player_names"] if row["player_names"] is not pd.NA else None
    placeholders_used = row["placeholders_used"] if row["placeholders_used"] is not pd.NA else None
    print(games_df.sample(1).iloc[0])
    return md.Game(id=id,title=title, body=body, category_id=category_id, mechanic_id=mechanic_id, uses_player_names=uses_player_names, placeholders_used=placeholders_used)
    