from app.services.llm_client import LLMClient

# This service is a thin wrapper around LLMClient for now, 
# but allows for future expansion if we need more complex logic 
# (e.g. multi-step refactoring, running tests, etc.)

class AutoFixService:
    def __init__(self):
        self.llm_client = LLMClient()
        
    def fix_code(self, code: str, language: str):
        return self.llm_client.fix_code(code, language)
