import pandas as pd
import numpy as np
from fastapi import FastAPI
from typing import List

import models as md
app = FastAPI(title="FotLi Ya!")

games_df = pd.read_csv("data/games.csv").replace({np.nan: None})
#categories_df = pd.read_csv("data/categories.csv").replace({np.nan: None})
#mechanics_df = pd.read_csv("data/mechanics.csv").replace({np.nan: None})
theme_df = pd.read_csv("data/theme.csv").replace({np.nan: None})
place_df = pd.read_csv("data/place.csv").replace({np.nan: None})
likely_to_df = pd.read_csv("data/likely_to.csv").replace({np.nan: None})
red_flag_df = pd.read_csv("data/red_flag.csv").replace({np.nan: None})
word_df = pd.read_csv("data/word.csv").replace({np.nan: None})
spicy_questions_df = pd.read_csv("data/spicy_questions.csv").replace({np.nan: None})
questions_df = pd.read_csv("data/random_questions.csv").replace({np.nan: None})

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
        for _, row in place_df.iterrows()
    ]

@app.get("/place/random", response_model = md.Place)
def get_random_place() -> md.Place:
    row = place_df.sample(1).iloc[0]
    return md.Place(**row)

@app.get("/theme", response_model = List[md.Theme])
def get_all_categories() -> List[md.Theme]:
    return [md.Theme(**row) for _, row in theme_df.iterrows()]

@app.get("/theme/random", response_model = md.Theme)
def get_random_category() -> md.Theme:
    return md.Theme(**theme_df.sample(1).iloc[0])

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

@app.get("/questions", response_model = List[md.Question])
def get_all_questions() -> List[md.Question]:
    return [md.Question(**row) for _, row in questions_df.iterrows()]

@app.get("/question/random", response_model = md.Question)
def get_random_question() -> md.Question:
    return md.Question(**questions_df.sample(1).iloc[0])

@app.get("/spicy_questions", response_model = List[md.SpicyQuestion])
def get_all_spicy_questions() -> List[md.SpicyQuestion]:
    return [md.SpicyQuestion(**row) for _, row in spicy_questions_df.iterrows()]

@app.get("/spicy_question/random", response_model = md.SpicyQuestion)
def get_random_spicy_question() -> md.SpicyQuestion:
    return md.SpicyQuestion(**spicy_questions_df.sample(1).iloc[0])

@app.get("/games", response_model = List[md.Game])
def get_all_games() -> List[md.Game]:
    return [
        md.Game(**row)
        for _, row in games_df.iterrows()
    ]

@app.get("/games/random", response_model = md.Game)
def get_random_game() -> md.Game:
    row = games_df.sample(1).iloc[0]
    return md.Game(**row)
