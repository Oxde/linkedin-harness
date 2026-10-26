import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

SPEC = importlib.util.spec_from_file_location("clean", Path(__file__).resolve().parents[2] / "skills" / "anti-ai-writing" / "scripts" / "clean.py")
clean = importlib.util.module_from_spec(SPEC)
sys.modules["clean"] = clean
SPEC.loader.exec_module(clean)


class CleanTest(unittest.TestCase):
    def test_removes_invisible_and_odd_spaces_only(self):
        text, counts = clean.clean("a​b c’d", plain_punct=False)
        self.assertEqual(text, "ab c’d")
        self.assertEqual(counts, {"invisible characters": 1, "odd spaces": 1})
        self.assertEqual(clean.clean("’…", plain_punct=True)[0], "'...")

    def test_flags_words_shapes_and_bait(self):
        kinds = {(f.line, f.kind) for f in clean.check("We leverage it.\nIt's not the model. It's the loop.\nThe result?\nThoughts?", [])}
        self.assertIn((1, "banned word"), kinds)
        self.assertIn((2, "fake contrast"), kinds)
        self.assertIn((3, "staged reveal"), kinds)
        self.assertIn((4, "engagement bait"), kinds)
        self.assertNotIn((4, "closing question"), kinds)

    def test_concrete_post_passes(self):
        post = "Acme Labs cut our agent bill from $31 to $3.10.\n\nSame findings over 41 runs. Long plans still drift."
        self.assertEqual(clean.check(post, []), [])

    def test_weak_hook_and_voice_words(self):
        self.assertIn("weak hook", {f.kind for f in clean.check("this is something everyone should know", [])})
        with tempfile.TemporaryDirectory() as tmp:
            voice = Path(tmp) / "VOICE.md"
            voice.write_text("- **Words I never use:** synergies, hustle\n")
            words = clean.voice_words(voice)
        self.assertEqual(words, ["synergies", "hustle"])
        self.assertIn("banned word", {f.kind for f in clean.check("Acme loves the hustle.", words)})


if __name__ == "__main__":
    unittest.main()
