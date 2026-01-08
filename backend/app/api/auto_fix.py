from fastapi import APIRouter, HTTPException
from app.models.schemas import AutoFixRequest, AutoFixResponse
from app.services.llm_client import LLMClient
from app.utils.validators import validate_code_submission

router = APIRouter()
llm_client = LLMClient()

@router.post("/auto-fix", response_model=AutoFixResponse)
async def auto_fix_code(request: AutoFixRequest):
    # 1. Validation
    validate_code_submission(request.code)
    
    # 2. Call LLM Service
    try:
        response = llm_client.fix_code(request.code, request.language)
        return response
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Auto-fix failed: {str(e)}"
        )
