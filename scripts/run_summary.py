import json
from pathlib import Path

s = json.loads(Path("data/status.json").read_text())
print("## Beebe refresh\n")
for name, source in s["sources"].items():
    print(f"- {name}: last success {source.get('last_success', 'never')}")
if "imaging" in s:
    for name, value in s["imaging"].items():
        print(f"- {name}: {value}")
print("\n### Source warnings\n")
for error in s.get("errors", []):
    print(f"- {error}")
if not s.get("errors"):
    print("None recorded.")
