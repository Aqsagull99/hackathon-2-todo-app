-- Migration: Add Conversation and Message Tables for Phase III AI Chatbot
-- Feature: AI Chatbot (005-ai-chatbot-mcp)
-- Created: 2026-01-11

-- 1. Create conversations table
CREATE TABLE conversations (
    conversation_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- 2. Create messages table
CREATE TABLE messages (
    message_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID NOT NULL REFERENCES conversations(conversation_id) ON DELETE CASCADE,
    role VARCHAR(10) NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    tool_calls JSONB DEFAULT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- 3. Create indexes for performance
CREATE INDEX idx_conversations_user_id ON conversations(user_id);
CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX idx_messages_created_at ON messages(created_at);

-- 4. Add conversations relationship to users table (if needed)
-- Note: The relationship is handled in the models, not in the DB schema

-- Verification queries (run after migration):
-- SELECT tablename FROM pg_tables WHERE schemaname = 'public'
-- AND tablename IN ('conversations', 'messages');

-- SELECT indexname FROM pg_indexes WHERE tablename IN ('conversations', 'messages');