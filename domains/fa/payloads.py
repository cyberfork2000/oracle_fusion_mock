from helpers.payload_loader import load_payload

def create_asset_payload():
    return load_payload("fa_create_asset_payload.json")

def run_depreciation_payload():
    return load_payload("fa_run_depreciation_payload.json")

def retire_asset_payload():
    return load_payload("fa_retire_asset_payload.json")
