
import track_manager

from textual import log
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, TabbedContent, TabPane, ProgressBar, ContentSwitcher

from media_pane import MediaPane

# i apologize for this code

class SyncApp(App):
    CSS_PATH = "style.tcss"

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True, time_format="%-I:%M %p")
        with TabbedContent(id="media-panes"):
            with TabPane("Tracks"):
                yield MediaPane("track")
            with TabPane("Albums"):
                yield MediaPane("album")
            with TabPane("Artists"):
                yield MediaPane("artist")
            with TabPane("Playlists"):
                yield MediaPane("playlist")
        yield ProgressBar(total=track_manager.ipod.get_total_space_on_ipod(), show_eta=False)
        yield Footer()

    def on_mount(self) -> None:
        self.title = "iPod Navidrome Sync Tool"
        self.query_one(ProgressBar).update(total=track_manager.ipod.get_total_space_on_ipod(), progress=track_manager.find_tracks_to_sync())

    def on_unmount(self) -> None:
        track_manager.save_previously_selected()

if __name__ == "__main__":
    app = SyncApp()
    app.run()