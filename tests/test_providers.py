"""No-network integration checks for official optional Groq provider and glossary."""
import os
import unittest
from unittest.mock import patch
import agent_engine as agents
from glossary import define_term

class ProviderAndMCPTests(unittest.TestCase):
    def test_groq_requires_secret_and_operator_enabled(self):
        with patch.dict(os.environ, {
            "AI_LLM_PROVIDER":"groq",
            "AI_AGENT_ENABLED":"1",
            "AGENT_ACCESS_TOKEN":"correct-horse-battery-staple-long"
        },clear=True):
            self.assertFalse(agents.configured())
        with patch.dict(os.environ, {
            "AI_LLM_PROVIDER":"groq",
            "AI_AGENT_ENABLED":"1",
            "AGENT_ACCESS_TOKEN":"correct-horse-battery-staple-long",
            "GROQ_API_KEY":"fake-test-groq-secret"
        },clear=True):
            self.assertTrue(agents.configured())
            self.assertEqual(agents.selection()[1],"openai/gpt-oss-20b")

    @patch("agent_engine._request")
    @patch("agent_engine.discover")
    def test_groq_calls_each_agent_with_usage_and_reference_costs(self, discover, model):
        discover.return_value=[{
            "title":"AI Learning Research","doi":"10.1000/abc",
            "doi_url":"https://doi.org/10.1000/abc",
            "year":2024,"publisher":"Example","title_relevance":0.95
        }]
        model.return_value={"id":"test-generation","usage":{"prompt_tokens":200,"completion_tokens":100},
                            "choices":[{"message":{"content":"Evidence is limited to bibliographic metadata."}}]}
        with patch.dict(os.environ,{
            "AI_LLM_PROVIDER":"groq",
            "AI_AGENT_ENABLED":"1",
            "AGENT_ACCESS_TOKEN":"correct-horse-battery-staple-long",
            "GROQ_API_KEY":"fake-test-groq-secret"
        },clear=True):
            result=agents.orchestrate("AI research ethics")
        self.assertEqual(model.call_count,3)
        self.assertEqual(result["billing"]["provider"],"Groq official API")
        self.assertEqual(result["billing"]["model"],"openai/gpt-oss-20b")
        self.assertEqual(result["billing"]["requests"],3)
        self.assertEqual(result["billing"]["input_tokens"],600)
        self.assertEqual(result["billing"]["output_tokens"],300)
        self.assertAlmostEqual(result["billing"]["estimated_usd"],0.000135,places=8)
        self.assertIn("not",result["billing"]["actual_provider_invoice"].lower())

    @patch("glossary.request_json")
    def test_dictionary_lookups_return_source(self, fetch):
        fetch.return_value=[{"meanings":[{"partOfSpeech":"noun","definitions":[{"definition":"A set of ideas."}]}]}]
        result=define_term("theory")
        self.assertEqual(result["definitions"][0]["part_of_speech"],"noun")
        self.assertEqual(result["provider"],"Free Dictionary API")
        self.assertIn("dictionaryapi.dev",fetch.call_args.args[0])

    def test_reject_injection(self):
        for value in ["http://localhost","a/../../b","x"*70]:
            with self.assertRaises(ValueError):
                define_term(value)

    def test_groq_has_no_vercel_credit_endpoint(self):
        with patch.dict(os.environ,{
            "AI_LLM_PROVIDER":"groq",
            "AI_AGENT_ENABLED":"1",
            "AGENT_ACCESS_TOKEN":"correct-horse-battery-staple-long",
            "GROQ_API_KEY":"fake-test-groq-secret"
        },clear=True):
            with self.assertRaises(agents.AgentError):
                agents.credit_balance()

if __name__=="__main__":
    unittest.main()
