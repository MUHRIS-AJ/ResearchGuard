"""Offline tests for real LLM agent orchestration, authorization and spend attribution."""
import os
import unittest
from unittest.mock import patch

import agent_engine as eng

SOURCE = [
    {"title": "AI in Higher Education", "doi": "10.1000/abc",
     "doi_url": "https://doi.org/10.1000/abc",
     "year": 2024, "publisher": "Test Press", "title_relevance": 0.92}
]
SETUP = {
    "AI_AGENT_ENABLED": "1",
    "AGENT_ACCESS_TOKEN": "a-strong-operator-secret-of-32-characters",
    "VERCEL_OIDC_TOKEN": "test-only-nonreal-oidc"
}

class AgentTests(unittest.TestCase):
    def test_disabled_by_default(self):
        with patch.dict(os.environ, {"AI_AGENT_ENABLED":"0"}, clear=True):
            self.assertFalse(eng.configured())

    @patch("agent_engine._request")
    @patch("agent_engine.discover", return_value=SOURCE)
    def test_three_real_separate_calls_and_billing(self, discover, gateway):
        responses = ["Metadata summary with DOI https://doi.org/10.1000/abc.",
                     "Do not infer article conclusions.",
                     "Verified references: https://doi.org/10.1000/abc. Full text not reviewed."]
        gateway.side_effect = [
            {"id":"gen-"+str(i+1),"choices":[{"message":{"content":value}}],
             "usage":{"prompt_tokens":200,"completion_tokens":100}}
            for i,value in enumerate(responses)
        ]
        with patch.dict(os.environ, SETUP, clear=True):
            data = eng.orchestrate("AI in higher education")
        self.assertEqual(gateway.call_count, 3)
        self.assertEqual(discover.call_count, 1)
        self.assertEqual(data["billing"]["requests"], 3)
        self.assertEqual(data["billing"]["input_tokens"], 600)
        self.assertEqual(data["billing"]["output_tokens"], 300)
        self.assertAlmostEqual(data["billing"]["estimated_usd"],0.00018,places=8)
        self.assertEqual(len(data["stages"]),3)
        self.assertIn("Full text not reviewed",data["report"])
        self.assertEqual(data["stages"][0]["generation_id"],"gen-1")
        self.assertTrue(data["sources"][0]["doi_url"].startswith("https://doi.org/"))

    @patch("agent_engine._request")
    @patch("agent_engine.discover", return_value=SOURCE)
    def test_missing_usage_fails_closed(self, discover, gateway):
        gateway.return_value={"choices":[{"message":{"content":"Some text"}}]}
        with patch.dict(os.environ, SETUP, clear=True):
            with self.assertRaisesRegex(eng.AgentError,"omitted token usage"):
                eng.orchestrate("AI in higher education")

    @patch("agent_engine.discover", return_value=[])
    def test_no_sources_no_bill(self, _):
        with patch.dict(os.environ, SETUP, clear=True):
            data=eng.orchestrate("some topic")
        self.assertEqual(data["billing"]["requests"],0)
        self.assertEqual(data["billing"]["estimated_usd"],0)

    def test_disallowed_unconfigured(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(eng.AgentError):
                eng.orchestrate("some topic")
    def test_topic_length(self):
        with patch.dict(os.environ, SETUP, clear=True):
            with self.assertRaises(ValueError):
                eng.orchestrate("x")

    @patch("agent_engine._request")
    def test_credit_balance_fields_only(self, request):
        request.return_value={"balance":1.35,"total_spent":2,"internal_key":"must-not-leak"}
        with patch.dict(os.environ,SETUP,clear=True):
            self.assertEqual(eng.credit_balance(),{"balance":1.35,"total_spent":2})

if __name__=="__main__":
    unittest.main()
