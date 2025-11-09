import { useEffect, useState } from "react";
import { api, setLoggedOut } from "../api/client";
import { AuthContext } from "./AuthContext";

const roleHome = (user) => {
  if (!user) return "/login";
  switch (user.role) {
    case "admin": return "/admin";
    case "pro":   return "/pro";
    case "collector":
    default:      return `/u/${user.username}`;
  }
};

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  console.log('provider', user); //provider null

  useEffect(() => {
    (async () => {
      try {
        const hasAccess = !!localStorage.getItem("access");
        if (hasAccess) {
          const { data } = await api.get("/accounts/me/"); // без skipAuthRefresh
          setUser(data);
          return;
        }
        // access нет — пробуем cookie-refresh
        try {
          const r = await api.post("/accounts/token/refresh/", {});
          const newAccess = r.data?.access;
          if (newAccess) {
            localStorage.setItem("access", newAccess);
            api.defaults.headers.common.Authorization = `Bearer ${newAccess}`;
            const { data } = await api.get("/accounts/me/");
            setUser(data);
            return;
          }
        } catch {console.log("catch refresh");}
        setUser(null);
      } catch {
        setUser(null);
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  const login = async ({ username, password }) => {
    try {
      setLoggedOut(false); // разрешаем рефреши
      delete api.defaults.headers.common.Authorization;
      localStorage.removeItem("access");

      const { data } = await api.post("/accounts/login/", { username, password });
      if (data?.access) {
        localStorage.setItem("access", data.access);
        api.defaults.headers.common.Authorization = `Bearer ${data.access}`;
      }
      if (data?.user) setUser(data.user);
      return { success: true, user: data.user };
    } catch (e) {
      return { success: false, error: e.response?.data || "Login failed" };
    }
  };

  const logout = async () => {
    try { await api.post("/accounts/logout/"); } catch {
      console.log('catch logout');
    }
    localStorage.removeItem("access");
    delete api.defaults.headers.common.Authorization;
    setLoggedOut(true);
    setUser(null);
  };

  const updateUser = (patch) => setUser((u) => (u ? { ...u, ...patch } : u));

  return (
    <AuthContext.Provider value={{ user, loading, login, logout, updateUser, roleHome }}>
      {children}
    </AuthContext.Provider>
  );
}

export default AuthProvider;