import { useAuth } from "../lib/auth";
import { Navigate } from "react-router-dom";
import FullPageSpinner from "./FullPageSpinner";

/**
 * A wrapper component for private routes.
 * It checks the authentication status using the useAuth hook.
 * If the user is authenticated, it renders the children.
 * Otherwise, it redirects to the login page.
 */
export default function PrivateRoute({ children }: { children: React.ReactNode }) {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    return <FullPageSpinner />;
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return children;
}