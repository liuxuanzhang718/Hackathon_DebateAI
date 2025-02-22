import React, { useState } from 'react'
// import './AgentTraining.css'

const AgentTraining: React.FC = () => {
  const [topic, setTopic] = useState('Global Warming')
  const [supportingPoints, setSupportingPoints] = useState<string[]>([])
  const [opposingPoints, setOpposingPoints] = useState<string[]>([])

  // useEffect(() => {
  //   axios.get('/api/agent-training/topics').then(res => {
  //     ...
  //   })
  // }, [])

  const handleTrain = () => {
    console.log('Training agent on topic:', topic)
  }

  return (
    <div className="agent-training-container">
      <h2>Agent Training</h2>
      <div>
        <label>Select Topic: </label>
        <select
          value={topic}
          onChange={(e) => setTopic(e.target.value)}
        >
          <option value="Global Warming">Global Warming</option>
          <option value="Carbon Emission">Carbon Emission</option>
          <option value="Fuel Cost">Fuel Cost</option>
        </select>
      </div>
      <div>
        <p>Supporting Points</p>
        {/*  */}
      </div>
      <div>
        <p>Opposing Points</p>
        
      </div>
      <button onClick={handleTrain}>Start Training</button>
    </div>
  )
}

export default AgentTraining
