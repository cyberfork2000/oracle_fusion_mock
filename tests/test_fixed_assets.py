from domains.fa.workflow import FAWorkflow

def test_fixed_assets_end_to_end(base_url, token):
    flow = FAWorkflow(base_url, token)

    # 1. Create asset
    asset_id, asset_data = flow.create_asset()

    # 2. Run depreciation
    flow.run_depreciation(asset_id)

    # 3. Retire asset
    journal_ref = flow.retire_asset(asset_id)

    # 4. Validate journal entries
    flow.journal_entries(journal_ref, expected_amount=asset_data.get("cost", 0))
