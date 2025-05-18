import asyncpg
import asyncio
import uuid
import json

class Database:
    def __init__(self, dsn: str):
        self.dsn = dsn
        self.pool = None

    async def connect(self):
        if self.pool is None:
            self.pool = await asyncpg.create_pool(dsn=self.dsn, min_size=1, max_size=10)
    
    async def check_connection(self):
        if not self.pool:
            raise RuntimeError("Database not connected")

    async def close(self):
        """Close the connection pool."""
        if self.pool:
            await self.pool.close()
            self.pool = None

    async def fetch(self, query, *args):
        await self.check_connection()

        async with self.pool.acquire() as conn:
            return await conn.fetch(query, *args)

    async def execute(self, query, *args):
        await self.check_connection()

        async with self.pool.acquire() as conn:
            return await conn.execute(query, *args)
    
    async def add_user(self, user_id: int):
        await self.check_connection()
        
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                row = await conn.fetchrow("SELECT * FROM userchats WHERE userid = $1", user_id)

                if row is not None:
                    return -1
                
                # init first chat with user
                chat_id = await self.create_chat(user_id)

                # Insert new user into UserChats with the first chat ID
                await conn.execute(
                    "INSERT INTO userchats (userid, chatids, activechatid) VALUES ($1, ARRAY[$2::uuid], $2)",
                    user_id, chat_id
                )

                return chat_id

    async def create_chat(self, user_id: int) -> uuid:
        await self.check_connection()

        """Creates a new chat entry and links it to a user."""
        chat_id = uuid.uuid4()  # Generate a new UUID
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                await conn.execute(
                    "INSERT INTO chatstable (chatid, chatmemorysummary, chatdailyconversation, chatsettings) VALUES ($1, '', '[]', '[]')",
                    chat_id
                )
                await conn.execute(
                    "UPDATE userchats SET chatids = array_append(chatids, $1), activechatid = $1 WHERE userid = $2",
                    chat_id, user_id
                )
        return chat_id

    async def get_current_chat_id(self, user_id: int):
        await self.check_connection()

        async with self.pool.acquire() as conn:
            row = await conn.fetchrow("SELECT activechatid FROM userchats WHERE userid = $1", user_id)
            if row:
                return row["activechatid"]
            else:
                raise Warning("User not found in the database")
        

    async def fetch_chat(self, chat_id: str):
        """Fetches a chat by UUID."""
        async with self.pool.acquire() as conn:
            return await conn.fetchrow("SELECT * FROM chatstable WHERE chatid = $1", uuid.UUID(chat_id))
    

    # getting informatio from db
    async def retrieve_conversation(self, chat_id: str) -> list:
        await self.check_connection()

        async with self.pool.acquire() as conn:
            async with conn.transaction():
                row = await conn.fetchrow("SELECT chatdailyconversation FROM chatstable WHERE chatid = $1", chat_id)
                if row and row["chatdailyconversation"]:
                    conversation = json.loads(row["chatdailyconversation"])
                else:
                    conversation = []
                return conversation
        
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
                for msg in conversation:
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
                
                return messages
    
    # async def store_conversation(self, chat_id: str, user_message: str, assistant_response: str):
    #     await self.check_connection()

    #     async with self.pool.acquire() as conn:
    #         async with conn.transaction():
    #             row = await conn.fetchrow("SELECT chatdailyconversation FROM chatstable WHERE chatid = $1", chat_id)

    #             conversation = row["chatdailyconversation"] if row and row["chatdailyconversation"] else []
                
    #             # Append the new message pair
    #             conversation.append({
    #                 "user": user_message,
    #                 "assistant": assistant_response
    #             })
                
    #             # Store back into the database
    #             await conn.execute(
    #                 "UPDATE chatstable SET chatdailyconversation = $1 WHERE chatid = $2",
    #                 json.dumps(conversation), chat_id
    #             )
        
    #     return
    
    async def get_conversation_summary(self, chat_id: str) -> str:
        await self.check_connection()

        async with self.pool.acquire() as conn:
            async with conn.transaction():
                row = await conn.fetchrow("SELECT conversation_summary FROM chatstable WHERE chatid = $1", chat_id)
                if row and row["conversation_summary"]:
                    conversation_summary = row["conversation_summary"]
                else:
                    conversation_summary = "there is not summary yet. This most likely means that the user is chatting with you for the first time."
                return conversation_summary
    
    async def get_bot_personality_summary(self, chat_id: str) -> str:
        await self.check_connection()

        async with self.pool.acquire() as conn:
            async with conn.transaction():
                row = await conn.fetchrow("SELECT personality_summary FROM chatstable WHERE chatid = $1", chat_id)
                if row and row["personality_summary"]:
                    bot_personality_summary = row["personality_summary"]
                else:
                    bot_personality_summary = "you have yet to create a personality."
                return bot_personality_summary
    
    async def get_user_details(self, chat_id: str) -> str:
        await self.check_connection()

        async with self.pool.acquire() as conn:
            async with conn.transaction():
                row = await conn.fetchrow("SELECT user_details FROM chatstable WHERE chatid = $1", chat_id)
                if row and row["user_details"]:
                    user_details = row["user_details"]
                else:
                    user_details = "the user has not provided any details about him/her self yet."
                return user_details


    # writing informatio to db
    async def store_conversation(self, chat_id: str, user_message: str, assistant_response: str):
        await self.check_connection()

        async with self.pool.acquire() as conn:
            async with conn.transaction():
                row = await conn.fetchrow(
                    "SELECT chatdailyconversation FROM chatstable WHERE chatid = $1", chat_id
                )

                if row and row["chatdailyconversation"]:
                    conversation = json.loads(row["chatdailyconversation"])
                    # If the conversation is a dict (i.e., stored as "{}"), convert it to an empty list.
                    if isinstance(conversation, dict):
                        conversation = []
                else:
                    conversation = []
                
                # print("converstaion: ", conversation)
                # print("type: ", type(conversation))
                
                # Append the new message pair
                conversation.append({
                    "user": user_message,
                    "assistant": assistant_response
                })
                
                # Store back into the database
                await conn.execute(
                    "UPDATE chatstable SET chatdailyconversation = $1 WHERE chatid = $2",
                    json.dumps(conversation), chat_id
                )
    
    async def store_conversation_summary(self, chat_id: str, new_summary: str) -> str:
        await self.check_connection()

        async with self.pool.acquire() as conn:
            async with conn.transaction():
                row = await conn.fetchrow(
                    "SELECT conversation_summary FROM chatstable WHERE chatid = $1", chat_id
                )

                # Store back into the database
                await conn.execute(
                    "UPDATE chatstable SET conversation_summary = $1 WHERE chatid = $2",
                    new_summary, chat_id
                )
