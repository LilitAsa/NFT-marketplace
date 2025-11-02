import { useState } from "react";
import { useNavigate } from "react-router-dom";
import RegisterForm from "../components/auth/RegisterForm";
import axios from "axios";

export default function RegisterPage() {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleRegister = async (formData) => {
    console.log(formData);
    
    setIsLoading(true);
    setError("");

    // Валидация формы
    if (!formData.username.trim()) {
      setError("Имя пользователя обязательно");
      setIsLoading(false);
      return;
    }

    if (!formData.email.trim()) {
      setError("Email обязателен");
      setIsLoading(false);
      return;
    }

    if (!formData.password) {
      setError("Пароль обязателен");
      setIsLoading(false);
      return;
    }

    if (formData.password !== formData.confirmPassword) {
      setError("Пароли не совпадают");
      setIsLoading(false);
      return;
    }

    if (formData.password.length < 6) {
      setError("Пароль должен содержать минимум 6 символов");
      setIsLoading(false);
      return;
    }

    // Валидация email
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(formData.email)) {
      setError("Неверный формат email");
      setIsLoading(false);
      return;
    }

    // Валидация номера телефона
    if (formData.phone && !/^\+?\d{10,15}$/.test(formData.phone)) {
      setError("Введите корректный номер телефона");
      setIsLoading(false);
      return;
    }

    try {
      // Подготавливаем данные для отправки (убираем confirmPassword)
      const { confirmPassword: _, ...registrationData } = formData;
      
      const response = await axios.post("http://127.0.0.1:8000/api/accounts/register/", registrationData);
      
      if (response.status === 201 || response.status === 200) {
        // Регистрация успешна
        alert("Регистрация успешна! Теперь вы можете войти в систему.");
        navigate("/login");
      }
    } catch (err) {
      console.error("Ошибка регистрации:", err);
      
      // Обрабатываем разные типы ошибок
      if (err.response) {
        // Сервер ответил с ошибкой
        if (err.response.status === 400) {
          const errorData = err.response.data;
          if (errorData.username) {
            setError("Пользователь с таким именем уже существует");
          } else if (errorData.email) {
            setError("Пользователь с таким email уже существует");
          } else {
            setError("Проверьте правильность введенных данных");
          }
        } else if (err.response.status === 500) {
          setError("Ошибка сервера. Попробуйте позже");
        } else {
          setError("Ошибка регистрации. Попробуйте позже");
        }
      } else if (err.request) {
        // Запрос был отправлен, но ответа не получено
        setError("Не удается подключиться к серверу. Проверьте подключение к интернету");
      } else {
        // Что-то пошло не так при настройке запроса
        setError("Ошибка при отправке запроса");
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="dark-bg min-h-screen flex items-center justify-center p-4">
      <RegisterForm 
        onSubmit={handleRegister}
        loading={isLoading}
        error={error}
      />
    </div>
  );
}