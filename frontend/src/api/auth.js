import { api } from "./client";

export async function login(username, password) {
  // твой эндпоинт: /api/accounts/login/ -> SimpleJWT (access, refresh)
  const { data } = await api.post("/accounts/login/", { username, password });
  // сохраним токены ДО навигации
  localStorage.setItem("access", data.access);
  return data;
}

export async function logout() {
  localStorage.removeItem("access");
}

export async function fetchMe() {
  const { data } = await api.get("/accounts/me/");
  return data; // { id, username, email }
}
export async function register(username, email, password) {
  const { data } = await api.post("/accounts/register/", {
    username,
    email,
    password,
  });
  return data;
}