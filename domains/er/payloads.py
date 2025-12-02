from helpers.payload_loader import load_payload

def submit_expense_report_payload():
    return load_payload("er_submit_expense_report_payload.json")

def generate_expense_payment_payload():
    return load_payload("er_generate_expense_payment_payload.json")

def expense_report_invalid_payload():
    return load_payload("er_expense_report_invalid_payload.json")
