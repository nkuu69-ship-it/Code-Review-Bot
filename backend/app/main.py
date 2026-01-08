from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import review, auto_fix
from app.core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(review.router, prefix=settings.API_V1_STR, tags=["review"])
app.include_router(auto_fix.router, prefix=settings.API_V1_STR, tags=["auto-fix"])

@app.get("/health")
def health_check():
    return {"status": "ok", "app_name": settings.APP_NAME}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
