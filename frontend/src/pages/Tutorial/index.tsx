import React from 'react'
import { Navigate, useNavigate } from 'react-router-dom';

import styles from './Tutorial.module.css'; 

import NotIcon from '../../assets/icons/Not.svg';
import OrIcon from '../../assets/icons/Or.svg';
import EquivIcon from '../../assets/icons/Equiv.svg';
import AndIcon from '../../assets/icons/And.svg';
import ImplyIcon from '../../assets/icons/Imply.svg';
import ExitIcon from '../../assets/icons/Exit.svg';
import SmallSwirlIcon from '../../assets/images/image2-1.png'
import SwirlImage from '../../assets/images/image2.png';

/** Top */
const TopSection: React.FC = () => {
  const navigate = useNavigate();
  return (
    <div className={styles.topSection}>
      <div className={styles.topBar}>
      <img
          className={styles.smallSwirlIcon}
          src={SmallSwirlIcon}
          alt="Small Swirl Icon"
        />
        <img
          className={styles.exitIcon}
          src={ExitIcon}
          alt="Exit Icon"
          onClick={() => navigate('/')}
        />
      </div>

      {/* middle + text */}
      <div className={styles.swirlContainer}>
        <img
          src={SwirlImage}
          alt="Swirl"
          className={styles.swirlImage}
        />
        <h2 className={styles.swirlTitle}>
          Let Start With Basic Symbols
        </h2>
      </div>
    </div>
  );
};

/** Middle */
const MiddleSection: React.FC = () => {
  return (
    <div className={styles.middleSection}>
      <div className={styles.symbolRow}>
        {/* Not */}
        <div className={styles.symbolItem}>
          <img
            className={styles.symbolIcon}
            src={NotIcon}
            alt="Not"
          />
          <p>Not</p>
        </div>

        {/* Or */}
        <div className={styles.symbolItem}>
          <img
            className={styles.symbolIcon}
            src={OrIcon}
            alt="Or"
          />
          <p>Or</p>
        </div>

        {/* If and only if */}
        <div className={styles.symbolItem}>
          <img
            className={styles.symbolIcon}
            src={EquivIcon}
            alt="If and only if"
          />
          <p>If and only if</p>
        </div>

        {/* And */}
        <div className={styles.symbolItem}>
          <img
            className={styles.symbolIcon}
            src={AndIcon}
            alt="And"
          />
          <p>And</p>
        </div>

        {/* If... then */}
        <div className={styles.symbolItem}>
          <img
            className={styles.symbolIcon}
            src={ImplyIcon}
            alt="If... then"
          />
          <p>If...then</p>
        </div>
      </div>
    </div>
  );
};

/** Bottom */
const BottomSection: React.FC = () => {
  return (
    <div className={styles.bottomSection}>

      <div className={styles.divider} />
      <div className={styles.logicContainer}>

        {/* Left */}
        <div className={styles.leftLogic}>
          <h3>Have Dessert</h3>
          <img
            className={styles.symbolIcon}
            src={ImplyIcon}
            alt="If... then"
          />
          <h3>Emily Happy</h3>
        </div>

        {/* Right*/}
        <div className={styles.rightLogic}>
          <h3>Q: Emily Happy ~ Have Dessert</h3>
          <div className={styles.buttonRow}>
            <button className={styles.btn}>True</button>
            <button className={styles.btn}>False</button>
          </div>
        </div>

      </div>
    </div>
  );
};


const Tutorial: React.FC = () => {
  return (
    <div className={styles.tutorialContainer}>
      <TopSection />
      <MiddleSection />
      <BottomSection />
    </div>
  );
};

export default Tutorial;