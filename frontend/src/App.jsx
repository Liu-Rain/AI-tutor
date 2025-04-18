import { useState } from "react";
import { Chat } from "./components/Chat/chat";
import { Assistant } from "./aiassistants/google";
import styles from "./App.module.css";
import { Controls } from "./components/Controls/Controls";
import Choosechapters from "./components/Choosechapters/Choosechapters";
import Chathistory from "./components/Chathistory/Chathistory";

function App() {
  const assistant = new Assistant();
  const [messages, setMessages] = useState([]);
  function addMessage(message) {
    setMessages((prevMessages) => [...prevMessages, message]);
  }
  async function handleContentSend(content) {
    addMessage({ content, role: "user" });

    try {
      const result = await assistant.chat(content, messages);
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
      <div className={styles.Main}>
        <div className={styles.Sidebar}>
          <Choosechapters />
          <Chathistory />
        </div>
        <div className={styles.ChatContent}>
          <div className={styles.ChatContainer}>
            <Chat messages={messages} />
          </div>
          <Controls onSend={handleContentSend} />
        </div>
      </div>
    </div>
  );
}

export default App;
