import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from backend.app.crew.diplomat_crew import crew

import os
print(f"[TEST DEBUG] OPENAI_API_KEY env var value: {os.getenv('OPENAI_API_KEY')}")

inputs = {"text": "Increase synergy and move fast", "direction": "corporate_to_casual"}

result = crew.kickoff(inputs)

print("Test Crew.kickoff result:")
print(result)
