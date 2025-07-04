from pathlib import Path
from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Button, Header, Footer, Input, Label, Select
from textual.binding import Binding

from .base import BaseScreen


class CreateContestScreen(BaseScreen):

    def compose(self) -> ComposeResult:
        yield Header()
        with Container():
            yield Label("Contest Number:")
            yield Input(placeholder="Enter contest number", id="contest")
            yield Label("Problems Range:")
            yield Input(placeholder="A-D or A,B,C", id="problems")
            yield Label("Select Template:")
            templates = self.app.manager.list_templates()
            default_template = Path(
                self.app.manager.config.config["paths"]["template"]
            ).name
            yield Select(
                [(t, t) for t in templates],
                prompt="Select template",
                value=default_template,
                id="template",
            )
            yield Button("Create", variant="primary", id="create")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "create":
            contest = self.query_one("#contest").value
            problems = self.query_one("#problems").value
            template = self.query_one("#template").value

            if not contest or not problems:
                self.notify_error("Contest number and problems range are required!")
                return

            if "-" in problems:
                start, end = problems.split("-")
                problems_list = [chr(i) for i in range(ord(start), ord(end) + 1)]
            else:
                problems_list = problems.split(",")

            contest_dir = self.app.manager.create_contest_dir(contest)
            self.app.manager.create_problem_files(contest_dir, problems_list, template)
            self.notify_success(f"Contest {contest} created successfully!")
            self.app.pop_screen()
