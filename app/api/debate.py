"""
Debate API endpoints for argument analysis and audio processing.

This module provides endpoints for submitting and analyzing debate arguments,
including both text and audio inputs. It handles logical analysis of arguments
and speech-to-text conversion for audio submissions.
"""

from fastapi import APIRouter, HTTPException, UploadFile, File, Body
from ..models.schemas import DebateRound, DebateResponse, Side
from ..services.stt import stt_service
from ..services.logic_chain import logic_chain_service
from ..services.llm import llm_service
from ..services.tts import tts_service
from datetime import datetime
from pathlib import Path
import os
import uuid
import json
from typing import List, Dict
from pydantic import BaseModel

router = APIRouter()

# File path for debate data persistence
DEBATE_DATA_FILE = "debate_data.json"

# Load existing debate data from file
def load_debates() -> Dict[str, dict]:
    if os.path.exists(DEBATE_DATA_FILE):
        with open(DEBATE_DATA_FILE, "r") as f:
            return json.load(f)
    return {}

# Save debate data to file
def save_debates(debates: Dict[str, dict]):
    with open(DEBATE_DATA_FILE, "w") as f:
        json.dump(debates, f, default=str)

# Initialize debates from file
debates: Dict[str, dict] = load_debates()

class DebateStartRequest(BaseModel):
    topic: str
    supporting_speaker_id: str
    opposing_speaker_id: str

class DebateRoundRequest(BaseModel):
    debate_text: str
    speaker_id: str

@router.post("/start")
async def start_conversation(request: DebateStartRequest) -> Dict:
    """
    Start a new debate conversation.
    
    This endpoint initializes a new debate session with a specified topic
    and both participants' information.
    
    Args:
        request: DebateStartRequest containing:
            - topic: The debate topic or statement
            - supporting_speaker_id: ID of the speaker supporting the topic
            - opposing_speaker_id: ID of the speaker opposing the topic
            
    Returns:
        Dict containing:
            - debate_id: Unique identifier for the debate
            - topic: The debate topic
            - participants: Dict of participants and their sides
    """
    try:
        debate_id = str(uuid.uuid4())
        
        # Initialize debate data
        debates[debate_id] = {
            "topic": request.topic,
            "start_time": datetime.utcnow(),
            "rounds": [],
            "participants": {
                request.supporting_speaker_id: {
                    "side": Side.SUPPORTING,
                    "join_time": datetime.utcnow()
                },
                request.opposing_speaker_id: {
                    "side": Side.OPPOSING,
                    "join_time": datetime.utcnow()
                }
            }
        }
        
        # Save updated debate data
        save_debates(debates)
        
        return {
            "debate_id": debate_id,
            "topic": request.topic,
            "participants": debates[debate_id]["participants"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/round/{debate_id}")
async def submit_debate_round(
    debate_id: str,
    request: DebateRoundRequest
) -> Dict:
    """
    Submit a debate round for logical analysis.
    
    This endpoint processes a debate round submission, analyzing the logical structure
    and validity of the arguments presented.
    
    Args:
        debate_id: Identifier of the debate session
        request: DebateRoundRequest containing:
            - debate_text: The argument text to analyze
            - speaker_id: Identifier of the speaker
            
    Returns:
        Dict containing:
            - argument: Dict containing the argument analysis:
                - text: The original text
                - speaker_id: The speaker's identifier
                - side: The speaker's side (supporting/opposing)
                - logical_expression: The logical form of the argument
                - converted_logical_expression: Tokenized form of the logical expression
                - performance: Analysis of validity and soundness
            - round_id: Unique identifier for this round
    """
    try:
        if debate_id not in debates:
            raise HTTPException(status_code=404, detail="Debate session not found")
            
        debate = debates[debate_id]
        
        if request.speaker_id not in debate["participants"]:
            raise HTTPException(status_code=403, detail="Speaker is not a participant in this debate")
        
        if not request.debate_text:
            raise HTTPException(status_code=400, detail="No debate text provided")

        # Analyze the argument
        analysis = await logic_chain_service.analyze_logic(request.debate_text)
        
        # Store the round in debate history
        round_id = str(uuid.uuid4())
        round_data = {
            "round_index": len(debate["rounds"]),
            "text": request.debate_text,
            "speaker_id": request.speaker_id,
            "side": debate["participants"][request.speaker_id]["side"],
            "logic_chain": {
                "logic_expression": analysis.logic_expression,
                "converted_logical_expression": analysis.converted_logical_expression,
                "performance": {
                    "valid": analysis.performance.valid,
                    "valid_explanation": analysis.performance.valid_explanation,
                    "sound": analysis.performance.sound,
                    "sound_explanation": analysis.performance.sound_explanation
                }
            },
            "timestamp": datetime.utcnow()
        }
        debate["rounds"].append(round_data)
        
        # Save updated debate data
        save_debates(debates)
        
        return {
            "argument": {
                "text": request.debate_text,
                "speaker_id": request.speaker_id,
                "side": debate["participants"][request.speaker_id]["side"],
                "logical_expression": analysis.logic_expression,
                "converted_logical_expression": analysis.converted_logical_expression,
                "performance": {
                    "valid": analysis.performance.valid,
                    "valid_explanation": analysis.performance.valid_explanation,
                    "sound": analysis.performance.sound,
                    "sound_explanation": analysis.performance.sound_explanation
                }
            },
            "round_id": round_id
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/audio/{debate_id}")
async def submit_audio(debate_id: str, file: UploadFile = File(...), speaker_id: str = None) -> Dict:
    """
    Process audio input for debate analysis.
    
    This endpoint handles audio submissions for debate arguments. It performs
    speech-to-text conversion and then processes the transcribed text through
    the debate round analysis pipeline.
    
    Args:
        debate_id: The identifier of the debate session
        file: Audio file upload (WAV format) containing the spoken argument
        speaker_id: Identifier of the speaker
            
    Returns:
        Same as submit_debate_round endpoint
            
    Raises:
        HTTPException: If there are errors in audio processing or analysis
    """
    try:
        if debate_id not in debates:
            raise HTTPException(status_code=404, detail="Debate session not found")

        # Save audio file with unique name
        temp_audio_path = Path(f"temp_{uuid.uuid4()}.wav")
        with open(temp_audio_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)

        try:
            # Convert speech to text
            debate_text = await stt_service.transcribe_audio(temp_audio_path)
        finally:
            # Clean up temporary file
            if temp_audio_path.exists():
                os.remove(temp_audio_path)

        # Process text through debate round analysis
        return await submit_debate_round(debate_id, DebateRoundRequest(debate_text=debate_text, speaker_id=speaker_id))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history/{debate_id}")
async def get_debate_history(debate_id: str) -> Dict:
    """
    Retrieve the full history of a debate conversation.
    
    This endpoint returns all rounds of debate for a given session,
    including all participants' arguments and logical analyses.
    
    Args:
        debate_id: The unique identifier of the debate session
        
    Returns:
        Dict containing:
            - debate_id: The requested debate ID
            - topic: The debate topic
            - participants: Dict of participants and their sides
            - rounds: List of all debate rounds, each containing:
                - round_index: Index of the round
                - text: The argument text
                - speaker_id: Identifier of the speaker
                - side: The speaker's side
                - logic_chain: Analysis of the argument
                - timestamp: When the round occurred
            
    Raises:
        HTTPException: If the debate session is not found
    """
    try:
        if debate_id not in debates:
            raise HTTPException(status_code=404, detail="Debate session not found")
            
        debate = debates[debate_id]
        
        return {
            "debate_id": debate_id,
            "topic": debate["topic"],
            "participants": debate["participants"],
            "rounds": debate["rounds"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 