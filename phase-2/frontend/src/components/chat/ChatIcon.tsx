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
          className={`fixed ${positionClasses} z-[100] bg-gradient-to-r from-pink-500 to-purple-600 p-[14px] w-14 h-14 rounded-full text-white shadow-xl hover:scale-110 transition-all duration-200 md:p-4 md:w-auto md:h-auto`}
        >
          <MessageCircle size={26} />
        </button>
      )}

      {/* Chat Panel */}
      {isOpen && !isMinimized && (
        <div className="fixed z-[100] bg-black/95 backdrop-blur-xl border border-pink-500/30 rounded-3xl shadow-2xl flex flex-col overflow-hidden left-4 right-4 bottom-4 h-[calc(100vh-3.5rem)] max-h-[75vh] sm:max-h-[85vh] md:left-auto md:right-6 md:bottom-24 md:w-[420px] md:h-[620px] md:max-h-none">

          {/* Header */}
          <div className="flex items-center justify-between px-4 py-3 border-b border-pink-500/20 md:px-6 md:py-4 gap-1.5 md:gap-2">
            <div className="flex items-center gap-2">
              <Bot className="text-pink-400" />
              <span className="text-white font-semibold text-base md:text-lg">
                Task Assistant
              </span>
              <span className="w-2 h-2 bg-pink-500 rounded-full animate-pulse" />
            </div>
            <div className="flex gap-1 md:gap-2">
              <button onClick={() => setIsMinimized(true)}>
                <Minus className="text-gray-400/70 hover:text-white p-2.5 w-10 h-10 flex items-center justify-center rounded-xl hover:bg-white/10 transition-colors md:p-3 md:w-11 md:h-11" />
              </button>
              <button onClick={() => setIsOpen(false)}>
                <X className="text-gray-400/70 hover:text-white p-2.5 w-10 h-10 flex items-center justify-center rounded-xl hover:bg-white/10 transition-colors md:p-3 md:w-11 md:h-11" />
              </button>
            </div>
          </div>

          {/* Messages */}
          <div className="flex-1 overflow-y-auto px-3 py-3 space-y-3 md:px-5 md:py-4 md:space-y-4 [&amp;&amp;.scrollbar-thin]:scrollbar-thin [&amp;&amp;.scrollbar-thumb-pink-500/50]:scrollbar-thumb-pink-500/50 [&amp;&amp;.scrollbar-track-transparent]:scrollbar-track-transparent min-h-0">
            {messages.map(msg => (
              <div
                key={msg.id}
                className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-[90%] md:max-w-[85%] px-3 py-2.5 md:px-4 md:py-3 rounded-2xl leading-relaxed text-sm md:text-base shadow-lg ${
                    msg.role === 'user'
                      ? 'bg-gradient-to-r from-pink-500 to-purple-600 text-white'
                      : 'bg-gray-800/60 border border-pink-500/20 text-white'
                  }`}
                >
                  <div className="flex gap-1 md:gap-2 items-start">
                    {msg.role === 'assistant' && (
                      <Bot size={14} className="text-pink-400 flex-shrink-0 mt-0.5 md:mt-1 md:size-18" />
                    )}
                    <span>{msg.content}</span>
                    {msg.role === 'user' && (
                      <User size={14} className="flex-shrink-0 mt-0.5 md:mt-1 md:size-18 text-white opacity-80" />
                    )}
                  </div>
                </div>
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>

          {/* Input */}
          <div className="p-3 border-t border-pink-500/20 md:p-4">
            <div className="flex items-end gap-2 md:gap-3">
              <input
                value={inputValue}
                onChange={e => setInputValue(e.target.value)}
                onKeyDown={e => e.key === 'Enter' && handleSendMessage()}
                placeholder="Type your task request..."
                className="flex-1 px-3 py-[11px] rounded-2xl bg-gray-800/60 border border-gray-700/50 text-white text-sm md:text-base placeholder-gray-400/80 focus:outline-none focus:ring-2 focus:ring-pink-500/50 focus:border-pink-500/50 min-h-[44px] md:px-5 md:py-3 md:rounded-full md:min-h-0 resize-none"
              />
              <button
                onClick={handleSendMessage}
                disabled={isLoading}
                className="bg-gradient-to-r from-pink-500 to-pink-600 hover:from-pink-600 hover:to-pink-700 p-2.5 w-11 h-11 rounded-2xl flex items-center justify-center text-white shadow-lg hover:shadow-pink-500/25 transition-all duration-200 md:p-3 md:w-12 md:h-12 md:rounded-full disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:shadow-none"
              >
                {isLoading ? <Loader className="animate-spin" /> : <Send />}
              </button>
              <button className="bg-gray-800/50 hover:bg-gray-700/60 p-2.5 w-11 h-11 rounded-2xl flex items-center justify-center border border-gray-600/50 hover:border-gray-500/50 transition-all duration-200 md:p-3 md:w-12 md:h-12 md:rounded-full">
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
