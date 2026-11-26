import importlib.util
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

validator = load("validate-skills")
syncer = load("sync-skills")

class SharedSkillTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for directory in (".agents", ".claude"):
            shutil.copytree(ROOT / directory, self.root / directory)

    def test_registered_shared_skills_valid(self):
        self.assertEqual(validator.validate(self.root), [])

    def test_custom_skill_not_copied_or_rejected(self):
        custom = self.root / ".agents/skills/local-custom/SKILL.md"
        custom.parent.mkdir(parents=True)
        custom.write_text("Project-only skill")
        syncer.sync(self.root)
        self.assertFalse((self.root / ".claude/skills/local-custom/SKILL.md").exists())
        self.assertEqual(custom.read_text(), "Project-only skill")
        self.assertEqual(validator.validate(self.root), [])

    def test_changed_copy_rejected(self):
        target = next((self.root / ".claude/skills").glob("*/SKILL.md"))
        target.write_text("unexpected")
        self.assertTrue(validator.validate(self.root))
