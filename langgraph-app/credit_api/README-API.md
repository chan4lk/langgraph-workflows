# Credit Approval API Server

This is a Node.js Express server that implements the API endpoints for the Credit Approval Workflow. It uses SQLite as the database backend.

## Setup

1. Install dependencies:
   ```bash
   cd src/credit_agents
   npm install
   ```

2. Initialize the database:
   ```bash
   node init-db.js
   ```
   This will create the SQLite database file (`credit_demo.sqlite`) with all the necessary tables and sample data.

3. Start the server:
   ```bash
   npm start
   ```
   The server will run on port 3000 by default. You can change this by setting the `PORT` environment variable.

## API Endpoints

### Customers
- `GET /customers` - Get a list of customers (limited to 10)
- `GET /customer?id={customer_id}` - Get a specific customer by ID

### Credit Applications
- `GET /applications` - Get a list of credit applications (limited to 10, sorted by date)
- `GET /application?id={application_id}` - Get a specific application by ID
- `POST /applications` - Create a new application
  ```json
  {
    "customer_id": "CUST001",
    "product_type": "credit_card",
    "requested_amount": 5000
  }
  ```

### Credit Checks
- `GET /credit-check?application_id={application_id}` - Get credit check for an application
- `POST /credit-check` - Create a new credit check
  ```json
  {
    "application_id": "APP001",
    "credit_score": 720
  }
  ```

### KYC Checks
- `GET /kyc-check?application_id={application_id}` - Get KYC check for an application
- `POST /kyc-check` - Create a new KYC check
  ```json
  {
    "application_id": "APP001",
    "kyc_passed": true,
    "remarks": "All documents verified"
  }
  ```

### Income Verification
- `GET /income-verification?application_id={application_id}` - Get income verification for an application
- `POST /income-verification` - Create a new income verification
  ```json
  {
    "application_id": "APP001",
    "declared_income": 60000,
    "verified_income": 58000,
    "remarks": "Income verified through employer"
  }
  ```

### Background Checks
- `GET /background-check?application_id={application_id}` - Get background check for an application
- `POST /background-check` - Create a new background check
  ```json
  {
    "application_id": "APP001",
    "criminal_record": false,
    "debt_collections": false,
    "remarks": "No issues found"
  }
  ```

### Manual Approval
- `GET /manual-approval?application_id={application_id}` - Get manual approval for an application
- `POST /manual-approval` - Create a new manual approval
  ```json
  {
    "application_id": "APP001",
    "approver_name": "Jane Smith",
    "approval_notes": "Approved based on good credit history",
    "approved": true
  }
  ```

### Final Decision
- `GET /final-decision?application_id={application_id}` - Get final decision for an application
- `POST /final-decision` - Create a new final decision
  ```json
  {
    "application_id": "APP001",
    "decision": "Approved",
    "reason": "All checks passed successfully"
  }
  ```

## Health Check
- `GET /health` - Check if the API server is running

## Database Schema

The database has the following tables:
- `customers` - Customer information
- `credit_applications` - Credit application details
- `credit_checks` - Credit score checks
- `kyc_checks` - Know Your Customer verification
- `income_verifications` - Income verification details
- `background_checks` - Background check results
- `manual_approvals` - Manual approval decisions
- `final_decisions` - Final application decisions

## Integration with LangGraph

To use this API with the LangGraph Credit Approval Workflow:

1. Start this API server
2. Update the `BASE_URL` in the LangGraph workflow to point to this server:
   ```python
   BASE_URL = "http://localhost:3000"
   ```
3. Run the LangGraph workflow to process credit applications through the API
