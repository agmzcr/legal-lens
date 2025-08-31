import { Outlet, useMatch } from "react-router-dom";
import Topbar from "../../components/TopBar";
import PageHeader from "../../components/PageHeader";

export default function DashboardLayout() {
  // Check if the current route is a document detail page
  const isDocumentDetailPage = useMatch("/dashboard/doc/:docId");

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      {/* Top navigation bar */}
      <Topbar />

      {/* Main content area */}
      <div className="pt-20 flex-1 flex flex-col">
        <div className="max-w-5xl mx-auto w-full px-4 sm:px-8 lg:px-12 py-8">
          {/*
           * The PageHeader component is now aware of the current page.
           * If it's a document detail page, it displays a back button.
           * We can also add a dynamic title here.
           */}
          <PageHeader
            title={isDocumentDetailPage ? "Details of Document" : "My Documents"}
            backTo={isDocumentDetailPage ? "/dashboard" : undefined}
          />

          {/* Nested route content will be injected here */}
          <Outlet />
        </div>
      </div>
    </div>
  );
}