import { Outlet, useMatch } from "react-router-dom";
import Topbar from "../../components/TopBar";
import PageHeader from "../../components/PageHeader";

export default function DashboardLayout() {
  // Detect if the current route matches a document detail view
  const matchDetail = useMatch({ path: "/dashboard/doc/:docId", end: true });

  // Page header props
  let title = "";                    // Optional dynamic title
  let backTo: string | undefined;   // Optional back navigation path

  // If on a document detail page, show back button
  if (matchDetail) {
    backTo = "/dashboard";
  }

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col">
      {/* Top navigation bar */}
      <Topbar />

      {/* Main content area */}
      <div className="pt-16 flex-1 flex flex-col">
        <div className="max-w-7xl mx-auto w-full p-6">
          {/* Page header with optional back button */}
          <PageHeader title={title} backTo={backTo} />

          {/* Nested route content will be injected here */}
          <Outlet />
        </div>
      </div>
    </div>
  );
}