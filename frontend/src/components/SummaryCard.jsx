import React from 'react';

function SummaryCard({ title, value, className, note }) {
  return (
    <div className={`summary-card ${className}`}>
      <div className="summary-card-label">{title}</div>
      <div>
        <div className="summary-card-value">{value}</div>
        {note && <div className="summary-card-note">{note}</div>}
      </div>
    </div>
  );
}

export default SummaryCard;
