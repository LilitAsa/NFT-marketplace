import React, { Suspense, lazy } from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";

import { AuthProvider } from "./context/AuthContextProvider";
import RoleRoute from "./routes/RoleRoute.jsx";

import TopNav from "./components/layout/TopNav.jsx";
import HomePage from "./pages/Home.jsx";
import ProfilePage from "./pages/ProfilePage.jsx";
import LoginWithRedirect from "./components/auth/LoginWithRedirect.jsx";

import "./styles/index.css";

const ProDashboard = lazy(() => import("./pages/pro/Dashboard.jsx"));
const AdminPanel  = lazy(() => import("./pages/admin/Panel.jsx"));

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <AuthProvider>
      <BrowserRouter>
        <TopNav />    
        <Suspense fallback={<div className="p-6">Загрузка…</div>}>
          <Routes>

            <Route path="/" element={<HomePage />} />
            <Route path="/login" element={<LoginWithRedirect />} />

            <Route
              path="/profile"
              element={
                <RoleRoute allow={["collector", "pro", "admin"]}>
                  <ProfilePage />
                </RoleRoute>
              }
            />
            <Route
              path="/u/:username"
              element={
                <RoleRoute allow={["collector", "pro", "admin"]}>
                  <ProfilePage />
                </RoleRoute>
              }
            />

            <Route
              path="/pro"
              element={
                <RoleRoute allow={["pro", "admin"]}>
                  <ProDashboard />
                </RoleRoute>
              }
            />
            <Route
              path="/admin"
              element={
                <RoleRoute allow={["admin"]}>
                  <AdminPanel />
                </RoleRoute>
              }
            />

            <Route path="*" element={<div className="p-6">404</div>} />
          </Routes>
        </Suspense>
      </BrowserRouter>
    </AuthProvider>
  </React.StrictMode>
);
