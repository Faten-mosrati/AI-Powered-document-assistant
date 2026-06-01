from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.api import router

app = FastAPI(
    title="Email Triage Agent",
    version="0.1.0",
    description=(
        "Classifies emails and drafts replies. Stateless service consumed by NestJS."
    ),
)

# CORS: in this phase you only call from Postman + NestJS (local).
# Lock this down to specific origins before deploying anywhere.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
