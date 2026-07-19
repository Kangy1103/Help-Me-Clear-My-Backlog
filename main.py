from howlongtobeatpy import HowLongToBeat
from rich import print
from rich.console import Console
from rich.progress import Progress

console = Console(highlight=False)


def main():
    print("[bold blue]Hello from steam-cli![/bold blue]")
    console.print("[italics]Made by Kangy[/italics]")
    print("Searching for game...")
    with Progress(transient=True) as progress:
        progress.add_task("", total=None)
        results = HowLongToBeat().search("dragons dogma")
    if not results:
        console.print("No game found", style="blink")
    else:
        best = max(results, key=lambda e: e.similarity)
        print("[bold green]Game found![/bold green]")
        console.print(
            f"[bold blue]{best.game_name}[/bold blue] — [bold green]Main: [/bold green][white]{best.main_story}h,[/white] [bold green]Completionist: [/bold green][white]{best.completionist}h[/white]"
        )


if __name__ == "__main__":
    main()
