import React from "react";
import styles from "./Chathistory.module.css";

const Chathistory = () => {
  return (
    <div className={styles.chatHistory}>
      <h3 className={styles.title}>Chat History</h3>
      <ul className={styles.list}>
        <li>Session 1: LLM Basics</li>
        <li>Session 2: Prompt Design</li>
        <li>Session 3: React Integration</li>
      </ul>
    </div>
  );
};

export default Chathistory;
