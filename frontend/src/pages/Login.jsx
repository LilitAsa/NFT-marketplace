import { useContext, useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";
import LoginForm from "../components/auth/LoginForm";

export default function LoginPage({ onSuccess }) {
  const { login, user, loading, roleHome } = useContext(AuthContext);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    if (user && !loading) {
      navigate(roleHome(user), { replace: true });
    }
  }, [user, loading, navigate, roleHome]);

  const handleLogin = async ({ username, password }) => {
    setIsLoading(true);
    setError("");
    try {
      const res = await login({ username, password });
      if (res.success) {
        onSuccess?.(res.user);
        navigate(roleHome(res.user), { replace: true });
      } else {
        setError(res.error || "Ошибка входа");
      }
    } catch (e) {
      console.error("Ошибка при входе:", e);
      setError("Произошла ошибка при входе");
    } finally {
      setIsLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="dark-bg min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <p className="text-gray-400">Проверка авторизации...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="dark-bg min-h-screen flex items-center justify-center mt-20 p-4">
      <LoginForm onSubmit={handleLogin} loading={isLoading} error={error} />
    </div>
  );
}
