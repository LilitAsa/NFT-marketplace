import { useEffect, useState, useContext } from "react";
import { useParams, useNavigate } from "react-router-dom";
import NFTGrid from "../components/nft/NFTGrid.jsx";
import { api } from "../api/client";
import { AuthContext } from "../context/AuthContext.jsx";

export default function ProfilePage() {
  const { username: usernameFromRoute } = useParams();
  const navigate = useNavigate();
  const { user, logout } = useContext(AuthContext);
  const [username, setUsername] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;

    async function init() {
      if (usernameFromRoute) {
        if (!cancelled) {
          setUsername(usernameFromRoute);
          setLoading(false);
        }
        return;
      }

      try {
        const { data } = await api.get("/accounts/me/");
        if (cancelled) return;
        setUsername(data.username);
        navigate(`/u/${data.username}`, { replace: true });
      } catch {
        if (!cancelled) {
          setUsername("");
          setLoading(false);
        }
      }
    }

    init();
    return () => { cancelled = true; };
  }, [usernameFromRoute, navigate]);

  const handleLogout = async () => { 
    await logout(); 
    navigate("/", { replace: true });
  }

  if (loading) return <div className="p-6">Загрузка профиля…</div>;
  if (!username) return <div className="p-6">Нужно войти</div>;

  return (
    <div className="max-w-6xl mx-auto p-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold">@{username}</h1>
        {user && (
          <button
            onClick={handleLogout}
           className="px-3 py-2 rounded-lg text-white hover:text-blue-300"
          >
            Выйти
          </button>
        )}
      </div>

      <div className="mt-6">
        <NFTGrid username={username} type="owned" />
      </div>
    </div>
  );
}
