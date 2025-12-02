from helpers.payload_loader import load_payload

def customer_payload():
    return load_payload("ar_customer_payload.json")

def invoice_payload():
    return load_payload("ar_invoice_payload.json")

def receipt_payload():
    return load_payload("ar_receipt_payload.json")