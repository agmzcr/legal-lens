import { HiOutlineRefresh } from 'react-icons/hi';

/**
 * FullPageSpinner component.
 * Displays a full-screen loading spinner to prevent UI flashes
 * while checking for authentication status.
 */
export default function FullPageSpinner() {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-white bg-opacity-80">
      <div className="flex flex-col items-center">
        <HiOutlineRefresh className="w-12 h-12 text-blue-500 animate-spin" />
        <p className="mt-4 text-sm font-medium text-gray-700">Loading...</p>
      </div>
    </div>
  );
}