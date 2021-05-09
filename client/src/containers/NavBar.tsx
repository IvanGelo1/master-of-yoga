import './NavBar.css';
import React from 'react';
import { Link } from 'react-router-dom';

import { openModal } from '../redux/modalSlice';
import { useAppDispatch } from '../redux/hooks';

const NavBar: React.FC = () => {
  const dispatch = useAppDispatch();

  const handleClick = () => {
    dispatch(openModal());
  };

  return (
    <nav className="navbar-container">
      <Link to="/about">Meet the Team</Link>
      <a style={{ cursor: 'pointer' }} onClick={handleClick}>
        Sign In
      </a>
    </nav>
  );
};

export default NavBar;