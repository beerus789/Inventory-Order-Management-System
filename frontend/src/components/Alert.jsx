import React, { useEffect } from 'react';

function Alert({ type, message, onClose, duration = 5000 }) {
  useEffect(() => {
    const timer = setTimeout(onClose, duration);
    return () => clearTimeout(timer);
  }, [onClose, duration]);

  return (
    <div className={`alert alert-${type}`}>
      <span>{message}</span>
      <button className="alert-close" onClick={onClose} aria-label="Close alert">
        x
      </button>
    </div>
  );
}

export default Alert;
