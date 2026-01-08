import json
from typing import List, Optional, Any, Dict

from app.core.config import settings
from app.services.prompt_builder import PromptBuilder
from app.models.schemas import ReviewIssue, AutoFixResponse, AutoFixChange

from huggingface_hub import InferenceClient

class LLMClient:
    def __init__(self):
        self.api_token = settings.HUGGINGFACE_API_TOKEN
        
        # Initialize client only if key is present
        self.client = None
        if self.api_token:
            self.client = InferenceClient(
                token=self.api_token,
                model=settings.MODEL_NAME
            )

    def analyze_code(self, code: str, language: str) -> List[ReviewIssue]:
        if not self.client:
            return []
            
        system_msg = PromptBuilder.build_system_message()
        user_msg = PromptBuilder.build_user_message(code, language)

        try:
            return self._call_llm_review(system_msg, user_msg)
        except Exception:
            # Retry once
            try:
                return self._call_llm_review(system_msg, user_msg)
            except Exception as e:
                print(f"LLM Review Failure: {e}")
                return []

    def fix_code(self, code: str, language: str) -> AutoFixResponse:
        if not self.client:
            raise ValueError("Hugging Face API Client not initialized. Please check your HUGGINGFACE_API_TOKEN.")
            
        system_msg = PromptBuilder.build_auto_fix_system_message()
        user_msg = PromptBuilder.build_auto_fix_user_message(code, language)

        try:
            return self._call_llm_fix(system_msg, user_msg)
        except Exception:
            # Retry once
            try:
                return self._call_llm_fix(system_msg, user_msg)
            except Exception as e:
                print(f"LLM Auto-Fix Failure: {e}")
                raise e

    def _call_llm_review(self, system_msg: str, user_msg: str) -> List[ReviewIssue]:
        content = self._make_request(system_msg, user_msg)
        if not content:
            return []

        # Parse JSON
        try:
            # Cleanup potential markdown code blocks if the model includes them despite instructions
            cleaned_content = self._clean_json_markdown(content)
            data = json.loads(cleaned_content, strict=False)
            
            issues_data = data.get("issues", [])
            
            valid_issues = []
            for item in issues_data:
                if "explanation" in item and "suggested_fix" in item and "severity" in item:
                    sev = item["severity"].lower()
                    if sev not in ["bug", "warning", "improvement", "security"]:
                        sev = "warning"
                    valid_issues.append(ReviewIssue(
                        line=item.get("line"),
                        severity=sev,
                        explanation=item["explanation"],
                        suggested_fix=item["suggested_fix"]
                    ))
            return valid_issues
        except json.JSONDecodeError:
            print(f"JSON Parse Error. Content: {content}")
            raise ValueError("Failed to parse LLM response as JSON")

    def _call_llm_fix(self, system_msg: str, user_msg: str) -> AutoFixResponse:
        content = self._make_request(system_msg, user_msg)
        if not content:
            raise ValueError("Empty response from LLM")

        try:
            cleaned_content = self._clean_json_markdown(content)
            data = json.loads(cleaned_content, strict=False)
            
            # Validate response structure
            if "fixed_code" not in data or "summary" not in data:
                 raise ValueError("Missing required fields in AutoFix response")
            
            changes = []
            if "changes" in data and isinstance(data["changes"], list):
                for c in data["changes"]:
                    changes.append(AutoFixChange(
                        line=c.get("line"),
                        before=c.get("before", ""),
                        after=c.get("after", ""),
                        reason=c.get("reason", "")
                    ))

            return AutoFixResponse(
                fixed_code=data["fixed_code"],
                summary=data["summary"],
                changes=changes
            )
        except json.JSONDecodeError:
             print(f"JSON Parse Error. Content: {content}")
             raise ValueError("Failed to parse LLM response as JSON")

    def _make_request(self, system_msg: str, user_msg: str) -> str:
        # Use chat_completion for easy interface
        response = self.client.chat_completion(
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_msg}
            ],
            temperature=0.2,
            max_tokens=3000,
            seed=42
        )
        return response.choices[0].message.content

    def _clean_json_markdown(self, content: str) -> str:
        content = content.strip()
        if content.startswith("```json"):
            content = content[7:]
        elif content.startswith("```"):
            content = content[3:]
        
        if content.endswith("```"):
            content = content[:-3]
        return content.strip()
