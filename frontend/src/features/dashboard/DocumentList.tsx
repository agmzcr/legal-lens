import { useEffect, useState } from "react";
import axios from "axios";
import { useNavigate, Link } from "react-router-dom";
import { HiDocumentText, HiOutlineChevronRight, HiOutlineTrash } from "react-icons/hi";

import PageHeader from "../../components/PageHeader";
import UploadDocumentModal from "../../components/UploadDocumentModal";
import toast from "react-hot-toast";

// Document data type
type Doc = {
  id: string;
  title: string;
  content: string;
  summary: string;
  red_flags: string[];
  clauses: string[];
  created_at: string;
};

/**
 * DocumentList component
 * Displays a searchable list of uploaded documents with delete and upload functionality.
 */
export default function DocumentList() {
  const [documents, setDocuments] = useState<Doc[]>([]);
  const [filtered, setFiltered] = useState<Doc[]>([]);
  const [search, setSearch] = useState("");
  const [error, setError] = useState("");
  const [showModal, setShowModal] = useState(false);

  const navigate = useNavigate();

  // Fetch documents from API when component mounts
  useEffect(() => {
    const fetchDocuments = async () => {
      try {
        const token = localStorage.getItem("token");
        const { data } = await axios.get<Doc[]>("http://localhost:8000/documents", {
          headers: { Authorization: `Bearer ${token}` },
        });
        setDocuments(data);
        setFiltered(data);
      } catch (err: any) {
        setError("Failed to fetch documents");
      }
    };

    fetchDocuments();
  }, []);

  // Filter documents when the search input or document list changes
  useEffect(() => {
    const term = search.toLowerCase();
    setFiltered(
      documents.filter(
        (d) =>
          d.title.toLowerCase().includes(term) ||
          d.summary.toLowerCase().includes(term)
      )
    );
  }, [search, documents]);

  // Callback for successful document upload
  const handleUploadComplete = (docId: string) => {
    console.log("Redirecting to:", `/dashboard/doc/${docId}`);
    setShowModal(false);
    navigate(`/dashboard/doc/${docId}`);
  };

  // Handle deletion of a document with undo option
  const handleDelete = (docId: string) => {
    const deleted = documents.find((doc) => doc.id === docId);
    if (!deleted) return;

    setDocuments((prev) => prev.filter((doc) => doc.id !== docId));
    let wasUndone = false;

    toast(
      (t) => (
        <div className="flex items-center justify-between space-x-2">
          <span className="text-sm text-gray-800">
            ⏳ Deleting document: <strong>{deleted.title}</strong>
          </span>
          <button
            onClick={() => {
              wasUndone = true;
              setDocuments((prev) => [deleted, ...prev]);
              toast.dismiss(t.id);
            }}
            className="text-blue-600 text-sm font-medium hover:underline"
          >
            Undo
          </button>
        </div>
      ),
      { duration: 5000 }
    );

    // Delay actual deletion to allow undo
    setTimeout(async () => {
      if (!wasUndone) {
        try {
          const token = localStorage.getItem("token");
          await axios.delete(`http://localhost:8000/document/${docId}`, {
            headers: { Authorization: `Bearer ${token}` },
          });
          toast.success(`Document "${deleted.title}" deleted`);
        } catch (err) {
          toast.error(`Failed to delete "${deleted.title}"`);
          setDocuments((prev) => [deleted, ...prev]);
        }
      }
    }, 5000);
  };

  // Show error message if fetching documents failed
  if (error) {
    return <p className="text-red-600 text-center mt-6">{error}</p>;
  }

  return (
    <article className="space-y-6">
      <PageHeader
        title="Your Documents"
        searchInput={
          <input
            type="text"
            placeholder="Search documents..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-64 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 ml-auto"
          />
        }
      />

      {/* Handle empty or no search result states */}
      {documents.length === 0 ? (
        <p className="text-gray-500 text-center">
          You haven't uploaded any documents yet.
        </p>
      ) : filtered.length === 0 ? (
        <p className="text-gray-500 text-center">
          No results found for “{search}”.
        </p>
      ) : (
        <ul className="space-y-4">
          {filtered.map((doc) => (
            <li key={doc.id} className="relative group">
              <Link
                to={`doc/${doc.id}`}
                className="flex items-center gap-4 p-4 bg-white border border-gray-200 rounded-lg shadow-sm hover:shadow-md transition"
              >
                <HiDocumentText className="text-2xl text-blue-600 flex-shrink-0" />
                <div className="flex-1">
                  <h2 className="text-sm sm:text-base font-semibold text-gray-800 truncate sm:truncate-none max-w-full sm:max-w-none">
                    {doc.title}
                  </h2>
                  <p className="text-sm text-gray-500">
                    Uploaded: {new Date(doc.created_at).toLocaleString()}
                  </p>
                  <p className="mt-1 text-gray-700 text-sm line-clamp-2">
                    {doc.summary}
                  </p>
                </div>
                <HiOutlineChevronRight className="text-xl text-gray-400" />
              </Link>

              {/* Delete button visible on hover */}
              <button
                onClick={() => handleDelete(doc.id)}
                className="absolute top-2 right-2 text-gray-300 group-hover:text-red-500 transition"
                title="Delete document"
              >
                <HiOutlineTrash className="text-xl" />
              </button>
            </li>
          ))}
        </ul>
      )}

      {/* Floating button to upload a new document */}
      <button
        onClick={() => setShowModal(true)}
        className="fixed bottom-6 right-6 bg-blue-600 text-white px-4 py-3 rounded-full shadow-lg hover:bg-blue-700 z-50"
      >
        Upload Document
      </button>

      {/* Upload modal */}
      {showModal && (
        <UploadDocumentModal
          onClose={() => setShowModal(false)}
          onComplete={handleUploadComplete}
        />
      )}
    </article>
  );
}