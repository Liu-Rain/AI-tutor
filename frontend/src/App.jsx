import { useState } from "react";
import { Chat } from "./components/Chat/chat";
import styles from "./App.module.css";
import { Controls } from "./components/Controls/Controls";

function App() {
  const [messages, setMessages] = useState([]);

  function handleContentSend(content) {
    setMessages((previousMessages) => [
      ...previousMessages,
      { content, role: "user" },
    ]);
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
