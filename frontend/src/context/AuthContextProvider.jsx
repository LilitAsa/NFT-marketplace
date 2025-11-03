import { useState, useEffect } from "react";
import { AuthContext } from "./AuthContext";
import axios from "axios";
import { api } from "../api/client";

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // Проверяем, есть ли сохраненный токен при загрузке
  useEffect(() => {
    const token = localStorage.getItem("access");
    if (token) {
      // Проверяем валидность токена
      checkAuthStatus();
    } else {
      setLoading(false);
    }
  }, []);

  const checkAuthStatus = async () => {
    try {
      const token = localStorage.getItem("access");
      const response = await axios.get("http://127.0.0.1:8000/api/accounts/me/", {
        headers: { Authorization: `Bearer ${token}` }
      });
      console.log("📦 Данные профиля из бэкенда:", response.data);
      setUser(response.data);
    } catch {
      // Токен недействителен, очищаем его
      localStorage.removeItem("access");
      setUser(null);
    } finally {
      setLoading(false);
    }
  };

  const login = async (formData) => {
    try {
      const response = await axios.post("http://127.0.0.1:8000/api/accounts/login/", {
        username: formData.username,
        password: formData.password
      });
      
      localStorage.setItem("access", response.data.access);
      
      // Получаем данные пользователя
      const profileResponse = await axios.get("http://127.0.0.1:8000/api/accounts/me/", {
        headers: { Authorization: `Bearer ${response.data.access}` }
      });
      
      setUser(profileResponse.data);
      return { success: true };
    } catch (error) {
      console.error("Login error:", error);
      if (error.response?.status === 401) {
        return { success: false, error: "Неверное имя пользователя или пароль" };
      } else if (error.response?.status === 400) {
        return { success: false, error: "Проверьте правильность введенных данных" };
      } else {
        return { success: false, error: "Ошибка входа. Попробуйте позже" };
      }
    }
  };

  const logout = async () => {
    try {
      await api.post("/accounts/logout/"); // сервер удалит refresh_cookie
    } catch (e) {
      console.warn("logout api failed, ignore", e);
    }
    localStorage.removeItem("access");
    delete api.defaults.headers.common.Authorization; 
    setUser(null);
    setLoading(false);
  };

  const updateUser = (updatedData) => {
    setUser((prev) => ({
      ...prev,
      ...updatedData,
    }));
  };

  return (
    <AuthContext.Provider 
      value={{
        user, login, 
        logout, setUser, 
        loading, updateUser 
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};
