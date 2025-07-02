#!/bin/bash

# Load environment variables from .env file if it exists
if [ -f ".env" ]; then
  echo "Loading environment variables from .env file..."
  export $(grep -v '^#' .env | xargs)
else
  echo "Warning: .env file not found. Make sure OPENAI_API_KEY is set in your environment."
fi

# Run the test workflow
echo "Running credit agents dynamic workflow test..."
uv run pytest tests/integration_tests/test_graph.py::test_self_learning_summary_with_custom_rules -v