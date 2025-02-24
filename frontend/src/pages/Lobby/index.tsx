import React from "react";
import liveGameIcon from "../../assets/icons/LiveGame.svg";
import settingIcon from "../../assets/icons/Setting.svg";
import agentIcon from "../../assets/icons/Agent.svg";
import tutorialIcon from "../../assets/icons/Tutorial.svg";
import optionIcon from "../../assets/icons/Option.svg";
import userInfoIcon from "../../assets/icons/UserInfo.svg";

import { useNavigate } from "react-router-dom";

import "./style.css";

const Lobby = (): JSX.Element => {
  const navigate = useNavigate();

  return (
    <div className="lobby">
      <img className="user-info-icon" alt="User Info" src={userInfoIcon}/>

      <div className="main-layout">
        {/* Sphere */}
        <div className="overlap-2">
          <h1 className="text-wrapper-2">VeriVox</h1>
          <img 
            className="setting-2" alt="Setting" 
            src={settingIcon}
            onClick={() => navigate("/agentSetUp")} />
        </div>

        {/* Right*/}
        <div className="overlap">
          <div className="gradient">
            <div className="overlap-group">
              <div className="eclipse" />
              <div className="planet" />
            </div>
          </div>

          {/* Live Game */}
          <div className="frame" onClick={() => navigate("/liveGame")}>
            <div className="div">
              <img className="setting" alt="Live Game" src={liveGameIcon} />
              <div className="text-wrapper">Live Game</div>
            </div>
            <img className="vector" alt="Option" src={optionIcon} />
          </div>

          {/* AI Agent */}
          <div className="frame-wrapper" onClick={() => navigate("/agentTraining")}>
            <div className="frame-2">
              <img className="img" alt="AI Agent" src={agentIcon} />
              <div className="text-wrapper">AI Agent</div>
            </div>
          </div>

          {/* Tutorial */}
          <div className="div-wrapper" onClick={() => navigate("/tutorial")}>
            <div className="frame-3">
              <img className="vector-2" alt="Tutorial" src={tutorialIcon} />
              <div className="text-wrapper">Tutorial</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Lobby;
