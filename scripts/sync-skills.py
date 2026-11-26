from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / ".agents" / "skills"
TARGET = ROOT / ".claude" / "skills"

def main():
    for path in sorted(SOURCE.glob("*/SKILL.md")):
        destination = TARGET / path.parent.name / "SKILL.md"
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, destination)
    # Never delete an unexpected skill automatically. Validator reports drift.

if __name__ == "__main__":
    main()
