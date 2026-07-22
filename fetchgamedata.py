# import asyncio
# import os
import re

from howlongtobeatpy import HowLongToBeat

# from rich import print
from rich.console import Console

# from rich.progress import Progress

console = Console(highlight=False)


async def fetch_game_data(game, semaphore, progress, console):
    async with semaphore:
        game_name: str = re.sub(r"[™®©]", "", game.get("name"))
        game_name: str = re.sub(r"-", " ", game_name)
        game_name: str = re.sub(
            r"[-:]?\s*(ultimate|definitive|deluxe|GOTY)\s+edition.*",
            "",
            game_name,
            flags=re.IGNORECASE,
        )
        results = await HowLongToBeat(0.3).async_search(game_name)
        playtime = game.get("playtime")
        if not results and game_name.isupper():
            results = await HowLongToBeat(0.3).async_search(game_name.title())
        if not results:
            game["hltb_main"] = 0.0
            game["hltb_completionist"] = 0.0
            console.print(f"[bold red]No game found:[/bold red] {game_name}")
        else:
            best = max(results, key=lambda e: e.similarity)
            progress.console.print("[bold green]Game found![/bold green]")
            progress.console.print(f"[bold blue]{best.game_name}[/bold blue]")
            progress.console.print(f"Playtime: {playtime /60:.2f} hours")
            progress.console.print(
                f"[bold green]Main: [/bold green][white]{best.main_story}h[/white]"
            )
            progress.console.print(
                f"[bold green]Completionist: [/bold green][white]{best.completionist}h[/white]"
            )
            game["hltb_main"] = best.main_story
            game["hltb_completionist"] = best.completionist

    return game
