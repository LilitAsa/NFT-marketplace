import { useContext } from "react";
import { useNavigate } from "react-router-dom";
import LoginPage from "../../pages/Login.jsx";
import { AuthContext } from "../../context/AuthContext";

export default function LoginWithRedirect() {
  const { roleHome } = useContext(AuthContext);
  const navigate = useNavigate();

  return (
    <LoginPage onSuccess={(user) => navigate(roleHome(user), { replace: true })} />
  );
}
