import { Link } from 'react-router-dom';
import UserMenu from './UserMenu';

/**
 * Topbar navigation component for LegalLens dashboard.
 * Features:
 * - Fixed header with logo
 * - Responsive layout
 * - User menu dropdown
 */
export default function Topbar() {
  return (
    <header className="fixed top-0 left-0 right-0 bg-white shadow z-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        {/* Application Logo - navigates to dashboard */}
        <Link to="/dashboard" className="text-xl font-bold text-blue-700">
          LegalLens
        </Link>

        {/* User avatar and menu */}
        <UserMenu />
      </div>
    </header>
  );
}