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
    }

    Container {
        width: 80%;
        height: auto;
        background: $panel;
        border: solid $primary;
        padding: 1;
    }

    Button {
        width: 100%;
        margin: 1;
    }

    Input {
        margin: 1;
    }

    Select {
        margin: 1;
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
