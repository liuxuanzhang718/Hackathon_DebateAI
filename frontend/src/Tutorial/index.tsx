import React, { useState } from 'react'
// import './Tutorial.css'

const Tutorial: React.FC = () => {
  const [selectedSymbol, setSelectedSymbol] = useState('')

  const logicSymbols = [
    { label: 'Not', symbol: '¬' },
    { label: 'Or', symbol: '∨' },
    { label: 'And', symbol: '∧' },
    { label: 'If...Then', symbol: '→' },
    { label: 'Equiv', symbol: '↔' },
  ]

  return (
    <div className="tutorial-container">
      <h2>Tutorial</h2>
      <p>Learn basic logic symbols:</p>
      <div className="symbol-list">
        {logicSymbols.map((s) => (
          <button
            key={s.label}
            onClick={() => setSelectedSymbol(s.symbol)}
          >
            {s.label} ({s.symbol})
          </button>
        ))}
      </div>
      <p>Selected Symbol: {selectedSymbol}</p>

      {/* Q: "Emily Happy" / "Have Dessert" / "Watching Anime" */}
      {/* Yes/No*/}

      
    </div>
  )
}

export default Tutorial
