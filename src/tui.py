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
        height: 100%;
        width: 100%;
        padding: 2;
    }

    Screen.menu-screen {
        overflow: hidden;
    }

    Container {
        width: 90%;
        min-width: 50;
        max-width: 120;
        height: auto;
        min-height: 20;
        max-height: 80vh;
        background: $panel;
        border: solid $primary;
        padding: 1;
        overflow-y: auto;
    }

    Vertical {
        height: auto;
        width: 100%;
        min-height: 10;
        overflow-y: auto;
    }

    Button {
        width: 100%;
        margin: 1;
    }

    Input {
        margin: 1;
        width: 100%;
    }

    Select {
        margin: 1;
        width: 100%;
    }

    TextArea {
        height: auto;
        min-height: 5;
        max-height: 20;
        width: 100%;
    }

    #app-header {
        text-align: center;
        padding: 1;
        text-style: bold;
        background: $accent;
        color: $text;
        border: solid $primary;
        margin-bottom: 1;
    }

    #input_section, #output_section {
        width: 1fr;
        height: auto;
        min-height: 10;
        margin: 1;
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
