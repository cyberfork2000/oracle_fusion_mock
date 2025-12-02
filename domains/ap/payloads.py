from helpers.payload_loader import load_payload

def supplier_payload():
    return load_payload("ap_supplier_payload.json")

def invoice_payload():
    return load_payload("ap_invoice_payload.json")

def payment_payload():
    return load_payload("ap_payment_payload.json")
