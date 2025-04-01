import React from "react";
import styles from "./Choosechapters.module.css";

const Choosechapters = () => {
  return (
    <div className={styles.chapters}>
      <h3 className={styles.title}>Course Chapters</h3>
      <ul className={styles.list}>
        <li>Chapter 1: Introduction</li>
        <li>Chapter 2: Basics</li>
        <li>Chapter 3: Advanced Topics</li>
      </ul>
    </div>
  );
};

export default Choosechapters;
