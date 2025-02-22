import React, { useState } from 'react'

const AgentSetUp: React.FC = () => {
  const [selectedName, setSelectedName] = useState<string>('')
  const [selectedStyle, setSelectedStyle] = useState<string>('')

  const names = ['Lily', 'Jake', 'Emily']
  const styles = ['Energetic', 'Formal', 'Casual', 'Academic', 'Robot']

  const handleStartConversation = () => {
    console.log(`Starting conversation with ${selectedName} in ${selectedStyle} style`)
  }

  return (
    <div className="setup-container">
      <h2>Set Up Your Agent</h2>
      
      <div className="section">
        <h3>Select Agent</h3>
        <div className="options-grid">
          {names.map((name) => (
            <button
              key={name}
              className={`option-btn ${selectedName === name ? 'selected' : ''}`}
              onClick={() => setSelectedName(name)}
            >
              {name}
            </button>
          ))}
        </div>
      </div>

      <div className="section">
        <h3>Select Style</h3>
        <div className="options-grid">
          {styles.map((style) => (
            <button
              key={style}
              className={`option-btn ${selectedStyle === style ? 'selected' : ''}`}
              onClick={() => setSelectedStyle(style)}
            >
              {style}
            </button>
          ))}
        </div>
      </div>

      <button 
        className="start-btn"
        disabled={!selectedName || !selectedStyle}
        onClick={handleStartConversation}
      >
        Start Conversation
      </button>
    </div>
  )
}

export default AgentSetUp