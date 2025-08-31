import { Routes, Route, Navigate } from "react-router-dom";
import Home from "./features/home/Home";
import Login from "./features/auth/Login";
import Register from "./features/auth/Register";
import DocumentDetails from "./features/dashboard/DocumentDetail";
import DocumentList from "./features/dashboard/DocumentList";
import DashboardLayout from "./features/dashboard/DashboardLayout";
import PrivateRoute from "./components/PrivateRoute";
import { Toaster } from "react-hot-toast";
import { AuthProvider } from "./lib/auth";

/**
 * Root component of the LegalLens Single Page Application (SPA).
 * Manages all route definitions and global toast notifications.
 */
export default function App() {
  return (

    <AuthProvider>
      <Routes>
        {/* Public routes */}
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        {/* Protected dashboard routes */}
        <Route
          path="/dashboard"
          element={
            <PrivateRoute>
              <DashboardLayout />
            </PrivateRoute>
          }
        >
          {/* Nested routes within dashboard */}
          <Route index element={<DocumentList />} />
          <Route path="doc/:docId" element={<DocumentDetails />} />
        </Route>

        {/* Catch-all: redirect any unknown path to dashboard */}
        <Route path="*" element={<Navigate to="/dashboard" replace />} />
      </Routes>

      {/* Global toast notification system */}
      <Toaster
        position="bottom-center"
        toastOptions={{
          className: "",
          style: {
            background: "#ffffff",
            color: "#333",
            borderRadius: "8px",
            boxShadow: "0 4px 12px rgba(0,0,0,0.1)",
            padding: "12px 16px",
          },
        }}
      />
    </AuthProvider>
  );
}