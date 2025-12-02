import pytest

from domains.je.payloads import journal_invalid_payload
from domains.je.workflow import JEWorkflow
from requests.exceptions import HTTPError

from helpers.api_client import je_create_journal_entry


def test_journal_entries_end_to_end(base_url, token):
    flow = JEWorkflow(base_url, token)

    # 1. Create journal
    journal_id, journal_data = flow.create_journal()

    # 2. Submit for approval
    flow.submit_for_approval(journal_id)

    # 3. Approve journal
    flow.approve_journal(journal_id)

    # 4. Post journal and validate ledger
    flow.post_journal(journal_id)

    ledger = flow.get_ledger(journal_id)
    expected_total_debit = sum(line["debit"] for line in journal_data["lines"])
    expected_total_credit = sum(line["credit"] for line in journal_data["lines"])
    assert ledger["totalDebit"] == expected_total_debit
    assert ledger["totalCredit"] == expected_total_credit

def test_journal_entries_invalid(base_url, token):
    # Load invalid payload
    data = journal_invalid_payload()
    data["lines"][0]["debit"] += 100  # intentionally break DR/CR balance

    # Call API directly — no retries
    with pytest.raises(HTTPError):
        je_create_journal_entry(base_url, token, data)
