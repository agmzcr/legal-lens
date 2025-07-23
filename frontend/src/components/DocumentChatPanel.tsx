import { useEffect, useState } from 'react';
import axios from 'axios';
import { HiX } from "react-icons/hi";

// Props expected from parent component
type Props = {
  context: string;           // The full text of the document
  onClose: () => void;       // Callback to close the chat panel
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
export default function DocumentChatPanel({ context, onClose }: Props) {
  const [messages, setMessages] = useState<Message[]>([]); // Chat history
  const [input, setInput] = useState('');                  // User input
  const [loading, setLoading] = useState(false);           // Loading indicator

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
      const token = localStorage.getItem('token');
      const res = await axios.post(
        'http://localhost:8000/ai/chat',
        { context, question },
        { headers: { Authorization: `Bearer ${token}` } }
      );

      const reply = res.data.answer;
      setMessages((prev) => [...prev, { from: 'ai', text: reply }]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { from: 'ai', text: "Sorry, I couldn't process your question at this time." }
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed bottom-0 right-0 w-full max-w-md h-[80vh] bg-white shadow-lg border rounded-t-lg flex flex-col z-50">
      {/* Header */}
      <header className="p-4 border-b flex justify-between items-center">
        <h2 className="font-semibold">Ask the Document</h2>
        <button onClick={onClose} className="text-blue-500 hover:text-blue-700">
          <HiX />
        </button>
      </header>

      {/* Chat message history */}
      <div className="flex-1 overflow-y-auto p-4 space-y-3 text-sm">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`p-2 rounded-lg ${
              msg.from === 'user' ? 'bg-blue-100 text-right' : 'bg-gray-100 text-left'
            }`}
          >
            {msg.text}
          </div>
        ))}
        {loading && <p className="text-blue-500">Thinking…</p>}
      </div>

      {/* Input form */}
      <form
        onSubmit={(e) => {
          e.preventDefault();
          askAI();
        }}
        className="p-4 border-t flex gap-2"
      >
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          className="flex-1 border rounded px-3 py-2 text-sm"
          placeholder="Ask a question about the document…"
        />
        <button
          type="submit"
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Send
        </button>
      </form>
    </div>
  );
}