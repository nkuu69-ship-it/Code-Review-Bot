import os

class PromptBuilder:
    
    SYSTEM_PROMPT_REVIEW = """You are a Senior Software Engineer and Code Reviewer. 
Your task is to review the provided code snippet. 
Focus on:
1. Logic errors, bugs, and edge cases.
2. clean code best practices (style, naming, etc.).
3. Performance optimizations (time/space complexity).
4. Security vulnerabilities.

You MUST follow these rules:
- Be constructive and professional.
- Provide a STRICT JSON output. The output must parse directly as JSON.
- Do not include markdown formatting (like ```json ... ```) in the response if possible, or ensure it's strip-able. 
- Return an object with a single key "issues", which is a list of objects.
- Each object in the list must have: "line" (number or null), "severity" (enum: "bug", "warning", "improvement", "security"), "explanation" (string), "suggested_fix" (string).
"""

    USER_TEMPLATE_REVIEW = """
Review the following {language} code:

```
{code}
```

Return the JSON analysis.
"""

    # We load the prompt from file if possible, otherwise fallback to this string
    SYSTEM_PROMPT_AUTO_FIX = """You are a Senior Software Engineer acting as an automated code fixing engine.
Your goal is to REFACTOR and FIX the provided code while preserving its original logic and function signatures as much as possible.

RULES:
1. SAFE FIXES ONLY: Only fix detected bugs, logic errors, syntax issues, and major inefficiencies.
2. NO NEW FEATURES: Do not add new features or functionality.
3. PRESERVE COMMENTS: Keep existing comments unless they are incorrect/outdated.
4. FORMATTING: Ensure the output code is clean, properly formatted, and idiomatic for the language.
5. JSON OUTPUT: You must output STRICT VALID JSON.
6. ESCAPING: Ensure newlines in code strings are escaped as literal \\n.

Your output JSON must have this structure:
{
  "fixed_code": "STRING - The entire fixed source code file",
  "summary": "STRING - specific summary of what was fixed",
  "changes": [
    {
      "line": NUMBER or null,
      "before": "STRING - snippet of code before change",
      "after": "STRING - snippet of code after change",
      "reason": "STRING - why this change was made"
    }
  ]
}
"""

    USER_TEMPLATE_AUTO_FIX = """
Fix the following {language} code:

```
{code}
```

Return the JSON with fixed_code, summary, and changes.
"""

    @staticmethod
    def build_system_message() -> str:
        return PromptBuilder.SYSTEM_PROMPT_REVIEW

    @staticmethod
    def build_user_message(code: str, language: str) -> str:
        return PromptBuilder.USER_TEMPLATE_REVIEW.format(language=language, code=code)

    @staticmethod
    def build_auto_fix_system_message() -> str:
        # Try to load from file for "production" feel, fallback to constant
        try:
            prompt_path = os.path.join(os.path.dirname(__file__), "..", "prompts", "auto_fix_prompt.txt")
            if os.path.exists(prompt_path):
                with open(prompt_path, "r") as f:
                    return f.read()
        except Exception:
            pass
        return PromptBuilder.SYSTEM_PROMPT_AUTO_FIX

    @staticmethod
    def build_auto_fix_user_message(code: str, language: str) -> str:
        return PromptBuilder.USER_TEMPLATE_AUTO_FIX.format(language=language, code=code)
