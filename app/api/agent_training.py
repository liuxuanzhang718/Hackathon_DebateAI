"""
Agent Training API endpoints for debate simulation.

This module provides endpoints for training debate agents through interactive sessions.
It handles conversation management, debate rounds, and logical analysis of arguments.
"""

from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks, Form
from ..models.schemas import (
    AgentTrainingStartRequest,
    AgentTrainingRoundRequest,
    AgentTrainingResponse,
    AgentTrainingHistoryResponse,
    Side
)
from ..services.stt import stt_service
from ..services.llm import llm_service
from ..services.tts import tts_service
from ..services.logic_chain import logic_chain_service
from pathlib import Path
import os
from typing import Dict, List, Optional
import uuid
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

router = APIRouter()

# Predefined debate topics for training sessions
DEBATE_TOPICS = [
    {
        "id": 1,
        "title": "Climate Policy",
        "description": "Renewable energy must be adopted immediately to protect our planet."
    },
    {
        "id": 2,
        "title": "Artificial Intelligence",
        "description": "Strict AI ethics are needed to safeguard human rights."
    },
    {
        "id": 3,
        "title": "Healthcare Reform",
        "description": "Universal healthcare should be affordable and accessible."
    },
    {
        "id": 4,
        "title": "Economic Policy",
        "description": "Progressive taxation is key to reducing income inequality."
    },
    {
        "id": 5,
        "title": "Education Systems",
        "description": "Modern education must leverage tech and personalization."
    },
    {
        "id": 6, 
        "title": "Global Security",
        "description": "International cooperation and strong defense are essential."
    },
    {
        "id": 7,
        "title": "Social Justice",
        "description": "Eliminating bias and ensuring equal rights is vital."
    }
]

# In-memory storage for active conversations (replace with database in production)
conversations: Dict[str, dict] = {}

@router.post("/start")
async def start_conversation(request: AgentTrainingStartRequest) -> Dict:
    """
    Start a new debate training conversation.
    
    Args:
        request: AgentTrainingStartRequest containing:
            - topic_id: The ID of the debate topic
            - user_side: The side chosen by the user
            
    Returns:
        Dict containing:
            - conversation_id: Unique identifier for the conversation
            - topic: Topic information
            - user_side: The side chosen by the user
    """
    try:
        conversation_id = str(uuid.uuid4())
        
        # Get topic information
        topic = next((t for t in DEBATE_TOPICS if t["id"] == request.topic_id), None)
        if not topic:
            raise HTTPException(status_code=400, detail="Invalid topic ID")
        
        # Initialize conversation data
        conversations[conversation_id] = {
            "topic": request.topic_id,
            "topic_info": topic,
            "user_side": request.user_side,
            "start_time": datetime.utcnow(),
            "rounds": []
        }
        
        return {
            "conversation_id": conversation_id,
            "topic": topic,
            "user_side": request.user_side
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/round/{conversation_id}")
async def process_debate_round(
    conversation_id: str,
    request: AgentTrainingRoundRequest
) -> AgentTrainingResponse:
    """
    Process a debate round with text input.
    
    Args:
        conversation_id: ID of the active conversation
        request: AgentTrainingRoundRequest containing:
            - user_utterance: The user's argument text
            
    Returns:
        AgentTrainingResponse containing:
            - user_response: User's argument analysis
            - ai_response: AI's response and analysis
            - round_id: Unique identifier for this round
    """
    try:
        if conversation_id not in conversations:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        conversation = conversations[conversation_id]
        
        if not request.user_utterance:
            raise HTTPException(status_code=400, detail="No user text provided")

        # Analyze user's argument
        user_analysis = await logic_chain_service.analyze_logic(request.user_utterance)

        # Generate AI's response
        agent_response = await llm_service.generate_debate_response(
            topic=conversation["topic"],
            user_side=conversation["user_side"],
            user_utterance=request.user_utterance
        )

        # Generate audio for AI's response
        audio_url = await tts_service.text_to_speech(agent_response)

        # Analyze AI's response
        agent_analysis = await logic_chain_service.analyze_logic(agent_response)

        # Store the round in conversation history
        round_id = str(uuid.uuid4())
        round_data = {
            "round_index": len(conversation["rounds"]),
            "user": {
                "text": request.user_utterance,
                "logic_chain": {
                    "logic_expression": user_analysis.logic_expression,
                    "converted_logical_expression": user_analysis.converted_logical_expression,
                    "performance": {
                        "valid": user_analysis.performance.valid,
                        "valid_explanation": user_analysis.performance.valid_explanation,
                        "sound": user_analysis.performance.sound,
                        "sound_explanation": user_analysis.performance.sound_explanation
                    }
                }
            },
            "ai": {
                "text": agent_response,
                "audio_url": audio_url,
                "logic_chain": {
                    "logic_expression": agent_analysis.logic_expression,
                    "converted_logical_expression": agent_analysis.converted_logical_expression,
                    "performance": {
                        "valid": agent_analysis.performance.valid,
                        "valid_explanation": agent_analysis.performance.valid_explanation,
                        "sound": agent_analysis.performance.sound,
                        "sound_explanation": agent_analysis.performance.sound_explanation
                    }
                }
            },
            "timestamp": datetime.utcnow()
        }
        conversation["rounds"].append(round_data)

        return AgentTrainingResponse(
            user_response={
                "text": request.user_utterance,
                "logic_chain": {
                    "logic_expression": user_analysis.logic_expression,
                    "converted_logical_expression": user_analysis.converted_logical_expression,
                    "performance": {
                        "valid": user_analysis.performance.valid,
                        "valid_explanation": user_analysis.performance.valid_explanation,
                        "sound": user_analysis.performance.sound,
                        "sound_explanation": user_analysis.performance.sound_explanation
                    }
                }
            },
            ai_response={
                "text": agent_response,
                "audio_url": audio_url,
                "logic_chain": {
                    "logic_expression": agent_analysis.logic_expression,
                    "converted_logical_expression": agent_analysis.converted_logical_expression,
                    "performance": {
                        "valid": agent_analysis.performance.valid,
                        "valid_explanation": agent_analysis.performance.valid_explanation,
                        "sound": agent_analysis.performance.sound,
                        "sound_explanation": agent_analysis.performance.sound_explanation
                    }
                }
            },
            round_id=round_id
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history/{conversation_id}")
async def get_conversation_history(conversation_id: str) -> AgentTrainingHistoryResponse:
    """
    Retrieve the full history of a debate conversation.
    
    Args:
        conversation_id: The unique identifier of the conversation
        
    Returns:
        AgentTrainingHistoryResponse containing:
            - conversation_id: The requested conversation ID
            - topic_id: The debate topic ID
            - rounds: List of all debate rounds
    """
    try:
        if conversation_id not in conversations:
            raise HTTPException(status_code=404, detail="Conversation not found")
            
        conversation = conversations[conversation_id]
        
        return AgentTrainingHistoryResponse(
            conversation_id=conversation_id,
            topic_id=conversation["topic"],
            rounds=conversation["rounds"]
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/audio/{conversation_id}")
async def submit_audio(conversation_id: str, file: UploadFile = File(...), speaker_id: str = Form(...)) -> Dict:
    """
    Process audio input for training debate.
    
    This endpoint handles audio submissions for debate arguments. It performs
    speech-to-text conversion and then processes the transcribed text through
    the debate round analysis pipeline.
    
    Args:
        conversation_id: The identifier of the training conversation
        file: Audio file upload (WAV format) containing the spoken argument
        speaker_id: The ID of the speaker
            
    Returns:
        Dict containing:
            - user_response: Dict containing user's argument analysis:
                - text: The transcribed text from audio
                - logical_expression: The logical form of the argument
                - converted_logical_expression: Tokenized form of the logical expression
                - performance: Analysis of validity and soundness
            - ai_response: Dict containing AI's response:
                - text: The AI's response text
                - audio_url: URL to the generated audio file
                - logical_expression: The logical form of AI's response
                - converted_logical_expression: Tokenized form of AI's response
                - performance: Analysis of validity and soundness
            - round_id: Unique identifier for this round
            
    Raises:
        HTTPException: If there are errors in audio processing or analysis
        
    Note:
        The audio file is temporarily stored during processing and then
        automatically cleaned up.
    """
    try:
        logger.info(f"Processing audio submission for conversation {conversation_id}")
        
        # Validate conversation exists
        if conversation_id not in conversations:
            logger.error(f"Conversation {conversation_id} not found")
            raise HTTPException(status_code=404, detail="Conversation not found")

        # Get conversation data
        conversation = conversations[conversation_id]
        logger.info(f"Found conversation with topic: {conversation['topic']}")

        # Validate file content type
        logger.info(f"File content type: {file.content_type}, filename: {file.filename}")
        if not (file.content_type.startswith('audio/') or file.filename.endswith('.wav')):
            logger.error(f"Invalid file type: {file.content_type}")
            raise HTTPException(status_code=400, detail="Invalid file type. Must be audio file.")

        # Create audio_storage directory if it doesn't exist
        audio_dir = Path("audio_storage")
        audio_dir.mkdir(exist_ok=True)
        logger.info(f"Audio directory ensured: {audio_dir}")
        
        # Save audio file with unique name in audio_storage directory
        temp_audio_path = audio_dir / f"temp_{uuid.uuid4()}.wav"
        try:
            # Save uploaded file
            logger.info(f"Saving uploaded file to {temp_audio_path}")
            content = await file.read()
            logger.info(f"Read file content, size: {len(content)} bytes")
            
            if len(content) == 0:
                logger.error("Uploaded file is empty")
                raise HTTPException(status_code=400, detail="Uploaded file is empty")
            
            with open(temp_audio_path, "wb") as buffer:
                buffer.write(content)
            logger.info(f"Successfully saved audio file")

            # Convert speech to text
            logger.info("Starting speech-to-text conversion")
            try:
                debate_text = await stt_service.transcribe_audio(temp_audio_path)
                logger.info(f"Successfully transcribed audio to text: {debate_text}")
            except FileNotFoundError as fnf:
                logger.error(f"Audio file not found: {str(fnf)}")
                raise HTTPException(status_code=500, detail=f"Audio file not found: {str(fnf)}")
            except PermissionError as pe:
                logger.error(f"Permission error: {str(pe)}")
                raise HTTPException(status_code=500, detail=f"Permission error: {str(pe)}")
            except ValueError as ve:
                logger.error(f"Invalid audio content: {str(ve)}")
                raise HTTPException(status_code=400, detail=f"Invalid audio content: {str(ve)}")
            except Exception as stt_error:
                logger.error(f"Speech-to-text error: {str(stt_error)}")
                raise HTTPException(status_code=500, detail=f"Speech-to-text error: {str(stt_error)}")

            # Process text through debate round analysis
            logger.info("Processing debate round")
            try:
                request = AgentTrainingRoundRequest(
                    user_utterance=debate_text
                )
                logger.info("Created debate round request")
                
                result = await process_debate_round(conversation_id, request)
                logger.info("Successfully processed debate round")
                
                # Convert AgentTrainingResponse to dictionary
                response_dict = {
                    "user_response": result.user_response,
                    "ai_response": {
                        "text": result.ai_response["text"],
                        "audio_url": result.ai_response["audio_url"],
                        "logic_chain": result.ai_response["logic_chain"]
                    },
                    "round_id": result.round_id
                }
                return response_dict
                
            except Exception as process_error:
                logger.error(f"Error processing debate round: {str(process_error)}")
                raise HTTPException(status_code=500, detail=f"Error processing debate round: {str(process_error)}")

        except HTTPException as he:
            raise he
        except Exception as e:
            logger.error(f"Error processing audio: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            # Clean up temporary file
            if temp_audio_path.exists():
                try:
                    os.remove(temp_audio_path)
                    logger.info(f"Cleaned up temporary file: {temp_audio_path}")
                except Exception as cleanup_error:
                    logger.error(f"Failed to clean up temporary file: {str(cleanup_error)}")

    except HTTPException as he:
        logger.error(f"HTTP Exception in submit_audio: {he.detail}")
        raise he
    except Exception as e:
        logger.error(f"Unexpected error in submit_audio: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/logic-chain/{conversation_id}")
async def get_logic_chain(conversation_id: str) -> Dict:
    """
    Retrieve the logical chain analysis for a conversation.
    
    Args:
        conversation_id: The unique identifier of the conversation
        
    Returns:
        Dict containing:
            - topic: The debate topic
            - logic_chains: List of all logical analyses in chronological order:
                - round_index: Index of the debate round
                - user_chain: User's logical analysis
                - ai_chain: AI's logical analysis
                - timestamp: When the analysis occurred
    """
    try:
        if conversation_id not in conversations:
            raise HTTPException(status_code=404, detail="Conversation not found")
            
        conversation = conversations[conversation_id]
        
        logic_chains = []
        for round_data in conversation["rounds"]:
            logic_chains.append({
                "round_index": round_data["round_index"],
                "user_chain": {
                    "text": round_data["user"]["text"],
                    "logic_expression": round_data["user"]["logic_chain"]["logic_expression"],
                    "converted_logical_expression": round_data["user"]["logic_chain"]["converted_logical_expression"],
                    "performance": round_data["user"]["logic_chain"]["performance"]
                },
                "ai_chain": {
                    "text": round_data["ai"]["text"],
                    "logic_expression": round_data["ai"]["logic_chain"]["logic_expression"],
                    "converted_logical_expression": round_data["ai"]["logic_chain"]["converted_logical_expression"],
                    "performance": round_data["ai"]["logic_chain"]["performance"]
                },
                "timestamp": round_data["timestamp"]
            })
        
        return {
            "topic": conversation["topic_info"],
            "logic_chains": logic_chains
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/logic-chain/{conversation_id}/current")
async def get_current_logic_chain(conversation_id: str) -> Dict:
    """
    Retrieve the logical chain analysis for the current round.
    
    Args:
        conversation_id: The unique identifier of the conversation
        
    Returns:
        Dict containing the latest round's logical analysis
    """
    try:
        if conversation_id not in conversations:
            raise HTTPException(status_code=404, detail="Conversation not found")
            
        conversation = conversations[conversation_id]
        
        if not conversation["rounds"]:
            raise HTTPException(status_code=404, detail="No rounds found in conversation")
            
        # Get the latest round
        current_round = conversation["rounds"][-1]
        
        return {
            "topic": conversation["topic_info"],
            "current_chain": {
                "round_index": current_round["round_index"],
                "user_chain": {
                    "text": current_round["user"]["text"],
                    "logic_expression": current_round["user"]["logic_chain"]["logic_expression"],
                    "converted_logical_expression": current_round["user"]["logic_chain"]["converted_logical_expression"],
                    "performance": current_round["user"]["logic_chain"]["performance"]
                },
                "ai_chain": {
                    "text": current_round["ai"]["text"],
                    "logic_expression": current_round["ai"]["logic_chain"]["logic_expression"],
                    "converted_logical_expression": current_round["ai"]["logic_chain"]["converted_logical_expression"],
                    "performance": current_round["ai"]["logic_chain"]["performance"]
                },
                "timestamp": current_round["timestamp"]
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 