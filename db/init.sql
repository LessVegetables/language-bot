-- psql -U lbot -d lbproject -f schema.sql
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE TABLE userchats (
    userid BIGINT PRIMARY KEY,
    -- Telegram User ID (Persistent)
    chatids UUID [],
    -- Array of Chat UUIDs associated with the user
    activechatid UUID -- The currently active Chat UUID
);
CREATE TABLE ChatsTable (
    chatid UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    -- Unique Chat UUID
    chatmemorysummary TEXT,
    -- Summary of the conversation
    chatdailyconversation JSONB,
    -- JSON formatted daily conversation
    chat_settings JSONB, -- JSON formatted chat settings
    conversation_summary TEXT,
    personality_summary TEXT,
    user_details TEXT
);