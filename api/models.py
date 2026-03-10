from pydantic import BaseModel
from typing import Optional

class Game(BaseModel):
    id: int
    title: str | None = None
    body: str | None = None
    category_id: int | None = None
    mechanic_id: int | None = None
    uses_player_names: bool | None = None
    placeholders_used: str | None = None

class Place(BaseModel):
    id : int
    place : str

class Theme(BaseModel):
    id: int
    theme: str

class LikelyTo(BaseModel):
    id: int
    most_likely_to: str

class RedFlag(BaseModel):
    id: int
    red_flag: str

class Word(BaseModel):
    id: int
    object: str

class Question(BaseModel):
    id: int
    random_questions: str

class SpicyQuestion(BaseModel):
    id: int
    spicy_questions: str