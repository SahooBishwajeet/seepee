import os
import shutil
import subprocess
from typing import Optional
from pathlib import Path
from .config import Config


class ContestManager:
    def __init__(self):
        self.config = Config()

    def create_contest_dir(self, contest_number: str) -> Path:
        contest_dir = self.config.get_workspace_path() / contest_number
        contest_dir.mkdir(parents=True, exist_ok=True)
        return contest_dir

    def create_problem_files(
        self,
        contest_dir: Path,
        problem_numbers: list[str],
        template_name: Optional[str] = None,
    ):
        template_path = self.get_template_path(template_name)

        for prob in problem_numbers:
            prob_file = contest_dir / self.config.get_problem_file_name(prob)
            input_file = contest_dir / self.config.get_input_file_name(prob)
            output_file = contest_dir / self.config.get_output_file_name(prob)

            if not prob_file.exists():
                shutil.copy2(template_path, prob_file)
            if not input_file.exists():
                input_file.touch()
            if not output_file.exists():
                output_file.touch()

    def compile_and_run(
        self, problem_path: Path, input_path: Path
    ) -> tuple[str, str, bool]:
        problem_name = problem_path.stem
        executable = str(problem_path.parent / problem_name)

        compile_cmd = self.config.get_compile_command(str(problem_path), executable)
        run_cmd = self.config.get_run_command(executable, str(input_path))

        try:
            subprocess.run(compile_cmd, shell=True, check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            return "", e.stderr.decode(), False

        try:
            result = subprocess.run(
                run_cmd, shell=True, check=True, capture_output=True, text=True
            )
            return result.stdout, result.stderr, True
        except subprocess.CalledProcessError as e:
            return "", e.stderr, False
        finally:
            if os.path.exists(executable):
                os.remove(executable)

    def verify_output(self, actual_output: str, expected_output: str) -> bool:
        actual = actual_output.strip().splitlines()
        expected = expected_output.strip().splitlines()
        return actual == expected

    def write_input(self, contest_dir: Path, problem: str, content: str) -> None:
        input_path = contest_dir / self.config.get_input_file_name(problem)
        with open(input_path, "w") as f:
            f.write(content.strip() + "\n")

    def write_output(self, contest_dir: Path, problem: str, content: str) -> None:
        output_path = contest_dir / self.config.get_output_file_name(problem)
        with open(output_path, "w") as f:
            f.write(content.strip() + "\n")

    def list_templates(self) -> list[str]:
        templates_dir = self.config.get_templates_dir()
        if not templates_dir.exists():
            return []

        return [f.name for f in templates_dir.glob("*.cpp")]

    def get_template_path(self, template_name: str = None) -> Path:
        if template_name:
            template_path = self.config.get_templates_dir() / template_name
            if template_path.exists():
                return template_path
        return self.config.get_template_path()
