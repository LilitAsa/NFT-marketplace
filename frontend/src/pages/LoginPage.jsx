import { useContext, useState } from "react";
import { AuthContext } from "../context/AuthContext";

export default function LoginPage() {
  const { login } = useContext(AuthContext);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [mode, setMode] = useState("collector");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await login(username, password);
      alert("Вход выполнен успешно ");
    } catch (err) {
      console.error(err);
      alert("Ошибка входа ");
    }
  };

  return (
    <div className="dark-bg min-h-screen flex items-center justify-center p-4">
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

          <div className="space-y-4">
            <div>
              <label className="block text-blue-300 text-sm font-medium mb-2">
                Имя пользователя
              </label>
              <input
                type="text"
                placeholder="Введите имя пользователя"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
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
                placeholder="Введите пароль"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full p-3 input-modern rounded-lg placeholder-gray-500"
                required
              />
            </div>

            <button
              type="submit"
              className="w-full btn-modern py-3 px-6 rounded-lg font-medium"
            >
              Войти в систему
            </button>
          </div>

          <div className="mt-6 text-center">
            <p className="text-gray-400 text-sm">
              Нет аккаунта?{" "}
              <a href="#" className="text-blue-400 link-hover">
                Зарегистрироваться
              </a>
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
    </div>
  );
}
