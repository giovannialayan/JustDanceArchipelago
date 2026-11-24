from BaseClasses import Location, Item
from typing import NamedTuple, Dict
import json
import pkgutil

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
    name: str = None
    song: str = None
    jdgame: str = None
    coach: int = None
    difficulty: str = None
    jdplus: bool = None

jd_locations: Dict[int, LocationData] = {}
jd_location_name_to_id: Dict[str, int] = {}
jd_location_id_to_name: Dict[int, str] = {}
loc_prev_id = loc_offset

item_table: Dict[str, ItemData] = {}
jd_item_name_to_id: Dict[str, int] = {}
jd_item_id_to_name: Dict[int, str] = {}
item_prev_id = item_offset

songsData = pkgutil.get_data(__name__, "songs.json")
songsJson = json.loads(songsData.decode("utf-8"))

for song in songsJson["songs"]:
    for coach in range(song["coaches"]):
        location_name = song["game"] + (" (+)" if song["jdplus"] and song["game"] != "plus" else "") + " - " + song["title"] + (" - coach " + str(coach + 1) if song["coaches"] > 1 else "")
        location_id = loc_prev_id
        loc_prev_id += 1
        jd_locations[location_id] = LocationData(location_name, song["title"], song["game"], coach, song["difficulty"], song["jdplus"])
        jd_location_name_to_id[location_name] = location_id
        jd_location_id_to_name[location_id] = location_name

        item_id = item_prev_id
        item_prev_id += 1
        item_table[location_name] = ItemData(item_id, location_name, song["title"], song["game"], coach, song["difficulty"], song["jdplus"])
        jd_item_name_to_id[location_name] = item_id
        jd_item_id_to_name[item_id] = location_name