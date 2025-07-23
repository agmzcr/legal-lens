import { Link } from "react-router-dom";

export default function Home() {
  return (
    <main className="p-4">
      {/* Header section with navigation buttons */}
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

      {/* Welcome headline and description */}
      <h1 className="text-4xl font-bold text-center mb-2">
        Welcome to LegalLens
      </h1>
      <p className="text-center text-gray-600">
        Your AI-powered legal document assistant.
      </p>
    </main>
  );
}