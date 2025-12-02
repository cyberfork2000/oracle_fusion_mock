from helpers.payload_loader import load_payload

def journal_payload():
    return load_payload("je_journal_payload.json")

def journal_invalid_payload():
    return load_payload("je_journal_invalid_payload.json")
