from openai import OpenAI
from typing import List, Dict
from ..config import settings
from ..models.schemas import Side

class LLMService:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    async def generate_debate_response(
        self,
        topic: str,
        user_side: Side,
        user_utterance: str,
        conversation_history: List[Dict[str, str]] = None
    ) -> str:
        """
        Generate a debate response using OpenAI's GPT API.
        
        Args:
            topic: The debate topic
            user_side: The side chosen by the user (supporting/opposing)
            user_utterance: The user's latest argument
            conversation_history: Previous exchanges in the debate (optional)
            
        Returns:
            A focused counterargument to one key point from the user's argument
        """
        # Configure the AI debater with system instructions
        messages = [
            {"role": "system", "content": f"""You are a debate simulator. The topic is: {topic}.
            The user has chosen the {user_side.value} side, so you should take the {'opposing' if user_side == Side.SUPPORTING else 'supporting'} side.
            
            Instructions:
            1. Identify ONE key point from the user's argument to counter.
            2. Provide a single, focused counterargument.
            3. Keep your response concise, under 150 characters.
            4. Be clear and direct in your reasoning.
            5. Maintain a respectful tone.
            
            Example format:
            "While [acknowledge point], [counter with specific evidence/reasoning]."
            """}
        ]

        # Include previous debate context if available
        if conversation_history:
            for msg in conversation_history:
                messages.append(msg)

        # Add the user's current argument
        messages.append({"role": "user", "content": user_utterance})

        try:
            # Generate the AI's response
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                temperature=0.7,
                max_tokens=100  # Reduced to ensure shorter responses
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"Error in generating LLM response: {str(e)}")


# Initialize the LLM service
llm_service = LLMService() 