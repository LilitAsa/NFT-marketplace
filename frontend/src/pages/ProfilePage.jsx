import { useContext, useEffect, useMemo } from "react";
import { useParams, useNavigate } from "react-router-dom";
import NFTGrid from "../components/nft/NFTGrid.jsx";
import { AuthContext } from "../context/AuthContext";


export default function ProfilePage() {
  const { username: usernameFromRoute } = useParams();
  const { user, loading } = useContext(AuthContext);
  const navigate = useNavigate();

  // Итоговый username: из URL или из контекста
  const username = useMemo(
    () => usernameFromRoute || user?.username || "",
    [usernameFromRoute, user?.username]
  );

  // Если зашли на /profile (без :username), а юзер известен — один раз делаем редирект
  useEffect(() => {
    if (!usernameFromRoute && user?.username) {
      navigate(`/u/${user.username}`, { replace: true });
    }
  }, [usernameFromRoute, user?.username, navigate]);

  if (loading) return <div className="p-6">Загрузка профиля…</div>;
  if (!username) return <div className="p-6">Нужно войти</div>;

  return (
    <div className="max-w-6xl mx-auto p-6">
      <h1 className="text-2xl font-semibold">@{username}</h1>
      <div className="mt-6">
        <NFTGrid username={username} type="owned" />
      </div>
    </div>
  );
}