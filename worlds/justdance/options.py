from dataclasses import dataclass
from Options import PerGameCommonOptions, Toggle, Range, Choice, OptionSet

class NumberOfSongs(Range):
    """
    the number of songs required to be completed to win
    """
    range_start = 1
    range_end = 1180
    default = 0

