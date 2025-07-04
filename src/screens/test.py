from pathlib import Path
from textual.app import ComposeResult
from textual.containers import Container, Vertical, Horizontal
from textual.widgets import Button, Header, Footer, Input, Label, TextArea, Static
from textual.binding import Binding
from rich.syntax import Syntax
from rich.table import Table

from .base import BaseScreen


class TestProblemScreen(BaseScreen):

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

            yield Button("Run Test", variant="primary", id="test")
            yield Label("Test Results:")
            yield Static(id="results", markup=True)
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "test":
            contest = self.query_one("#contest").value
            problem = self.query_one("#problem").value

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
            input_path = contest_dir / self.app.manager.config.get_input_file_name(
                problem
            )
            output_path = contest_dir / self.app.manager.config.get_output_file_name(
                problem
            )

            if not output_path.exists():
                self.notify_error(
                    "Expected output file not found! Add test cases first."
                )
                return

            with open(output_path) as f:
                expected_output = f.read()

            output, error, success = self.app.manager.compile_and_run(
                problem_path, input_path
            )
            results_widget = self.query_one("#results")

            if not success:
                self.notify_error("Compilation/Runtime Error!")
                results_widget.update(Syntax(error, "text", theme="monokai"))
                return

            matches = self.app.manager.verify_output(output, expected_output)
            if matches:
                self.notify_success("✓ Output matches expected output!")
            else:
                self.notify_error("✗ Output does not match expected output!")

            table = Table()
            table.add_column("Expected", style="green")
            table.add_column("Got", style="blue" if matches else "red")
            table.add_row(expected_output, output)
            results_widget.update(table)
