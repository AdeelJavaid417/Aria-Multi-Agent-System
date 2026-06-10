# 🤖 ARIA System - Setup & Run Guide

## **All Errors Fixed! ✅**

The project has been corrected with:
- ✅ All missing `__init__.py` files created in packages
- ✅ ChromaDB configuration updated to new API
- ✅ Import paths corrected (removed `src.` prefix)
- ✅ Tool function exports fixed
- ✅ Prompt imports corrected
- ✅ Tavily API key configuration added

---

## **Step 1: Install Dependencies**

Run this command in your terminal:

```bash
cd "d:\Multi Agent System"
pip install -r requirements.txt
```

This will install all required packages:
- langchain, langchain-core, langchain-groq
- langgraph
- chromadb
- typer, rich
- pydantic, pydantic-settings
- And more...

**Expected output:** Should complete without errors.

---

## **Step 2: Configure API Keys**

Edit the `.env` file at: `d:\Multi Agent System\.env`

Make sure it has these keys:

```env
# Groq API (Required - for LLM)
GROQ_API_KEY=your-api-key
GROQ_MODEL=openai/gpt-oss-120b

# Tavily API (Required - for web search)
TAVILY_API_KEY=tvly-dev-YOUR_KEY_HERE

# System Configuration
DEBUG=True
LOG_LEVEL=INFO

# Memory & Storage
CHROMA_DB_PATH=./data/memories
METRICS_DB_PATH=./data/metrics.db

# Feature Flags
ENABLE_WEB_SEARCH=True
ENABLE_CODE_EXECUTION=True
ENABLE_MEMORY=True
```

**To get Tavily API Key:**
1. Visit https://tavily.com
2. Sign up for free
3. Copy your API key
4. Add it to `.env`

---

## **Step 3: Run the Application**

### **Option A: Run a Single Task**
```bash
python main.py run "Research machine learning and write a beginner guide"
```

### **Option B: Interactive Chat Mode**
```bash
python main.py chat
```

### **Option C: Research a Topic**
```bash
python main.py research "quantum computing" --deep
```

### **Option D: Generate Content**
```bash
python main.py write "Python async programming" --style blog
```

### **Option E: Analyze Code**
```bash
python main.py analyze-code
```

### **Option F: View System Status**
```bash
python main.py status
```

### **Option G: View Task History**
```bash
python main.py history --limit 20
```

### **Option H: Clear Memory**
```bash
python main.py clear-memory
```

---

## **Troubleshooting**

### Issue: `ModuleNotFoundError: No module named 'chromadb'`
**Solution:** Run `pip install -r requirements.txt`

### Issue: `ValueError: You are using a deprecated configuration of Chroma`
**Solution:** Already fixed in the code! Just install fresh dependencies.

### Issue: `ImportError: cannot import name 'ARIAWorkflow'`
**Solution:** All `__init__.py` files are now correctly set up.

### Issue: Tavily API key not working
**Solution:** 
- Verify key is correct in `.env`
- Restart the application after editing `.env`
- Check rate limits on tavily.com

### Issue: Groq API not working
**Solution:**
- Verify API key is correct
- Check if model name is valid
- Visit console.groq.com to confirm key is active

---

## **Project Structure**

```
d:\Multi Agent System\
├── main.py                    # CLI entry point
├── config.py                  # Configuration & settings
├── requirements.txt           # Dependencies
├── .env                       # API keys (don't commit!)
│
├── agents/                    # AI Agent implementations
│   ├── __init__.py
│   ├── base_agent.py
│   ├── research_agent.py
│   ├── creative_agent.py
│   └── technical_agent.py
│
├── graph/                     # LangGraph workflow
│   ├── __init__.py
│   └── workflow.py
│
├── memory/                    # Memory systems
│   ├── __init__.py
│   ├── vector_store.py        # ChromaDB
│   └── metadata_db.py         # SQLite
│
├── tools/                     # Tool integrations
│   ├── __init__.py
│   ├── web_tools.py           # Tavily search
│   ├── code_tools.py          # Code execution
│   └── data_tools.py          # Data operations
│
├── routing/                   # Task routing logic
│   ├── __init__.py
│   ├── classifier.py
│   └── router.py
│
├── prompts/                   # LLM prompts
│   ├── __init__.py
│   ├── research_prompts.py
│   ├── creative_prompts.py
│   └── technical_prompts.py
│
├── utils/                     # Utilities
│   ├── __init__.py
│   ├── logger.py
│   ├── formatter.py
│   └── metrics.py
│
├── reasoning/                 # Reasoning engines
│   └── __init__.py
│
└── data/                      # Data storage
    └── memories/              # ChromaDB data
```

---

## **Features Available**

✅ **Multi-Agent Orchestration** - Intelligent routing to best agent
✅ **Research Agent** - Gathers and analyzes information
✅ **Creative Agent** - Generates content and ideas
✅ **Technical Agent** - Analyzes and debugs code
✅ **Persistent Memory** - ChromaDB vector store
✅ **Task Tracking** - SQLite metadata database
✅ **Performance Metrics** - Track execution times
✅ **Interactive Chat** - Real-time conversation mode

---

## **Example Commands**

### Research + Writing
```bash
python main.py run "Research the latest AI breakthroughs and write a comprehensive article"
```

### Code Review
```bash
python main.py run "Review my Python function for bugs and performance issues"
```

### Tutorial Creation
```bash
python main.py write "Getting started with Docker" --style tutorial
```

### Multi-step Analysis
```bash
python main.py run "Search for best practices in microservices, write a guide, and analyze sample code"
```

---

## **Support**

If you encounter issues:
1. Check the troubleshooting section above
2. Verify all API keys are correct
3. Run `pip install -r requirements.txt` again
4. Check that all directories exist: `data/`, `data/memories/`

---

**Ready to use!** 🚀
