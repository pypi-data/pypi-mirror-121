import json
from pathlib import Path


with open(Path(__file__).parent / "country_code_iso_alpha2.json", "r") as f:
    country_code_iso_alpha_2 = json.load(f)
