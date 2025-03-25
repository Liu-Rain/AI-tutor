import styles from "./Chat.module.css";

const WelcomeMessage = {
  role: "assistant",
  content: "Hello! I am your AI Tutor, how can I help you?",
};

export function Chat({ messages }) {
  return (
    <div className={styles.Chat}>
      {[WelcomeMessage, ...messages].map(({ role, content }, index) => (
        <div key={index} className={styles.Message} data-role={role}>
          {content}
        </div>
      ))}
    </div>
  );
}
