"""
LLM Processing Module using OpenRouter API
Handles conversation with DeepSeek V3.1 or other models
"""

import requests
from typing import Optional, List, Dict
import json


class LLMProcessor:
    """LLM processor using OpenRouter API"""

    def __init__(self, api_key: str, model: str = "deepseek/deepseek-chat",
                 max_tokens: int = 500, temperature: float = 0.7,
                 system_prompt: Optional[str] = None):
        """
        Initialize LLM Processor

        Args:
            api_key: OpenRouter API key
            model: Model identifier (default: deepseek/deepseek-chat for DeepSeek V3.1)
            max_tokens: Maximum tokens in response
            temperature: Creativity level (0.0-1.0)
            system_prompt: System prompt to set behavior
        """
        self.api_key = api_key
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"

        # Default system prompt for school robot
        if system_prompt is None:
            self.system_prompt = (
                "You are a friendly, helpful school robot assistant. "
                "You help students with their questions in a clear, educational, "
                "and engaging way. Keep responses concise (2-3 sentences) and appropriate "
                "for a school environment. Be encouraging and supportive."
            )
        else:
            self.system_prompt = system_prompt

        # Conversation history for context
        self.conversation_history: List[Dict[str, str]] = []
        self.max_history = 10  # Keep last 10 exchanges

    def generate_response(self, user_input: str) -> Optional[str]:
        """
        Generate response from LLM

        Args:
            user_input: User's question or statement

        Returns:
            LLM's response or None if error
        """
        try:
            print(f"💭 Thinking about: {user_input}")

            # Build messages with conversation history
            messages = [
                {"role": "system", "content": self.system_prompt}
            ]

            # Add conversation history
            messages.extend(self.conversation_history)

            # Add current user input
            messages.append({"role": "user", "content": user_input})

            # Make API request
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://github.com/your-repo",  # Optional
                "X-Title": "School Robot Assistant"  # Optional
            }

            payload = {
                "model": self.model,
                "messages": messages,
                "max_tokens": self.max_tokens,
                "temperature": self.temperature
            }

            print("🔄 Contacting LLM...")
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=30
            )

            response.raise_for_status()
            result = response.json()

            # Extract response text
            assistant_message = result["choices"][0]["message"]["content"]

            # Update conversation history
            self.conversation_history.append({"role": "user", "content": user_input})
            self.conversation_history.append({"role": "assistant", "content": assistant_message})

            # Trim history if too long
            if len(self.conversation_history) > self.max_history * 2:
                self.conversation_history = self.conversation_history[-(self.max_history * 2):]

            print(f"💬 Response: {assistant_message}")
            return assistant_message

        except requests.exceptions.Timeout:
            print("❌ LLM request timed out")
            return "I'm sorry, I'm taking too long to think. Can you ask me again?"

        except requests.exceptions.HTTPError as e:
            print(f"❌ LLM API error: {e}")
            if response.status_code == 401:
                return "Sorry, there's an authentication issue. Please check the API key."
            elif response.status_code == 429:
                return "I'm a bit overwhelmed right now. Please try again in a moment."
            else:
                return "Sorry, I'm having trouble processing that right now."

        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return "Sorry, I encountered an error. Can you try asking that differently?"

    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        print("🗑️  Conversation history cleared")

    def set_system_prompt(self, prompt: str):
        """Update system prompt"""
        self.system_prompt = prompt
        print(f"✏️  System prompt updated")

    def get_history_summary(self) -> str:
        """Get summary of conversation history"""
        if not self.conversation_history:
            return "No conversation history"

        exchanges = len(self.conversation_history) // 2
        return f"Conversation history: {exchanges} exchanges"


# Example usage
if __name__ == "__main__":
    import os
    from dotenv import load_dotenv

    # Load environment variables
    load_dotenv()
    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        print("❌ Please set OPENROUTER_API_KEY in .env file")
        exit(1)

    # Initialize LLM
    llm = LLMProcessor(
        api_key=api_key,
        model="deepseek/deepseek-chat",
        max_tokens=500,
        temperature=0.7
    )

    print("=" * 50)
    print("🤖 LLM Processor Test")
    print("=" * 50)

    # Test conversation
    test_questions = [
        "What is photosynthesis?",
        "Can you explain it more simply?",
        "What plants do photosynthesis?"
    ]

    for question in test_questions:
        print(f"\n👤 User: {question}")
        response = llm.generate_response(question)
        if response:
            print(f"🤖 Robot: {response}")
        print("-" * 50)

    # Show history
    print(f"\n{llm.get_history_summary()}")
