import React, { useEffect, useState } from 'react';
import './B.module.css';

interface BottomData {
  logicResult: string;
  performance: string;
  summary: string;
}

const BottomSection: React.FC = () => {
  const [data, setData] = useState<BottomData | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/bottom-section-data');
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const result: BottomData = await response.json();
        setData(result);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return <div className="bottom-section">Loading...</div>;
  }

  if (error) {
    return null;
  }

  return (
    <div className="bottom-section">
      <div className="results-container">
        {/* Show logic result */}
        <div className="result-box">
          <h2>Logic result</h2>
          <p>{data?.logicResult}</p>
        </div>

        {/* Performance */}
        <div className="result-box">
          <h2>Performance</h2>
          <p>{data?.performance}</p>
        </div>

        {/* Summary */}
        <div className="result-box">
          <h2>Summary</h2>
          <p>{data?.summary}</p>
        </div>
      </div>
    </div>
  );
};

export default BottomSection;
