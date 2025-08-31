import { useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../../lib/auth";
import FullPageSpinner from "../../components/FullPageSpinner";

export default function Home() {
  const { isAuthenticated, isLoading } = useAuth();
  const navigate = useNavigate();

  // Redirect to dashboard if the user is already authenticated
  useEffect(() => {
    if (!isLoading && isAuthenticated) {
      navigate("/dashboard", { replace: true });
    }
  }, [isLoading, isAuthenticated, navigate]);

  // Show a loading spinner while the auth state is being checked
  if (isLoading) {
    return <FullPageSpinner />;
  }

  // Render the home page for unauthenticated users
  return (
    <main className="p-4">
      <header className="flex justify-end space-x-4 mb-6">
        <Link to="/login">
          <button className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
            Login
          </button>
        </Link>
        <Link to="/register">
          <button className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700">
            Register
          </button>
        </Link>
      </header>
      <h1 className="text-4xl font-bold text-center mb-2">
        Welcome to LegalLens
      </h1>
      <p className="text-center text-gray-600">
        Your AI-powered legal document assistant.
      </p>
    </main>
  );
}