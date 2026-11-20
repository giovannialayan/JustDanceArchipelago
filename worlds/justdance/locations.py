from BaseClasses import Location
from typing import NamedTuple, Dict
import json

offset = 94473619_000

class JustDanceLocation(Location):
    game = "Just Dance"

class LocationData(NamedTuple):
    name: str = None
    song: str = None
    jdgame: str = None
    coach: int = None
    difficulty: str = None
    jdplus: bool = None

jd_locations = Dict[int, JustDanceLocation] = {}
prev_id = offset

with open("songs.json", mode="r", encoding="utf-8") as file:
    songsJson = json.load(file)
    for song in songsJson["songs"]:
        for coach in range(song.coaches):
            location_name = song.game + (" (+)" if song.jdplus else "") + " - " + song.title + (" coach " + coach if song.coaches > 1 else "")
            location_id = prev_id
            prev_id += 1
            jd_locations[location_id] = LocationData(location_name, song.title, song.game, coach, song.difficulty, song.jdplus)