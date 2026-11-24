import unittest
from unittest.mock import patch
import core

class ResearchTests(unittest.TestCase):
    @patch("core.request_json")
    def test_discovery_and_deduplication(self, fake):
        fake.return_value = {"message": {"items": [
            {"title":["Machine Learning in Healthcare"],"DOI":"10.1000/abc","publisher":"Example","published":{"date-parts":[[2024]]}},
            {"title":["Duplicate"],"DOI":"10.1000/abc"},
            {"title":["No DOI"]}
        ]}}
        data = core.report("machine learning")
        self.assertEqual(data["paper_count"], 1)
        self.assertEqual(data["papers"][0]["doi_url"], "https://doi.org/10.1000/abc")
        self.assertIn("limitations", data)

    @patch("core.request_json")
    def test_verify(self, fake):
        fake.return_value = {"message": {"title":["A Study"],"DOI":"10.1000/abc"}}
        self.assertTrue(core.verify_doi("10.1000/abc")["metadata_verified"])

    def test_input_safety(self):
        with self.assertRaises(ValueError):
            core.verify_doi("https://localhost/admin")
        with self.assertRaises(ValueError):
            core.run("test", "Nonexistent")

    def test_source_failure_not_fabricated(self):
        with patch("core.request_json", side_effect=core.SourceError("offline")):
            with self.assertRaises(core.SourceError):
                core.report("relevant papers")

if __name__ == "__main__":
    unittest.main()
