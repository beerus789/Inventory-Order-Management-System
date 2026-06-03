import React from 'react';
import Sidebar from './Sidebar';
import Navbar from './Navbar';

function Layout({ children, title }) {
  return (
    <div className="app-container">
      <Sidebar />
      <div className="main-content">
        <Navbar title={title} />
        <div className="content">
          {children}
        </div>
      </div>
    </div>
  );
}

export default Layout;
