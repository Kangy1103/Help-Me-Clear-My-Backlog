import os

from dotenv import load_dotenv
from steam_web_api import Steam


def empty_key_guard():
    load_dotenv(override=True)
    key = os.environ.get("STEAM_API_KEY")
    return Steam(key)


def fetch_steam_user_data() -> list:
    steam = empty_key_guard()
    username = os.environ.get("STEAM_VANITY_NAME")
    user_data = steam.users.search_user(username)
    if user_data and "player" in user_data:
        return user_data["player"]
    else:
        raise Exception("Player not found")


def fetch_steam_library_data(steamid):
    steam = empty_key_guard()
    library = steam.users.get_owned_games(steamid)
    games_list = library.get("games", [])
    skimmed_library = [
        {
            "appid": game.get("appid"),
            "name": game.get("name"),
            "playtime": game.get("playtime_forever"),
            "playtime_2weeks": game.get("playtime_2weeks", 0),
            "playtime_windows": game.get("playtime_windows_forever", 0),
            "playtime_mac": game.get("playtime_mac_forever", 0),
            "playtime_linux": game.get("playtime_linux_forever", 0),
            "last_played": game.get("rtime_last_played"),
            "img_icon_url": game.get(""),
        }
        for game in games_list
    ]

    return skimmed_library
