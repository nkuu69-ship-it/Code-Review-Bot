from fastapi import HTTPException
from app.core.config import settings

def validate_code_submission(code: str):
    """
    Validates the input code submission for size limits.
    """
    if len(code) > settings.MAX_CODE_LENGTH:
        raise HTTPException(
            status_code=413,
            detail=f"Code submission exceeds maximum length of {settings.MAX_CODE_LENGTH} characters."
        )
    
    if not code.strip():
        raise HTTPException(
            status_code=400,
            detail="Code cannot be empty."
        )
