"""Slack Lead Processing Workflow.

This module defines a workflow for processing leads from Slack messages,
assigning them to appropriate sales people, and creating them in Hubspot after approval.
"""

from slack_approval.graph import graph

__all__ = ["graph"]
