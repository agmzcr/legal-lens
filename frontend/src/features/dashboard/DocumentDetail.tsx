import { useParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";

import {
  HiOutlineChat,
  HiExclamationCircle,
  HiOutlineClipboardList,
  HiOutlineBookOpen,
  HiOutlineDocumentText,
  HiOutlineTrash,
} from "react-icons/hi";

import PageHeader from "../../components/PageHeader";
import DocumentChatPanel from "../../components/DocumentChatPanel";
import { apiFetch } from "../../lib/apiFetch";
import { useDeleteDocument } from "../../hooks/useDeleteDocument";
import type { Document } from "../../types/document"; 
import { useState } from "react";

/**
 * DocumentDetail component
 * Displays the full details of a selected legal document.
 */
export default function DocumentDetail() {
  const { docId } = useParams<{ docId: string }>();
  
  // Use the custom hook for deletion logic
  const { deleteDocument, isDeleting } = useDeleteDocument();
  
  // State for controlling the chat panel, correctly placed
  const [chatOpen, setChatOpen] = useState(false);

  // Use useQuery to handle data fetching, caching, and errors
  const { data: doc, isLoading, error } = useQuery<Document>({
    queryKey: ['document', docId],
    queryFn: async () => {
      // Use the centralized apiFetch to make the authenticated request
      const response = await apiFetch.get(`/documents/${docId}`);
      return response.data; // Axios returns the data in the .data property
    },
    enabled: !!docId,
  });

  // Document deletion handler
  const handleDelete = async () => {
    if (!doc || !docId) return;
    deleteDocument(docId);
  };

  // Conditional rendering based on loading state
  if (isLoading) {
    return (
      <p className="text-gray-500 text-center mt-8 text-lg">
        Loading document...
      </p>
    );
  }

  if (error) {
    return (
      <p className="text-red-600 text-center mt-8 text-lg">
        Failed to load document.
      </p>
    );
  }

  if (!doc) {
    return (
      <p className="text-gray-500 text-center mt-8 text-lg">
        Document not found.
      </p>
    );
  }

  return (
    <article className="space-y-8 px-2 sm:px-8 lg:px-24 py-8 bg-gray-50 min-h-screen animate-fade-in">
      {/* Header with dynamic title and delete button */}
      <PageHeader
        title={doc.title}
        actionButton={
          <button
            onClick={handleDelete}
            disabled={isDeleting}
            className="flex items-center gap-2 bg-red-600 text-white px-5 py-2 rounded-full shadow hover:bg-red-700 transition font-semibold text-base disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <HiOutlineTrash className="w-5 h-5" />
            {isDeleting ? "Deleting..." : "Delete Document"}
          </button>
        }
      />

      {/* Summary Section */}
      <section className="bg-white/80 backdrop-blur p-6 rounded-2xl shadow-lg border border-blue-100 mb-8 animate-fade-in">
        <h2 className="text-2xl font-bold text-blue-700 mb-3 flex items-center gap-3">
          <HiOutlineBookOpen className="text-blue-400 w-7 h-7" />
          Summary
        </h2>
        <p className="text-gray-700 text-lg leading-relaxed">{doc.summary}</p>
      </section>

      {/* Key Clauses Section */}
      {doc.clauses?.length > 0 && (
        <section className="bg-white/80 backdrop-blur p-6 rounded-2xl shadow-lg border border-blue-100 mb-8 animate-fade-in">
          <h2 className="text-2xl font-bold text-blue-700 mb-3 flex items-center gap-3">
            <HiOutlineClipboardList className="text-blue-400 w-7 h-7" />
            Key Clauses
          </h2>
          <ul className="divide-y divide-blue-100">
            {doc.clauses.map((clause, idx) => (
              <li key={idx} className="py-4">
                <div className="flex items-center gap-2 mb-1">
                  <span className="inline-block w-2 h-2 bg-blue-400 rounded-full"></span>
                  <h4 className="font-semibold text-gray-800 text-base">{clause.title}</h4>
                </div>
                <p className="text-gray-600 text-sm pl-4 border-l-2 border-blue-100">{clause.content}</p>
              </li>
            ))}
          </ul>
        </section>
      )}

      {/* Red Flags Section */}
      {doc.red_flags?.length > 0 && (
        <section className="bg-white/80 backdrop-blur p-6 rounded-2xl shadow-lg border border-red-200 mb-8 animate-fade-in">
          <h2 className="text-2xl font-bold text-red-600 mb-3 flex items-center gap-3">
            <HiExclamationCircle className="text-red-400 w-7 h-7" />
            Red Flags
          </h2>
          <ul className="list-disc list-inside text-red-700 space-y-2 text-base pl-4">
            {doc.red_flags.map((flag, idx) => (
              <li key={idx} className="bg-red-50 rounded px-2 py-1 border border-red-100 shadow-sm">{flag}</li>
            ))}
          </ul>
        </section>
      )}

      {/* Full Content Section */}
      <section className="bg-white/80 backdrop-blur p-6 rounded-2xl shadow-lg border border-blue-100 animate-fade-in">
        <h2 className="text-2xl font-bold text-blue-700 mb-3 flex items-center gap-3">
          <HiOutlineDocumentText className="text-blue-400 w-7 h-7" />
          Full Content
        </h2>
        <div className="text-gray-700 whitespace-pre-wrap text-base leading-relaxed max-h-[60vh] overflow-y-auto border border-blue-100 rounded-xl p-4 bg-blue-50/40 custom-scrollbar">
          {doc.content}
        </div>
      </section>

      {/* AI Chat Popup */}
      <>
        <button
          onClick={() => setChatOpen(true)}
          className="fixed bottom-8 right-8 bg-blue-600 text-white p-5 rounded-full shadow-xl hover:bg-blue-700 transition z-50 border-4 border-white"
        >
          <HiOutlineChat className="w-7 h-7" />
        </button>

        {chatOpen && (
          <DocumentChatPanel
            documentId={doc.id}
            onClose={() => setChatOpen(false)}
          />
        )}
      </>
    </article>
  );
}