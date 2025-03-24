import { useState } from "react";
import { Chat } from "./components/Chat/chat";
import styles from "./App.module.css";

function App() {
  const [messages, setMessages] = useState(MESSAGES);
  return (
    <div className={styles.App}>
      <header className={styles.Header}>
        <img className={styles.Logo} src="/aitutor.png" alt="AI Tutor" />
        <h2 className={styles.Title}>AI Tutor</h2>
      </header>
      <div className={styles.ChatContainer}>
        <Chat messages={messages} />
      </div>
    </div>
  );
}
const MESSAGES = [
  {
    role: "user",
    content: "Hello!",
  },
  {
    role: "assistant",
    content: "Hi! How can I help you today?",
  },
];

export default App;
