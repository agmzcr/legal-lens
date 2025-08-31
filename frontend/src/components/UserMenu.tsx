import { useState, useRef, useEffect } from 'react';
import { HiChevronDown } from 'react-icons/hi';
import { useAuth } from '../lib/auth';

import avatarImg from '../assets/avatar.png';

interface UserMenuProps {
  mobile?: boolean;
}

/**
 * UserMenu component for displaying user avatar and logout functionality.
 * Features:
 * - Click outside detection to close dropdown
 * - Supports both mobile and desktop render modes
 * - Secure logout via API call using the centralized auth context
 */
export default function UserMenu({ mobile = false }: UserMenuProps) {
  const [open, setOpen] = useState(false);
  const menuRef = useRef<HTMLDivElement>(null);
  const { logout, isLoading } = useAuth();

  // Close menu when clicking outside
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
        setOpen(false);
      }
    }

    if (open) {
      document.addEventListener('mousedown', handleClickOutside);
    }
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [open]);

  // Mobile version: Logout button only
  if (mobile) {
    return (
      <div className="border-t px-4 py-2">
        <button
          onClick={logout}
          disabled={isLoading}
          className="w-full text-left px-2 py-2 text-gray-700 hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isLoading ? 'Logging out...' : 'Logout'}
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
        disabled={isLoading}
      >
        <img src={avatarImg} alt="Avatar" className="w-8 h-8 rounded-full" />
        <HiChevronDown className="w-4 h-4 text-gray-600" />
      </button>

      {open && (
        <div className="absolute right-0 mt-2 w-48 bg-white shadow-lg rounded-md z-10">
          <button
            onClick={logout}
            disabled={isLoading}
            className="w-full text-left px-4 py-2 text-gray-700 hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isLoading ? 'Logging out...' : 'Logout'}
          </button>
        </div>
      )}
    </div>
  );
}