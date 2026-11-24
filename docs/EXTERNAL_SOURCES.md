# Reviewed community API and MCP references · 2026-11-24

These are source materials supplied for the AI Lab project. They are not automatically trusted dependencies. GitHub README claims are not guarantees of service uptime, security, pricing or authorization.

| Reference | What the project actually provides | Adoption decision |
|---|---|---|
| [chatanywhere/GPT_API_free](https://github.com/chatanywhere/GPT_API_free) | A third-party compatible model API relay. README offers a personal, non-commercial free-key tier with quotas and warns about public/commercial use. | **Do not connect by default**: provenance, data routing, availability and licensing differ from official provider APIs. |
| [fangzesheng/free-api](https://github.com/fangzesheng/free-api) | Chinese-language directory linking many unrelated public API services. | Reference **catalogue only**; inspect providers individually before integration. |
| [mnfst/awesome-free-llm-apis](https://github.com/mnfst/awesome-free-llm-apis) | Curated list of free-tier LLM inference providers and rate limits. | Discovery resource; current official provider terms and model IDs take priority. |
| [open-free-llm-api/awesome-freellm-apis](https://github.com/open-free-llm-api/awesome-freellm-apis) | Frequently updated directory of free-model providers. | Discovery and comparison only. No automatic key harvesting or scraping. |
| [meetDeveloper/freeDictionaryAPI](https://github.com/meetDeveloper/freeDictionaryAPI) | Free English dictionary API at api.dictionaryapi.dev, v2. | **Integrated:** allowlisted `glossary.define_term` and FastMCP `explain_english_term`. Definitions are not evidence of scientific claims. |
| [jellyfin/jellyfin](https://github.com/jellyfin/jellyfin) | A GPL-licensed self-hosted .NET media server. | **Not relevant** to academic literature research; no dependency added. |
| [public-apis/public-apis](https://github.com/public-apis/public-apis) | Public API directory, now with extensive APILayer promotion. | Discovery only; it does not itself guarantee providers are free or safe. |
| [GitHub MCP repository search](https://github.com/search?q=MCP&type=repositories) | Search results may include unofficial or unmaintained servers. | **Use audited implementations.** Our own read-only tools use FastMCP; consult [MCP reference servers](https://github.com/modelcontextprotocol/servers) and the [MCP Registry](https://registry.modelcontextprotocol.io/) before adding third-party servers. |

## Official inference routes selected

1. **Groq Cloud**: official OpenAI-compatible API (`api.groq.com/openai/v1`), model `openai/gpt-oss-20b` from its currently published model list. Free plan may be available, subject to account-level limits, verification and terms. Groq's official list shows $0.075/1M input and $0.30/1M output tokens outside an eligible free allowance. This is NOT a live billing guarantee.
2. **Vercel AI Gateway**: official `ai-gateway.vercel.sh/v1`, `google/gemini-2.5-flash-lite`, catalog reference $0.10/1M input and $0.40/1M output.
3. **Crossref API**: source of publication metadata. Model responses must link to the retrieved DOI URLs, not invented references.

## Integration and security rules

- Require private provider-issued keys; do not expose them to browsers or check them into Git.
- Keep model host allowlisted in source code; do not permit user-supplied arbitrary API bases or proxy URLs.
- Provider terms, free allowances and model availability must be checked on official pages before charging or launching commercially.
- Free tiers may impose account verification, daily usage limits, and reduced data retention guarantees.
- The per-run reference cost estimate is not an invoice. Official provider billing remains authoritative.
- Run third-party MCP servers only after reviewing permissions, source, network endpoints and tool actions. Reference MCP implementations explicitly warn they are educational examples, not production-ready servers.

## Official references

- [Groq models](https://console.groq.com/docs/models)
- [Groq OpenAI compatibility](https://console.groq.com/docs/openai)
- [Groq rate limits](https://console.groq.com/docs/rate-limits)
- [Vercel AI Gateway usage](https://vercel.com/docs/ai-gateway/observability-and-spend/usage)
- [MCP protocol](https://modelcontextprotocol.io/)
