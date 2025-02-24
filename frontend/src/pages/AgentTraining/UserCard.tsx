import React from "react";
import styles from "./UserCard.module.css";
import defaultAvatar from "../../assets/images/user1.png";

interface UserCardProps {
  photoUrl?: string;                        
  isSpeaking: boolean;                      
  cardTitle: "SUPPORTING" | "OPPOSING";     
  count?: number;                           
}

const UserCard: React.FC<UserCardProps> = ({
  photoUrl,
  isSpeaking,
  cardTitle,
  count
}) => {
  
  const finalPhotoUrl = photoUrl && photoUrl.trim() !== "" ? photoUrl : defaultAvatar;

  return (
    <div className={styles.card}>
      {/* Top */}
      <div className={styles.cardHeader}>
        <h3 className={styles.title}>{cardTitle}</h3>
        {typeof count === "number" && <div className={styles.count}>{count}</div>}
      </div>

      {/* Pic + “Speaking...” */}
      <div className={styles.chatBubble}>
        <img src={finalPhotoUrl} alt="User" className={styles.userImage} />
        {isSpeaking && <div className={styles.speakingText}>Speaking...</div>}
      </div>
    </div>
  );
};

export default UserCard;
