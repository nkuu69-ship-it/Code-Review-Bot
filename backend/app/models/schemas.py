from pydantic import BaseModel, Field
from typing import List, Optional, Literal

class ReviewRequest(BaseModel):
    code: str = Field(..., min_length=1, description="Source code to review")
    language: Literal["python", "javascript", "java", "cpp"] = Field(..., description="Programming language of the code")

class ReviewIssue(BaseModel):
    line: Optional[int] = Field(None, description="Line number where the issue occurs (1-indexed)")
    severity: Literal["bug", "warning", "improvement", "security"] = Field(..., description="Severity level of the issue")
    explanation: str = Field(..., description="Detailed explanation of the issue")
    suggested_fix: str = Field(..., description="Code snippet or description of how to fix it")

class ReviewResponse(BaseModel):
    issues: List[ReviewIssue] = Field(default_factory=list, description="List of detected issues")

class ErrorResponse(BaseModel):
    detail: str

# Auto-Fix Schemas
class AutoFixRequest(BaseModel):
    code: str = Field(..., min_length=1, description="Source code to fix")
    language: Literal["python", "javascript", "java", "cpp"] = Field(..., description="Programming language of the code")

class AutoFixChange(BaseModel):
    line: Optional[int] = Field(None, description="Line number where the change occurred")
    before: str = Field(..., description="Original code snippet")
    after: str = Field(..., description="Fixed code snippet")
    reason: str = Field(..., description="Reason for the change")

class AutoFixResponse(BaseModel):
    fixed_code: str = Field(..., description="The completely fixed source code")
    summary: str = Field(..., description="Summary of changes made")
    changes: List[AutoFixChange] = Field(default_factory=list, description="List of specific changes")
