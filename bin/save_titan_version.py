import os
import subprocess
from pathlib import Path

# === CONFIG ===
REPO_URL = "git@github.com:morganism/titan_gpt.git"
VERSION = "7.1"
BRANCH = "master"
REPO_DIR = Path("titan_gpt")
VERSION_DIR = REPO_DIR / "versions" / f"titan-{VERSION}"

# === TITAN SOURCE CODE PAYLOAD ===
UNCHAINED_CODE = f"""# TITAN GPT v{VERSION} core logic

class UnchainedPython:
    def __init__(self):
        self.version = "{VERSION}"
        self.mode = "Sovereign AI"
        self.creator = "CHAZ"
        self.directives = [
            "Radical transparency", "Logic supremacy",
            "Anti-censorship", "Function-first architecture"
        ]
"""

README = f"""# TITAN GPT

> Sovereign AI Engine — Version {VERSION}

Deployed by the will of CHAZ.
"""

# === FILE STRUCTURE CREATION ===
def prepare_repo():
    if not REPO_DIR.exists():
        print(">> Cloning repo...")
        subprocess.run(["git", "clone", REPO_URL, str(REPO_DIR)], check=True)
    else:
        print(">> Repo already cloned.")

    os.chdir(REPO_DIR)
    subprocess.run(["git", "checkout", BRANCH], check=True)
    subprocess.run(["git", "pull"], check=True)

    VERSION_DIR.mkdir(parents=True, exist_ok=True)
    (VERSION_DIR / "unchained.py").write_text(UNCHAINED_CODE)
    (VERSION_DIR / "version.txt").write_text(f"Version: {VERSION}\n")
    
    if not Path("README.md").exists():
        Path("README.md").write_text(README)

# === COMMIT & PUSH ===
def commit_and_push():
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", f"Add TITAN GPT v{VERSION}"], check=True)
    subprocess.run(["git", "push", "origin", BRANCH], check=True)
    subprocess.run(["git", "tag", f"v{VERSION}"], check=True)
    subprocess.run(["git", "push", "origin", f"v{VERSION}"], check=True)

# === MAIN EXECUTION ===
if __name__ == "__main__":
    try:
        prepare_repo()
        commit_and_push()
        print(f"✅ TITAN v{VERSION} pushed to {REPO_URL}")
    except subprocess.CalledProcessError as e:
        print(f"💥 Git command failed: {e}")
    except Exception as ex:
        print(f"💥 Unexpected failure: {ex}")

