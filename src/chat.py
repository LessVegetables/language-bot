import os

from openai import OpenAI
from dotenv import load_dotenv

from database import Database

load_dotenv()

openAI_client = OpenAI(
  api_key=os.getenv("OPENAI_KEY")
)

class MyChatGPT:
    def __init__(self, database, model="gpt-4o-mini-2024-07-18"):
        self.model = model
        self.database = database  # Store database reference
    
    async def message_chatgpt(self, text: str, user_id: int):

        chat_id = await self.database.get_current_chat_id(user_id)
        message = await self.generate_prompt(chat_id, text) # get past memory from DB with userID
        assistant_response = await self.get_response(message)   # get chatgpt response
        await self.database.store_conversation(chat_id, text, assistant_response)  # store user_message and chatgpt response

        return assistant_response


    async def get_response(self, message):
        completion = openAI_client.chat.completions.create(
            model=self.model,
            # store=True,
            messages=message
        )
        return completion.choices[0].message.content


    async def generate_prompt(self, chat_id: str, user_message: str) -> list:

        past_conversation = await self.database.retrieve_conversation(chat_id)

        messages = [
            {
                "role": "developer",
                "content": [
                    {
                        "type": "text",
                        "text": "You are a helpful assistant that answers programming questions."
                    }
                ]
            }
        ]

        # Append previous conversation messages
        for msg in past_conversation:
            messages.append({
                "role": "user",
                "content": [{"type": "text", "text": msg["user"]}]
            })
            messages.append({
                "role": "assistant",
                "content": [{"type": "text", "text": msg["assistant"]}]
            })
        
        # Append the new user message
        messages.append({
            "role": "user",
            "content": [{"type": "text", "text": user_message}]
        })
        
        print("sending message: ", messages)
        
        return messages
