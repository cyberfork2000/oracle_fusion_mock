# File: helpers/api_client.py

from typing import Dict, Any
from .rest_api import RestApi


# -------------------------
# Internal helper
# -------------------------
def _api_request(method: str, url: str, token: str, json: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Helper to perform API call with RestApi wrapper, raising HTTPError on failure.
    """
    api = RestApi(url, token)
    resp = getattr(api, method.lower())(json=json)
    resp.raise_for_status()
    return resp.json()


# -------------------------
# Accounts Payable (ap)
# -------------------------
def create_ap_supplier(base_url: str, token: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    return _api_request("POST", f"{base_url}/ap/suppliers", token, json=payload)

def create_ap_invoice(base_url: str, token: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    return _api_request("POST", f"{base_url}/ap/invoices", token, json=payload)

def approve_ap_invoice(base_url: str, token: str, invoice_id: str) -> Dict[str, Any]:
    return _api_request("POST", f"{base_url}/ap/invoices/{invoice_id}/actions", token, json={"action": "APPROVE"})

def pay_ap_invoice(base_url: str, token: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    return _api_request("POST", f"{base_url}/ap/payments", token, json=payload)

def get_ap_invoice_status(base_url: str, token: str, invoice_id: str) -> str:
    return _api_request("GET", f"{base_url}/ap/invoices/{invoice_id}", token)["status"]

def get_ap_journal_entries(base_url: str, token: str, reference: str) -> Dict[str, Any]:
    return _api_request("GET", f"{base_url}/gl/journals?reference={reference}", token)

# -------------------------
# Accounts Receivable (AR)
# -------------------------
def ar_create_customer(base_url: str, token: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    return _api_request("POST", f"{base_url}/ar/customers", token, json=payload)

def ar_create_invoice(base_url: str, token: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    return _api_request("POST", f"{base_url}/ar/invoices", token, json=payload)

def ar_apply_receipt(base_url: str, token: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    return _api_request("POST", f"{base_url}/ar/receipts", token, json=payload)

def ar_get_invoice_status(base_url: str, token: str, invoice_id: str) -> str:
    return _api_request("GET", f"{base_url}/ar/invoices/{invoice_id}", token)["status"]

def ar_get_journal_entries(base_url: str, token: str, reference: str) -> Dict[str, Any]:
    return _api_request("GET", f"{base_url}/ar/gl/journals?reference={reference}", token)

# -------------------------
# Journals / GL
# -------------------------
def je_create_journal_entry(base_url: str, token: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    return _api_request("POST", f"{base_url}/journals", token, json=payload)

def je_submit_journal_for_approval(base_url: str, token: str, journal_id: str) -> Dict[str, Any]:
    return _api_request("POST", f"{base_url}/journals/{journal_id}/submit", token)

def je_approve_journal(base_url: str, token: str, journal_id: str) -> Dict[str, Any]:
    return _api_request("POST", f"{base_url}/journals/{journal_id}/approve", token)

def je_post_journal(base_url: str, token: str, journal_id: str) -> Dict[str, Any]:
    return _api_request("POST", f"{base_url}/journals/{journal_id}/post", token)

def je_get_journal_entries(base_url: str, token: str, reference: str) -> Dict[str, Any]:
    return _api_request("GET", f"{base_url}/gl/journals?reference={reference}", token)

# -------------------------
# Fixed Assets
# -------------------------
def fa_create_asset(base_url: str, token: str, payload: dict):
    return _api_request("POST", f"{base_url}/api/assets", token, json=payload)

def fa_run_asset_depreciation(base_url: str, token: str, asset_id: str, payload: dict):
    """
    Trigger depreciation for an asset with an optional run payload.
    """
    return _api_request(
        "POST",
        f"{base_url}/api/assets/{asset_id}/depreciate",
        token,
        json=payload
    )

def fa_retire_asset(base_url: str, token: str, asset_id: str, payload: dict):
    return _api_request("POST", f"{base_url}/api/assets/{asset_id}/retire", token, json=payload)

def fa_get_asset_journal_entries(base_url: str, token: str, journal_entry_id: str):
    """
    Fetch a journal entry by its ID (used for retirement journals).
    """
    return _api_request("GET", f"{base_url}/api/gl/journals/{journal_entry_id}", token)


# -------------------------
# Expense Reports / Employee Reimbursements
# -------------------------
def submit_expense_report(base_url: str, token: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Submit a new expense report for an employee.
    """
    return _api_request("POST", f"{base_url}/expenses", token, json=payload)

def approve_expense(base_url: str, token: str, expense_id: str) -> Dict[str, Any]:
    """
    Approve a submitted expense report.
    """
    return _api_request("POST", f"{base_url}/expenses/{expense_id}/approve", token)

def generate_expense_payment(base_url: str, token: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate payment for an approved expense report.
    """
    return _api_request("POST", f"{base_url}/expenses/payments", token, json=payload)

def get_expense_journal_entries(base_url: str, token: str, expense_id: str) -> Dict[str, Any]:
    """
    Retrieve journal entries associated with an expense report.
    """
    print(f"Expense_id is {expense_id}")
    return _api_request("GET", f"{base_url}/gl/journals?reference={expense_id}", token)

