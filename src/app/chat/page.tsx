"use client"; // Required for using useState & event handlers

import React, { useState, useRef, useEffect } from "react";

const ChatPage: React.FC = () => {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState<{ text: string; user: boolean }[]>([]);
  const [loading, setLoading] = useState(false);  

  const chatContainerRef = useRef<HTMLDivElement>(null); 

  // ✅ Scroll to bottom when messages update
  useEffect(() => {
    chatContainerRef.current?.scrollTo({ top: chatContainerRef.current.scrollHeight, behavior: "smooth" });
  }, [messages]);

  const sendMessage = async () => {
    if (!message.trim()) return; // Boş mesajları engelle
  
    setMessages((prev) => [...prev, { text: message, user: true }]);
    setMessage("");
    setLoading(true);
    try {
      console.log(" API isteği gönderiliyor: ", message);
  
      const response = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message }),
      });
  
      if (!response.ok) {
        console.error(` HTTP Error! Status: ${response.status} - ${response.statusText}`);
        setMessages((prev) => [...prev, { text: `HTTP Error: ${response.status}`, user: false }]);
        return;
      }
  
      const data = await response.json();
      setMessages((prev) => [...prev, { text: data.reply, user: false }]);
  
    } catch (error) {
      console.error("❌ Fetch Hatası: ", error);
      setMessages((prev) => [...prev, { text: "⚠️ Sunucu hatası!", user: false }]);
    }
    finally{
      setLoading(false);
    }
  
    
  };
  
  

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-900 p-4">
      {/* ✅ Chat Container */}
      <div className="w-[90%] max-w-[600px] bg-gray-800 text-white shadow-lg rounded-lg p-4 flex flex-col h-[80%] max-h-[500px]">
      <h1 className="text-2xl font-bold text-center text-blue-400 mb-4">AI Chatbot</h1>

        {/* ✅ Scrollable Chat Messages */}
        <div className="flex-1 overflow-y-auto space-y-3 p-3 max-h-[400px]">
          {messages.map((msg, index) => (
            <div
              key={index}
              className={`p-3 rounded-xl text-sm max-w-[75%] ${
                msg.user ? "bg-blue-500 text-white self-end ml-auto" : "bg-gray-600 text-gray-200 self-start mr-auto"
              }`}
            >
              {msg.text}
            </div>
          ))}
          {/* ✅ Loading Spinner (Cevap Beklerken Gözükecek) */}
          {loading && (
            <div className="flex justify-center items-center mt-2">
              <div className="animate-spin rounded-full h-8 w-8 border-t-4 border-blue-400"></div>
            </div>
          )}
        </div>

        {/* ✅ Input Field & Send Button */}
        <div className="flex gap-2 mt-2">
          <input
            type="text"
            className="flex-1 p-3 border rounded-lg text-white bg-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Type a message..."
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && sendMessage()} // ✅ Enter ile mesaj gönder
          />
          <button
            className="bg-blue-500 text-white px-4 py-3 rounded-lg hover:bg-blue-600 transition"
            onClick={sendMessage}
            disabled={loading} // ✅ Yanıt beklerken buton disable olsun
          >
            Gönder
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatPage;