from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / ".agents" / "skills"
TARGET = ROOT / ".claude" / "skills"

def main():
    errors = []
    canonical = {p.parent.name: p for p in SOURCE.glob("*/SKILL.md")}
    copies = {p.parent.name: p for p in TARGET.glob("*/SKILL.md")}
    if not canonical:
        errors.append("No canonical skills found")
    if canonical.keys() != copies.keys():
        errors.append("Skill sets differ: " + str(sorted(canonical.keys() ^ copies.keys())))
    for name, path in sorted(canonical.items()):
        text = path.read_text(encoding="utf-8")
        match = re.match(r"\A---\nname: ([^\n]+)\ndescription: ([^\n]+)\n---\n", text)
        if not match:
            errors.append(f"{name}: invalid metadata")
            continue
        declared, description = match.groups()
        if declared != name or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or len(name) > 64:
            errors.append(f"{name}: invalid name")
        try:
            description = json.loads(description) if description.startswith('"') else description
        except ValueError:
            errors.append(f"{name}: invalid description quoting")
            continue
        if not isinstance(description, str) or not description.strip() or len(description) > 1024:
            errors.append(f"{name}: invalid description length")
        if name in copies and path.read_bytes() != copies[name].read_bytes():
            errors.append(f"{name}: generated copy differs")
        for ref in re.findall(r"`(\.\./[^ `]+/SKILL\.md)`", text):
            if not (path.parent / ref).is_file():
                errors.append(f"{name}: missing reference {ref}")
    cases = json.loads((ROOT / "docs" / "skill-evaluations.json").read_text(encoding="utf-8"))
    expected = {"positive", "negative", "boundary", "normal", "failure"}
    ids = [c["id"] for c in cases]
    if len(ids) != len(set(ids)):
        errors.append("Duplicate evaluation IDs")
    if {c["skill"] for c in cases} != set(canonical):
        errors.append("Evaluation skill set differs")
    for name in canonical:
        rows = [c for c in cases if c["skill"] == name]
        if len(rows) != 5 or {c["kind"] for c in rows} != expected:
            errors.append(f"{name}: missing or duplicate evaluation cases")
        if any(not c.get("request") or not c.get("success_criteria") for c in rows):
            errors.append(f"{name}: incomplete evaluation case")
    if errors:
        print("\n".join(errors))
        return 1
    print(f"Validated {len(canonical)} skills and {len(cases)} evaluation definitions; behavioral execution not implied.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
