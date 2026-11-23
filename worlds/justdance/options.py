from dataclasses import dataclass
from Options import PerGameCommonOptions, Toggle, Range, Choice, OptionSet

class SongCount(Range):
    """
    the number of songs required to be completed to win
    """
    display_name = "number of songs"
    range_start = 5
    range_end = 1180
    default = 40

class StartingSongs(Range):
    """
    number of songs to start unlocked
    """
    display_name = "starting songs"
    range_start = 1
    range_end = 1180
    default = 5

class RequiredScore(Range):
    """
    score required to count a song as completed
    """
    display_name = "required score"
    range_start = 1
    range_end = 13333
    default = 12000

class GamePool(OptionSet):
    """
    just dance games to use in the song pool, leave empty to use all games
    valid inputs: 1, 2, 3, 4, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026, doh, plus
    """
    display_name = "just dance game pool"
    default = ['2023', '2024', '2025', '2026', 'doh', 'plus']
    valid_keys = ['1', '2', '3', '4', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025', '2026', 'doh', 'plus']

@dataclass
class JustDanceOptions(PerGameCommonOptions):
    song_count: SongCount
    starting_songs: StartingSongs
    required_score: RequiredScore
    game_pool: GamePool