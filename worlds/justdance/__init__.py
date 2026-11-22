from typing import Dict, Union, List
from worlds.AutoWorld import World, WebWorld
from BaseClasses import ItemClassification, Region, LocationProgressType, Tutorial, CollectionState
from worlds.generic.Rules import add_rule
from locations_items import JustDanceItem, JustDanceLocation

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