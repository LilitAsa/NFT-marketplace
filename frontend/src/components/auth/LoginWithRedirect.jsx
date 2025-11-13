import { useContext } from "react";
import { useNavigate } from "react-router-dom";
import LoginPage from "../../pages/Login.jsx";
import { AuthContext } from "../../context/AuthContext";
import { login } from "../../api/auth.js";

export default function LoginWithRedirect() {
  const { roleHome } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleLogin = async (form) => {
    const res = await login(form);
    if (res?.success) navigate(roleHome(res.user), { replace: true });
  };

  return (
    <LoginPage onSuccess={(handleLogin, { replace: true })} />
  );
}
