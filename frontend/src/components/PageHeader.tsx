import { useNavigate } from 'react-router-dom';
import { HiArrowLeft } from "react-icons/hi";

interface PageHeaderProps {
  title: string;
  backTo?: string;
  actionButton?: React.ReactNode;
  searchInput?: React.ReactNode;
}

export default function PageHeader({ title, backTo, actionButton, searchInput }: PageHeaderProps) {
  const navigate = useNavigate();

  return (
    <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
      {/* Title and Back button group */}
      <div className="flex items-center gap-4">
        {backTo && (
          <button
            onClick={() => navigate(backTo)}
            className="flex items-center gap-2 px-4 py-2 bg-gray-100 text-gray-700 rounded hover:bg-gray-200 border border-gray-300 w-full sm:w-auto text-sm"
          >
            <HiArrowLeft className="w-4 h-4" />
            Back
          </button>
        )}
        <h1 className="text-2xl font-semibold text-gray-800 break-words max-w-full overflow-hidden text-ellipsis whitespace-nowrap sm:whitespace-normal">
          {title}
        </h1>
      </div>

      {/* Action/Search group - directly placed for a cleaner DOM */}
      {/* This makes it easy to add both actionButton and searchInput side-by-side */}
      <div className="flex items-center gap-4 flex-wrap justify-end">
        {searchInput}
        {actionButton}
      </div>
    </div>
  );
}