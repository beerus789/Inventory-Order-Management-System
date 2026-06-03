import React from 'react';

function SummaryCard({ title, value, className }) {
  return (
    <div className={`summary-card ${className}`}>
      <div className="summary-card-value">{value}</div>
      <div className="summary-card-label">{title}</div>
    </div>
  );
}

export default SummaryCard;
