import React, { useRef, useState } from 'react';
import styles from './T.module.css';
import UserCard from "./UserCard";
import SphereGIF from '../../assets/particles/2-1.gif'
import TapToTalk from './TapToTalk';

interface TopSectionProps {
  topic?: string;

}

const TopSection: React.FC<TopSectionProps> = ({
  topic = "\''Can EV Effectively Reduce the Negative Effect from Global Warming?\''",
}) => {
  const [isSpeaking] = useState(false);


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
        <TapToTalk
          conversationId="conversation-id"
          speakerId="speaker-id"
          onStopRecording={() => {
            console.log("Recording stopped");
          }}
        />


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