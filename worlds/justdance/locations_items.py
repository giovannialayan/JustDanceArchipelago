from BaseClasses import Location, Item
from typing import NamedTuple, Dict
import json

item_offset = 94473618_000
loc_offset = 94473619_000

class JustDanceLocation(Location):
    game = "Just Dance"

class LocationData(NamedTuple):
    name: str = None
    song: str = None
    jdgame: str = None
    coach: int = None
    difficulty: str = None
    jdplus: bool = None

class JustDanceItem(Item):
    game = "Just Dance"

class ItemData(NamedTuple):
    code: int

jd_locations = Dict[int, JustDanceLocation] = {}
loc_prev_id = loc_offset

item_table: Dict[str, ItemData] = {}
item_prev_id = item_offset

with open("songs.json", mode="r", encoding="utf-8") as file:
    songsJson = json.load(file)
    for song in songsJson["songs"]:
        for coach in range(song.coaches):
            location_name = song.game + (" (+)" if song.jdplus else "") + " - " + song.title + (" coach " + coach if song.coaches > 1 else "")
            location_id = loc_prev_id
            loc_prev_id += 1
            jd_locations[location_id] = LocationData(location_name, song.title, song.game, coach, song.difficulty, song.jdplus)

            item_id = item_prev_id
            item_prev_id += 1
            item_table[location_name] = ItemData(item_id)