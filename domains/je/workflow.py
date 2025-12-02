from helpers.workflow_base import BaseWorkflow, logger
from helpers.api_client import (
    je_create_journal_entry,
    je_submit_journal_for_approval,
    je_approve_journal,
    je_post_journal,
    je_get_journal_entries,
)
from domains.je.payloads import journal_payload, journal_invalid_payload
from helpers.errors import WorkflowError
from requests.exceptions import HTTPError

class JEWorkflow(BaseWorkflow):
    """General Ledger Journal workflow with logging and step reporting."""

    def create_journal(self, data=None):
        data = data or journal_payload()
        response = self.execute_step(je_create_journal_entry, self.base_url, self.token, data)
        journal_id = response["journalId"]
        logger.info(f"Created journal entry {journal_id}")
        return journal_id, data

    def submit_for_approval(self, journal_id):
        response = self.execute_step(je_submit_journal_for_approval, self.base_url, self.token, journal_id)
        if response.get("status") != "SUBMITTED":
            raise WorkflowError(f"Journal {journal_id} submission failed: {response}")
        logger.info(f"Journal {journal_id} submitted for approval")
        return response

    def approve_journal(self, journal_id):
        response = self.execute_step(je_approve_journal, self.base_url, self.token, journal_id)
        if response.get("status") != "APPROVED":
            raise WorkflowError(f"Journal {journal_id} approval failed: {response}")
        logger.info(f"Journal {journal_id} approved")
        return response

    def post_journal(self, journal_id):
        response = self.execute_step(je_post_journal, self.base_url, self.token, journal_id)
        if response.get("status") != "POSTED":
            raise WorkflowError(f"Journal {journal_id} posting failed: {response}")
        logger.info(f"Journal {journal_id} posted")
        return response

    def get_ledger(self, journal_id):
        ledger = self.execute_step(je_get_journal_entries, self.base_url, self.token, journal_id)
        logger.info(f"Retrieved ledger entries for journal {journal_id}")
        return ledger

    def negative_test_invalid_journal(self, data=None):
        """Intentionally submit invalid journal and expect HTTPError."""
        data = data or journal_invalid_payload()
        data["lines"][0]["debit"] += 100
        self.execute_step(
            je_create_journal_entry,
            self.base_url,
            self.token,
            data,
            retry=False  # disable retry for negative scenario
        )

