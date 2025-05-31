# MCP-Server
MCP Server for tool calling

## 🚀 Getting Started

### 1. Create a Virtual Environment and Install Dependencies

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Start the MCP Server

```bash
python src/main.py
```

### 3. Available API endpoints
- `/v1/status/` — Check if the MCP server is up  
- `/v1/tools/` — Get the list of available tools 