from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import workflow_router, template_router

app = FastAPI(title="Workflow Management API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(workflow_router.router)
app.include_router(template_router.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
