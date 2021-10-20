import datetime
from typing import Union, Optional

from pydantic import BaseModel
from pydantic.validators import str_validator


def empty_to_none(v: str) -> Optional[str]:
    if v == '':
        return None
    return v


class EmptyStrToNone(str):
    @classmethod
    def __get_validators__(cls):
        yield str_validator
        yield empty_to_none
        

class AKA(BaseModel):
    title_id: str
    title: str
    region: str
    language: str
    types: str
    attributes: str
    is_original_title: bool


class Genre(BaseModel):
    genre: str


class Title(BaseModel):
    title_id: str
    type: str
    primary_title: str
    original_title: str
    is_adult: bool
    premiered: int
    ended: Union[int, None]
    runtime_minutes: int
    genres: list[Genre]
    

class Person(BaseModel):
    person_id: str
    name: str
    born: int
    died: int


class CrewMember(BaseModel):
    title_id: str
    person_id: str
    category: str
    job: Union[str, None]
    characters: str
    

class Rating(BaseModel):
    title_id: str
    rating: float
    votes: int
    
    
class Episode(BaseModel):
    episode_title_id: str
    show_title_id: str
    season_number: int
    episode_number: int