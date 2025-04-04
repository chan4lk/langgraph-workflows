# Credit Approval Workflow

This implementation demonstrates a credit approval workflow using LangGraph with a supervisor and multi-agent pattern. The workflow dynamically routes applications based on credit score, KYC results, and income verification.

## Architecture

The workflow implements the following pattern:
- **Supervisor Pattern**: A central supervisor function that routes between agent outputs
- **Multi-Agent Workflow**: Multiple specialized agents handle different aspects of the credit approval process

### Agent Roles

1. **Credit Score Checker Agent**: Checks the applicant's credit score
2. **KYC Validator Agent**: Validates Know Your Customer requirements
3. **Income Verifier Agent**: Verifies the applicant's declared income
4. **Background Check Agent**: Performs background checks (criminal record, debt collections)
5. **Manual Approver Agent**: Reviews applications that need human intervention
6. **Final Decision Agent**: Makes the final approval/rejection decision

### Dynamic Workflow Features

- **Branching Logic**: Routes applications based on credit score and other factors without hardcoded if/else rules
- **Dynamic Subflow Spawning**: Conditionally includes background checks and manual approval only when needed
- **Error Handling**: Gracefully handles API errors and continues the workflow
- **Supervisor Control**: Central routing logic that determines the next step based on the current state

## State Management

The workflow uses a dataclass-based state management approach:
- `CreditState` contains the application data and messages
- `CreditKeys` TypedDict holds all the analysis data
- Each agent directly modifies and returns the state object

## How to Run

1. Start the API server (mock implementation for testing)
2. Run the test workflow:

```bash
python -m credit_agents.test_workflow
```

## Implementation Details

- The workflow uses the LangGraph `StateGraph` to define the flow
- Conditional edges determine the next step based on the current state
- Each agent is implemented as a function that takes and returns a state object
- The supervisor uses helper functions to determine if background checks or manual approval are needed
