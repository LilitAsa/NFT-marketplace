import { createContext } from "react";

export const AuthContext = createContext({
  user: null,
  loading: true,
  login: async () => {},
  logout: async () => {},
  updateUser: () => {},
  roleHome: () => "/",
});
