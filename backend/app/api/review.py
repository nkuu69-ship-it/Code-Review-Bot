from fastapi import APIRouter, HTTPException, Depends
from app.models.schemas import ReviewRequest, ReviewResponse, ReviewIssue
from app.services.static_analysis import StaticAnalyzer
from app.services.llm_client import LLMClient
from app.utils.validators import validate_code_submission

router = APIRouter()
llm_client = LLMClient()

@router.post("/review", response_model=ReviewResponse)
async def review_code(request: ReviewRequest):
    # 1. Validation
    validate_code_submission(request.code)
    
    # 2. Static Analysis
    static_issues = StaticAnalyzer.analyze(request.code, request.language)
    
    # 3. LLM Analysis
    # We catch errors internally in llm_client, but could handle specific HTTP errors here
    llm_issues = llm_client.analyze_code(request.code, request.language)
    
    # 4. Merge Results
    all_issues = static_issues + llm_issues
    
    # Sort by line number for better UX (handle None lines by putting them at the top or bottom)
    all_issues.sort(key=lambda x: x.line if x.line is not None else -1)
    
    return ReviewResponse(issues=all_issues)
