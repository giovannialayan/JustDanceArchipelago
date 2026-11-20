from BaseClasses import Item
from typing import NamedTuple, Dict
import json

offset = 94473618_000

class JustDanceItem(Item):
    game = "Just Dance"

class ItemData(NamedTuple):
    code: int
    song: str
    game: str
    coach: int

item_table: Dict[str, ItemData] = {}
prev_id = offset

with open("songs.json", mode="r", encoding="utf-8") as file:
    songsJson = json.load(file)
    for song in songsJson["songs"]:
        for coach in range(song.coaches):
            item_name = song.game + (" (+)" if song.jdplus else "") + " - " + song.title + (" coach " + coach if song.coaches > 1 else "")
            item_id = prev_id
            prev_id += 1
            item_table[item_id] = ItemData(item_id, song.title, song.game, coach, song.difficulty, song.jdplus)