import webbrowser

import httpx
from dotenv import set_key
from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, ContentSwitcher, Input, Label

env = ".env"


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
                yield Input(placeholder="Paste API key here...", id="api_input")
                yield Button("Validate", id="api_validate_btn")
                yield Button("Next", id="next_btn", variant="primary", disabled=True)

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
                yield Input(
                    placeholder="Steam vanity name goes here...", id="steam_name_input"
                )
                yield Button("Validate Profile", id="name_validate_btn")
                # Validate Profile container (hidden)
                with Vertical(id="pull_steam_profile"):
                    yield Label("", id="steam_name")
                    yield Label("", id="steam_id")
                    yield Label("", id="profile_url")
                    yield Button("Confirm", id="confirm_steam_profile")

    # Hide pull_steam_profile container until needed (remove when styling file made)
    def on_mount(self):
        self.query_one("#pull_steam_profile").styles.display = "none"

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        # Event handler for api key creation link button
        if event.button.id == "api_key_btn":
            webbrowser.open("https://steamcommunity.com/dev/apikey")
        # Event handler for api kay validation button
        elif event.button.id == "api_validate_btn":
            api_key = self.query_one("#api_input").value
            # httpx request to validate the steam api key works
            async with httpx.AsyncClient() as hmcmb:
                url = f"https://api.steampowered.com/ISteamWebAPIUtil/GetSupportedAPIList/v1/?key={api_key}"
                response = await hmcmb.get(url)
                if response.status_code == 200:
                    self.query_one("#next_btn").disabled = False
                    set_key(env, "STEAM_API_KEY", api_key)
                else:
                    self.notify("Steam API key not valid!", severity="error")
        # event handler for next button after api key validation
        elif event.button.id == "next_btn":
            self.query_one(ContentSwitcher).current = "steam-name"

        # Pull steam profile data to confirm the correct profile has been found
        # before passing the variable to the .env file
        elif event.button.id == "name_validate_btn":
            steam_vanity_name = self.query_one("#steam_name_input").value
            api_key = self.query_one(
                "#api_input"
            ).value  # Doobious and whether this will still be accessible
            async with httpx.AsyncClient() as hmcmb:
                steam_vanity_url = f"https://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key={api_key}&vanityurl={steam_vanity_name}"
                steam_vanity_result = await hmcmb.get(steam_vanity_url)
                steam_vanity_data = steam_vanity_result.json()

                if steam_vanity_data.get("response", {}).get("success") == 1:
                    steam_id = steam_vanity_data["response"]["steamid"]

                    # Pull the profile
                    steam_summary_url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={api_key}&steamids={steam_id}"
                    steam_summary_res = await hmcmb.get(steam_summary_url)
                    steam_summary_data = steam_summary_res.json()

                    if steam_summary_data.get("response", {}).get("players"):
                        player_info = steam_summary_data["response"]["players"][0]
                        persona_name = player_info.get("personaname", "Unknown")
                        profile_url = player_info.get("profileurl", "Unknown")

                        # Update pull_steam_profile container labels
                        self.query_one("#steam_id").update(f"Steam ID: {steam_id}")
                        self.query_one("#steam_name").update(
                            f"Profile Name: {persona_name}"
                        )
                        self.query_one("#profile_url").update(f"URL: {profile_url}")
                        self.query_one("#pull_steam_profile").styles.display = "block"
                    else:
                        self.notify("You can't do that Dave...", severity="warning")
                else:
                    self.notify(
                        f"No profile found for {steam_vanity_name}",
                        severity="error",
                    )

        # Event handler for confirming and closing the modal
        elif event.button.id == "confirm_steam_profile":
            steam_vanity_name = self.query_one("#steam_name_input").value
            set_key(env, "STEAM_VANITY_NAME", steam_vanity_name)
            self.dismiss()


class DummyApp(App[None]):
    def compose(self) -> ComposeResult:
        yield Button("Open modal.", id="open_modal")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "open_modal":
            self.push_screen(FirstTimeSetup())


app = DummyApp()
if __name__ == "__main__":
    app.run()
