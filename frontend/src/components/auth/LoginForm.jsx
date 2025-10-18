import { useState } from "react";
import { Link } from "react-router-dom";
import Button from "../common/button/Button";

const LoginForm = ({ onSubmit, loading = false, error = "" }) => {
  const [formData, setFormData] = useState({
    username: "",
    password: ""
  });
  const [mode, setMode] = useState("collector");

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
    <div className="w-full max-w-md">
      {/* Header */}
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold gradient-text mb-2 cursor-pointer">
          NFT Marketplace
        </h1>
        <p className="text-gray-400 text-sm">
          Добро пожаловать в будущее цифрового искусства
        </p>
      </div>

      {/* Mode Switcher */}
      <div className="mode-switcher flex mb-6">
        <button
          onClick={() => setMode("collector")}
          className={`flex-1 py-2 px-4 rounded-lg text-sm font-medium mode-button ${
            mode === "collector" ? "mode-active" : "text-gray-400"
          }`}
        >
          Collector Mode
        </button>
        <button
          onClick={() => setMode("pro")}
          className={`flex-1 py-2 px-4 rounded-lg text-sm font-medium mode-button ${
            mode === "pro" ? "mode-active" : "text-gray-400"
          }`}
        >
          Pro Mode
        </button>
      </div>

      {/* Login Form */}
      <form onSubmit={handleSubmit} className="glass-card p-8 neon-border">
        <div className="text-center mb-6">
          <h2 className="text-2xl font-bold text-white mb-2">
            {mode === "collector" ? "Войти как коллекционер" : "Войти как трейдер"}
          </h2>
          <p className="text-gray-400 text-sm">
            {mode === "collector" 
              ? "Откройте для себя уникальные NFT" 
              : "Торгуйте с профессиональными инструментами"
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
          <div>
            <label className="block text-blue-300 text-sm font-medium mb-2">
              Имя пользователя
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

          <div>
            <label className="block text-blue-300 text-sm font-medium mb-2">
              Пароль
            </label>
            <input
              type="password"
              name="password"
              placeholder="Введите пароль"
              value={formData.password}
              onChange={handleChange}
              className="w-full p-3 input-modern rounded-lg placeholder-gray-500"
              required
            />
          </div>

          <Button
            type="submit"
            className="w-full btn-modern py-3 px-6 rounded-lg font-medium"
            disabled={loading}
          >
            {loading ? "Вход..." : "Войти в систему"}
          </Button>
        </div>

        <div className="mt-6 text-center">
          <p className="text-gray-400 text-sm">
            Нет аккаунта?{" "}
            <Link to="/register" className="text-blue-400 link-hover">
              Зарегистрироваться
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

export default LoginForm;
