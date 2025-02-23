# Agentic AI Workflow Engine

A powerful workflow engine for orchestrating AI agents using LangGraph, Pydantic Agents, and React Flow.

## Features

- Visual workflow designer using React Flow
- LangGraph-based workflow orchestration
- Pydantic Agents with LLM capabilities
- MCP Server for tool execution
- Human-in-the-loop tasks
- Role-Based Access Control (RBAC)
- Workflow versioning and rollback
- PostgreSQL state management

## Project Structure

```
langgraph-workflows/
├── backend/         # FastAPI backend service
├── mcp_server/     # Tool execution server
├── frontend/       # React Flow UI
├── docker/         # Docker configurations
├── k8s/            # Kubernetes manifests
└── docs/           # Documentation
```

## Getting Started

### Prerequisites

- Node.js >= 18
- Python >= 3.9
- PostgreSQL >= 14
- Docker (optional)
- Kubernetes (optional)

### Development Setup

1. Frontend Development
```bash
cd frontend
npm install
npm run dev
```

2. Backend Development
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

3. MCP Server Development
```bash
cd mcp_server
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```

## License

MIT License
