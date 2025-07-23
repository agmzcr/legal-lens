import { useParams, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import axios from "axios";

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
import toast from "react-hot-toast";

/**
 * DocumentDetail component
 * Displays the full details of a selected legal document including summary, clauses, flags,
 * and full content. Also includes AI-assisted chat and delete functionality.
 */
export default function DocumentDetail() {
  const { docId } = useParams<{ docId: string }>();
  const [doc, setDoc] = useState<any>(null); // Document object
  const [error, setError] = useState("");    // Error message state
  const [chatOpen, setChatOpen] = useState(false); // Toggle for AI chat
  const navigate = useNavigate();

  // Fetch a document by ID when component mounts
  useEffect(() => {
    const fetchDoc = async () => {
      try {
        const token = localStorage.getItem("token");
        const response = await axios.get(`http://localhost:8000/document/${docId}`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        setDoc(response.data);
      } catch (err: any) {
        setError("Failed to load document");
      }
    };

    fetchDoc();
  }, [docId]);

  // Handle document deletion with undo option
  const handleDelete = () => {
    const token = localStorage.getItem("token");
    let wasUndone = false;

    // Show toast with Undo option
    toast(
      (t) => (
        <div className="flex items-center justify-between space-x-2">
          <span className="text-sm text-gray-800">
            ⏳ Deleting: <strong>{doc.title}</strong>
          </span>
          <button
            onClick={() => {
              wasUndone = true;
              setDoc(doc); // Restore document if undo triggered
              toast.dismiss(t.id);
            }}
            className="text-red-600 text-sm font-medium hover:underline"
          >
            Undo
          </button>
        </div>
      ),
      { duration: 5000 }
    );

    // Final deletion after delay (if not undone)
    setTimeout(async () => {
      if (!wasUndone) {
        try {
          await axios.delete(`http://localhost:8000/document/${doc.id}`, {
            headers: { Authorization: `Bearer ${token}` },
          });
          toast.success(`"${doc.title}" deleted`);
          navigate("/documents");
        } catch (err) {
          toast.error(`Failed to delete "${doc.title}"`);
          setDoc(doc); // Restore if deletion fails
        }
      }
    }, 5000);
  };

  // Display error if failed to fetch
  if (error)
    return <p className="text-red-600 text-center mt-8 text-lg">{error}</p>;

  // Show loading message until document is available
  if (!doc)
    return (
      <p className="text-gray-500 text-center mt-8 text-lg">
        Loading document...
      </p>
    );

  return (
    <article className="space-y-6 px-4 sm:px-6 lg:px-8">
      {/* Header with delete button */}
      <PageHeader
        title={doc.title}
        actionButton={
          <button
            onClick={handleDelete}
            className="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700 transition"
          >
            <HiOutlineTrash className="w-5 h-5 inline-block mr-2" />
            Delete Document
          </button>
        }
      />

      {/* Summary Section */}
      <section className="bg-white p-5 rounded-lg shadow-sm mb-6">
        <h2 className="text-xl font-semibold text-gray-800 mb-4 flex items-center gap-2">
          <HiOutlineBookOpen className="text-blue-500 w-6 h-6" />
          Summary
        </h2>
        <p className="text-gray-700 leading-relaxed">{doc.summary}</p>
      </section>

      {/* Key Clauses Section */}
      {doc.clauses?.length > 0 && (
        <section className="bg-white p-5 rounded-lg shadow-sm mb-6">
          <h2 className="text-xl font-semibold text-gray-800 mb-4 flex items-center gap-2">
            <HiOutlineClipboardList className="text-blue-500 w-6 h-6" />
            Key Clauses
          </h2>
          <ul className="divide-y divide-gray-200">
            {doc.clauses.map((clause: any, idx: number) => (
              <li key={idx} className="py-3">
                <h4 className="font-medium text-gray-700">{clause.title}</h4>
                <p className="text-sm text-gray-600 mt-1">{clause.content}</p>
              </li>
            ))}
          </ul>
        </section>
      )}

      {/* Red Flags Section */}
      {doc.red_flags?.length > 0 && (
        <section className="bg-white p-5 rounded-lg shadow-sm mb-6 border-l-4 border-red-500">
          <h2 className="text-xl font-semibold text-red-600 mb-2 flex items-center gap-2">
            <HiExclamationCircle />
            Red Flags
          </h2>
          <ul className="list-disc list-inside text-red-700 space-y-1 text-sm">
            {doc.red_flags.map((flag: string, idx: number) => (
              <li key={idx}>{flag}</li>
            ))}
          </ul>
        </section>
      )}

      {/* Full Content Section */}
      <section className="bg-white p-5 rounded-lg shadow-sm">
        <h2 className="text-xl font-semibold text-gray-800 mb-4 flex items-center gap-2">
          <HiOutlineDocumentText className="text-blue-500 w-6 h-6" />
          Full Content
        </h2>
        <div className="text-gray-700 whitespace-pre-wrap text-sm leading-relaxed max-h-[60vh] overflow-y-auto border border-gray-200 rounded p-4">
          {doc.content}
        </div>
      </section>

      {/* AI Chat Popup */}
      <>
        <button
          onClick={() => setChatOpen(true)}
          className="fixed bottom-6 right-6 bg-blue-600 text-white p-4 rounded-full shadow-lg hover:bg-blue-700 z-50"
        >
          <HiOutlineChat className="w-6 h-6" />
        </button>

        {chatOpen && (
          <DocumentChatPanel
            context={doc.content}
            onClose={() => setChatOpen(false)}
          />
        )}
      </>
    </article>
  );
}