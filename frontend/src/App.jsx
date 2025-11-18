import { useState } from 'react';
import axios from 'axios';
import BotResponse from './components/BotResponse';
import './App.css';

function App() {
  const API_URL = import.meta.env.VITE_API_URL || 'https://real-estate-jazy.onrender.com';
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSendMessage = async () => {
    if (inputValue.trim() === '') return;

    const userMessage = { type: 'user', text: inputValue };
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      const response = await axios.post(`${API_URL}/api/chat/`, { query: inputValue });
      const botMessage = { type: 'bot', data: response.data };
      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      const errorMessage = { type: 'bot', data: { summary: 'Sorry, something went wrong. Please try again.' } };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gray-100">
      <header className="bg-blue-600 text-white p-4 text-center">
        <h1 className="text-2xl font-bold">Real Estate AI Analyst</h1>
      </header>
      <main className="flex-1 overflow-y-auto p-4">
        <div className="max-w-4xl mx-auto">
          {messages.map((msg, index) => (
            <div key={index} className={`my-2 ${msg.type === 'user' ? 'text-right' : 'text-left'}`}>
              {msg.type === 'user' ? (
                <div className="inline-block bg-blue-500 text-white p-2 rounded-lg">
                  {msg.text}
                </div>
              ) : (
                <BotResponse message={msg.data} />
              )}
            </div>
          ))}
          {isLoading && (
            <div className="text-left">
              <div className="inline-block bg-gray-200 p-2 rounded-lg">
                Typing...
              </div>
            </div>
          )}
        </div>
      </main>
      <footer className="bg-white p-4 border-t">
        <div className="max-w-4xl mx-auto flex">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
            className="flex-1 p-2 border rounded-l-lg"
            placeholder="Ask about real estate trends..."
          />
          <button
            onClick={handleSendMessage}
            className="bg-blue-600 text-white p-2 rounded-r-lg"
            disabled={isLoading}
          >
            Send
          </button>
        </div>
      </footer>
    </div>
  );
}

export default App;
