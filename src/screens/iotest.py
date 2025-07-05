from pathlib import Path
from textual.app import ComposeResult
from textual.containers import Container, Vertical, Horizontal
from textual.widgets import Button, Header, Footer, Input, Label, TextArea
from textual.binding import Binding

from .base import BaseScreen


class IOTestScreen(BaseScreen):

    def on_mount(self) -> None:
        self.add_class("iotest-screen")

    def compose(self) -> ComposeResult:
        yield Header()
        with Container():
            yield Label("Contest Number:")
            yield Input(
                placeholder="Enter contest number",
                id="contest",
                classes="short-input",
            )
            yield Label("Problem:")
            yield Input(placeholder="A", id="problem", classes="short-input")
            with Horizontal():
                with Vertical(id="input_section"):
                    yield Label("Input:")
                    yield TextArea(id="input", language="text")
                with Vertical(id="output_section"):
                    yield Label("Expected Output:")
                    yield TextArea(id="output", language="text")
            with Horizontal():
                yield Button("Save Test Case", variant="primary", id="save")
                yield Button("Save and Test", variant="primary", id="save_and_test")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id in ["save", "save_and_test"]:
            contest = self.query_one("#contest").value
            problem = self.query_one("#problem").value
            input_content = self.query_one("#input").text
            output_content = self.query_one("#output").text

            if not contest or not problem:
                self.notify_error("Contest number and problem are required!")
                return

            if not input_content:
                self.notify_error("Input is required!")
                return

            contest_dir = Path(contest)
            if not contest_dir.exists():
                self.notify_error(f"Contest directory '{contest}' not found!")
                return

            problem_path = contest_dir / self.app.manager.config.get_problem_file_name(
                problem
            )
            if not problem_path.exists():
                self.notify_error(f"Problem {problem} not found!")
                return

            self.app.manager.write_input(contest_dir, problem, input_content)
            if output_content:
                self.app.manager.write_output(contest_dir, problem, output_content)

            self.notify_success("Test case saved successfully!")

            if event.button.id == "save_and_test" and output_content:
                self.app.push_screen("test", {"contest": contest, "problem": problem})
