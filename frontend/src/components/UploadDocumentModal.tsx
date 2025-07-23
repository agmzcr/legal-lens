import {
  useState,
  useRef,
  type DragEvent,
  type ChangeEvent,
} from 'react';
import axios from 'axios';
import {
  HiOutlineUpload,
  HiCloudUpload,
} from 'react-icons/hi';

type Props = {
  onClose: () => void;
  onComplete: (docId: string) => void;
};

/**
 * UploadModal component for uploading PDF documents.
 * Features:
 * - Drag-and-drop support
 * - File preview and upload progress
 * - Error handling and upload result callback
 */
export default function UploadModal({ onClose, onComplete }: Props) {
  const [file, setFile] = useState<File | null>(null);          // Selected file
  const [error, setError] = useState('');                       // Upload error
  const [loading, setLoading] = useState(false);                // Upload status
  const [dragActive, setDragActive] = useState(false);          // Drag hover state
  const fileInputRef = useRef<HTMLInputElement>(null);          // Hidden input trigger

  // Handle drag-over event
  const handleDragOver = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setDragActive(true);
  };

  // Handle drag-leave event
  const handleDragLeave = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setDragActive(false);
  };

  // Handle file drop
  const handleDrop = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setDragActive(false);
    const droppedFile = e.dataTransfer.files?.[0];
    if (droppedFile) {
      setFile(droppedFile);
      setError('');
    }
  };

  // Handle file selection from input
  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    const chosenFile = e.target.files?.[0] || null;
    setFile(chosenFile);
    setError('');
  };

  // Upload file to backend
  const handleUpload = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    setLoading(true);
    setError('');

    try {
      const token = localStorage.getItem('token');
      const res = await axios.post(
        'http://localhost:8000/document/upload',
        formData,
        {
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'multipart/form-data',
          },
        }
      );

      const docId = res.data?.id;
      if (docId) {
        onComplete(docId); // Trigger parent callback
      } else {
        setError('Could not retrieve document ID');
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Error uploading document');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 bg-black bg-opacity-40 flex items-center justify-center">
      <div className="bg-white w-full max-w-md mx-4 sm:mx-auto p-6 rounded-lg shadow-lg space-y-6">
        {/* Modal header */}
        <header className="flex items-center gap-3">
          <HiCloudUpload className="text-2xl text-blue-600" />
          <h2 className="text-xl font-bold text-gray-800">Upload Document</h2>
        </header>

        {/* Drop zone or file preview */}
        <div
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          onClick={() => fileInputRef.current?.click()}
          className={`cursor-pointer p-6 border-2 rounded-lg text-center transition-colors
            ${dragActive ? 'border-blue-500 bg-blue-50' : 'border-gray-300 bg-white'}`}
        >
          {loading ? (
            <>
              <HiOutlineUpload className="w-10 h-10 text-blue-600 animate-spin mx-auto" />
              <p className="mt-2 text-blue-600 font-medium">Analyzing…</p>
            </>
          ) : file ? (
            <>
              <p className="font-medium text-gray-700">{file.name}</p>
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  handleUpload();
                }}
                disabled={loading}
                className="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
              >
                Upload & Analyze
              </button>
            </>
          ) : (
            <>
              <HiOutlineUpload className="w-12 h-12 text-gray-400 mx-auto" />
              <p className="mt-2 text-gray-600">Drag here or click to select a document</p>
            </>
          )}
          <input
            ref={fileInputRef}
            type="file"
            accept="application/pdf"
            onChange={handleFileChange}
            className="hidden"
          />
        </div>

        {/* Display error if any */}
        {error && (
          <p className="text-red-600 text-sm text-center">{error}</p>
        )}

        {/* Cancel button */}
        <div className="flex justify-end gap-2">
          <button
            onClick={onClose}
            className="px-4 py-2 bg-gray-100 text-gray-800 rounded hover:bg-gray-200 border border-gray-300"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  );
}