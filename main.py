
import track_manager

import time

from textual import log
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, SelectionList

class SyncApp(App):
    CSS_PATH = "style.tcss"

    def __init__(self):
        super().__init__()
        self.track_listings: list[track_manager.Track] = track_manager.load_track_listings()[0]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True, time_format="%-I:%M %p")
        yield SelectionList[track_manager.Track](*[(str(track), track, track.is_on_ipod) for track in self.track_listings if int(time.time())%10!=0])
        yield Footer()

    def on_mount(self) -> None:
        self.title = "iPod Navidrome Sync Tool"

if __name__ == "__main__":
    app = SyncApp()
    app.run()