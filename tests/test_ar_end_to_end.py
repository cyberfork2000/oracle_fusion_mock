from domains.ar.workflow import ARWorkflow

def test_ar_end_to_end(base_url, token):
    flow = ARWorkflow(base_url, token)

    # 1. Create customer
    customer_id, _ = flow.create_customer()

    # 2. Create invoice
    invoice_id, invoice_payload = flow.create_invoice(customer_id)

    # 3. Check invoice status
    flow.check_invoice_status(invoice_id, expected_status="OPEN")

    # 4. Apply receipt
    flow.apply_receipt(invoice_id)

    # 5. Validate journal
    journal = flow.journal_entries(invoice_id)
    expected_amount = invoice_payload.get("amount", 500)
    assert journal["status"] == "POSTED", f"Journal not posted: {journal}"
    assert journal["totalDebit"] == expected_amount
    assert journal["totalCredit"] == expected_amount
