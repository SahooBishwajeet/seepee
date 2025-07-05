# SeePee

SeePee is a terminal-based application to help with CodeForces contest participation. It provides both CLI and TUI interfaces to manage contest directories, test cases, and problem solutions.

## Features

- Create contest directories with customizable templates
- Multiple template support
- Interactive test case management
- Compile and run solutions with custom compiler flags
- Test solutions against expected outputs
- Both Command Line Interface (CLI) and Terminal User Interface (TUI)
- Keyboard navigation support in TUI
- Configurable settings

## Installation

1. Clone the repository:

```bash
git clone git@github.com:SahooBishwajeet/seepee.git
cd seepee
```

2. Install dependencies:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

OR

```bash
uv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
uv pip install -r requirements.txt
```

## Configuration

The configuration file is located at `config/config.yaml`. Example configuration:

```yaml
paths:
  template: templates/template.cpp # Default template
  templates_dir: templates/ # Templates directory
  workspace: . # Working directory

compile:
  command: g++
  flags:
    - -Wall
    - -Wextra
    - -Wconversion
    - -std=c++20
    - -lfmt

file_naming:
  problem: "{}.cpp" # Problem file naming pattern
  input: "{}.txt" # Input file naming pattern
  output: "{}_out.txt" # Output file naming pattern

commands:
  compile: "{compiler} {flags} {source} -o {executable}"
  run: "./{executable} < {input_file}"
```

## Usage

### CLI Mode

1. **Create a new contest:**

```bash
python main.py create 1234          # Creates contest 1234 with problems A-F
python main.py create 1234 A-D      # Creates problems A to D
python main.py create 1234 A,B,C    # Creates specific problems
```

2. **Run a problem:**

```bash
python main.py run 1234 A           # Runs problem A from contest 1234
python main.py run 1234 A "3\n1 2 3"  # Runs with specific input
```

3. **Test a problem:**

```bash
python main.py test 1234 A          # Tests problem A against expected output
```

4. **Add test cases interactively:**

```bash
python main.py iotest 1234 A        # Add input/output for problem A
```

5. **Manage configuration:**

```bash
python main.py config show          # Show current configuration
python main.py config update        # Update configuration
```

### TUI Mode

Launch the Terminal User Interface:

```bash
python main.py tui
```

Navigation in TUI:

- Use arrow keys (↑/↓) to navigate between fields
- Press Enter to activate buttons
- Press Escape to go back/exit
- Use Tab to cycle through inputs
- Press 'q' to quit from main menu

#### TUI Screens:

1. **Main Menu**

   - Create Contest
   - Run Problem
   - Test Problem
   - Add Test Cases
   - Configuration

2. **Create Contest**

   - Enter contest number
   - Specify problem range
   - Choose template

3. **Run Problem**

   - Enter contest/problem
   - Input test case
   - View output

4. **Test Problem**

   - Enter contest/problem
   - Run against saved test cases
   - View comparison results

5. **Add Test Cases**

   - Enter contest/problem
   - Add input and expected output
   - Save or Save and Test

6. **Configuration**
   - Modify compiler settings
   - Update paths
   - Change templates
   - Reset to defaults

## Directory Structure

```
SeePee/
├── config/
│   └── config.yaml       # Configuration file
├── templates/
│   └── template.cpp      # Default CP template
├── src/
│   ├── __init__.py
│   ├── contest.py        # Contest management
│   ├── config.py         # Configuration handling
│   ├── tui.py            # TUI implementation
│   └── screens/          # TUI screens
│       ├── __init__.py
│       ├── base.py       # Base screen class
│       ├── config.py     # Configuration screen
│       ├── create.py     # Contest creation screen
│       ├── iotest.py     # IO testing screen
│       ├── menu.py       # Main menu screen
│       ├── run.py        # Problem running screen
│       └── test.py       # Problem testing screen
├── main.py               # Entry point
└── requirements.txt
```

## Contest Directory Structure

For a contest number 1234:

```
1234/
├── A.cpp        # Problem solution
├── A.txt        # Input file
├── A_out.txt    # Expected output
├── B.cpp
├── B.txt
└── B_out.txt
```
