import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "scripts" / "build_dashboard.py"


class DashboardBuilderTest(unittest.TestCase):
    def test_builds_dashboard_data_from_archive_and_active_drafts(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            archive = tmp_path / "archive"
            archive.mkdir()
            (archive / "POSTS.md").write_text(
                "# LinkedIn post archive index\n\n"
                "## 2026-10-25T13:38:01+00:00\n\n"
                "- Hook: Example hook line.\n"
                "- LinkedIn URN: `urn:li:share:0000000000000000001`\n"
                "- Topic: Example topic\n\n"
                "## 2026-09-09T15:38:25+00:00\n\n"
                "- Hook: Older post.\n"
                "- LinkedIn URN: `urn:li:share:older`\n"
                "- Topic: Old topic\n"
            )
            active = tmp_path / "ACTIVE.md"
            active.write_text("1. [[example-draft]] — `posted`; verified.\n")
            out = tmp_path / "data.json"

            result = subprocess.run(
                [sys.executable, str(BUILD), "--archive", str(archive), "--active", str(active), "--out", str(out)],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            data = json.loads(out.read_text())
            self.assertEqual(data["analytics"]["status"], "not_connected")
            self.assertEqual(data["latest_posts"][0]["hook"], "Example hook line.")
            self.assertEqual(data["latest_posts"][0]["urn"], "urn:li:share:0000000000000000001")
            self.assertEqual(data["active_items"][0]["title"], "example-draft")
            self.assertTrue(any(source["type"] == "RSS" for source in data["sources"]))
            self.assertTrue(any(job["name"] == "Research menu" for job in data["queues"]))
