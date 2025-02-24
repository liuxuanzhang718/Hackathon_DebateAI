import React, { useRef, useState } from 'react';
import styles from './T.module.css';

interface TapToTalkProps {
  conversationId: string;
  speakerId: string;
  onStopRecording: () => void;
}

const BASE_URL = 'http://localhost:8000';

const TapToTalk: React.FC<TapToTalkProps> = ({ conversationId, speakerId, onStopRecording }) => {
  const [recording, setRecording] = useState<boolean>(false);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);

  // Start recording audio
  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      audioChunksRef.current = [];

      mediaRecorder.ondataavailable = (event: BlobEvent) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      mediaRecorder.onstop = () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
        uploadAudio(audioBlob);
        // Once recording is fully stopped, invoke the callback
        onStopRecording();
      };

      mediaRecorder.start();
      setRecording(true);
    } catch (error) {
      console.error('Failed to get microphone access:', error);
    }
  };

  // Stop recording audio
  const stopRecording = () => {
    if (mediaRecorderRef.current) {
      mediaRecorderRef.current.stop();
      setRecording(false);
    }
  };

  // Upload the audio blob to the Debate AI Platform API
  const uploadAudio = async (audioBlob: Blob) => {
    // For real WAV, you would do a conversion if needed
    const file = new File([audioBlob], 'recording.wav', { type: 'audio/wav' });
    const formData = new FormData();
    formData.append('file', file);
    formData.append('speaker_id', speakerId);

    try {
      const response = await fetch(`${BASE_URL}/agent-training/audio/${conversationId}`, {
        method: 'POST',
        body: formData,
      });
      if (!response.ok) {
        throw new Error(`Upload failed, status: ${response.status}`);
      }
      const result = await response.json();
      console.log('Audio uploaded successfully:', result);
    } catch (error) {
      console.error('Audio upload error:', error);
    }
  };

  // Toggle recording on click
  const handleClick = () => {
    if (!recording) {
      startRecording();
    } else {
      stopRecording();
    }
  };

  return (
    <div className={styles.middleBall} onClick={handleClick} style={{ cursor: 'pointer' }}>
      <div className={styles.talkBall}>
        <h3>{recording ? 'Recording...' : 'Tap to Talk...'}</h3>
      </div>
    </div>
  );
};

export default TapToTalk;
