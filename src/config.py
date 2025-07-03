import os
import yaml
from pathlib import Path
from typing import Dict, Any, List


class Config:
    def __init__(self, config_path: str = "config/config.yaml"):
        self.config_path = Path(config_path)
        self.config = self.load_config()

    def load_config(self) -> Dict[str, Any]:
        if not self.config_path.exists():
            raise FileNotFoundError(
                f"Configuration file not found at {self.config_path}"
            )

        with open(self.config_path) as f:
            return yaml.safe_load(f)

    def save_config(self) -> None:
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, "w") as f:
            yaml.dump(self.config, f, default_flow_style=False)

    def get_compile_command(self, source_file: str, executable: str) -> str:
        flags = " ".join(self.config["compile"]["flags"])
        return self.config["commands"]["compile"].format(
            compiler=self.config["compile"]["command"],
            flags=flags,
            source=source_file,
            executable=executable,
        )

    def get_run_command(self, executable: str, input_file: str) -> str:
        return self.config["commands"]["run"].format(
            executable=executable, input_file=input_file
        )

    def get_problem_file_name(self, problem_number: str) -> str:
        return self.config["file_naming"]["problem"].format(problem_number)

    def get_input_file_name(self, problem_number: str) -> str:
        return self.config["file_naming"]["input"].format(problem_number)

    def get_output_file_name(self, problem_number: str) -> str:
        return self.config["file_naming"]["output"].format(problem_number)

    def get_template_path(self) -> Path:
        return Path(self.config["paths"]["template"])

    def get_workspace_path(self) -> Path:
        return Path(self.config["paths"]["workspace"])

    def get_templates_dir(self) -> Path:
        return Path(self.config["paths"]["templates_dir"])

    def update_config_value(self, section: str, key: str, value: Any) -> None:
        if section not in self.config:
            self.config[section] = {}
        self.config[section][key] = value
        self.save_config()

    def get_compiler_flags(self) -> List[str]:
        return self.config["compile"]["flags"]

    def update_compiler_flags(self, flags: List[str]) -> None:
        self.config["compile"]["flags"] = flags
        self.save_config()

    def update_compiler(self, compiler: str) -> None:
        self.config["compile"]["command"] = compiler
        self.save_config()

    def update_template(self, template: str) -> None:
        self.config["paths"]["template"] = template
        self.save_config()

    def update_templates_dir(self, templates_dir: str) -> None:
        self.config["paths"]["templates_dir"] = templates_dir
        self.save_config()
