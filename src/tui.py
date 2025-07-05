from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Header, Footer

from .contest import ContestManager
from .screens.menu import MainMenu
from .screens.create import CreateContestScreen
from .screens.run import RunProblemScreen
from .screens.test import TestProblemScreen
from .screens.iotest import IOTestScreen
from .screens.config import ConfigScreen


class SeePeeTUI(App):
    TITLE = "SeePee"
    BINDINGS = [("q", "quit", "Quit"), ("escape", "quit", "Quit")]

    CSS = """
    Screen {
        align: center middle;
        layers: base overlay;
    }

    Screen > Container {
        width: 90%;
        min-width: 50;
        max-width: 120;
        height: auto;
        min-height: 20;
        max-height: 90vh;
        background: $panel;
        border: solid $primary;
        overflow-y: auto;
        padding: 1 2;
        layout: vertical;
    }

    Screen.menu-screen > Container, Screen.iotest-screen > Container {
        height: 100%;
        max-height: 95vh;
    }

    Vertical {
        width: 100%;
        height: auto;
        margin-bottom: 1;
    }

    Horizontal {
        height: auto;
        margin: 1 0;
    }

    Button {
        width: 100%;
        margin: 0 0 1 0;
    }

    Input {
        width: 100%;
        margin: 0 0 1 0;
    }

    Select {
        width: 100%;
        margin: 0 0 1 0;
    }

    TextArea {
        width: 100%;
        height: auto;
        min-height: 3;
        margin: 0 0 1 0;
    }

    Label {
        margin: 1 0;
        padding: 0;
    }

    #input_section, #output_section {
        width: 1fr;
        height: auto;
    }

    #input TextArea, #output TextArea {
        overflow: hidden;
        height: auto;
    }

    #app-header {
        dock: top;
        text-align: center;
        background: $accent;
        color: $text;
        border: solid $primary;
        padding: 1;
        margin-bottom: 1;
    }

    Screen.create-screen Button {
        margin-top: 1;
    }
    """

    SCREENS = {
        "menu": MainMenu,
        "create": CreateContestScreen,
        "run": RunProblemScreen,
        "test": TestProblemScreen,
        "iotest": IOTestScreen,
        "config": ConfigScreen,
    }

    def __init__(self):
        super().__init__()
        self.manager = ContestManager()

    def on_mount(self) -> None:
        self.push_screen("menu")

    def compose(self) -> ComposeResult:
        yield Container()

    def action_quit(self) -> None:
        self.exit()


def run_tui():
    app = SeePeeTUI()
    app.run()
