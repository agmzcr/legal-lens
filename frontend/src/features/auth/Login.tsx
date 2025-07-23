import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

/**
 * Login page component for LegalLens.
 * Features:
 * - Vertical and horizontal centering
 * - Smooth UI and input handling
 * - Authentication via API and token storage
 */

export default function Login() {
  // State for form inputs and error message
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  // Submit handler for login form
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      // Send login request
      const response = await axios.post('http://localhost:8000/auth/login', {
        email,
        password,
      });

      // Extract token and store it locally
      const { access_token } = response.data;
      localStorage.setItem('token', access_token);
      setError('');
      navigate('/dashboard'); // Redirect to dashboard
    } catch (err: any) {
      // Show error message if authentication fails
      setError(err.response?.data?.detail || 'Login failed');
    }
  };

  return (
    <main className="min-h-screen flex items-center justify-center bg-gray-50 px-4">
      <div className="w-full max-w-md bg-white rounded-xl shadow-md p-8">
        {/* Page title */}
        <h2 className="text-3xl font-bold text-center text-gray-800 mb-6">
          Sign In to LegalLens
        </h2>

        {/* Login form */}
        <form onSubmit={handleSubmit} className="space-y-5">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Email
            </label>
            <input
              type="email"
              placeholder="you@example.com"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Password
            </label>
            <input
              type="password"
              placeholder="••••••••"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          {/* Show error if present */}
          {error && <p className="text-red-600 text-sm">{error}</p>}

          {/* Submit button */}
          <button
            type="submit"
            className="w-full bg-blue-600 text-white font-semibold py-2 rounded-lg hover:bg-blue-700 transition duration-200"
          >
            Log In
          </button>
        </form>

        {/* Link to registration page */}
        <p className="mt-4 text-center text-sm text-gray-600">
          Don't have an account?{' '}
          <a href="/register" className="text-blue-600 hover:underline">
            Register here
          </a>
        </p>
      </div>
    </main>
  );
}