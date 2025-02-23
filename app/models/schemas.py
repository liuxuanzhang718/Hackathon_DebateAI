from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Literal
from enum import Enum
from datetime import datetime

class Side(str, Enum):
    SUPPORTING = "supporting"
    OPPOSING = "opposing"

class LogicalPerformance(BaseModel):
    valid: bool = Field(description="Whether the argument is logically valid")
    valid_explanation: Optional[str] = Field(description="Explanation if argument is invalid")
    sound: bool = Field(description="Whether the argument is logically sound") 
    sound_explanation: Optional[str] = Field(description="Explanation if argument is unsound")

class LogicChain(BaseModel):
    logic_expression: str = Field(description="The logical expression of the argument")
    converted_logical_expression: List[str] = Field(description="The converted logical expression tokens")
    performance: LogicalPerformance = Field(description="Analysis of logical validity and soundness")

# Tutorial Models
class TutorialQuestion(BaseModel):
    id: int
    example: List[str]
    question: List[str]
    answer: bool
    explanation: str

class TutorialAnswerRequest(BaseModel):
    question_id: int
    user_answer: bool

class TutorialAnswerResponse(BaseModel):
    correct: bool
    explanation: Optional[str] = None

# Debate Models
class DebateRound(BaseModel):
    speaker_id: str
    debate_text: str
    debate_id: str
    timestamp: datetime = Field(default_factory=datetime.now)

class DebateResponse(BaseModel):
    success: bool
    logic_chain: LogicChain
    round_id: Optional[str] = None

# Agent Training Models
class AgentTrainingStartRequest(BaseModel):
    topic_id: str
    user_side: Side

class AgentTrainingRoundRequest(BaseModel):
    user_utterance: str

class AgentTrainingResponse(BaseModel):
    user_response: Dict = Field(description="User's argument analysis")
    ai_response: Dict = Field(description="AI's response and analysis")
    round_id: str = Field(description="Unique identifier for this round")

class AgentTrainingHistoryResponse(BaseModel):
    conversation_id: str
    topic_id: str
    rounds: List[Dict]

# Topic Models
class DebateTopic(BaseModel):
    id: str
    title: str
    description: str
    difficulty_level: Optional[str] = None
    categories: Optional[List[str]] = None

# Audio Processing Models
class AudioTranscriptionRequest(BaseModel):
    file_path: str
    speaker_id: Optional[str] = None
    debate_id: Optional[str] = None

class AudioTranscriptionResponse(BaseModel):
    text: str
    confidence: float
    duration: float 