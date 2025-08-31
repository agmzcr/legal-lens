import { useState, useMemo } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import {
  HiDocumentText,
  HiOutlineTrash
} from "react-icons/hi";

import type { Document } from "../../types/document";
import { useDeleteDocument } from "../../hooks/useDeleteDocument";
import { apiFetch } from "../../lib/apiFetch";
import UploadDocumentModal from "../../components/UploadDocumentModal";

/**
 * DocumentList component
 * Displays a searchable list of uploaded documents with delete and upload functionality.
 */
export default function DocumentList() {
  const [search, setSearch] = useState("");
  const [showModal, setShowModal] = useState(false);
  const navigate = useNavigate();

  // Re-use the custom hook for document deletion
  const { deleteDocument, isDeleting } = useDeleteDocument();

  // Fetch documents using TanStack Query for caching and state management
  const {
    data: documents,
    isLoading,
    isError,
  } = useQuery<Document[]>({
    queryKey: ["documents"],
    queryFn: async () => {
      // Use the streamlined apiFetch.get() to leverage the centralized configuration
      const { data } = await apiFetch.get("/documents");
      return data;
    },
  });

  const filteredDocuments = useMemo(() => {
    if (!documents) return [];
    const term = search.toLowerCase();
    return documents.filter(
      (doc) =>
        doc.title.toLowerCase().includes(term) ||
        doc.summary.toLowerCase().includes(term)
    );
  }, [search, documents]);

  // Callback for a successful document upload
  const handleUploadComplete = (docId: string) => {
    console.log("Redirecting to:", `/dashboard/doc/${docId}`);
    setShowModal(false);
    navigate(`/dashboard/doc/${docId}`);
  };

  const handleDelete = (docId: string) => {
    deleteDocument(docId);
  };

  if (isLoading) {
    return (
      <p className="text-gray-500 text-center mt-8 text-lg">
        Loading documents...
      </p>
    );
  }

  if (isError) {
    return (
      <p className="text-red-600 text-center mt-8 text-lg">
        Failed to fetch documents.
      </p>
    );
  }

  return (
    <section className="space-y-8">
      {/* Search and upload section */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-8">
        <input
          type="text"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="border border-blue-200 rounded-lg px-4 py-2 w-full sm:w-72 shadow focus:ring-2 focus:ring-blue-400 focus:outline-none bg-white"
          placeholder="Search documents..."
        />
        <button
          onClick={() => setShowModal(true)}
          className="bg-blue-600 text-white px-5 py-2 rounded-full shadow hover:bg-blue-700 transition font-semibold text-base"
        >
          <HiDocumentText className="w-5 h-5 inline-block mr-2" />
          Upload Document
        </button>
      </div>

      {/* Message if no documents are uploaded */}
      {filteredDocuments.length === 0 ? (
        <div className="bg-white rounded-2xl shadow-lg border border-blue-100 p-8 text-center text-gray-500">
          <HiDocumentText className="w-12 h-12 mx-auto mb-4 text-blue-200" />
          <h3 className="text-xl font-semibold mb-2">No documents uploaded</h3>
          <p className="mb-4">Upload your first document to start legal analysis.</p>
        </div>
      ) : (
        <ul className="divide-y divide-blue-100 bg-white rounded-2xl shadow-lg border border-blue-100">
          {filteredDocuments.map((doc) => (
            <li
              key={doc.id}
              className="flex items-center justify-between px-6 py-5 hover:bg-blue-50 transition rounded-xl"
            >
              <Link to={`/dashboard/doc/${doc.id}`} className="flex-1 min-w-0 flex items-center gap-4">
                <HiDocumentText className="text-blue-500 w-7 h-7 flex-shrink-0" />
                <div className="flex-1 min-w-0">
                  <h3 className="font-semibold text-gray-800 text-lg truncate">{doc.title}</h3>
                  <p className="text-sm text-gray-600 truncate">{doc.summary}</p>
                </div>
              </Link>
              <button
                onClick={() => handleDelete(String(doc.id))}
                disabled={isDeleting}
                className="ml-4 bg-red-600 text-white px-4 py-2 rounded-full shadow hover:bg-red-700 transition font-semibold text-base disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <HiOutlineTrash className="w-5 h-5" />
              </button>
            </li>
          ))}
        </ul>
      )}

      {/* Upload modal */}
      {showModal && (
        <UploadDocumentModal
          onClose={() => setShowModal(false)}
          onComplete={handleUploadComplete}
        />
      )}
    </section>
  );
}