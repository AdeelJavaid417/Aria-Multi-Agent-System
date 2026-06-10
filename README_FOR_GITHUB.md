# ARIA — Advanced Reasoning & Intelligence Agent

ARIA is a multi-agent CLI system that routes tasks to specialized agents (Research, Creative, Technical). It uses LangChain, LangGraph, and Groq for LLM-powered reasoning, Tavily for web search, ChromaDB for vector memory, and SQLite for metadata.

## Features

- Intelligent task classification and conditional routing
- Specialized agents: Research, Creative, Technical
- Web research integration (Tavily)
- Code analysis and execution tools
- Persistent semantic memory (ChromaDB) and metadata (SQLite)
- Interactive CLI (Typer + Rich)

## Quickstart

1. Create virtual env:

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Add API keys in `.env` (do NOT commit this file):

```env
GROQ_API_KEY=your_groq_key
TAVILY_API_KEY=your_tavily_key
GROQ_MODEL=mixtral-8x7b-32768
```

4. Run a simple task:

```bash
python main.py run "Research the latest AI breakthroughs"
```

## Usage

- Run single tasks: `python main.py run "<task>"`
- Interactive chat: `python main.py chat`
- Research (deep): `python main.py research "topic" --deep`
- Generate content: `python main.py write "topic" --style blog`
- Analyze code: `python main.py analyze_code`
- View status: `python main.py status`

## Project layout

```
Multi Agent System/
├── main.py
├── config.py
├── agents/
├── graph/
├── routing/
├── tools/
├── memory/
├── prompts/
├── utils/
└── data/
```

## Databases & Tools

- ChromaDB: semantic vector memory
- SQLite: task metadata & history
- Tavily: web search (requires API key)
- Groq: LLM provider (configure model & key)

## Git & Deployment

Suggested .gitignore includes venv, .env, data/memories, and logs. To initialize a repo and push:

```bash
git init
git add .
git commit -m "chore: initial commit"
git branch -M main
git remote add origin https://github.com/<username>/<repo>.git
git push -u origin main
```

Or use GitHub CLI:

```bash
gh repo create <username>/<repo> --public --source=. --remote=origin --push
```

## Notes & Troubleshooting

- Ensure `TAVILY_API_KEY` and `GROQ_API_KEY` are set in `.env`.
- If web search fails, confirm `langchain-tavily` is installed and importable.
- If ChromaDB is missing, install `chromadb` or disable memory in config.

## Contributing

PRs welcome. Add tests and documentation.

## License

MIT

---

