import json
from typing import Optional

class GlossaryTool:
    def __init__(self, glossary_path: str):
        with open(glossary_path, 'r', encoding='utf-8') as f:
            self.glossary_data = json.load(f)
        self.term_map = {item['term'].lower(): item['definition'] for item in self.glossary_data.get('terms', [])}

    def query(self, term: str) -> Optional[str]:
        """Query the glossary for a term (case-insensitive). Return the definition or None if not found."""
        return self.term_map.get(term.lower())
