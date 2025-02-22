import React from "react";
import { useNavigate } from "react-router-dom";
import image2 from "../../assets/image2.png";
import polygon8 from "../../assets/Polygon8.svg";
import polygon9 from "../../assets/Polygon9.svg";
import styles from "./Lobby.module.css";


const Lobby: React.FC = () => {
  const navigate = useNavigate();
  return (
    <div className={styles.lobby}>
      
      <div className={styles.overlap} onClick={() => navigate("/account")}>
        <div className={styles["text-wrapper"]}>Set Up Your Agent</div>
      </div>

      <div className={styles.frame}>
        <img className={styles.image} alt="Image" src={image2} />
      </div>

      <div className={styles["overlap-group-wrapper"]}>
        <div className={styles["overlap-group"]}>
          <div className={styles.div} />
          <div className={styles["frame-2"]} />
        </div>
      </div>

      <div className={styles["overlap-2"]}>
        <div
          className={styles["div-wrapper"]}
          onClick={() => navigate("/agent-training")}
        >
          <div className={styles["text-wrapper-2"]}>Agent Training</div>
        </div>

        <div
          className={styles["overlap-3"]}
          onClick={() => navigate("/tutorial")}
        >
          <div className={styles["text-wrapper-3"]}>Tutorial</div>
        </div>

        <div
          className={styles["text-wrapper-4"]}
          onClick={() => navigate("/debate")}
        >
          Live Game
        </div>

        <div
          className={styles["text-wrapper-5"]}
          onClick={() => navigate("/debate")}
        >
          Debate
        </div>

        <img className={styles.polygon} alt="Polygon" src={polygon8} />
        <img className={styles.img} alt="Polygon" src={polygon9} />
      </div>
    </div>
  );
};

export default Lobby;
