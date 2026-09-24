import json
from pathlib import Path

# utils/schema_loader.py -> project root -> schemas/- Path for schema-not hardcoded
SCHEMAS_DIR = Path(__file__).resolve().parent.parent / "api"

def load_schema(filename: str) -> dict:
    path = SCHEMAS_DIR / filename
    # if not path.exists():
    #     raise FileNotFoundError(
    #         f"Schema '{filename}' not found in {SCHEMAS_DIR}. "
    #         f"Available: {[p.name for p in SCHEMAS_DIR.glob('*.json')]}"
    #     )
    with path.open() as f:
        return json.load(f)