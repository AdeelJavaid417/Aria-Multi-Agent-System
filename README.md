# 🤖 ARIA - Advanced Reasoning & Intelligence Agent

A powerful multi-agent CLI system built with LangChain, LangGraph, and Groq API.

## Features

- **Intelligent Conditional Routing**: Automatically routes tasks to the best-fit agent
- **Tool Use & Function Calling**: Integrates with Tavily Search and other tools
- **Chain-of-Thought Reasoning**: Agents think step-by-step before acting
- **ReAct Pattern**: Reason → Act → Observe cycles
- **Persistent Memory**: ChromaDB vector store for semantic memory
- **Multi-Agent Orchestration**: Seamless coordination between agents
- **MCP Server Ready**: Can be integrated with Claude via Model Context Protocol

## Agents

### 🔬 Research Agent
- Gathers information from the web
- Analyzes and synthesizes findings
- Conducts deep research on topics
- Verifies claims

### ✍️ Creative Agent
- Generates creative content
- Writes blog posts and tutorials
- Brainstorms ideas
- Enhances and refines content

### 💻 Technical Agent
- Analyzes and debugs code
- Optimizes algorithms
- Conducts code reviews
- Provides technical solutions

## Installation

```bash
# Clone repository
git clone <repo-url>
cd aria_system

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Tavily (for web search)
pip install langchain-tavily

# Set up environment
cp .env.example .env
# Edit .env and add your API keys
```

## Setup

### 1. Get Tavily API Key
- Visit [Tavily Console](https://tavily.com)
- Sign up for free account
- Create API key
- Add to `.env`:
  ```
  TAVILY_API_KEY=your_key_here
  ```

### 2. Get Groq API Key
- Visit [Groq Console](https://console.groq.com)
- Create API key
- Add to `.env`:
  ```
  GROQ_API_KEY=your_key_here
  GROQ_MODEL=llama-3.3-70b-versatile
  ```

### 3. Create `.env` file
```env
GROQ_API_KEY=your_groq_key
TAVILY_API_KEY=your_tavily_key
GROQ_MODEL=llama-3.3-70b-versatile
DEBUG=True
LOG_LEVEL=INFO
ENABLE_WEB_SEARCH=True
ENABLE_CODE_EXECUTION=True
ENABLE_MEMORY=True
```

## Usage

### Run a Task
```bash
python -m main run "Research machine learning and write a beginner guide"
```

### Interactive Chat Mode
```bash
python -m main chat
```

### Research Command
```bash
python -m main research "quantum computing" --deep
```

### Write Content
```bash
python -m main write "Python async programming" --style blog
```

### Analyze Code
```bash
python -m main analyze-code
# Then paste your code and enter 'END' when done
```

### View Status
```bash
python -m main status
```

### View History
```bash
python -m main history --limit 20
```

### Clear Memory
```bash
python -m main clear-memory
```

## Command Examples

### Research + Writing
```bash
aria run "Research the latest AI breakthroughs and write a comprehensive article"
```

### Code Review
```bash
aria run "Review my Python function for bugs and performance issues"
```

### Tutorial Creation
```bash
aria write "Getting started with Docker" --style tutorial
```

### Multi-step Analysis
```bash
aria run "Search for best practices in microservices architecture, write a guide, and analyze sample code"
```

## Architecture

```
┌─────────────────────────────────────────┐
│         CLI Interface (Typer)           │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│      Task Orchestrator (Router)         │
│  • Classification                       │
│  • Conditional Routing                  │
└──────────────────┬──────────────────────┘
                   │
       ┌───────────┼───────────┐
       │           │           │
   ┌───▼──┐  ┌────▼───┐  ┌───▼───┐
   │Rsrch │  │Crtive  │  │ Tech  │
   │Agent │  │ Agent  │  │ Agent │
   └───┬──┘  └────┬───┘  └───┬───┘
       │          │          │
       └──────────┼──────────┘
                  │
          ┌───────▼────────┐
          │  Tools Layer   │
          │ • Tavily Search│
          │ • Code Execute │
          │ • Data Fetch   │
          └───────┬────────┘
                  │
          ┌───────▼────────┐
          │  Memory Layer  │
          │ • ChromaDB     │
          │ • SQLite       │
          └────────────────┘
```

## Project Structure

```
aria_system/
├── src/
│   ├── main.py                    # CLI entry point
│   ├── config.py                  # Configuration
│   ├── agents/                    # Agent implementations
│   ├── routing/                   # Task routing logic
│   ├── tools/                     # Tool integrations
│   ├── reasoning/                 # Reasoning engines
│   ├── memory/                    # Memory systems
│   ├── graph/                     # LangGraph workflow
│   ├── prompts/                   # LLM prompts
│   └── utils/                     # Utilities
├── tests/                         # Tests
├── data/                          # Data storage
├── requirements.txt               # Dependencies
├── .env                           # Configuration
└── README.md                      # This file
```

## Performance

- **Average Task Execution**: ~5-10 seconds
- **Tool Calls**: 50-100ms per call
- **Memory Operations**: <10ms per query
- **LLM Response**: 1-3 seconds

## Limitations

- Code execution is sandboxed and restricted
- Web search limited to Tavily rate limits
- Memory is local (can be extended to distributed)
- CLI is synchronous (async support coming)

## Future Enhancements

- [ ] MCP Server integration
- [ ] Async/parallel agent execution
- [ ] Distributed memory store
- [ ] Advanced tool chaining
- [ ] Custom agent creation
- [ ] Web UI interface
- [ ] Integration with Claude/GPT-4
- [ ] Advanced monitoring and logging

## Troubleshooting

### Tavily API key not working
- Verify key is correct and active
- Check rate limits
- Ensure .env file is properly loaded

### Agents not executing
- Check Groq API key
- Verify model name
- Check logs for errors

### Memory not persisting
- Ensure `data/memories` directory exists
- Check ChromaDB permissions
- Verify `ENABLE_MEMORY=True`

## License

MIT License - see LICENSE file

## Support

For issues, questions, or suggestions:
- Open GitHub issue
- Check existing issues first
- Provide clear reproduction steps

