import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / 'backend'))

from app.crew.agents import DiplomatTranslatorAgent

# Dummy glossary_tool
class GlossaryTool:
    term_map = {"term1": "definition1"}


def test_env_loading():
    agent = DiplomatTranslatorAgent(GlossaryTool())
    assert agent.client is not None


if __name__ == "__main__":
    test_env_loading()
    print("Test completed.")
