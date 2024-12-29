# GACS - Git Auto Commit Script

GACS - Git Auto Commit Script is a Python script that automatically commits changes to your Git repository. It watches for file changes in real-time and handles git operations automatically with customizable debounce timing. It also supports remote pushing and branch selection.

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
- `watchdog` for file watching (i created this script using v6.0.0 (current stable as of writing this) and the script just installs the latest version)

## Installation and Usage

1. Clone the repository:
```bash
git clone https://github.com/FurqanHun/GACS-py.git
```
2. Change directory:
```bash
cd GACS-py
```
3. Run the script:
```bash
python main.py
```

## Why create this script?

1. I could use `inotify-tools`, but there's no windows equivalent and you've to rely on github actions or other CI/CD tools.
2. I could also create a simple bash script and create a task scheduler in Windows, but it doesn't account for real-time file watching.
3. I could also create a powershell script, but no one sane installs powershell on Linux.
4. I wanted a script that can run on both Linux and Windows and can be used for personal projects.
5. Python is preinstalled on most Linux distros and you probably have it installed on Windows too.

If i find something for windows then i may update or create a shell script that handles both Linux and Windows.

_Before someone mentions the `inotify-tools` port `inotify-win`, i already know about it and yet have too look into it._

Feel free to contribute or suggest changes.

## License
Licensed under the GPLv3 License. See [LICENSE](LICENSE) for more information.

_Tested on Fedora 41 and Windows 10_
