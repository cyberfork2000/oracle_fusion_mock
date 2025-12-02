from helpers.workflow_base import BaseWorkflow, logger
from helpers.api_client import (
    ar_create_customer,
    ar_create_invoice,
    ar_apply_receipt,
    ar_get_invoice_status,
    ar_get_journal_entries
)
from domains.ar.payloads import customer_payload, invoice_payload, receipt_payload
from helpers.errors import WorkflowError

class ARWorkflow(BaseWorkflow):
    """Accounts Receivable workflow with logging and step reporting."""

    def create_customer(self, data=None):
        data = data or customer_payload()
        response = self.execute_step(ar_create_customer, self.base_url, self.token, data)
        customer_id = response["customerId"]
        logger.info(f"Created customer with ID: {customer_id}")
        return customer_id, data

    def create_invoice(self, customer_id, data=None):
        data = data or invoice_payload()
        data["customerId"] = customer_id
        response = self.execute_step(ar_create_invoice, self.base_url, self.token, data)
        invoice_id = response["invoiceId"]
        logger.info(f"Created invoice {invoice_id} for customer {customer_id}")
        return invoice_id, data

    def check_invoice_status(self, invoice_id, expected_status="OPEN"):
        status = self.execute_step(ar_get_invoice_status, self.base_url, self.token, invoice_id)
        if status != expected_status:
            raise WorkflowError(f"Invoice {invoice_id} expected status {expected_status}, got {status}")
        logger.info(f"Invoice {invoice_id} status verified: {status}")
        return status

    def apply_receipt(self, invoice_id, data=None):
        data = data or receipt_payload()
        data["invoiceId"] = invoice_id
        response = self.execute_step(ar_apply_receipt, self.base_url, self.token, data)
        if response.get("status") != "APPLIED":
            raise WorkflowError(f"Receipt not applied for invoice {invoice_id}: {response}")
        logger.info(f"Receipt applied successfully for invoice {invoice_id}")
        return response

    def journal_entries(self, invoice_id):
        journal = self.execute_step(ar_get_journal_entries, self.base_url, self.token, invoice_id)
        logger.info(f"Retrieved journal entries for invoice {invoice_id}")
        return journal
