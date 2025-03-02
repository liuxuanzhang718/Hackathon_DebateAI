import React from 'react';
import { useNavigate } from 'react-router-dom';
import TopSection from './TopSection';
import BottomSection from './BottomSection';

import styles from './Agent.module.css';

const AgentTraining: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div className={styles.agentTraining}>
      <div style={{ flex: 5 }}>
        <TopSection />
      </div>
      <div className={styles.divider} />
      <div style={{ flex: 2 }}>
        <BottomSection />
      </div>
    </div>
  );
};

export default AgentTraining;