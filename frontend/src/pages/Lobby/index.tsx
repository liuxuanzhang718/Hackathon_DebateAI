import React from "react";
import liveGameIcon from "../../assets/icons/LiveGame.svg";
import settingIcon from "../../assets/icons/Setting.svg";
import agentIcon from "../../assets/icons/Agent.svg";
import tutorialIcon from "../../assets/icons/Tutorial.svg";
import optionIcon from "../../assets/icons/Option.svg";
import userInfoIcon from "../../assets/icons/UserInfo.svg"

import { useNavigate } from "react-router-dom";

import "./style.css";

const Lobby = (): JSX.Element => {
  return (
    <div className="lobby">
      <img className="user-info-icon" alt="User Info" src={userInfoIcon} />
      
      {/* Sphere */}
      <div className="overlap-2">
        <div className="text-wrapper-2">Xiaoyang</div>
        <img className="setting-2" alt="Setting" src={settingIcon} />
      </div>

      {/* Right */}
      <div className="overlap">
        <div className="gradient">
          <div className="overlap-group">
            <div className="eclipse" />
            <div className="planet" />
          </div>
        </div>

        {/* Live Game */}
        <div className="frame">
          <div className="div">
            <img className="setting" alt="Live Game" src={liveGameIcon} />
            <div className="text-wrapper">Live Game</div>
          </div>
          <img className="vector" alt="Setting" src={optionIcon} />
        </div>

        {/* AI Agent */}
        <div className="frame-wrapper">
          <div className="frame-2">
            <img className="img" alt="AI Agent" src={agentIcon} />
            <div className="text-wrapper">AI Agent</div>
          </div>
        </div>

        {/* Tutorial */}
        <div className="div-wrapper">
          <div className="frame-3">
            <img className="vector-2" alt="Tutorial" src={tutorialIcon} />
            <div className="text-wrapper">Tutorial</div>
          </div>
        </div>
      </div>



    </div>
  );
};

export default Lobby;



// import React from "react";
// import { useNavigate } from "react-router-dom";
// import image2 from "../../assets/image2.png";
// import polygon8 from "../../assets/Polygon8.svg";
// import polygon9 from "../../assets/Polygon9.svg";
// import styles from "./Lobby.module.css";


// const Lobby: React.FC = () => {
//   const navigate = useNavigate();
//   return (
//     <div className={styles.lobby}>
      
//       <div className={styles.overlap} onClick={() => navigate("/account")}>
//         <div className={styles["text-wrapper"]}>Set Up Your Agent</div>
//       </div>

//       <div className={styles.frame}>
//         <img className={styles.image} alt="Image" src={image2} />
//       </div>

//       <div className={styles["overlap-group-wrapper"]}>
//         <div className={styles["overlap-group"]}>
//           <div className={styles.div} />
//           <div className={styles["frame-2"]} />
//         </div>
//       </div>

//       <div className={styles["overlap-2"]}>
//         <div
//           className={styles["div-wrapper"]}
//           onClick={() => navigate("/agent-training")}
//         >
//           <div className={styles["text-wrapper-2"]}>Agent Training</div>
//         </div>

//         <div
//           className={styles["overlap-3"]}
//           onClick={() => navigate("/tutorial")}
//         >
//           <div className={styles["text-wrapper-3"]}>Tutorial</div>
//         </div>

//         <div
//           className={styles["text-wrapper-4"]}
//           onClick={() => navigate("/debate")}
//         >
//           Live Game
//         </div>

//         <div
//           className={styles["text-wrapper-5"]}
//           onClick={() => navigate("/debate")}
//         >
//           Debate
//         </div>

//         <img className={styles.polygon} alt="Polygon" src={polygon8} />
//         <img className={styles.img} alt="Polygon" src={polygon9} />
//       </div>
//     </div>
//   );
// };

// export default Lobby;
