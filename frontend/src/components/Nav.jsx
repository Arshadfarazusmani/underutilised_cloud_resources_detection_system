import React from "react";
import { Link, useNavigate } from "react-router-dom";

export default function Nav() {
  const nav = useNavigate();
  const logout = () => {
    localStorage.removeItem("token");
    nav("/login");
  };

  return (
    <nav className="p-4 bg-gray-900 text-white flex gap-4">
      <Link to="/">Dashboard</Link>
      <Link to="/predict">Predict</Link>
      <button onClick={logout} className="ml-auto text-red-300">
        Logout
      </button>
    </nav>
  );
}
