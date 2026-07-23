import re

from howlongtobeatpy import HowLongToBeat

from database import game_query


async def fetch_game_data(game, semaphore, log):
    async with semaphore:
        steam_appid = game.get("appid")
        game_in_database = await game_query(steam_appid)
        if game_in_database:
            return game_in_database

        game_name: str = re.sub(r"[™®©]", "", game.get("name"))
        game_name: str = re.sub(r"-", " ", game_name)
        game_name: str = re.sub(
            r"[-:]?\s*(ultimate|definitive|deluxe|GOTY)\s+edition.*",
            "",
            game_name,
            flags=re.IGNORECASE,
        )

        log(f"Searching for: {game_name}...")
        results = await HowLongToBeat(0.3).async_search(game_name)
        playtime = game.get("playtime")
        if not results and game_name.isupper():
            results = await HowLongToBeat(0.3).async_search(game_name.title())
        if not results:
            game["hltb_main"] = 0.0
            game["hltb_completionist"] = 0.0
            log(f"[bold red]No game found:[/bold red] {game_name}")
        else:
            best = max(results, key=lambda e: e.similarity)
            log("[bold green]Game found![/bold green]")
            log(f"[bold blue]{best.game_name}[/bold blue]")
            log(f"Playtime: {playtime / 60:.2f} hours")
            log(f"[bold green]Main: [/bold green][white]{best.main_story}h[/white]")
            log(
                f"[bold green]Completionist: [/bold green][white]{best.completionist}h[/white]"
            )
            log("─" * 40)
            game["hltb_main"] = best.main_story
            game["hltb_completionist"] = best.completionist

    return game
