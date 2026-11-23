from typing import Dict, Union, List
from worlds.AutoWorld import World, WebWorld
from BaseClasses import ItemClassification, Region, LocationProgressType, Tutorial, CollectionState
from worlds.generic.Rules import add_rule
from .locations_items import JustDanceItem, JustDanceLocation, ItemData, item_table, jd_locations
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

    locations_set = 0

    song_count = 5
    game_pool: list[str] = ["Just Dance 2023", "Just Dance 2024", "Just Dance 2025", "Just Dance 2026", "Just Dance: Decades of Hits", "Just Dance+"]

    itempool: list

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
        self.song_count = self.options.song_count
        self.game_pool = [self.game_dict[game] for game in list(self.options.game_pool.value)]

        if len(self.game_pool) == 0:
            self.game_pool = list(self.game_dict.values())

    def create_items(self):
        songs_to_unlock = self.options.starting_songs.value

        excluded_items: Dict[str, ItemData]
        song_pool_tuple_list = [
            (key, item)
            for key, item in item_table.items()
            if item.jdgame in self.game_pool
        ]
        for i in range(songs_to_unlock):
            song = self.random.choice(song_pool_tuple_list)
            song_name = song[0]
            song_data = song[1]

            precollected_item = self.create_item(song_name)
            self.multiworld.push_precollected(precollected_item)
            excluded_items[song_name] = song_data
            song_pool_tuple_list.remove(song)

        self.itempool = []
        for item_name in item_table:
            if not item_name in excluded_items:
                self.itempool.append(self.create_item(item_name))

        self.multiworld.itempool += self.itempool

    def create_item(self, item_name: str):
        item = item_table[item_name]
        return JustDanceItem(item_name, ItemClassification.progression, item.code, self.player)

    def create_regions(self):
        menu_region = Region("Menu", self.player, self.multiworld)

        placed_locations: List[JustDanceLocation] = list()

        song_pool_tuple_list = [
            (key, item)
            for key, item in jd_locations.items()
            if item.jdgame in self.game_pool
        ]

        for song_location in song_pool_tuple_list:
            new_location = JustDanceLocation(self.player, song_location[1].name, song_location[0], menu_region)
            new_location.progress_type = LocationProgressType.DEFAULT

            self.locations_set += 1
            menu_region.locations.append(new_location)
            placed_locations.append(new_location)
        
        self.multiworld.regions.append(menu_region)

        #completion condition
        def can_reach_count(state: CollectionState, locations: List[JustDanceLocation], count: int = 1) -> bool:
            counter = 0
            for loc in locations:
                if state.can_reach_location(loc.name, self.player):
                    counter += 1
                    if counter >= count:
                        return True
            return False

        self.multiworld.completion_condition[self.player] = lambda state: can_reach_count(state, placed_locations, self.song_count)

    def fill_slot_data(self):
        base_data = {
            "song_count": self.song_count,
            "required_score": self.options.required_score.value,
        }
        return base_data