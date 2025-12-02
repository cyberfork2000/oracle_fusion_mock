from helpers.workflow_base import BaseWorkflow, logger
from helpers.api_client import (
    fa_create_asset,
    fa_run_asset_depreciation,
    fa_retire_asset,
    fa_get_asset_journal_entries,
)
from domains.fa.payloads import (
    create_asset_payload,
    run_depreciation_payload,
    retire_asset_payload
)
from helpers.errors import WorkflowError

class FAWorkflow(BaseWorkflow):
    """Fixed Assets workflow with logging and step reporting."""

    def create_asset(self, data=None):
        data = data or create_asset_payload()
        response = self.execute_step(fa_create_asset, self.base_url, self.token, data)
        asset_id = response["assetId"]
        if response.get("status") != "created":
            raise WorkflowError(f"Asset creation failed: {response}")
        logger.info(f"Created asset {asset_id}")
        return asset_id, data

    def run_depreciation(self, asset_id, data=None):
        data = data or run_depreciation_payload()
        response = self.execute_step(fa_run_asset_depreciation, self.base_url, self.token, asset_id, data)
        if response.get("status") not in ["simulated", "completed"]:
            raise WorkflowError(f"Depreciation failed for asset {asset_id}: {response}")
        if response.get("assetId") != asset_id:
            raise WorkflowError(f"Depreciation assetId mismatch: {response}")
        if "depreciationAmount" not in response:
            raise WorkflowError(f"Missing depreciation amount in response: {response}")
        logger.info(f"Depreciation run for asset {asset_id}: {response.get('depreciationAmount')}")
        return response

    def retire_asset(self, asset_id, data=None):
        data = data or retire_asset_payload()
        response = self.execute_step(fa_retire_asset, self.base_url, self.token, asset_id, data)
        if response.get("status") != "retired":
            raise WorkflowError(f"Asset retirement failed for {asset_id}: {response}")
        if response.get("assetId") != asset_id:
            raise WorkflowError(f"Retire assetId mismatch: {response}")
        journal_ref = response.get("journalEntryId")
        if not journal_ref:
            raise WorkflowError(f"No journal entry returned for asset retirement {asset_id}")
        logger.info(f"Retired asset {asset_id}, journal entry {journal_ref}")
        return journal_ref

    def journal_entries(self, journal_ref, expected_amount=0):
        journal = self.execute_step(fa_get_asset_journal_entries, self.base_url, self.token, journal_ref)
        if not isinstance(journal, dict):
            raise WorkflowError(f"Invalid journal response: {journal}")
        if journal.get("status") != "POSTED":
            raise WorkflowError(f"Journal not posted: {journal}")
        if journal.get("totalDebit") != expected_amount:
            raise WorkflowError(f"Expected debit {expected_amount}, got {journal.get('totalDebit')}")
        if journal.get("totalCredit") != expected_amount:
            raise WorkflowError(f"Expected credit {expected_amount}, got {journal.get('totalCredit')}")
        logger.info(f"Journal entries validated for {journal_ref}")
        return journal

