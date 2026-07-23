import webbrowser

from textual.app import App, ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Label


class FirstTimeSetup(ModalScreen):

    def compose(self) -> ComposeResult:
        yield Label(
            "Help Me Clear My Backlog requires you to make and use a Steam API key"
        )
        yield Label(
            "to query your library. You'll need to log into your Steam account."
        )
        yield Label("Please use the link below to create your API key.")
        yield Button("Create Steam API Key", id="api_key_btn", variant="primary")
        yield Label("")
        yield Label("Enter the generated key in the box below.")
        yield Label(
            "[italics]Psst![/italics] Don't worry it's saved to a loval .env file only you can access!"
        )
        yield Input(placeholder="Paste API key here...", type="integer", password=True)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "api_key_btn":
            # This forces the host operating system to open the default web browser
            webbrowser.open("https://steamcommunity.com/dev/apikey")


class DummyApp(App[None]):
    def compose(self) -> ComposeResult:
        yield Button("Open modal.")

    def on_button_pressed(self) -> None:
        self.push_screen(FirstTimeSetup())


app = DummyApp()
if __name__ == "__main__":
    app.run()
