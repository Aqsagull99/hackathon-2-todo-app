'use client';

import React, { useState, useEffect, useRef } from 'react';
import {
  MessageCircle,
  Bot,
  User,
  Send,
  Mic,
  Minus,
  X,
  CheckCircle,
  Trash2,
  List,
  Check,
  Loader,
} from 'lucide-react';
import { api } from '@/lib/api';

interface ChatIconProps {
  position?: 'bottom-right' | 'top-right';
  accessToken?: string;
  userId: string;
  onTaskCreated?: () => void;
}

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  type?: 'task_added' | 'task_deleted' | 'task_list' | 'task_completed' | 'task_updated' | 'normal';
}

const ChatIcon: React.FC<ChatIconProps> = ({
  position = 'bottom-right',
  accessToken,
  userId,
  onTaskCreated,
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const [isMinimized, setIsMinimized] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const positionClasses =
    position === 'top-right' ? 'top-4 right-4' : 'bottom-6 right-6';

  const toggleChat = () => {
    setIsOpen(!isOpen);
    setIsMinimized(false);
  };

  const handleSendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    const content = inputValue;
    setInputValue('');
    setIsLoading(true);

    setMessages(prev => [
      ...prev,
      {
        id: Date.now().toString(),
        role: 'user',
        content,
        timestamp: new Date(),
      },
    ]);

    try {
      api.setToken(accessToken || null);
      const response = await api.sendMessage(userId, conversationId, content);
      setConversationId(response.conversation_id);

      setMessages(prev => [
        ...prev,
        {
          id: Date.now().toString(),
          role: 'assistant',
          content: response.response,
          timestamp: new Date(),
          type: response.tool_calls && response.tool_calls.length > 0 ? 'task_added' : 'normal',
        },
      ]);

      // Dispatch task-created event if tool_calls contains create_task action
      if (response.tool_calls && response.tool_calls.length > 0) {
        const hasCreateTask = response.tool_calls.some(
          (tc: any) => tc.tool === 'create_task' || tc.tool === 'add_task'
        );
        if (hasCreateTask) {
          window.dispatchEvent(new CustomEvent('task-created', { detail: response.tool_calls }));
        }
      }

      onTaskCreated?.();
    } catch (error) {
      console.error("Chat error:", error);

      let errorMessage = 'Something went wrong. Please try again.';

      // Check if it's a 401 error (User not found or unauthorized)
      if (error instanceof Error) {
        if (error.message.includes('401')) {
          errorMessage = 'Authentication error. Please refresh the page and try again.';
        } else if (error.message.includes('User not found')) {
          errorMessage = 'User session expired. Please refresh the page.';
        }
      }

      setMessages(prev => [
        ...prev,
        {
          id: Date.now().toString(),
          role: 'assistant',
          content: errorMessage,
          timestamp: new Date(),
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <>
      {/* Floating Button */}
      {!isOpen && (
        <button
          onClick={toggleChat}
          className={`fixed ${positionClasses} z-50 bg-gradient-to-r from-pink-500 to-purple-600 p-4 rounded-full text-white shadow-xl hover:scale-110 transition`}
        >
          <MessageCircle size={26} />
        </button>
      )}

      {/* Chat Panel */}
      {isOpen && !isMinimized && (
        <div className="fixed bottom-24 right-6 w-[420px] h-[620px] z-50 bg-black/95 backdrop-blur-xl border border-pink-500/30 rounded-3xl shadow-2xl flex flex-col">

          {/* Header */}
          <div className="flex items-center justify-between px-5 py-4 border-b border-pink-500/20">
            <div className="flex items-center gap-2">
              <Bot className="text-pink-400" />
              <span className="text-white font-semibold text-lg">
                Task Assistant
              </span>
              <span className="w-2 h-2 bg-pink-500 rounded-full animate-pulse" />
            </div>
            <div className="flex gap-2">
              <button onClick={() => setIsMinimized(true)}>
                <Minus className="text-gray-400 hover:text-white" />
              </button>
              <button onClick={() => setIsOpen(false)}>
                <X className="text-gray-400 hover:text-white" />
              </button>
            </div>
          </div>

          {/* Messages */}
          <div className="flex-1 overflow-y-auto px-5 py-4 space-y-4">
            {messages.map(msg => (
              <div
                key={msg.id}
                className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-[85%] px-4 py-3 rounded-2xl leading-relaxed text-base ${
                    msg.role === 'user'
                      ? 'bg-gradient-to-r from-pink-500 to-purple-600 text-white'
                      : 'bg-gray-800/60 border border-pink-500/20 text-white'
                  }`}
                >
                  <div className="flex gap-2 items-start">
                    {msg.role === 'assistant' && (
                      <Bot size={18} className="text-pink-400 mt-1" />
                    )}
                    <span>{msg.content}</span>
                    {msg.role === 'user' && (
                      <User size={18} className="mt-1 text-white" />
                    )}
                  </div>
                </div>
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>

          {/* Input */}
          <div className="p-4 border-t border-pink-500/20">
            <div className="flex items-center gap-3">
              <input
                value={inputValue}
                onChange={e => setInputValue(e.target.value)}
                onKeyDown={e => e.key === 'Enter' && handleSendMessage()}
                placeholder="Type your task request..."
                className="flex-1 px-5 py-3 rounded-full bg-gray-800/60 text-white text-base placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-pink-500"
              />
              <button
                onClick={handleSendMessage}
                disabled={isLoading}
                className="bg-pink-500 hover:bg-pink-600 p-3 rounded-full text-white"
              >
                {isLoading ? <Loader className="animate-spin" /> : <Send />}
              </button>
              <button className="bg-gray-700 p-3 rounded-full">
                <Mic />
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default ChatIcon;
