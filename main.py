import asyncio
import os

from database import database_init, game_database, game_query
from dotenv import load_dotenv
from rich import print
from rich.console import Console
from rich.progress import Progress
from steam_web_api import Steam

from fetchgamedata import fetch_game_data
from steamdata import fetch_steam_data

load_dotenv()
console = Console(highlight=False)
KEY = os.environ.get("STEAM_API_KEY")
steam = Steam(KEY)


async def main():
    print("[bold blue]Hello from Help Me Clear My Backlog![/bold blue]")
    console.print("[italics]Made by Kangy[/italics]")

    await database_init()

    library = fetch_steam_data("arconaute")

    print("Searching for game...")
    semaphore = asyncio.Semaphore(10)
    with Progress(console=console, transient=True) as progress:
        progress.add_task("", total=None)
        hltb_pulls = [
            fetch_game_data(game, semaphore, progress, console) for game in library
        ]
        library_data = await asyncio.gather(*hltb_pulls)
    print("Sync complete!")


if __name__ == "__main__":
    asyncio.run(main())
