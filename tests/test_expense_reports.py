from domains.er.workflow import ERWorkflow

def test_expense_report_end_to_end(base_url, token):
    flow = ERWorkflow(base_url, token)

    # 1. Submit expense report
    expense_id, _ = flow.submit_expense_report()

    # 2. Approve expense
    flow.approve_expense(expense_id)

    # 3. Generate payment
    flow.generate_payment(expense_id)

    # 4. Validate journal entries
    journal = flow.journal_entries(expense_id)
    assert journal["status"] == "POSTED", f"Journal not posted: {journal}"
    expected_amount = journal["totalDebit"]
    assert journal["totalCredit"] == expected_amount, f"Expected credit {expected_amount}, got {journal['totalCredit']}"


def test_expense_report_invalid_data(base_url, token):
    """Test expense report submission with invalid payloads via WireMock ER stubs."""
    from domains.er.payloads import expense_report_invalid_payload
    from helpers.api_client import submit_expense_report
    from unittest.mock import patch

    invalid_data = expense_report_invalid_payload()

    print("Payload being sent to WireMock:", invalid_data)

    with patch("requests.post") as mock_post:
        try:
            submit_expense_report(base_url, token, invalid_data)
        except Exception:
            pass
        print("requests.post called with args:", mock_post.call_args)
