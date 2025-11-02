import axios from "axios";
export const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api",
  withCredentials: true, // нужно для cookie
});

api.interceptors.request.use((config) => {
  const access = localStorage.getItem("access");
  if (access) config.headers.Authorization = `Bearer ${access}`;
  return config;
});

let refreshing = null;
api.interceptors.response.use(
  r => r,
  async (err) => {
    const orig = err.config;
    if (err.response?.status === 401 && !orig._retry) {
      try {
        orig._retry = true;
        refreshing ||= api.post("/accounts/token/refresh/", {}).then(res => {
          localStorage.setItem("access", res.data.access);
          return res.data.access;
        }).finally(() => { refreshing = null; });
        const token = await refreshing;
        orig.headers = { ...orig.headers, Authorization: `Bearer ${token}` };
        return api(orig);
      } catch {
        localStorage.removeItem("access");
        throw err;
      }
    }
    throw err;
  }
);
