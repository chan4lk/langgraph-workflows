"""Start a LangGraph server for the Slack lead processing workflow."""

import os
import sys
from pathlib import Path

# Add the src directory to the Python path
src_dir = Path(__file__).parent / "src"
sys.path.append(str(src_dir))

from langgraph.server import Server
from slack_approval.graph import graph

# Create a server
server = Server(
    graphs={
        "slack_approval": graph
    },
    port=2024,
)

if __name__ == "__main__":
    print("Starting LangGraph server on http://localhost:2024")
    server.serve()
