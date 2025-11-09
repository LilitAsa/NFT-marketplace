import { useState } from "react";
import { Link } from "react-router-dom";
import Button from "../common/button/Button";

export default function LoginForm({ onSubmit, loading = false, error = "" }) {
  const [formData, setFormData] = useState({ username: "", password: "" });
  const [mode, setMode] = useState("collector");

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((p) => ({ ...p, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();                 // важно!
    onSubmit?.({ ...formData, mode });  // передаём наверх
  };

  return (
    <div className="w-full max-w-md">
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold gradient-text mb-2">NFT Marketplace</h1>
        <p className="text-gray-400 text-sm">Добро пожаловать в будущее цифрового искусства</p>
      </div>

      <div className="mode-switcher flex mb-6">
        <button
          type="button"
          onClick={() => setMode("collector")}
          className={`flex-1 py-2 px-4 rounded-lg text-sm font-medium mode-button ${
            mode === "collector" ? "mode-active" : "text-gray-400"
          }`}
        >
          Collector Mode
        </button>
        <button
          type="button"
          onClick={() => setMode("pro")}
          className={`flex-1 py-2 px-4 rounded-lg text-sm font-medium mode-button ${
            mode === "pro" ? "mode-active" : "text-gray-400"
          }`}
        >
          Pro Mode
        </button>
      </div>

      <form onSubmit={handleSubmit} className="glass-card p-8 neon-border">
        {error && (
          <div className="mb-4 p-3 bg-red-900/20 border border-red-500/30 rounded-lg">
            <p className="text-red-400 text-sm text-center">{error}</p>
          </div>
        )}

        <div className="space-y-4">
          <div>
            <label className="block text-blue-300 text-sm font-medium mb-2">Имя пользователя</label>
            <input
              name="username"
              value={formData.username}
              onChange={handleChange}
              autoComplete="username"
              className="w-full p-3 input-modern rounded-lg"
              required
            />
          </div>

          <div>
            <label className="block text-blue-300 text-sm font-medium mb-2">Пароль</label>
            <input
              type="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              autoComplete="current-password"
              className="w-full p-3 input-modern rounded-lg"
              required
            />
          </div>

          <Button type="submit" className="w-full btn-modern py-3" disabled={loading}>
            {loading ? "Вход..." : "Войти в систему"}
          </Button>
        </div>

        <div className="mt-6 text-center">
          <p className="text-gray-400 text-sm">
            Нет аккаунта? <Link to="/register" className="text-blue-400 link-hover">Зарегистрироваться</Link>
          </p>
        </div>
      </form>
    </div>
  );
}
