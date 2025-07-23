import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

/**
 * User registration page for LegalLens.
 * Features:
 * - Form input validation
 * - API integration to register new users
 * - Visual feedback and error handling
 */

export default function Register() {
  // Form state variables
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  // Handle form submission
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      // Send registration request to backend
      await axios.post('http://localhost:8000/auth/register', {
        email,
        password,
      });

      setError('');
      alert('Registration successful');
      navigate('/login'); // Redirect to login page
    } catch (err: any) {
      // Show error message from server or default message
      setError(err.response?.data?.detail || 'Registration failed');
    }
  };

  return (
    <main className="min-h-screen flex items-center justify-center bg-gray-50 px-4">
      <div className="w-full max-w-md bg-white rounded-xl shadow-md p-8">
        {/* Heading */}
        <h2 className="text-3xl font-bold text-center text-gray-800 mb-6">
          Create Your Account
        </h2>

        {/* Registration Form */}
        <form onSubmit={handleSubmit} className="space-y-5">
          {/* Email input */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Email
            </label>
            <input
              type="email"
              placeholder="you@example.com"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>

          {/* Password input */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Password
            </label>
            <input
              type="password"
              placeholder="••••••••"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          {/* Error message */}
          {error && <p className="text-red-600 text-sm">{error}</p>}

          {/* Submit button */}
          <button
            type="submit"
            className="w-full bg-green-600 text-white font-semibold py-2 rounded-lg hover:bg-green-700 transition duration-200"
          >
            Sign Up
          </button>
        </form>

        {/* Navigation link to login */}
        <p className="mt-4 text-center text-sm text-gray-600">
          Already have an account?{' '}
          <a href="/login" className="text-green-600 hover:underline">
            Log in
          </a>
        </p>
      </div>
    </main>
  );
}