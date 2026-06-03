import React from 'react';

function Navbar({ title }) {
  return (
    <div className="navbar">
      <div className="navbar-title">{title}</div>
    </div>
  );
}

export default Navbar;
