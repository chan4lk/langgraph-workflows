from langchain_core.tools import tool
import requests
from typing import Dict, List, Optional, Union, Any

# API Tools for each agent
#BASE_URL = "https://fabricate.mockaroo.com/api/v1/databases/credit_demo/api"
BASE_URL = "http://localhost:3000"
# Authentication token
AUTH_TOKEN = "46ada160-f07b-4461-9f77-0eb36f383ded"
AUTH_HEADERS = {"Authorization": f"Bearer {AUTH_TOKEN}"}

# Credit Score Checker Agent tools
@tool
def check_credit_score(customer_id: str) -> Dict[str, Any]:
    """Check the credit score for a given customer"""
    """ Parameters:
    - customer_id: str""" 

    try:
        print("Checking credit score...\n")
        response = requests.get(
            f"{BASE_URL}/credit-check", 
            params={"customer_id": customer_id},
            headers=AUTH_HEADERS
        )
        if response.status_code == 200:
            print("Credit score checked successfully.\n", response.json())
            return response.json()
        else:
            return {"error": f"API returned status code {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

# KYC Validator Agent tools
@tool
def validate_kyc(customer_id: str) -> Dict[str, Any]:
    """Validate KYC for a given customer"""
    """ Parameters:
    - customer_id: str"""
    try:
        response = requests.get(
            f"{BASE_URL}/kyc-check", 
            params={"customer_id": customer_id},
            headers=AUTH_HEADERS
        )
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"API returned status code {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

# Income Verifier Agent tools
@tool
def verify_income(customer_id: str) -> Dict[str, Any]:
    """Verify income for a given customer"""
    """ Parameters:
    - customer_id: str"""
    try:
        response = requests.get(
            f"{BASE_URL}/income-verification", 
            params={"customer_id": customer_id},
            headers=AUTH_HEADERS
        )
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"API returned status code {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

# Background Check Agent tools
@tool
def perform_background_check(customer_id: str) -> Dict[str, Any]:
    """Perform background check for a given customer"""
    """ Parameters:
    - customer_id: str"""
    try:
        response = requests.get(
            f"{BASE_URL}/background-check", 
            params={"customer_id": customer_id},
            headers=AUTH_HEADERS
        )
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"API returned status code {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

# Manual Approver Agent tools
@tool
def manual_approval(application_id: str, approve: bool, notes: str) -> Dict[str, Any]:
    """Perform manual approval for a given application"""
    """ Parameters:
    - application_id: str
    - approve: bool
    - notes: str"""
    try:
        # Convert boolean to integer for SQLite compatibility
        approved_int = 1 if approve else 0
        
        response = requests.post(
            f"{BASE_URL}/manual-approval", 
            json={
                "application_id": application_id, 
                "approver_name": "AI Agent",
                "approval_notes": notes,
                "approved": approved_int  # Use integer instead of boolean
            },
            headers=AUTH_HEADERS
        )
        return response.json()
    except Exception as e:
        return {"error": str(e)}

# Final Decision Agent tools
@tool
def make_final_decision(application_id: str, decision: str, reason: str) -> Dict[str, Any]:
    """Make the final decision for a given application"""
    """Parameters:
    - application_id: str
    - decision: str
    - reason: str
    """
    try:
        response = requests.post(
            f"{BASE_URL}/final-decision", 
            json={
                "application_id": application_id, 
                "decision": decision,
                "reason": reason
            },
            headers=AUTH_HEADERS
        )
        return response.json()
    except Exception as e:
        return {"error": str(e)}