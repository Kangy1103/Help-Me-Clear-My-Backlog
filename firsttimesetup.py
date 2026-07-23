import webbrowser

from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, ContentSwitcher, Input, Label


class FirstTimeSetup(ModalScreen):

    def compose(self) -> ComposeResult:
        with ContentSwitcher(initial="steam-api-config"):
            with Vertical(id="steam-api-config"):
                yield Label(
                    "Help Me Clear My Backlog requires you to make and use a Steam API key"
                )
                yield Label(
                    "to query your library. You'll need to log into your Steam account."
                )
                yield Label("Please use the link below to create your API key.")
                yield Button(
                    "Create Steam API Key", id="api_key_btn", variant="primary"
                )
                yield Label("")
                yield Label("Enter the generated key in the box below.")
                yield Label(
                    "[italics]Psst![/italics] Don't worry it's saved to a local .env file only you can access!"
                )
                yield Input(placeholder="Paste API key here...", password=True)
                yield Button("Validate", id="validate_btn")
                yield Button("Next", id="next_btn")

            with Vertical(id="steam-name"):
                yield Label("Now we're going to need your Steam vanity name.")
                yield Label(
                    "Follow the instructions below if you don't know where to find it."
                )
                yield Label("Open the Steam desktop app")
                yield Label("Click your name on the top bar to view your profile")
                yield Label(
                    "A URL should have appeared just below the upper navigation bar"
                )
                yield Label(
                    "You want the portion after /id/<vanity-name>. Enter it below."
                )
                yield Input(placeholder="Steam vanity name goes here...")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "api_key_btn":
            webbrowser.open("https://steamcommunity.com/dev/apikey")
        elif event.button.id == "next_btn":
            self.query_one(ContentSwitcher).current = "steam-name"


class DummyApp(App[None]):
    def compose(self) -> ComposeResult:
        yield Button("Open modal.", id="open_modal")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "open_modal":
            self.push_screen(FirstTimeSetup())


app = DummyApp()
if __name__ == "__main__":
    app.run()
