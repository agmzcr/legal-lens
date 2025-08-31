import { useEffect, useState, useRef } from 'react';
import { apiFetch } from '../lib/apiFetch';
import { HiX } from "react-icons/hi";
import toast from 'react-hot-toast';

// Props expected from parent component
type Props = {
  documentId: number; 
  onClose: () => void; 
};

// Message type definition
type Message = {
  from: 'user' | 'ai';
  text: string;
};

/**
 * DocumentChatPanel component
 * Features:
 * - Chat interface that lets users ask questions about a specific document
 * - AI responses fetched via API using provided context
 * - Clean UI with loading state and message rendering
 */
export default function DocumentChatPanel({ documentId, onClose }: Props) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Display welcome message when component mounts
  useEffect(() => {
    setMessages([
      {
        from: 'ai',
        text: "👋 Hello! I'm here to help you understand this document. You can ask me about clauses, risks, or any legal questions you have."
      }
    ]);
  }, []);

  // Send question to AI API and get a response
  const askAI = async () => {
    if (!input.trim()) return;

    const question = input.trim();
    setMessages((prev) => [...prev, { from: 'user', text: question }]);
    setInput('');
    setLoading(true);

    try {
      const res = await apiFetch({
        method: 'post',
        url: '/ai/chat/',
        data: { 
          document_id: documentId,
          message: question
        },
      });
      const reply = res.data.response;
      setMessages((prev) => [...prev, { from: 'ai', text: reply }]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { from: 'ai', text: "Sorry, I couldn't process your question at this time. Please try again later." }
      ]);
      toast.error('Failed to get a response from the AI.');
    } finally {
      setLoading(false);
    }
  };

  // Auto-scroll to the bottom of the chat on new messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <div className="fixed bottom-0 right-0 w-full max-w-md h-[80vh] bg-gradient-to-br from-blue-50 via-white to-blue-100 shadow-2xl border border-blue-200 rounded-t-2xl flex flex-col z-50 animate-fade-in">
      {/* Header */}
      <header className="p-4 border-b flex justify-between items-center bg-gradient-to-r from-blue-600 to-blue-400 rounded-t-2xl">
        <h2 className="font-semibold text-white tracking-wide text-lg flex items-center gap-2">
          <span className="inline-block w-2 h-2 bg-green-400 rounded-full animate-pulse"></span>
          LegalLens AI Chat
        </h2>
        <button onClick={onClose} className="text-white hover:text-blue-100 text-xl">
          <HiX />
        </button>
      </header>

      {/* Chat message history */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 text-sm bg-transparent custom-scrollbar">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`flex ${msg.from === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-[80%] px-4 py-2 rounded-2xl shadow-md whitespace-pre-line break-words transition-all
                ${msg.from === 'user'
                  ? 'bg-blue-600 text-white rounded-br-md rounded-tr-2xl'
                  : 'bg-white text-gray-800 border border-blue-100 rounded-bl-md rounded-tl-2xl'}
              `}
            >
              {msg.from === 'ai' && (
                <span className="block text-xs text-blue-400 font-semibold mb-1">AI</span>
              )}
              {msg.from === 'user' && (
                <span className="block text-xs text-right text-blue-200 font-semibold mb-1">You</span>
              )}
              {msg.text}
            </div>
          </div>
        ))}
        {loading && (
          <div className="flex justify-start">
            <div className="bg-white border border-blue-100 text-blue-400 px-4 py-2 rounded-2xl shadow animate-pulse">
              Thinking…
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input form */}
      <form
        onSubmit={(e) => {
          e.preventDefault();
          askAI();
        }}
        className="p-4 border-t flex gap-2 bg-white rounded-b-2xl"
      >
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          className="flex-1 border border-blue-200 rounded-full px-4 py-2 text-sm focus:ring-2 focus:ring-blue-400 focus:outline-none bg-blue-50"
          placeholder="Ask a question about the document…"
          autoFocus
        />
        <button
          type="submit"
          className="bg-gradient-to-r from-blue-600 to-blue-400 text-white px-6 py-2 rounded-full font-semibold shadow hover:from-blue-700 hover:to-blue-500 transition disabled:opacity-50 disabled:cursor-not-allowed"
          disabled={loading || !input.trim()}
        >
          Send
        </button>
      </form>
      <style>{`
        .custom-scrollbar::-webkit-scrollbar { width: 8px; }
        .custom-scrollbar::-webkit-scrollbar-thumb { background: #c7d2fe; border-radius: 4px; }
        .animate-fade-in { animation: fadeIn 0.5s; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(40px);} to { opacity: 1; transform: none; } }
      `}</style>
    </div>
  );
}