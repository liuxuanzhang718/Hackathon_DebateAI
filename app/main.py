from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = FastAPI(title="Debate AI Platform")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import routers
from app.api.agent_training import router as agent_training_router
from app.api.debate import router as debate_router
from app.api.tutorial import router as tutorial_router

# Include routers
app.include_router(agent_training_router, prefix="/agent-training", tags=["agent-training"])
app.include_router(debate_router, prefix="/debate", tags=["debate"])
app.include_router(tutorial_router, prefix="/tutorial", tags=["tutorial"])

@app.get("/")
async def root():
    return {"message": "Welcome to Debate AI Platform"}

if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    debug = os.getenv("DEBUG", "True").lower() == "true"
    uvicorn.run("app.main:app", host=host, port=port, reload=debug) 