from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.widgets import Button, Header, Footer, Input, Label, Select
from textual.binding import Binding
from pathlib import Path
import yaml

from .base import BaseScreen


class ConfigScreen(BaseScreen):

    def __init__(self):
        super().__init__()
        self.initial_config = self.load_initial_config()

    def load_initial_config(self):
        config_path = Path("config/config.yaml")
        if config_path.exists():
            with open(config_path) as f:
                return yaml.safe_load(f)
        return None

    def compose(self) -> ComposeResult:
        yield Header()
        with Container():
            with Vertical():

                yield Label("Compiler Settings", classes="section-header")
                yield Label("Compiler:")
                yield Input(
                    value=self.app.manager.config.config["compile"]["command"],
                    id="compiler",
                )
                yield Label("Compiler Flags:")
                yield Input(
                    value=" ".join(self.app.manager.config.config["compile"]["flags"]),
                    id="flags",
                )

                yield Label("Path Settings", classes="section-header")
                yield Label("Template Path:")
                yield Input(
                    value=self.app.manager.config.config["paths"]["template"],
                    id="template",
                )
                yield Label("Templates Directory:")
                yield Input(
                    value=self.app.manager.config.config["paths"]["templates_dir"],
                    id="templates_dir",
                )

                yield Button("Save Changes", variant="primary", id="save")
                yield Button("Reset to Defaults", variant="error", id="reset")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save":

            compiler = self.query_one("#compiler").value
            flags = self.query_one("#flags").value
            self.app.manager.config.update_compiler(compiler)
            self.app.manager.config.update_compiler_flags(flags.split())

            template = self.query_one("#template").value
            templates_dir = self.query_one("#templates_dir").value
            self.app.manager.config.update_template(template)
            self.app.manager.config.update_templates_dir(templates_dir)

            self.notify_success("Configuration saved successfully!")
            self.app.pop_screen()

        elif event.button.id == "reset":
            if self.initial_config:

                self.query_one("#compiler").value = self.initial_config["compile"][
                    "command"
                ]
                self.query_one("#flags").value = " ".join(
                    self.initial_config["compile"]["flags"]
                )
                self.query_one("#template").value = self.initial_config["paths"][
                    "template"
                ]
                self.query_one("#templates_dir").value = self.initial_config["paths"][
                    "templates_dir"
                ]
                self.notify_success("Reset to initial configuration values")
            else:
                self.notify_error("Could not load initial configuration")
