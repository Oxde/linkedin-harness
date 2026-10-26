import datetime as dt
import importlib.util
import io
import json
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

SPEC = importlib.util.spec_from_file_location("linkedin_publish", Path(__file__).resolve().parents[1] / "linkedin_publish.py")
pub = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(pub)


class PublishTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.file = Path(self.tmp.name) / "post.txt"
        self.text = "Line one (with parens) and @mention.\n\n#agents"
        self.file.write_text(self.text + "\n")

    def tearDown(self):
        self.tmp.cleanup()

    def test_escapes_little_text_reserved_characters(self):
        self.assertEqual(pub.escape_commentary("a (b) @c #d"), "a \\(b\\) \\@c \\#d")

    def test_default_version_is_previous_month(self):
        self.assertEqual(pub.default_version(dt.date(2026, 1, 15)), "202512")
        self.assertEqual(pub.default_version(dt.date(2026, 10, 26)), "202609")

    def test_refuses_without_hash_and_on_changed_text(self):
        with self.assertRaisesRegex(SystemExit, "--sha256 is required"):
            pub.main([str(self.file)])
        with self.assertRaisesRegex(SystemExit, "text changed since approval"):
            pub.main([str(self.file), "--sha256", "0" * 64])

    def test_dry_run_prints_payload_and_never_calls_the_api(self):
        out = io.StringIO()
        with mock.patch.object(pub, "request") as req, mock.patch.dict(os.environ, {"LINKEDIN_AUTHOR_URN": "urn:li:person:abc"}), redirect_stdout(out):
            self.assertEqual(pub.main([str(self.file), "--sha256", pub.sha256(self.text)]), 0)
        req.assert_not_called()
        data = json.loads(out.getvalue())
        self.assertTrue(data["dry_run"])
        self.assertEqual(data["payload"]["author"], "urn:li:person:abc")
        self.assertIn("\\(with parens\\)", data["payload"]["commentary"])

    def test_post_sends_payload_and_reports_url(self):
        out = io.StringIO()
        env = {"LINKEDIN_ACCESS_TOKEN": "t", "LINKEDIN_AUTHOR_URN": "urn:li:person:abc", "LINKEDIN_API_VERSION": "202609"}
        with mock.patch.object(pub, "request", return_value=(201, {"x-restli-id": "urn:li:share:1"}, "")) as req, mock.patch.dict(os.environ, env), redirect_stdout(out):
            pub.main([str(self.file), "--sha256", pub.sha256(self.text), "--post"])
        url, token, version, body = req.call_args[0]
        self.assertEqual((url, token, version), (pub.POSTS_URL, "t", "202609"))
        self.assertEqual(body["lifecycleState"], "PUBLISHED")
        self.assertEqual(json.loads(out.getvalue())["url"], "https://www.linkedin.com/feed/update/urn:li:share:1/")

    def test_post_requires_token(self):
        with mock.patch.dict(os.environ, {"LINKEDIN_ACCESS_TOKEN": ""}), self.assertRaisesRegex(SystemExit, "LINKEDIN_ACCESS_TOKEN"):
            pub.main([str(self.file), "--sha256", pub.sha256(self.text), "--post"])


if __name__ == "__main__":
    unittest.main()
