
import track_manager

from textual import log
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, TabbedContent, TabPane

from media_pane import MediaPane

class SyncApp(App):
    CSS_PATH = "style.tcss"

    def __init__(self):
        super().__init__()
        self.track_list: list[track_manager.Track] = track_manager.load_track_listings()[0]
        self.album_list: list[tuple[str, str]] = track_manager.navidrome.get_albums()
        self.artist_list: list[str] = track_manager.navidrome.get_artists()
        self.playlist_list: list[str] = []

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True, time_format="%-I:%M %p")
        with TabbedContent():
            with TabPane("Tracks"):
                yield MediaPane(self.track_list, self.album_list, self.artist_list, self.playlist_list, "track")
            with TabPane("Albums"):
                yield MediaPane(self.track_list, self.album_list, self.artist_list, self.playlist_list, "album")
            with TabPane("Artists"):
                yield MediaPane(self.track_list, self.album_list, self.artist_list, self.playlist_list, "artist")
            with TabPane("Playlists"):
                yield MediaPane(self.track_list, self.album_list, self.artist_list, self.playlist_list, "playlist")
        yield Footer()

    def on_mount(self) -> None:
        self.title = "iPod Navidrome Sync Tool"

if __name__ == "__main__":
    app = SyncApp()
    app.run()