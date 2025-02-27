# Slack Lead Processing API

A FastAPI application for processing leads from Slack using LangGraph workflows.

## Overview

This API provides endpoints for processing leads from Slack, approving or rejecting lead assignments, and checking the status of workflow threads. It uses the LangGraph SDK to connect to a LangGraph server running locally.

## Requirements

- Python 3.9+
- FastAPI
- Uvicorn
- LangGraph SDK
- HTTPX

## Installation

1. Install the required packages:

```bash
pip install -r requirements.txt
```

2. Make sure the LangGraph server is running on http://localhost:2024.

## Running the API

Start the API server:

```bash
uvicorn main:app --reload
```

The API will be available at http://localhost:8000.

## API Endpoints

### Process a Lead

```
POST /api/slack/lead
```

Process a lead from Slack and start the workflow.

**Request Body:**

```json
{
  "event": "message",
  "user": {
    "id": "U123456",
    "name": "John Doe",
    "email": "john.doe@example.com"
  },
  "slack_message": {
    "text": "Hi, I'm interested in your product. I work for a healthcare company in New York and we're looking for a solution to manage our patient data. We have about 500 employees and are growing rapidly.",
    "channel": "C123456",
    "ts": "1234567890.123456"
  }
}
```

**Response:**

```json
{
  "thread_id": "thread-123",
  "status": "awaiting_approval",
  "requires_approval": true,
  "lead_attributes": {
    "geo_location": "New York",
    "industry": "Healthcare",
    "engagement": "High"
  },
  "assigned_sales_person": "Jane Smith",
  "approval_status": null,
  "hubspot_lead_created": false,
  "notification_sent": false,
  "messages": [
    "Lead information extracted: Healthcare company in New York with high engagement.",
    "Sales person Jane Smith has been assigned based on location and industry expertise."
  ]
}
```

### Approve a Lead

```
POST /api/slack/approve
```

Approve or reject a lead assignment.

**Request Body:**

```json
{
  "thread_id": "thread-123",
  "approved": true
}
```

**Response:**

```json
{
  "thread_id": "thread-123",
  "status": "completed",
  "requires_approval": false,
  "lead_attributes": {
    "geo_location": "New York",
    "industry": "Healthcare",
    "engagement": "High"
  },
  "assigned_sales_person": "Jane Smith",
  "approval_status": true,
  "hubspot_lead_created": true,
  "notification_sent": true,
  "messages": [
    "Lead information extracted: Healthcare company in New York with high engagement.",
    "Sales person Jane Smith has been assigned based on location and industry expertise.",
    "Lead assignment approved.",
    "Lead created in Hubspot.",
    "Notification sent to Jane Smith."
  ]
}
```

### Get Thread Status

```
GET /api/slack/thread/{thread_id}
```

Get the status of a workflow thread.

**Response:**

```json
{
  "thread_id": "thread-123",
  "status": "completed",
  "requires_approval": false,
  "lead_attributes": {
    "geo_location": "New York",
    "industry": "Healthcare",
    "engagement": "High"
  },
  "assigned_sales_person": "Jane Smith",
  "approval_status": true,
  "hubspot_lead_created": true,
  "notification_sent": true,
  "messages": [
    "Lead information extracted: Healthcare company in New York with high engagement.",
    "Sales person Jane Smith has been assigned based on location and industry expertise.",
    "Lead assignment approved.",
    "Lead created in Hubspot.",
    "Notification sent to Jane Smith."
  ]
}
```

## Testing

You can test the API using the included client script:

```bash
python client.py
```

This will run a demo workflow that processes a sample lead, approves it, and checks the status of the workflow thread.

## Architecture

The API uses the LangGraph SDK to connect to a LangGraph server running locally. The workflow is defined in the LangGraph server and is accessed through the SDK.

The workflow consists of the following steps:

1. Extract lead information from the Slack message
2. Assign a sales person based on the lead attributes
3. Send an approval request
4. Create a lead in Hubspot (if approved)
5. Notify the assigned sales person (if approved)

The API provides endpoints for starting the workflow, approving or rejecting lead assignments, and checking the status of workflow threads.

## Error Handling

The API includes error handling for common issues, such as:

- Invalid input data
- Thread not found
- LangGraph server errors

Errors are returned as HTTP error responses with appropriate status codes and error messages.
