from pathlib import Path
from textual.app import ComposeResult
from textual.containers import Container, Vertical, Horizontal
from textual.widgets import Button, Header, Footer, Input, Label, TextArea, Static
from textual.binding import Binding
from rich.syntax import Syntax

from .base import BaseScreen


class RunProblemScreen(BaseScreen):

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
            yield Label("Input:")
            yield TextArea(id="input", language="text")
            yield Button("Run", variant="primary", id="run")
            yield Label("Output:")
            yield Static(id="output", markup=False)
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "run":
            contest = self.query_one("#contest").value
            problem = self.query_one("#problem").value
            input_content = self.query_one("#input").text

            if not contest or not problem:
                self.notify_error("Contest number and problem are required!")
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

            input_path = contest_dir / self.app.manager.config.get_input_file_name(
                problem
            )
            if input_content.strip():
                with open(input_path, "w") as f:
                    f.write(input_content)

            output, error, success = self.app.manager.compile_and_run(
                problem_path, input_path
            )
            output_widget = self.query_one("#output")

            if success:
                self.notify_success("Compilation successful!")
                output_widget.update(Syntax(output, "text", theme="monokai"))
            else:
                self.notify_error("Compilation/Runtime Error!")
                output_widget.update(Syntax(error, "text", theme="monokai"))
