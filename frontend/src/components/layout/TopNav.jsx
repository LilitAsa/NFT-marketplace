import { useContext } from "react";
import { Link, useNavigate } from "react-router-dom";
import { AuthContext } from "../../context/AuthContext";

function RoleBadge({ role }) {
  if (!role) return null;
  const map = { admin: "bg-red-500/20 text-red-300", pro: "bg-purple-500/20 text-purple-300", collector: "bg-blue-500/20 text-blue-300" };
  return (
    <span className={`px-2 py-1 rounded-lg text-xs font-medium ${map[role] || "bg-gray-500/20 text-gray-300"}`}>
      {role}
    </span>
  );
}

export default function TopNav() {
  const { user, loading, logout, roleHome } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleLogout = async () => {
    await logout();
    navigate("/", { replace: true });
  };

  return (
    <header className="glass-card mx-4 mt-4 p-4 neon-border fixed top-0 left-0 right-0 z-40">
      <div className="flex items-center justify-between">
        {/* left */}
        <div className="flex items-center gap-4">
          <Link to="/" onClick={()=>navigate(user?roleHome(user):"/")} className="text-2xl font-bold gradient-text">NFT Marketplace</Link>
          <div className="flex items-center space-x-4">
            {/* если вошёл и pro/admin — показать кнопку Pro */}
            {user && (user.role === "pro" || user.role === "admin") && (
              <Link
                to="/pro"
                className="glass-card px-4 py-2 rounded-lg text-sm font-medium text-purple-300 hover:text-white"
              >
                Pro Dashboard
              </Link>
            )}

            {/* если admin — ещё кнопка Admin */}
            {user && user.role === "admin" && (
              <Link
                to="/admin"
                className="glass-card px-4 py-2 rounded-lg text-sm font-medium text-red-300 hover:text-white"
              >
                Admin
              </Link>
            )}

           
          </div>

          {/* быстрые ссылки */}
          <nav className="hidden sm:flex items-center gap-3 text-sm text-gray-300">
            <Link to="/" className="hover:text-white">Home</Link>
            <Link to="/pro" className="hover:text-white">Pro</Link>
            <Link to="/admin" className="hover:text-white">Admin</Link>
          </nav>
        </div>

        {/* right */}
        <div className="flex items-center gap-3">
          {loading ? (
            <div className="h-8 w-40 bg-white/5 rounded-lg animate-pulse" />
          ) : user ? (
            <>
              <RoleBadge role={user.role} />
              <Link
                to={`/u/${user.username}`}
                className="px-3 py-2 rounded-lg bg-white/5 hover:bg-white/10 text-white"
              >
                @{user.username}
              </Link>

                {/* если не вошёл — Login, если вошёл — Профиль */}
              {!user ? (
                <Link
                  to="/login"
                  className="btn-modern px-6 py-2 rounded-lg text-sm font-medium"
                >
                  Login
                </Link>
              ) : (
                <Link
                  to={`/u/${user.username}`}
                  className="btn-modern px-6 py-2 rounded-lg text-sm font-medium"
                >
                  Мой профиль
                </Link>
              )}

              <button
                onClick={handleLogout}
                className="px-3 py-2 rounded-lg text-white hover:text-blue-300"
                title="Выйти"
              >
                Выйти
              </button>
            </>
          ) : (
            <>
              <Link
                to="/login"
                className="btn-modern px-4 py-2 rounded-lg text-sm font-medium"
              >
                Войти
              </Link>
              <Link
                to="/register"
                className="px-4 py-2 rounded-lg text-sm font-medium text-gray-300 hover:text-white"
              >
                Регистрация
              </Link>
            </>
          )}
        </div>
      </div>
    </header>
  );
}
