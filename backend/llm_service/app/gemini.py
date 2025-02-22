import google.generativeai as genai
from typing import Optional
from config.settings import settings
from prompt import PromptTemplates

class GeminiClient:
    def __init__(self):
        # Ensure API key is set
        if not settings.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY is missing! Please set it in your environment variables.")

        genai.configure(api_key=settings.GOOGLE_API_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-pro')

    def get_response(self, prompt: str, context: Optional[str] = None) -> str:
        """
        Generates a response from Gemini AI.
        """
        try:
            chat = self.model.start_chat(history=[])
            system_prompt = PromptTemplates.get_system_prompt()
            
            # Construct full prompt
            if context:
                full_prompt = f"{system_prompt}\n\nContext: {context}\n\nQuestion: {prompt}"
            else:
                full_prompt = f"{system_prompt}\n\nQuestion: {prompt}"
            
            # Get response
            response = chat.send_message(full_prompt)

            # Ensure response is valid
            if not response or not response.text:
                return "Error: Received empty response from Gemini AI."

            return response.text
        
        except Exception as e:
            return f"Error generating response: {str(e)}"
