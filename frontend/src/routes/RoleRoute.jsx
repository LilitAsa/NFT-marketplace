import { useContext } from "react";
import { Navigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext"

export default function RoleRoute({ allow = [], children }) {
  const { user, loading } = useContext(AuthContext);

  if (loading) return <div className="p-6">Проверка авторизации…</div>;
  if (!user) return <Navigate to="/login" replace />;
  if (allow.length && !allow.includes(user.role)) return <Navigate to="/" replace />;
  return children;
}