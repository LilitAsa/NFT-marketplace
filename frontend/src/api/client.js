import axios from "axios";

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000/api",
  withCredentials: true, // чтобы HttpOnly cookie отправлялись
});

// Подкладываем access из LS
api.interceptors.request.use((config) => {
  const url = config.url || "";
  const noAuth =
    url.includes("/accounts/login/") ||
    url.includes("/accounts/token/refresh/");
  if (!noAuth) {
    const access = localStorage.getItem("access");
    if (access) config.headers.Authorization = `Bearer ${access}`;
  }
  return config;
});

let loggedOut = false;
export const setLoggedOut = (v) => { loggedOut = v; };

let refreshing = null;

api.interceptors.response.use(
  (r) => r,
  async (error) => {
    const res = error.response;
    const cfg = error.config || {};

    if (cfg.skipAuthRefresh) throw error;     // Первый /me может запретить авто-рефреш
    if (loggedOut) throw error;               // После logout не реанимируем
    if (!res || res.status !== 401) throw error;

    const isRefreshCall = cfg.url?.includes("/accounts/token/refresh/");
    if (cfg._retry || isRefreshCall) throw error;

    cfg._retry = true;

    try {
      if (!refreshing) {
        refreshing = api.post("/accounts/token/refresh/", {})
          .then((r) => {
            const access = r.data?.access;
            if (!access) throw new Error("No access in refresh response");
            localStorage.setItem("access", access);
            return access;
          })
          .finally(() => { refreshing = null; });
      }
      const newAccess = await refreshing;
      cfg.headers = { ...cfg.headers, Authorization: `Bearer ${newAccess}` };
      return api(cfg);
    } catch (e) {
      console.log(e);
      // refresh не удался — отдаём исходную ошибку 401
      throw error;
    }
  }
);
