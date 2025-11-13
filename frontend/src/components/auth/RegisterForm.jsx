import { useState } from "react";
import { Link } from "react-router-dom";
import Button from "../common/button/Button";

const RegisterForm = ({ onSubmit, loading = false, error = "" }) => {
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
    confirmPassword: "",
    first_name: "",
    last_name: "",
    role: "collector",
    phone: "",
    telegramChatId: "",
  });
  const [mode, setMode] = useState("collector");
  const setModeAndRole = (next) => {
    setMode(next);
    setFormData(prev => ({ ...prev, role: next === "pro" ? "pro" : "collector" }));
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData, mode);
  };

  return (
    <div className="w-full max-w-md mt-20 mx-auto p-6">
      {/* Header */}
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold gradient-text mb-2 cursor-pointer">
          NFT Marketplace
        </h1>
        <p className="text-gray-400 text-sm">
          Присоединяйтесь к сообществу коллекционеров
        </p>
      </div>

      {/* Mode Switcher */}
      <div className="mode-switcher flex mb-6">
        <button
          onClick={() => setModeAndRole("collector")}
          className={`flex-1 py-2 px-4 rounded-lg text-sm font-medium mode-button ${
            mode === "collector" ? "mode-active" : "text-gray-400"
          }`}
        >
          Collector Mode
        </button>
        <button
          onClick={() => setModeAndRole("pro")}
          className={`flex-1 py-2 px-4 rounded-lg text-sm font-medium mode-button ${
            mode === "pro" ? "mode-active" : "text-gray-400"
          }`}
        >
          Pro Mode
        </button>
      </div>

      {/* Register Form */}
      <form onSubmit={handleSubmit} className="glass-card p-8 neon-border">
        <div className="text-center mb-6">
          <h2 className="text-2xl font-bold text-white mb-2">
            {mode === "collector" ? "Регистрация коллекционера" : "Регистрация трейдера"}
          </h2>
          <p className="text-gray-400 text-sm">
            {mode === "collector" 
              ? "Создайте аккаунт для покупки NFT" 
              : "Создайте аккаунт для торговли NFT"
            }
          </p>
        </div>

        {/* Error Message */}
        {error && (
          <div className="mb-4 p-3 bg-red-900/20 border border-red-500/30 rounded-lg">
            <p className="text-red-400 text-sm text-center">{error}</p>
          </div>
        )}

        <div className="space-y-4">
          {/* Username */}
          <div>
            <label className="block text-blue-300 text-sm font-medium mb-2">
              Имя пользователя *
            </label>
            <input
              type="text"
              name="username"
              placeholder="Введите имя пользователя"
              value={formData.username}
              onChange={handleChange}
              className="w-full p-3 input-modern rounded-lg placeholder-gray-500"
              required
            />
          </div>

          {/* Email */}
          <div>
            <label className="block text-blue-300 text-sm font-medium mb-2">
              Email *
            </label>
            <input
              type="email"
              name="email"
              placeholder="Введите email"
              value={formData.email}
              onChange={handleChange}
              className="w-full p-3 input-modern rounded-lg placeholder-gray-500"
              required
            />
          </div>

          {/* First Name */}
          <div>
            <label className="block text-blue-300 text-sm font-medium mb-2">
              Имя
            </label>
            <input
              type="text"
              name="first_name"
              placeholder="Введите имя"
              value={formData.first_name}
              onChange={handleChange}
              className="w-full p-3 input-modern rounded-lg placeholder-gray-500"
            />
          </div>

          {/* Last Name */}
          <div>
            <label className="block text-blue-300 text-sm font-medium mb-2">
              Фамилия
            </label>
            <input
              type="text"
              name="last_name"
              placeholder="Введите фамилию"
              value={formData.last_name}
              onChange={handleChange}
              className="w-full p-3 input-modern rounded-lg placeholder-gray-500"
            />
          </div>

          {/* Password */}
          <div>
            <label className="block text-blue-300 text-sm font-medium mb-2">
              Пароль *
            </label>
            <input
              type="password"
              name="password"
              placeholder="Введите пароль (минимум 6 символов)"
              value={formData.password}
              onChange={handleChange}
              className="w-full p-3 input-modern rounded-lg placeholder-gray-500"
              required
            />
          </div>

          {/* Confirm Password */}
          <div>
            <label className="block text-blue-300 text-sm font-medium mb-2">
              Подтвердите пароль *
            </label>
            <input
              type="password"
              name="confirmPassword"
              placeholder="Повторите пароль"
              value={formData.confirmPassword}
              onChange={handleChange}
              className="w-full p-3 input-modern rounded-lg placeholder-gray-500"
              required
            />
          </div>

          {/* Phone */}
          <div>
            <label className="block text-blue-300 text-sm font-medium mb-2">
              Телефон
            </label>
            <input
              type="text"
              name="phone"
              placeholder="Введите телефон"
              value={formData.phone}
              onChange={handleChange}
              className="w-full p-3 input-modern rounded-lg placeholder-gray-500"
            />
          </div>

          {/* Telegram Chat ID */}
          <div>
            <label className="block text-blue-300 text-sm font-medium mb-2">
              Telegram Chat ID
            </label>
            <input
              type="text"
              name="telegramChatId"
              placeholder="Введите Telegram Chat ID"
              value={formData.telegramChatId}
              onChange={handleChange}
              className="w-full p-3 input-modern rounded-lg placeholder-gray-500"
            />
          </div>

          <Button
            type="submit"
            className="w-full btn-modern py-3 px-6 rounded-lg font-medium"
            disabled={loading}
          >
            {loading ? "Создание аккаунта..." : "Создать аккаунт"}
          </Button>
        </div>

        <div className="mt-6 text-center">
          <p className="text-gray-400 text-sm">
            Уже есть аккаунт?{" "}
            <Link to="/login" className="text-blue-400 link-hover">
              Войти
            </Link>
          </p>
        </div>
      </form>

      {/* Stats Cards */}
      <div className="grid grid-cols-2 gap-4 mt-6">
        <div className="stats-card p-4 text-center">
          <div className="text-2xl font-bold text-blue-400">1.2M+</div>
          <div className="text-gray-400 text-sm">NFT в коллекции</div>
        </div>
        <div className="stats-card p-4 text-center">
          <div className="text-2xl font-bold text-purple-400">500K+</div>
          <div className="text-gray-400 text-sm">Активных пользователей</div>
        </div>
      </div>
    </div>
  );
};

export default RegisterForm;
