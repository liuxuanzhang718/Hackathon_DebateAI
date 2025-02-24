import React, { useState } from 'react';
import styles from './T.module.css';
import UserCard from "./UserCard";

interface TopSectionProps {
  topic?: string;
}

const TopSection: React.FC<TopSectionProps> = ({
  topic = "\''Can EV Effectively Reduce the Negative Effect from Global Warming?\''",
}) => {
  const [isSpeaking, notSpeaking] = useState(false);


  return (
    <div className={styles.topSection}>
      {/* Topic */}
      <div className={styles.topic}>
        <h3>{topic}</h3>
      </div>

      <div className={styles.row}>
        {/* Left Speaker */}
        <div className={styles.speaker}>
          <UserCard
            isSpeaking={isSpeaking}
            cardTitle="SUPPORTING"
          />
        </div>

        {/* Tap to Talk */}
        <div className={styles.middleBall}>
          <div className={styles.talkBall}>
            <h3>Tap to Talk...</h3>
          </div>
        </div>

        {/* Speaker */}
        <div className={styles.speaker}>
          <UserCard
            isSpeaking={isSpeaking}
            cardTitle="OPPOSING"
          />
        </div>
      </div>
    </div>
  );
};

export default TopSection;