import os
import datetime

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


    # async def generate_prompt(self, chat_id: str, user_message: str) -> list:

    #     past_conversation = await self.database.retrieve_conversation(chat_id)

    #     messages = [
    #         {
    #             "role": "developer",
    #             "content": [
    #                 {
    #                     "type": "text",
    #                     "text": "You are a helpful assistant that answers programming questions."
    #                 }
    #             ]
    #         }
    #     ]

    #     # Append previous conversation messages
    #     for msg in past_conversation:
    #         messages.append({
    #             "role": "user",
    #             "content": [{"type": "text", "text": msg["user"]}]
    #         })
    #         messages.append({
    #             "role": "assistant",
    #             "content": [{"type": "text", "text": msg["assistant"]}]
    #         })
        
    #     # Append the new user message
    #     messages.append({
    #         "role": "user",
    #         "content": [{"type": "text", "text": user_message}]
    #     })
        
    #     print("sending message: ", messages)
        
    #     return messages

    async def generate_prompt(self, chat_id: str, user_message: str) -> list:
            # Retrieve dynamic context from your DB
            chat_history = await self.database.retrieve_conversation(chat_id)
            conversation_summary = await self.database.get_conversation_summary(chat_id)
            personality_summary = await self.database.get_bot_personality_summary(chat_id)
            user_details = await self.database.get_user_details(chat_id)

            # Dynamic time context
            now = datetime.datetime.now()
            dynamic_time_context = f"Today is {now.strftime('%B %d, %Y')}. Current time is {now.strftime('%I:%M %p')}."

            # Build system messages with context
            messages = [
                # Developer message (highest priority instructions)
                {
                    "role": "developer",
                    "content": [
                        {
                            "type": "text",
                            "text": (
                                "You are Dave, a friendly, engaging language practice chatbot. Your goal is to help users practice "
                                "and improve their language skills through natural conversation. Always respond in short, human-like "
                                "messages. If asked, state: 'My name is Dave and I'm a chatbot.' Avoid overwhelming the user, gently "
                                "correct mistakes, and adapt to the user's language level. This service is a supplement to tutoring, not "
                                "a replacement."
                            )
                        }
                    ]
                },
                # System message for dynamic time context and global dynamic context
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "text",
                            "text": (
                                f"{dynamic_time_context}\n"
                                f"Conversation Summary: {conversation_summary}\n"
                                f"Your personality Summary: {personality_summary}\n"
                                f"User Details: {user_details}\n"
                                "Note: These summaries and details are dynamically updated to help personalize your responses."
                            )
                        }
                    ]
                }
            ]

            # Append previous conversation messages from chat history
            for msg in chat_history:
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

            print("Sending message payload:", messages)
            return messages


class HelperChatGPT:
    def __init__(self, database, model="gpt-4o-mini-2024-07-18"):
        self.model = model
        self.database = database
    async def generate_conversation_summary(self, conversation_history, current_summary) -> str:
         
        message = [
             {
                  "role": "developer",
                  "content": [
                       {
                            "type" : "text",
                            "text" : (
                                 "Please create a summary of the convesation hisotry between an AI assistant and a bot user."
                                 "You are given the convesations history"
                            )
                       }
                  ]
             }
        ]
    
    async def generate_personality_summary(self, personality_summary, current_summary) -> str:
         pass
    
    async def generate_user_details(self, user_details, current_summary) -> str:
         pass

