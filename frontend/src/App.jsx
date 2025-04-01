import { useState } from "react";
import { Chat } from "./components/Chat/chat";
import { GoogleGenerativeAI } from "@google/generative-ai";
import styles from "./App.module.css";
import { Controls } from "./components/Controls/Controls";

const googlegenerativeai = new GoogleGenerativeAI(
  import.meta.env.VITE_GOOGLE_AI_API_KEY
);
const gemini = googlegenerativeai.getGenerativeModel({
  model: "gemini-1.5-flash",
});
const chat = gemini.startChat({ history: [] });

function App() {
  const [messages, setMessages] = useState([]);
  function addMessage(message) {
    setMessages((prevMessages) => [...prevMessages, message]);
  }
  async function handleContentSend(content) {
    addMessage({ content, role: "user" });
    setMessages((previousMessages) => [
      ...previousMessages,
      { content, role: "user" },
    ]);

    try {
      const result = await chat.sendMessage(content);
      addMessage({
        content: result.response.text(),
        role: "assistant",
      });
    } catch (error) {
      addMessage({ content: "Error!", role: "system" });
    }
  }
  return (
    <div className={styles.App}>
      <header className={styles.Header}>
        <img className={styles.Logo} src="/aitutor.png" alt="AI Tutor" />
        <h2 className={styles.Title}>AI Tutor</h2>
      </header>
      <div className={styles.ChatContainer}>
        <Chat messages={messages} />
      </div>
      <Controls onSend={handleContentSend} />
    </div>
  );
}

export default App;
