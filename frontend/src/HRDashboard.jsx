import React, { useState, useRef, useEffect } from 'react';

export default function HRDashboard() {
  const [messages, setMessages] = useState([
    { role: 'assistant', content: 'Welcome to the Corporate HR Assistant Hub. How can I guide your policy checks today?' }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  // Auto-scrolls chat window to the bottom whenever a new message lands
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage = { role: 'user', content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await fetch('http://127.0.0.1:8000/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: input, namespace: "" }),
      });

      if (!response.ok) throw new Error("Server communication fault");
      const data = await response.json();
      
      setMessages((prev) => [...prev, { role: 'assistant', content: data.answer }]);
    } catch (error) {
      setMessages((prev) => [...prev, { role: 'assistant', content: "⚠️ Error contacting the backend HR gateway." }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ fontFamily: 'Segoe UI, sans-serif', backgroundColor: '#000000', minHeight: '100vh', padding: '40px 20px' }}>
      <div style={{ maxWidth: '750px', margin: '0 auto', backgroundColor: '#ffffff', borderRadius: '12px', boxShadow: '0 4px 20px rgba(0,0,0,0.08)', overflow: 'hidden' }}>
        
        {/* Top Header Panel */}
        <div style={{ backgroundColor: '#1e293b', padding: '20px', color: '#ffffff', borderBottom: '3px solid #3b82f6' }}>
          <h2 style={{ margin: 0, fontSize: '22px', fontWeight: '600' }}>🏢 AI HR Policy Assistant</h2>
          <p style={{ margin: '5px 0 0 0', opacity: 0.8, fontSize: '13px' }}>Instant vector-verified company handbook retrieval system</p>
        </div>

        {/* Dynamic Chat Message Logs */}
        <div style={{ height: '450px', overflowY: 'auto', padding: '25px', backgroundColor: '#fafafa', display: 'flex', flexDirection: 'column', gap: '15px' }}>
          {messages.map((msg, index) => (
            <div key={index} style={{ display: 'flex', justifyContent: msg.role === 'user' ? 'flex-end' : 'flex-start' }}>
              <div style={{
                maxWidth: '75%',
                padding: '12px 16px',
                borderRadius: '8px',
                fontSize: '14px',
                lineHeight: '1.5',
                color: msg.role === 'user' ? '#ffffff' : '#334155',
                backgroundOpacity: 1,
                backgroundColor: msg.role === 'user' ? '#3b82f6' : '#5febeb',
                boxShadow: '0 1px 3px rgba(0,0,0,0.05)'
              }}>
                <strong>{msg.role === 'user' ? 'You' : 'HR Portal'}:</strong>
                <p style={{ margin: '5px 0 0 0', whiteSpace: 'pre-wrap' }}>{msg.content}</p>
              </div>
            </div>
          ))}
          {loading && (
            <div style={{ color: '#64748b', fontSize: '13px', fontStyle: 'italic', paddingLeft: '5px' }}>
              🤖 Fetching vectors and validating context parameters...
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input Form Controls */}
        <form onSubmit={handleSendMessage} style={{ display: 'flex', padding: '15px', borderTop: '1px solid #e2e8f0', backgroundColor: '#ffffff' }}>
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your policy question (e.g., What is the work timing policy?)..."
            style={{ flexGrow: 1, padding: '12px 15px', border: '1px solid #cbd5e1', borderRadius: '6px', fontSize: '14px', outline: 'none' }}
          />
          <button
            type="submit"
            disabled={loading}
            style={{
              marginLeft: '10px',
              padding: '0 24px',
              backgroundColor: '#3b82f6',
              color: '#ffffff',
              border: 'none',
              borderRadius: '6px',
              fontWeight: '600',
              cursor: loading ? 'not-allowed' : 'pointer',
              opacity: loading ? 0.6 : 1
            }}
          >
            Ask Engine
          </button>
        </form>
      </div>
    </div>
  );
}