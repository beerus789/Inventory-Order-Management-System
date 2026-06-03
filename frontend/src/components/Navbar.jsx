import React from 'react';

function Navbar({ title }) {
  return (
    <div className="navbar">
      <div>
        <div className="navbar-title">{title}</div>
        <div className="navbar-subtitle">Inventory and order operations</div>
      </div>
    </div>
  );
}

export default Navbar;
