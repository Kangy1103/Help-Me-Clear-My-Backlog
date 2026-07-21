import asyncio
import os

from dotenv import load_dotenv
from howlongtobeatpy import HowLongToBeat
from rich import print
from rich.console import Console
from rich.progress import Progress
from steam_web_api import Steam

load_dotenv()
console = Console(highlight=False)
KEY = os.environ.get("STEAM_API_KEY")
steam = Steam(KEY)


async def fetch_game_data(game, semaphore, progress):
    async with semaphore:
        game_name = game.get("name")
        playtime = game.get("playtime")
        if not game_name:
            return
        results = await HowLongToBeat().async_search(game_name)
        if not results:
            console.print(f"[bold red]No game found:[/bold red] {game_name}")
        else:
            best = max(results, key=lambda e: e.similarity)
            progress.console.print("[bold green]Game found![/bold green]")
            progress.console.print(
                f"[bold blue]{best.game_name}[/bold blue] — Playtime: {playtime /60:.2f} hours -  [bold green]Main: [/bold green][white]{best.main_story}h,[/white] [bold green]Completionist: [/bold green][white]{best.completionist}h[/white]"
            )
        # await asyncio.sleep(0.5)


async def main():
    print("[bold blue]Hello from steam-cli![/bold blue]")
    console.print("[italics]Made by Kangy[/italics]")

    user_data = steam.users.search_user("arconaute")
    if user_data and "player" in user_data:
        player = user_data["player"]

        print("\n[bold green]User Found![/bold green]")
        print(f"Name:     [white]{player.get('personaname')}[/white]")
        print(f"SteamID:  [white]{player.get('steamid')}[/white]")
        print(f"Profile:  [blue]{player.get('profileurl')}[/blue]")

    library = steam.users.get_owned_games(f"{player.get('steamid')}")
    games_list = library.get("games", [])
    skimmed_library = [
        {
            "name": game.get("name"),
            "appid": game.get("appid"),
            "playtime": game.get("playtime_forever"),
        }
        for game in games_list
    ]

    print("Searching for game...")
    semaphore = asyncio.Semaphore(20)
    with Progress(console=console, transient=True) as progress:
        progress.add_task("", total=None)
        hltb_pulls = [
            fetch_game_data(game, semaphore, progress) for game in skimmed_library
        ]
        await asyncio.gather(*hltb_pulls)
    print("Sync complete!")


if __name__ == "__main__":
    asyncio.run(main())
