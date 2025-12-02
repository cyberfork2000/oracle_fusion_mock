from helpers.workflow_base import BaseWorkflow, logger
from helpers.api_client import (
    submit_expense_report,
    approve_expense,
    generate_expense_payment,
    get_expense_journal_entries
)
from domains.er.payloads import (
    submit_expense_report_payload,
    generate_expense_payment_payload
)
from helpers.errors import WorkflowError

class ERWorkflow(BaseWorkflow):
    """Expense Report workflow with logging and step reporting."""

    def submit_expense_report(self, data=None):
        data = data or submit_expense_report_payload()
        response = self.execute_step(submit_expense_report, self.base_url, self.token, data)
        expense_id = response["expenseId"]
        status = response.get("status")
        if status != "SUBMITTED":
            raise WorkflowError(f"Expense report submission failed: {response}")
        logger.info(f"Submitted expense report {expense_id} with status {status}")
        return expense_id, data

    def approve_expense(self, expense_id):
        response = self.execute_step(approve_expense, self.base_url, self.token, expense_id)
        status = response.get("status")
        if status != "APPROVED":
            raise WorkflowError(f"Expense approval failed for {expense_id}: {response}")
        logger.info(f"Approved expense {expense_id}")
        return response

    def generate_payment(self, expense_id, data=None):
        data = data or generate_expense_payment_payload()
        data["expenseId"] = expense_id
        response = self.execute_step(generate_expense_payment, self.base_url, self.token, data)
        status = response.get("paymentStatus")
        if status != "SUCCESS":
            raise WorkflowError(f"Expense payment failed for {expense_id}: {response}")
        logger.info(f"Payment generated successfully for expense {expense_id}")
        return response

    def journal_entries(self, expense_id):
        journal = self.execute_step(get_expense_journal_entries, self.base_url, self.token, expense_id)
        logger.info(f"Retrieved journal entries for expense {expense_id}")
        return journal
