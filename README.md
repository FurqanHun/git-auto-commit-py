# GACS - Git Auto Commit Script

GACS is a Python script that automatically commits and pushes changes to your Git repository. It watches for file changes in real-time and handles git operations automatically with customizable debounce timing. It also supports remote pushing and branch selection.

## Features

- Real-time file watching
- Customizable debounce timing
- Support for specific file patterns
- Branch selection
- Optional remote pushing
- File ignoring (kind of, as it's harcoded for now)
- Detailed commit messages (also kind of, as modern apps makes changes in temp file and then rename it to original file, so it will commit it as "renamed file" instead of "changed file")
- Time-stamped commits (UTC)

## Prerequisites

- Python 3.x
- Git installed and configured (It assumes you already have a git repository initialized)
- Internet connection (for remote pushing)

The script will automatically check for and offer to install required Python packages:
- `watchdog`

## Installation and Usage

1. Clone the repository:
```bash
git clone https://github.com/FurqanHun/GACS-py.git
cd GACS-py
```

2. Run the script:
```bash
python main.py
```

## Why create this script?

I could use `inotify-tools`, but there's no windows equivalent and you've to rely on github actions or other CI/CD tools.
I could create a simple bash script and create a task scheduler in Windows, but it doesn't account for real-time file watching.
I could create a powershell script, but no one sane installs powershell on Linux.
I wanted a script that can run on both Linux and Windows and can be used for personal projects.
Python is preinstalled on most Linux distros and you probably have it installed on Windows too.

If i find something for windows then i may update or create a shell script that handles both Linux and Windows.

Feel free to contribute or suggest changes.

## License
Licensed under the GPLv3 License. See [LICENSE](LICENSE) for more information.
