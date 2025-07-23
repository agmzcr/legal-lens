import { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { HiChevronDown } from 'react-icons/hi';
import avatarImg from '../assets/avatar.png';

interface UserMenuProps {
  mobile?: boolean;
}

/**
 * UserMenu component for displaying user avatar and logout functionality.
 * Features:
 * - Click outside detection to close dropdown
 * - Supports both mobile and desktop render modes
 * - Token removal and logout redirection
 */
export default function UserMenu({ mobile = false }: UserMenuProps) {
  const [open, setOpen] = useState(false);            // Dropdown open state
  const menuRef = useRef<HTMLDivElement>(null);       // Ref for detecting outside clicks
  const navigate = useNavigate();

  // Close menu when clicking outside
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
        setOpen(false);
      }
    }

    if (open) document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [open]);

  // Log user out and redirect to login
  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  // Mobile version: Logout button only
  if (mobile) {
    return (
      <div className="border-t px-4 py-2">
        <button
          onClick={handleLogout}
          className="w-full text-left px-2 py-2 text-gray-700 hover:bg-gray-100"
        >
          Logout
        </button>
      </div>
    );
  }

  // Desktop version: Avatar with dropdown
  return (
    <div className="relative" ref={menuRef}>
      <button
        onClick={() => setOpen(!open)}
        className="flex items-center space-x-1 focus:outline-none"
        aria-label="User menu"
      >
        <img src={avatarImg} alt="Avatar" className="w-8 h-8 rounded-full" />
        <HiChevronDown className="w-4 h-4 text-gray-600" />
      </button>

      {open && (
        <div className="absolute right-0 mt-2 w-48 bg-white shadow-lg rounded-md z-10">
          <button
            onClick={handleLogout}
            className="w-full text-left px-4 py-2 text-gray-700 hover:bg-gray-100"
          >
            Logout
          </button>
        </div>
      )}
    </div>
  );
}