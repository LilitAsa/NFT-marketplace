import React from 'react';

const Button = ({ 
  children, 
  onClick, 
  type = 'button',
  className = '',
  disabled = false 
}) => {
  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled}
      className={`px-4 py-2 rounded-lg font-medium transition-colors ${className}`}
    >
      {children}
    </button>
  );
};

export default Button;
