from BaseClasses import Item
from typing import NamedTuple, Dict
import json

offset = 94473618_000

class JustDanceItem(Item):
    game = "Just Dance"

class ItemData(NamedTuple):
    code: int
    game: str
    difficulty: str
    coaches: int

item_table: Dict[str, ItemData] = {}

mode_to_coaches: Dict[str, int] = {
    "Solo": 1,
    "Duet": 2,
    "Trio": 3,
    "Quartet": 4,
    "Quintet": 5,
    "Sextet": 6,
    "Hold My Hand": 1
}

with open("songs.json", mode="r", encoding="utf-8") as file:
    songsJson = json.load(file)
    for song in songsJson["songs"]:
        item_table[song.title] = ItemData(offset + 1, song.game, song.difficulty, mode_to_coaches[song.mode])