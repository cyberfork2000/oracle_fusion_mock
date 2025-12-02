from pathlib import Path
import json

# Root/payloads directory
BASE_DIR = Path(__file__).parent.parent / "payloads"

def load_payload(file_name: str):
    """Load JSON payload by filename from the payloads directory."""
    path = BASE_DIR / file_name
    with open(path) as f:
        return json.load(f)
