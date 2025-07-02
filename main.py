from src.contest import ContestManager


def main():
    manager = ContestManager()

    contest_number = "1850"
    problems = ["A", "B", "C"]

    contest_dir = manager.create_contest_dir(contest_number)
    manager.create_problem_files(contest_dir, problems)

    problem_path = contest_dir / manager.config.get_problem_file_name("A")
    input_path = contest_dir / manager.config.get_input_file_name("A")

    with open(input_path, "w") as f:
        f.write("2\n3\n5\n")

    output, error, success = manager.compile_and_run(problem_path, input_path)
    if success:
        print(f"Output:\n{output}")
    else:
        print(f"Error:\n{error}")


if __name__ == "__main__":
    main()
