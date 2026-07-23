from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.widgets import DataTable, Footer, Header, Static

from database import query_all_games
from steamdata import fetch_steam_user_data


class HelpMeClearMyBacklog(App):
    BINDINGS = [("q", "quit", "Quit")]

    CSS = """
    #steam-hltb-stats {
        height: auto;
        padding: 1 2;
        background: $boost;
        border: round $accent;
        content-align: center middle;
        margin-bottom: 1;
    }
    DataTable {
    height: 1fr;
    }
    """

    current_sorts: set = set()

    def compose(self):
        yield Header()
        yield Static(id="steam-hltb-stats")
        yield DataTable()
        yield Footer()

    async def on_mount(self):
        tui_games_list = await query_all_games()
        table = self.query_one(DataTable)
        steam_hltb_panel = self.query_one("#steam-hltb-stats", Static)
        player = fetch_steam_user_data("arconaute")

        total_games = len(tui_games_list)
        total_hours_main = sum(game.get("hltb_main") for game in tui_games_list)

        steam_hltb_panel.update(
            f"Name:     [white]{player.get('personaname')}[/white]\n"
            f"SteamID:  [white]{player.get('steamid')}[/white]\n"
            f"Profile:  [blue]{player.get('profileurl')}[/blue]\n"
            f"Total Games: [red]{total_games} | Total Hours to Clear: {total_hours_main} hours[/red]"
        )

        table.add_columns(
            "Game",
            "Playtime (hrs)",
            "HLTB Main Story (hrs)",
            "HLTB Completionist (hrs)",
        )
        for game in tui_games_list:
            table.add_row(
                game["name"],
                f"{game["playtime"] / 60:.2f}",
                game["hltb_main"],
                game["hltb_completionist"],
            )
        table.cursor_type = "row"
        table.zebra_stripes = True

    def sort_reverse(self, sort_type):
        reverse = sort_type in self.current_sorts
        if reverse:
            self.current_sorts.remove(sort_type)
        else:
            self.current_sorts.add(sort_type)
        return reverse

    def sort_by_game(self, column_key):
        table = self.query_one(DataTable)
        table.sort(column_key, key=lambda game: game, reverse=self.sort_reverse("name"))

    def sort_by_playtime(self, column_key):
        table = self.query_one(DataTable)
        table.sort(
            column_key,
            key=lambda playtime: float(playtime),
            reverse=self.sort_reverse("playtime"),
        )

    def sort_by_hltb_main(self, column_key):
        table = self.query_one(DataTable)
        table.sort(
            column_key,
            key=lambda hltb_main_story: float(hltb_main_story),
            reverse=self.sort_reverse("hltb_main_story"),
        )

    def sort_by_hltb_completionist(self, column_key):
        table = self.query_one(DataTable)
        table.sort(
            column_key,
            key=lambda hltb_completionist_time: float(hltb_completionist_time),
            reverse=self.sort_reverse("hltb_completionist_time"),
        )

    def on_data_table_header_selected(self, event: DataTable.HeaderSelected):
        clicked_column = str(event.label)

        if clicked_column == "Game":
            self.sort_by_game(event.column_key)
        elif clicked_column == "Playtime (hrs)":
            self.sort_by_playtime(event.column_key)
        elif clicked_column == "HLTB Main Story (hrs)":
            self.sort_by_hltb_main(event.column_key)
        elif clicked_column == "HLTB Completionist (hrs)":
            self.sort_by_hltb_completionist(event.column_key)


if __name__ == "__main__":
    app = HelpMeClearMyBacklog()
    app.run()
