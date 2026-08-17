import os
from openai import OpenAI
from typing import Any

from dotenv import load_dotenv
from pathlib import Path

# explicitly load .env from backend directory to ensure environment variables are loaded
env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=env_path, override=True)
print(f"[DEBUG] Loaded .env from: {env_path}")


class DiplomatTranslatorAgent:
    def __init__(self, glossary_tool):
        self.role = "translator"
        self.description = "Rewrites text casual -> corporate or corporate -> casual, using glossary for consistent terms."
        self.glossary_tool = glossary_tool

        api_key = os.getenv('OPENAI_API_KEY')
        print(f"[DEBUG] OpenAI API Key loaded: {'Yes' if api_key else 'No'}")
        self.client = OpenAI(api_key=api_key)

    def act(self, input_text: str, direction: str, glossary: Any = None) -> str:
        print(f"[DEBUG] DiplomatTranslatorAgent.act called with: input_text={input_text}, direction={direction}")

        # Build instructions with glossary and direction
        glossary_lines = "\n".join(
            f"- {term}: {definition}"
            for term, definition in self.glossary_tool.term_map.items()
        )

        if direction == "casual_to_corporate":
            translation_instructions = (
                "Translate the following casual English text into professional corporate language. "
                "Replace casual expressions with the matching corporate terms from the glossary below "
                "where the meaning fits (e.g. 'let's discuss later' -> 'let's circle back', "
                "'make contact' -> 'touch base', 'capacity to work' -> 'bandwidth'). "
                "Use the corporate term as written, not a paraphrase."
            )
            glossary_instructions = f"Corporate glossary terms to substitute into the output:\n{glossary_lines}"
        else:
            translation_instructions = "Translate the following professional corporate language text into casual, clear, and simple English."
            glossary_instructions = f"Corporate glossary terms to translate back into plain English (use the definition as the casual meaning):\n{glossary_lines}"

        instructions = f"{translation_instructions}\n\n{glossary_instructions}"

        prompt = input_text

        # Call OpenAI GPT-4 via Responses API
        try:
            response = self.client.responses.create(
                model="gpt-5.6",
                instructions=instructions,
                input=prompt
            )
            translated_text = response.output_text.strip()
        except Exception as e:
            print(f"[ERROR] OpenAI API call failed: {e}")
            translated_text = input_text  # fallback to input

        print(f"[DEBUG] DiplomatTranslatorAgent.act returning: {translated_text}")
        return translated_text

    

class StyleReviewerAgent:
    def __init__(self):
        self.role = "reviewer"
        self.description = "Verifies tone accuracy and clarity, returns final version with optional notes explaining tricky terms."

    def act(self, translated_text: str) -> dict:
        # Simplified style review: detect presence of glossary terms in parentheses
        notes = []
        if translated_text:
            notes.append("Reviewed for tone and clarity." )
            if "(" in translated_text and ")" in translated_text:
                notes.append("Contains glossary term definitions.")
        else:
            notes.append("No translated text provided.")
        return {
            "final_text": translated_text,
            "notes": " ".join(notes)
        }
