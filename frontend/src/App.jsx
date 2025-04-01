import { useState } from "react";
import { Chat } from "./components/Chat/chat";
import { Assistant } from "./aiassistants/google";
import styles from "./App.module.css";
import { Controls } from "./components/Controls/Controls";

function App() {
  const assistant = new Assistant();
  const [messages, setMessages] = useState([]);
  function addMessage(message) {
    setMessages((prevMessages) => [...prevMessages, message]);
  }
  async function handleContentSend(content) {
    addMessage({ content, role: "user" });

    try {
      const result = await assistant.chat(content);
      addMessage({
        content: result,
        role: "assistant",
      });
    } catch {
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
