import time
import os
import subprocess
import sys

def check_and_install(package_name):
    try:
        __import__(package_name)
    except ImportError:
        print(f"Package '{package_name}' is not installed.")

        print("Would you like to install it now? (y/n) Default is YES: ", end="")
        choice = input().strip().lower()
        if choice == 'n':
            print(f"Please install '{package_name}' manually.")
            sys.exit(1)

        else:
            try:
                print(f"Attempting to install '{package_name}' via pip...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
                print(f"Successfully installed '{package_name}'.")
            except subprocess.CalledProcessError:
                print(f"Could not install '{package_name}'. Please check your internet connection or install it manually.")

check_and_install("watchdog")

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

check_and_install("watchdog")
class AutoCommitHandler(PatternMatchingEventHandler):
    def __init__(self, repo_path, files_to_watch, branch, remote, debounce_time):
        self.repo_path = os.path.abspath(repo_path)
        self.branch = branch
        self.last_event_time = {}  # track last event time for each file
        self.remote = remote
        self.debounce_time = float(debounce_time)

        # patterns to watch
        patterns = ["*"] if "*" in files_to_watch else [f"*{f.strip()}" for f in files_to_watch]

        #  these would NOT be watched
        ignore_patterns = [
            "*.goutputstream-*",
            "*.swp",
            "*.swx",
            "*~",
            "*/.git/*",
            ".git/*",
            ".git",
            "*.pyc",
            "__pycache__/*"
        ]

        # initialize the parent class first with patterns
        super().__init__(
            patterns=patterns,
            ignore_patterns=ignore_patterns,
            ignore_directories=True,
            case_sensitive=True
        )

        print("Initialized watcher:")
        print(f"Repository path: {self.repo_path}")
        print(f"Watching patterns: {patterns}")
        print(f"Ignored patterns: {ignore_patterns}")
        print(f"Branch: {self.branch}")

    def on_modified(self, event):
            if not event.is_directory and not self._is_git_path(event.src_path):
                print(f"\nFile modified: {event.src_path}")
                self.handle_event(event.src_path, "modified")

    def on_created(self, event):
            if not event.is_directory and not self._is_git_path(event.src_path):
                print(f"\nFile created: {event.src_path}")
                self.handle_event(event.src_path, "created")

    def on_deleted(self, event):
            if not event.is_directory and not self._is_git_path(event.src_path):
                print(f"\nFile deleted: {event.src_path}")
                self.handle_event(event.src_path, "deleted")

    def on_moved(self, event):
            if not event.is_directory and not self._is_git_path(event.dest_path):
                print(f"\nFile moved/renamed: {event.src_path} -> {event.dest_path}")
                self.handle_event(event.dest_path, "renamed")

    def _is_git_path(self, path):
        """Check if the path is within .git directory"""
        rel_path = os.path.relpath(path, self.repo_path)
        return rel_path.startswith('.git') or '.git' in rel_path.split(os.sep)

    def handle_event(self, file_path, event_type):
        try:
            # Check debounce time first
            current_time = time.time()
            last_time = self.last_event_time.get(file_path, 0)
            elapsed_time = current_time - last_time

            # Debug print to see what's happening
            print(f"\nDebounce Check for {event_type}:")
            print(f"Time since last event: {elapsed_time:.2f} seconds")
            print(f"Required debounce time: {self.debounce_time} seconds")

            if elapsed_time < self.debounce_time:
                print(f"Skipping {event_type} - Not enough time elapsed ({elapsed_time:.2f} < {self.debounce_time} seconds)")
                return

            # Update last event time
            self.last_event_time[file_path] = current_time

            # change to repository directory
            os.chdir(self.repo_path)

            # relative pathing for file
            rel_path = os.path.relpath(file_path, self.repo_path)

            # deletion, handled a bit diff
            if event_type == "deleted":
                subprocess.run(['git', 'add', '--all'], check=True)
            else:
                # for mod and create, add the specific file
                subprocess.run(['git', 'add', rel_path], check=True)

            # checks if there are actually changes to commit
            status = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
            if not status.stdout.strip():
                print("No changes to commit")
                return

            # commit changes with a bit more detailed message
            commit_message = f"Auto-commit by {os.getlogin()}: {rel_path} was {event_type}\nTimestamp: {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}"
            subprocess.run(['git', 'commit', '-m', commit_message], check=True)
            print(f"Changes committed: {commit_message}")

            # push push push
            if self.remote:
                subprocess.run(['git', 'push', 'origin', self.branch], check=True)
                print(f"Changes pushed to {self.branch}")
            else:
                print("Remote push disabled. Changes not pushed.")
            print("\nWatching for file changes. Press Ctrl+C to stop.")

        except subprocess.CalledProcessError as e:
            print(f"Git operation failed: {e}")
        except Exception as e:
            print(f"Error handling {event_type} event: {e}")

if __name__ == "__main__":
    print("GACS - Git Auto Commit Script- 0xQan")
    print("Upstream repo: https://github.com/FurqanHun/GACS-py\n")

    while True:
        repo_path = input("Enter the path to the repository/dir: ").strip()
        if os.path.isdir(repo_path) and os.path.isdir(os.path.join(repo_path, '.git')):
            break
        print("Invalid repository path. Please ensure it's a git repository.")

    files_input = input("Enter the files to watch (separated by comma) Default is all: ").strip()
    files = [f.strip() for f in files_input.split(',')] if files_input else ["*"]

    branch = input("Enter the branch to push to (default is master): ").strip() or 'master'

    remote = input("Would you like to push to remote? (y/n) Default is NO: ").strip()
    if remote.lower() == 'y':
        remote = input("Enter the remote name (default is origin): ").strip() or 'origin'
    else:
        remote = None

    while True:
            try:
                debounce_input = input("Enter debounce time in seconds (default is 60): ").strip()
                debounce_time = int(debounce_input) if debounce_input else 60
                if debounce_time < 1:
                    print("Debounce time must be at least 1 second")
                    continue
                break
            except ValueError:
                print("Please enter a valid number")

    # build/start the observer
    event_handler = AutoCommitHandler(repo_path, files, branch, remote, debounce_time)
    observer = Observer()
    observer.schedule(event_handler, repo_path, recursive=True)
    observer.start()

    print("\nWatching for file changes. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping file watch...")
        observer.stop()
    observer.join()
