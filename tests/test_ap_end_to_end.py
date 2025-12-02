from domains.ap.workflow import APWorkflow

def test_ap_end_to_end(base_url, token):
    flow = APWorkflow(base_url, token)

    supplier_id, _ = flow.create_supplier()
    invoice_id, invoice_payload = flow.create_invoice(supplier_id)

    flow.approve_invoice(invoice_id)
    flow.pay_invoice(invoice_id)

    journal = flow.journal_entries(invoice_id)
    assert journal["status"] == "POSTED"
    assert journal["totalDebit"] == invoice_payload["amount"]
    assert journal["totalCredit"] == invoice_payload["amount"]
