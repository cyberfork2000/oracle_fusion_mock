from helpers.workflow_base import BaseWorkflow, logger
from helpers.api_client import (
    create_ap_supplier,
    create_ap_invoice,
    approve_ap_invoice,
    pay_ap_invoice,
    get_ap_invoice_status,
    get_ap_journal_entries
)
from domains.ap.payloads import supplier_payload, invoice_payload, payment_payload

class APWorkflow(BaseWorkflow):
    """Accounts Payable workflow with logging and step reporting."""

    def create_supplier(self, data=None):
        data = data or supplier_payload()
        response = self.execute_step(create_ap_supplier, self.base_url, self.token, data)
        supplier_id = response["supplierId"]  # <- extract string ID only
        logger.info(f"Created supplier with ID: {supplier_id}")
        return supplier_id, data

    def create_invoice(self, supplier_id, data=None):
        data = data or invoice_payload()
        data["supplierId"] = supplier_id
        response = self.execute_step(create_ap_invoice, self.base_url, self.token, data)
        invoice_id = response["invoiceId"]  # <- extract string ID only
        logger.info(f"Created invoice with ID: {invoice_id} for supplier {supplier_id}")
        return invoice_id, data

    def approve_invoice(self, invoice_id):
        self.execute_step(approve_ap_invoice, self.base_url, self.token, invoice_id)
        logger.info(f"Invoice {invoice_id} approved. Waiting for status...")
        self.wait_until(
            lambda: get_ap_invoice_status(self.base_url, self.token, invoice_id) == "APPROVED",
            timeout=20,
            interval=2,
            error_msg=f"Invoice {invoice_id} did not reach APPROVED status"
        )
        logger.info(f"Invoice {invoice_id} status is APPROVED")

    def pay_invoice(self, invoice_id):
        data = payment_payload()
        data["invoiceId"] = invoice_id
        self.execute_step(pay_ap_invoice, self.base_url, self.token, data)
        logger.info(f"Payment executed successfully for invoice {invoice_id}")

    def journal_entries(self, invoice_id):
        journal = self.execute_step(get_ap_journal_entries, self.base_url, self.token, invoice_id)
        logger.info(f"Retrieved journal entries for invoice {invoice_id}")
        return journal
