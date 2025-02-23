from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(title="Debate AI Platform")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import routers - 修改这里的导入路径
from .api.agent_training import router as agent_training_router
from .api.debate import router as debate_router
from .api.tutorial import router as tutorial_router

# Include routers
app.include_router(agent_training_router, prefix="/agent-training", tags=["agent-training"])
app.include_router(debate_router, prefix="/debate", tags=["debate"])
app.include_router(tutorial_router, prefix="/tutorial", tags=["tutorial"])

@app.get("/")
async def root():
    return {"message": "Welcome to Debate AI Platform"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 