from typing import Dict, Union, List
from worlds.AutoWorld import World, WebWorld
from BaseClasses import ItemClassification, Region, LocationProgressType, Tutorial, CollectionState
from .locations_items import JustDanceItem, JustDanceLocation, ItemData, item_table, jd_locations, jd_item_id_to_name, jd_item_name_to_id, jd_location_id_to_name, jd_location_name_to_id
from .options import JustDanceOptions

#https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/world%20api.md

class JustDanceWebWorld(WebWorld):
    theme = "grassFlowers"
    bug_report_page = ""
    rich_text_options_doc = True
    setup_en = Tutorial(
        "Just Dance guide",
        "how to play Just Dance with Archipelago",
        "English",
        "setup_en.md",
        "setup/en",
        ["oig"]
    )

    tutorials = [setup_en]

class JustDanceWorld(World):
    """
    Just Dance is a dancing rhythm game
    """
    game = "Just Dance"
    web = JustDanceWebWorld()

    options: JustDanceOptions
    options_dataclass = JustDanceOptions

    topology_present = False

    item_name_to_id = jd_item_name_to_id
    item_id_to_name = jd_item_id_to_name

    location_name_to_id = jd_location_name_to_id
    location_id_to_name = jd_location_id_to_name

    item_name_groups = {"songs": {song for song in item_table}}

    song_count = 5
    game_pool: list[str] = ["Just Dance 2023", "Just Dance 2024", "Just Dance 2025", "Just Dance 2026", "Just Dance: Decades of Hits", "Just Dance+"]

    itempool: list

    starting_songs: Dict[str, ItemData]
    no_check_songs: Dict[str, ItemData]

    game_dict = {
        "1": "Just Dance 1",
        "2": "Just Dance 2",
        "3": "Just Dance 3",
        "4": "Just Dance 4",
        "2014": "Just Dance 2014",
        "2015": "Just Dance 2015",
        "2016": "Just Dance 2016",
        "2017": "Just Dance 2017",
        "2018": "Just Dance 2018",
        "2019": "Just Dance 2019",
        "2020": "Just Dance 2020",
        "2021": "Just Dance 2021",
        "2022": "Just Dance 2022",
        "2023": "Just Dance 2023",
        "2024": "Just Dance 2024",
        "2025": "Just Dance 2025",
        "2026": "Just Dance 2026",
        "doh": "Just Dance: Decades of Hits",
        "plus": "Just Dance+",
    }

    def generate_early(self):
        self.song_count = self.options.song_count.value
        self.game_pool = [self.game_dict[game] for game in list(self.options.game_pool.value)]

        if len(self.game_pool) == 0:
            self.game_pool = list(self.game_dict.values())

        songs_to_unlock = self.options.starting_songs.value
        
        self.starting_songs = {}
        self.no_check_songs = {}
        song_pool_tuple_list = [
            (key, item)
            for key, item in item_table.items()
            if item.jdgame in self.game_pool or ("Just Dance+" in self.game_pool and item.jdplus)
        ]
        for _ in range(songs_to_unlock):
            song = self.random.choice(song_pool_tuple_list)
            song_name = song[0]
            song_data = song[1]
        
            self.starting_songs[song_name] = song_data
            song_pool_tuple_list.remove(song)
        for _ in range(songs_to_unlock):
            song = self.random.choice(song_pool_tuple_list)
            song_name = song[0]
            song_data = song[1]
                
            self.no_check_songs[song_name] = song_data
            song_pool_tuple_list.remove(song)

    def create_items(self):
        for song_name in self.starting_songs:
            precollected_item = self.create_item(song_name)
            self.multiworld.push_precollected(precollected_item)

        self.itempool = []
        for item_name in item_table:
            if not item_name in self.starting_songs and \
                (item_table[item_name].jdgame in self.game_pool or ("Just Dance+" in self.game_pool and item_table[item_name].jdplus)):
                self.itempool.append(self.create_item(item_name))

        self.multiworld.itempool += self.itempool

    def create_item(self, item_name: str):
        item = item_table[item_name]
        return JustDanceItem(item_name, ItemClassification.progression, item.code, self.player)

    def create_regions(self):
        menu_region = Region("Menu", self.player, self.multiworld)

        song_pool_tuple_list = [
            (key, item)
            for key, item in jd_locations.items()
            if item.jdgame in self.game_pool or ("Just Dance+" in self.game_pool and item.jdplus) and item.name
        ]

        for song_location in song_pool_tuple_list:
            if not song_location[1].name in self.no_check_songs:
                new_location = JustDanceLocation(self.player, song_location[1].name, song_location[0], menu_region)
                new_location.progress_type = LocationProgressType.DEFAULT

                menu_region.locations.append(new_location)
        
        self.multiworld.regions.append(menu_region)        

    def set_rules(self):
        self.multiworld.completion_condition[self.player] = lambda state: state.has_group("songs", self.player, self.song_count)

    def fill_slot_data(self):
        base_data = {
            "song_count": self.song_count,
            "required_score": self.options.required_score.value,
        }
        return base_data