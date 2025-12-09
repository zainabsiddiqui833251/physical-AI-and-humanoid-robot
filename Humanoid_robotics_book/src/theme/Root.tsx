import React, { useState } from 'react';
import Chatbot from '../components/Chatbot';
import '../css/custom.css'; // Ensure custom CSS is imported

export default function Root({children}) {
  const [isChatbotOpen, setIsChatbotOpen] = useState(false);

  const toggleChatbot = () => {
    setIsChatbotOpen(!isChatbotOpen);
  };

  return (
    <>
      {children}
      <div className="chatbot-container">
        {isChatbotOpen && (
          <div className="chatbot-window-wrapper"> {/* New wrapper div for styling */}
            <Chatbot />
          </div>
        )}
        <button onClick={toggleChatbot} className="chatbot-toggle-button">
          {isChatbotOpen ? '✕' : '💬'} {/* '✕' for close, '💬' for open */}
        </button>
      </div>
    </>
  );
}
