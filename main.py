import typer
from pathlib import Path
from typing import Optional, List
from rich import print
from rich.console import Console
from rich.table import Table
from src.contest import ContestManager

app = typer.Typer()
console = Console()
manager = ContestManager()


@app.command()
def create(
    contest: str,
    problems: str = typer.Option("A-F", help="Problem range (e.g., 'A-D' or 'A,B,C')"),
):

    if "-" in problems:
        start, end = problems.split("-")
        problems_list = [chr(i) for i in range(ord(start), ord(end) + 1)]
    else:
        problems_list = problems.split(",")

    contest_dir = manager.create_contest_dir(contest)
    manager.create_problem_files(contest_dir, problems_list)

    table = Table(title=f"Contest {contest} Created")
    table.add_column("Problem", style="cyan")
    table.add_column("Files Created", style="green")

    for prob in problems_list:
        cpp_file = manager.config.get_problem_file_name(prob)
        txt_file = manager.config.get_input_file_name(prob)
        table.add_row(prob, f"{cpp_file}, {txt_file}")

    console.print(table)


@app.command()
def run(contest: str, problem: str, input_content: Optional[str] = None):

    contest_dir = Path(contest)
    if not contest_dir.exists():
        console.print(f"[red]Contest directory '{contest}' not found!")
        raise typer.Exit(1)

    problem_path = contest_dir / manager.config.get_problem_file_name(problem)
    input_path = contest_dir / manager.config.get_input_file_name(problem)

    if input_content:
        with open(input_path, "w") as f:
            f.write(input_content)

    console.print(
        f"\n[yellow]Running problem {problem} from contest {contest}[/yellow]"
    )
    output, error, success = manager.compile_and_run(problem_path, input_path)

    if success:
        console.print("\n[green]Compilation successful![/green]")
        console.print("\n[bold]Output:[/bold]")
        console.print(output)
    else:
        console.print("\n[red]Compilation/Runtime Error:[/red]")
        console.print(error)


@app.command()
def test(contest: str, problem: str, expected_output: str):

    contest_dir = Path(contest)
    problem_path = contest_dir / manager.config.get_problem_file_name(problem)
    input_path = contest_dir / manager.config.get_input_file_name(problem)

    output, error, success = manager.compile_and_run(problem_path, input_path)
    if not success:
        console.print("\n[red]Compilation/Runtime Error:[/red]")
        console.print(error)
        raise typer.Exit(1)

    if manager.verify_output(output, expected_output):
        console.print("\n[green]✓ Output matches expected output![/green]")
    else:
        console.print("\n[red]✗ Output does not match expected output![/red]")
        table = Table(title="Output Comparison")
        table.add_column("Expected", style="green")
        table.add_column("Got", style="red")
        table.add_row(expected_output, output)
        console.print(table)


if __name__ == "__main__":
    app()
