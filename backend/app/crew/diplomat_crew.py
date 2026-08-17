from backend.app.crew.agents import DiplomatTranslatorAgent, StyleReviewerAgent
from backend.app.tools.glossary import GlossaryTool
from backend.app.crew.tasks import TranslationTaskOutput, ReviewTaskOutput

class Crew:
    def __init__(self):
        self.glossary_tool = GlossaryTool("backend/data/glossary.json")
        self.translator = DiplomatTranslatorAgent(self.glossary_tool)
        self.reviewer = StyleReviewerAgent()

    def kickoff(self, inputs: dict) -> dict:
        print(f"[DEBUG] Crew.kickoff received inputs: {inputs}")
        # Sequential process
        input_text = inputs.get("text")
        direction = inputs.get("direction")
        translated_text = self.translator.act(input_text, direction)
        print(f"[DEBUG] Translated text: {translated_text}")
        review_result = self.reviewer.act(translated_text)
        print(f"[DEBUG] Review result: {review_result}")
        return {
            "translated": review_result["final_text"],
            "notes": review_result.get("notes")
        }

crew = Crew()
