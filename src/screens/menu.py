from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.widgets import Button, Header, Footer, Static
from textual.binding import Binding
from textual.events import Key

from .base import BaseScreen


class MainMenu(BaseScreen):

    BINDINGS = [Binding("q", "quit", "Quit", show=True), *BaseScreen.BINDINGS]

    def compose(self) -> ComposeResult:
        yield Header()
        with Container():
            yield Button("Create Contest", variant="primary", id="create")
            yield Button("Run Problem", variant="primary", id="run")
            yield Button("Test Problem", variant="primary", id="test")
            yield Button("Add Test Cases", variant="primary", id="iotest")
            yield Button("Configure", variant="primary", id="config")
            yield Button("Quit", variant="error", id="quit")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id
        if button_id == "quit":
            self.app.exit()
        elif button_id in self.app.SCREENS:
            self.app.push_screen(button_id)

    def on_key(self, event: Key) -> None:
        if event.key == "escape":
            self.app.exit()
