import React from 'react';

const BottomSection: React.FC = () => {
  return (
    <div className="bottom-section">
      <div className="results-container">

        {/* Show logic result */}
        <div className="result-box">
          <h2>Temp Logic result</h2>

        </div>

        {/* Performance */}
        <div className="result-box">
          <h2>Performance: sound or valid</h2>
        </div>

        {/* Summary */}
        <div className="result-box">
            <h2>Summary</h2>
        </div>
      </div>
    </div>
  );
};

export default BottomSection;
