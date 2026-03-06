"""
auto_commit.py
--------------
Automatically makes realistic-looking commits to a GitHub repository.
Run: python auto_commit.py
"""

import os
import random
import subprocess
import datetime
import string
import time

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────

MODIFIABLE_FILES = ["activity_log.txt", "random_data.py", "notes.md"]
MAX_COMMITS_PER_RUN = 5   # Will pick 1–5 randomly
DELAY_BETWEEN_COMMITS = (5, 30)  # seconds (min, max)

COMMIT_MESSAGES = [
    "refactor helper function",
    "update logging",
    "minor improvements",
    "cleanup unused code",
    "fix edge case in data processing",
    "add comments for clarity",
    "update utility functions",
    "improve error handling",
    "remove redundant checks",
    "code style cleanup",
    "update config defaults",
    "optimize loop logic",
    "fix typo in variable name",
    "add debug notes",
    "patch minor bug",
    "adjust output format",
    "update activity tracker",
    "refactor for readability",
    "streamline data flow",
    "minor logic fix",
]

# ─────────────────────────────────────────────
# RANDOM CONTENT GENERATORS
# ─────────────────────────────────────────────

def random_word(length=None):
    length = length or random.randint(4, 10)
    return ''.join(random.choices(string.ascii_lowercase, k=length))

def random_sentence():
    words = [random_word() for _ in range(random.randint(4, 10))]
    return ' '.join(words).capitalize() + '.'

def random_timestamp():
    now = datetime.datetime.now()
    delta = datetime.timedelta(
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59),
        seconds=random.randint(0, 59)
    )
    return (now - delta).strftime("%Y-%m-%d %H:%M:%S")

def random_log_lines(count):
    levels = ["INFO", "DEBUG", "WARNING", "ERROR"]
    modules = ["auth", "data_loader", "parser", "cache", "utils", "scheduler", "api"]
    lines = []
    for _ in range(count):
        ts = random_timestamp()
        level = random.choice(levels)
        module = random.choice(modules)
        msg = random_sentence()
        lines.append(f"[{ts}] [{level}] [{module}] {msg}")
    return lines

def random_python_snippet(count):
    """Generates realistic-looking Python lines."""
    snippets = []
    for _ in range(count):
        kind = random.randint(0, 5)
        if kind == 0:
            snippets.append(f"# {random_sentence()}")
        elif kind == 1:
            var = random_word()
            val = random.randint(1, 9999)
            snippets.append(f"{var} = {val}")
        elif kind == 2:
            var = random_word()
            snippets.append(f"{var} = '{random_word()}'")
        elif kind == 3:
            func = random_word()
            arg = random_word()
            snippets.append(f"def {func}({arg}):")
            snippets.append(f"    return {arg}")
        elif kind == 4:
            lst = [str(random.randint(1, 100)) for _ in range(random.randint(3, 6))]
            var = random_word()
            snippets.append(f"{var} = [{', '.join(lst)}]")
        else:
            snippets.append(f"print('{random_sentence()}')")
    return snippets

def random_markdown_lines(count):
    headers = ["Update", "Note", "Log", "Info", "Fix", "Change"]
    lines = []
    for _ in range(count):
        kind = random.randint(0, 3)
        if kind == 0:
            lines.append(f"## {random.choice(headers)} – {random_timestamp()}")
        elif kind == 1:
            lines.append(f"- {random_sentence()}")
        elif kind == 2:
            lines.append(f"> {random_sentence()}")
        else:
            lines.append(random_sentence())
    return lines

# ─────────────────────────────────────────────
# FILE OPERATIONS
# ─────────────────────────────────────────────

def ensure_file_exists(filepath):
    """Creates a file with initial content if it doesn't exist."""
    if not os.path.exists(filepath):
        ext = os.path.splitext(filepath)[1]
        with open(filepath, 'w') as f:
            if ext == '.py':
                f.write("# Auto-generated file\n\n")
            elif ext == '.md':
                f.write("# Project Notes\n\n")
            else:
                f.write("# Activity Log\n\n")
        print(f"  Created new file: {filepath}")

def modify_file(filepath):
    """Appends or rewrites a section of a file with random content."""
    ensure_file_exists(filepath)
    ext = os.path.splitext(filepath)[1]
    line_count = random.choices(
        [random.randint(1, 2), random.randint(10, 30)],
        weights=[0.6, 0.4]
    )[0]

    if ext == '.py':
        new_lines = random_python_snippet(line_count)
    elif ext == '.md':
        new_lines = random_markdown_lines(line_count)
    else:
        new_lines = random_log_lines(line_count)

    with open(filepath, 'a') as f:
        f.write('\n')
        f.write('\n'.join(new_lines))
        f.write('\n')

    print(f"  Modified: {filepath} (+{line_count} lines)")

def create_new_random_file():
    """Occasionally creates a brand-new file."""
    name = f"module_{random_word()}.py"
    lines = ["# Auto-generated module\n"]
    lines += random_python_snippet(random.randint(5, 15))
    with open(name, 'w') as f:
        f.write('\n'.join(lines))
    print(f"  Created new file: {name}")

# ─────────────────────────────────────────────
# GIT OPERATIONS
# ─────────────────────────────────────────────

def run_command(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  [ERROR] Command failed: {cmd}")
        print(f"  stderr: {result.stderr.strip()}")
    return result.returncode == 0

def git_commit_and_push():
    message = random.choice(COMMIT_MESSAGES)
    print(f"  Committing: '{message}'")
    ok = (
        run_command("git add .")
        and run_command(f'git commit -m "{message}"')
        and run_command("git push")
    )
    if ok:
        print("  ✓ Pushed successfully.")
    else:
        print("  ✗ Push failed — check git config / network.")
    return ok

# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

def make_changes():
    """Make random file changes for a single commit."""
    should_create_new = random.random() < 0.15  # 15% chance

    if should_create_new:
        create_new_random_file()

    files_to_change = random.sample(
        MODIFIABLE_FILES, k=random.randint(1, len(MODIFIABLE_FILES))
    )
    for filepath in files_to_change:
        modify_file(filepath)

def main():
    num_commits = random.randint(1, MAX_COMMITS_PER_RUN)
    print(f"\n🚀 auto_commit.py — Running {num_commits} commit(s) this session\n")

    for i in range(1, num_commits + 1):
        print(f"── Commit {i}/{num_commits} ──────────────────────")
        make_changes()
        success = git_commit_and_push()

        if not success:
            print("  Stopping early due to git error.")
            break

        if i < num_commits:
            delay = random.randint(*DELAY_BETWEEN_COMMITS)
            print(f"  Waiting {delay}s before next commit...\n")
            time.sleep(delay)

    print("\n✅ Done.\n")

if __name__ == "__main__":
    main()
