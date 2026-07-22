import os

from dotenv import load_dotenv
from rich import print
from steam_web_api import Steam

load_dotenv()
KEY = os.environ.get("STEAM_API_KEY")
steam = Steam(KEY)


def fetch_steam_data(username: str) -> list:
    username = "arconaute"
    user_data = steam.users.search_user(username)
    if user_data and "player" in user_data:
        player = user_data["player"]

        print("\n[bold green]User Found![/bold green]")
        print(f"Name:     [white]{player.get('personaname')}[/white]")
        print(f"SteamID:  [white]{player.get('steamid')}[/white]")
        print(f"Profile:  [blue]{player.get('profileurl')}[/blue]")
    else:
        raise Exception("Player not found")

    library = steam.users.get_owned_games(f"{player.get('steamid')}")
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
