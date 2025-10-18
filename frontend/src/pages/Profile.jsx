import { useEffect, useState, useContext } from "react";
import { useForm } from "react-hook-form";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";
import Button from "../components/common/button/Button";
import axios from "axios";

const Profile = () => {
  const { user: contextUser, logout, updateUser } = useContext(AuthContext);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const { register, handleSubmit, reset, formState: { errors } } = useForm();
  const navigate = useNavigate();

  // Если пользователь не авторизован, перенаправляем на логин
  useEffect(() => {
    if (!contextUser) {
      navigate("/login");
    } else {
      // Заполняем форму данными пользователя
      reset({
        email: contextUser.email || "",
        first_name: contextUser.first_name || "",
        last_name: contextUser.last_name || "",
        phone: contextUser.phone || "",
      });
    }
  }, [contextUser, navigate, reset]);

  const onSubmit = async (data) => {
    setSaving(true);
    setError("");
    setSuccess("");

    try {
      const token = localStorage.getItem("access");
      
      // Обновляем профиль
      await axios.patch("http://127.0.0.1:8000/api/accounts/me/", data, {
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      });

     // Обновляем данные в контексте через AuthProvider
      const updatedUserResponse = await axios.get("http://127.0.0.1:8000/api/accounts/me/", {
        headers: { Authorization: `Bearer ${token}` }
      });

      updateUser(updatedUserResponse.data);

      setSuccess("Профиль успешно обновлен !");
      setError("");
    } catch (err) {
      console.error("Ошибка обновления профиля:", err);

      if (err.response?.status === 401) {
        setError("Сессия истекла. Войдите заново");
        logout();
        navigate("/login");
      } else if (err.response?.data?.detail) {
        setError(err.response.data.detail);
      } else {
        setError("Ошибка при обновлении профиля");
      }
    } finally {
      setSaving(false);
    }
  };

  if (!contextUser) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <p className="text-gray-400">Перенаправление...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen p-4 flex flex-row justify-center items-start">
      <div className="max-w-2xl mx-auto">
        <div className="glass-card p-8 neon-border">
          <h2 className="text-3xl font-bold text-center gradient-text mb-8">Мой профиль</h2>

          {/* Success Message */}
          {success && (
            <div className="mb-6 p-4 bg-green-900/20 border border-green-500/30 rounded-lg">
              <p className="text-green-400 text-center">{success}</p>
            </div>
          )}

          {/* Error Message */}
          {error && (
            <div className="mb-6 p-4 bg-red-900/20 border border-red-500/30 rounded-lg">
              <p className="text-red-400 text-center">{error}</p>
            </div>
          )}

          <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
            {/* Username - только для чтения */}
            <div>
              <label className="block text-blue-300 text-sm font-medium mb-2">
                Имя пользователя
              </label>
              <input
                type="text"
                value={contextUser.username}
                readOnly
                className="w-full p-3 bg-gray-100 border rounded-lg text-gray-600"
              />
            </div>

            {/* Role - только для чтения */}
            <div>
              <label className="block text-blue-300 text-sm font-medium mb-2">
                Роль
              </label>
              <input
                type="text"
                value={contextUser.role}
                readOnly
                className="w-full p-3 bg-gray-100 border rounded-lg text-gray-600"
              />
            </div>

            {/* Email */}
            <div>
              <label className="block text-blue-300 text-sm font-medium mb-2">
                Email *
              </label>
              <input
                type="email"
                {...register("email", { 
                  required: "Email обязателен",
                  pattern: {
                    value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                    message: "Неверный формат email"
                  }
                })}
                className="w-full p-3 input-modern rounded-lg placeholder-gray-500"
                placeholder="Введите email"
              />
              {errors.email && (
                <p className="text-red-400 text-sm mt-1">{errors.email.message}</p>
              )}
            </div>

            {/* First Name */}
            <div>
              <label className="block text-blue-300 text-sm font-medium mb-2">
                Имя
              </label>
              <input
                type="text"
                {...register("first_name")}
                className="w-full p-3 input-modern rounded-lg placeholder-gray-500"
                placeholder="Введите имя"
              />
            </div>

            {/* Last Name */}
            <div>
              <label className="block text-blue-300 text-sm font-medium mb-2">
                Фамилия
              </label>
              <input
                type="text"
                {...register("last_name")}
                className="w-full p-3 input-modern rounded-lg placeholder-gray-500"
                placeholder="Введите фамилию"
              />
            </div>

            {/* Phone */}
            <div>
              <label className="block text-blue-300 text-sm font-medium mb-2">
                Телефон
              </label>
              <input
                type="tel"
                {...register("phone", {
                  pattern: {
                    value: /^[+]?[1-9][\d]{0,15}$/,
                    message: "Неверный формат телефона"
                  }
                })}
                className="w-full p-3 input-modern rounded-lg placeholder-gray-500"
                placeholder="Введите телефон"
              />
              {errors.phone && (
                <p className="text-red-400 text-sm mt-1">{errors.phone.message}</p>
              )}
            </div>

            {/* Buttons */}
            <div className="flex flex-col sm:flex-row gap-4 pt-4">
              <Button
                type="submit"
                className="flex-1 btn-modern py-3 rounded-lg font-medium"
                disabled={saving}
              >
                {saving ? "Сохранение..." : "Сохранить"}
              </Button>
              
              <Button
                type="button"
                onClick={() => reset()}
                className="flex-1 glass-card py-3 rounded-lg font-medium text-white hover:bg-opacity-80"
                disabled={saving}
              >
                Отменить
              </Button>
            </div>
          </form>

          {/* Additional Info */}
          <div className="mt-8 pt-6 border-t border-gray-700">
            <h3 className="text-lg font-semibold text-white mb-4">Дополнительная информация</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-gray-400">
              <div>
                <span className="text-blue-300">Дата регистрации:</span>
                <p>15 октября 2025</p>
              </div>
              <div>
                <span className="text-blue-300">Статус аккаунта:</span>
                <p className="text-green-400">Активен</p>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div id="logout">
        <button
          onClick={() => {
            logout();
            navigate("/login");
          }}
          className="mb-6 px-4 py-2  hover:text-blue-300 text-white rounded-lg transition"
        >
          Выйти
        </button>
      </div>
    </div>
  );
};

export default Profile;
