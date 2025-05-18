import asyncpg
import asyncio
import uuid
import json

from chat import HelperChatGPT


class BackgroundUserChatProcess:
    def __init__(self, database, gpt_helper):
        self.database = database
        self.gpt_helper = gpt_helper
    
    async def run_conversation_summary(self, chat_id: str):
        '''
        Is in charge of getting/processisng/storing/updating the conversation_summary

        Flow:
        1. gets current conversation_history
        2. if it exist - the process continues
        3. gets current conversation_summary
        4. calls HelperChatGPT to generate a summary
        5. calls database to write the new summary
        '''

        

        pass