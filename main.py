import typer
import click
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
    problems: str = typer.Argument(
        "A-F", help="Problem range (e.g., 'A-D' or 'A,B,C')"
    ),
):
    """Create a new contest directory with problem files."""

    if "-" in problems:
        start, end = problems.split("-")
        problems_list = [chr(i) for i in range(ord(start), ord(end) + 1)]
    else:
        problems_list = problems.split(",")

    # List available templates
    templates = manager.list_templates()
    default_template = Path(manager.config.config["paths"]["template"]).name

    if templates:
        console.print("\nAvailable templates:")
        for idx, template in enumerate(templates):
            is_default = "(default)" if template == default_template else ""
            console.print(f"{idx}. {template} {is_default}")

        try:
            choice = typer.prompt(
                "\nChoose template number (press Enter for default)",
                default=-1,
                type=int,
            )
            template_name = templates[choice] if 0 <= choice < len(templates) else None
        except (ValueError, IndexError):
            template_name = None
    else:
        template_name = None

    contest_dir = manager.create_contest_dir(contest)
    manager.create_problem_files(contest_dir, problems_list, template_name)

    # Show creation summary
    table = Table(title=f"Contest {contest} Created")
    table.add_column("Problem", style="cyan")
    table.add_column("Files Created", style="green")
    table.add_column("Template", style="yellow")

    template_used = template_name or default_template
    for prob in problems_list:
        cpp_file = manager.config.get_problem_file_name(prob)
        txt_file = manager.config.get_input_file_name(prob)
        out_file = manager.config.get_output_file_name(prob)
        table.add_row(prob, f"{cpp_file}, {txt_file}, {out_file}", template_used)

    console.print(table)


@app.command()
def run(contest: str, problem: str, input_content: Optional[str] = None):
    """Compile and run a specific problem from a contest."""

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
def test(contest: str, problem: str):
    """Run a problem and verify output against expected output file."""

    contest_dir = Path(contest)
    problem_path = contest_dir / manager.config.get_problem_file_name(problem)
    input_path = contest_dir / manager.config.get_input_file_name(problem)
    output_path = contest_dir / manager.config.get_output_file_name(problem)

    if not output_path.exists():
        console.print(
            f"\n[yellow]Warning: Expected output file {output_path} not found![/yellow]"
        )
        console.print(
            "[yellow]Creating empty output file. Please add expected output to this file.[/yellow]"
        )
        output_path.touch()
        raise typer.Exit(1)

    with open(output_path) as f:
        expected_output = f.read()

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
    table.add_column(
        "Got", style="blue" if manager.verify_output(output, expected_output) else "red"
    )
    table.add_row(expected_output, output)
    console.print(table)


@app.command()
def iotest(contest: str, problem: str):
    """Interactively add input and expected output for a problem."""

    contest_dir = Path(contest)
    if not contest_dir.exists():
        console.print(f"[red]Contest directory '{contest}' not found!")
        raise typer.Exit(1)

    problem_path = contest_dir / manager.config.get_problem_file_name(problem)
    if not problem_path.exists():
        console.print(f"[red]Problem {problem} not found in contest {contest}!")
        raise typer.Exit(1)

    console.print(
        "\n[yellow]Paste your test input below (press Ctrl+D or Ctrl+Z on Windows when done):[/yellow]"
    )
    try:
        input_content = []
        while True:
            try:
                line = input()
                input_content.append(line)
            except EOFError:
                break
    except KeyboardInterrupt:
        console.print("\n[red]Input cancelled![/red]")
        raise typer.Exit(1)

    if not input_content:
        console.print("[red]No input provided![/red]")
        raise typer.Exit(1)

    input_text = "\n".join(input_content)
    manager.write_input(contest_dir, problem, input_text)
    console.print("\n[green]Test input saved successfully![/green]")

    console.print(
        "\n[yellow]Paste your expected output below (press Ctrl+D or Ctrl+Z on Windows when done):[/yellow]"
    )
    try:
        output_content = []
        while True:
            try:
                line = input()
                output_content.append(line)
            except EOFError:
                break
    except KeyboardInterrupt:
        console.print("\n[red]Output cancelled![/red]")
        raise typer.Exit(1)

    if output_content:
        output_text = "\n".join(output_content)
        manager.write_output(contest_dir, problem, output_text)
        console.print("\n[green]Expected output saved successfully![/green]")
    else:
        console.print(
            "\n[yellow]No expected output provided. You can add it later.[/yellow]"
        )

    table = Table(title=f"Test Case for Problem {problem}")
    table.add_column("Type", style="cyan")
    table.add_column("Content", style="green")
    table.add_row("Input", input_text)
    if output_content:
        table.add_row("Expected Output", output_text)
    console.print(table)

    if output_content and typer.confirm("\nWould you like to test the solution now?"):
        test(contest, problem)


@app.command()
def config(action: str = typer.Argument("show", help="Action to perform: show/update")):
    """Show or update configuration."""

    if action == "show":
        show_config()
    elif action == "update":
        update_config()
    else:
        console.print("[red]Invalid action. Use 'show' or 'update'[/red]")
        raise typer.Exit(1)


def show_config():
    """Display current configuration."""

    compiler_table = Table(title="Compiler Settings")
    compiler_table.add_column("Setting", style="cyan")
    compiler_table.add_column("Value", style="green")

    compiler_table.add_row("Compiler", manager.config.config["compile"]["command"])
    compiler_table.add_row("Flags", " ".join(manager.config.get_compiler_flags()))
    console.print(compiler_table)

    paths_table = Table(title="\nPath Settings")
    paths_table.add_column("Setting", style="cyan")
    paths_table.add_column("Value", style="green")

    for key, value in manager.config.config["paths"].items():
        paths_table.add_row(key.replace("_", " ").title(), str(value))
    console.print(paths_table)

    naming_table = Table(title="\nFile Naming Patterns")
    naming_table.add_column("File Type", style="cyan")
    naming_table.add_column("Pattern", style="green")

    for key, value in manager.config.config["file_naming"].items():
        naming_table.add_row(key.replace("_", " ").title(), value)
    console.print(naming_table)


def update_config():
    """Update configuration interactively."""
    options = [
        "Cancel",
        "Compiler",
        "Compiler Flags",
        "Default Template",
        "Templates Directory",
    ]

    console.print("\nWhat would you like to update?")
    for idx, option in enumerate(options):
        console.print(f"{idx}. {option}")

    try:
        choice_num = int(typer.prompt("Enter the number of your choice", default="0"))
    except ValueError:
        console.print("[red]Invalid input. Exiting.[/red]")
        return

    if not (0 <= choice_num < len(options)):
        console.print("[red]Choice out of range. Exiting.[/red]")
        return

    choice = options[choice_num]

    if choice == "Cancel":
        return

    if choice == "Compiler":
        new_compiler = typer.prompt(
            "Enter new compiler", default=manager.config.config["compile"]["command"]
        )
        manager.config.update_compiler(new_compiler)
        console.print("[green]Compiler updated successfully![/green]")

    elif choice == "Compiler Flags":
        current_flags = " ".join(manager.config.get_compiler_flags())
        new_flags = typer.prompt(
            "Enter compiler flags (space-separated)", default=current_flags
        )
        manager.config.update_compiler_flags(new_flags.split())
        console.print("[green]Compiler flags updated successfully![/green]")

    elif choice == "Default Template":
        template_path = typer.prompt(
            "Enter template path (relative to workspace)",
            default=manager.config.config["paths"]["template"],
        )
        manager.config.update_template(template_path)
        console.print("[green]Default template updated successfully![/green]")

    elif choice == "Templates Directory":
        templates_dir = typer.prompt(
            "Enter templates directory path",
            default=manager.config.config["paths"]["templates_dir"],
        )
        manager.config.update_templates_dir(templates_dir)
        console.print("[green]Templates directory updated successfully![/green]")

    show_config()


if __name__ == "__main__":
    app()
