"""
Tutorial API endpoints for debate training exercises.

This module provides endpoints for interactive debate training tutorials,
helping users understand logical structures and argument analysis through
practice exercises with immediate feedback.
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

router = APIRouter()

# Tutorial questions with examples, questions, answers, and explanations
tutorial_questions = [
    {
        "id": 1,
        "example": ["emily happy", "4", "have desert"],
        "question": ["emily has desert", "4", "emily happy"],
        "answer": False,
        "explanation": "The example and question have different logical structures: 'emily happy' vs 'emily has desert'."
    }
]

class TutorialAnswerRequest(BaseModel):
    question_id: int
    user_answer: bool

@router.get("/next-question")
async def next_question():
    """
    Get the next tutorial question for practice.
    
    This endpoint provides a new logical analysis exercise, including an example
    logical expression and a question to analyze. Users can practice identifying
    logical structures and relationships between statements.
    
    Returns:
        JSONResponse containing:
            - example: List of tokens representing an example logical expression
            - question: List of tokens to analyze and compare with the example
            
    Note:
        The example and question are presented as tokenized lists to help users
        understand the logical structure more clearly.
    """
    # Return the next practice question
    question = tutorial_questions[0]
    return JSONResponse(content={
        "example": question["example"],
        "question": question["question"]
    })

@router.post("/answer")
async def submit_answer(request: TutorialAnswerRequest):
    """
    Submit an answer to a tutorial question.
    
    This endpoint processes user answers to tutorial questions, providing
    immediate feedback and explanations for incorrect answers. It helps users
    understand why their analysis was correct or incorrect.
    
    Args:
        request: TutorialAnswerRequest containing:
            - question_id: The identifier of the question being answered
            - user_answer: The user's True/False assessment of logical equivalence
        
    Returns:
        JSONResponse containing:
            - correct: Boolean indicating if the answer was correct
            - explanation: Detailed explanation if the answer was incorrect
            
    Raises:
        HTTPException: If the question ID is invalid
        
    Note:
        Explanations are only provided for incorrect answers to help users
        understand their mistakes and learn from them.
    """
    # Find the question by ID
    question = next((q for q in tutorial_questions if q["id"] == request.question_id), None)
    if not question:
        raise HTTPException(status_code=400, detail="Invalid question ID")
    
    # Check the answer and prepare response
    correct = (request.user_answer == question["answer"])
    response_data = {
        "correct": correct
    }
    if not correct:
        response_data["explanation"] = question["explanation"]
    
    return JSONResponse(content=response_data) 