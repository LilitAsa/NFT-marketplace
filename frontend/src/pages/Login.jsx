import { useContext, useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";
import LoginForm from "../components/auth/LoginForm";

export default function LoginPage() {
  const { login, user, loading } = useContext(AuthContext);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  // Если пользователь уже авторизован, перенаправляем в профиль
  useEffect(() => {
    if (user && !loading) {
      navigate("/profile");
    }
  }, [user, loading, navigate]);

  const handleLogin = async (formData, mode) => {
    setIsLoading(true);
    setError("");
    
    try {
      const result = await login(formData, mode);
      if (result.success) {
        navigate("/profile");
      } else {
        setError(result.error);
      }
    } catch (err) {
      console.error("Login error:", err);
      setError("Произошла ошибка при входе");
    } finally {
      setIsLoading(false);
    }
  };

  // Показываем загрузку, если проверяем авторизацию
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
    <div className="dark-bg min-h-screen flex items-center justify-center p-4">
      <LoginForm 
        onSubmit={handleLogin}
        loading={isLoading}
        error={error}
      />
    </div>
  );
}