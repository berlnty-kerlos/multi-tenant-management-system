import React, { createContext, useContext, useState, useEffect } from "react";
import { api, API_URL } from "../../lib/api";

const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [token, setToken] = useState(localStorage.getItem("token") || null);
  const [user, setUser] = useState(null); 
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const savedToken = localStorage.getItem("token");
    if (savedToken) {
      setToken(savedToken);
    }
    setLoading(false);
  }, []);

  async function login(credentials) {
    const data = await api.post("/auth/login", credentials);
    localStorage.setItem("token", data.access_token);
    localStorage.setItem("refresh_token", JSON.stringify(data.refresh_token));
    localStorage.setItem("token_type", JSON.stringify(data.token_type));
    setToken(data.access_token);
  
  }

  async function registerAccount(credentials) {
    const data = await api.post("/auth/register", credentials);
    localStorage.setItem("token", data.access_token);
    localStorage.setItem("refresh_token", JSON.stringify(data.refresh_token));
    localStorage.setItem("token_type", JSON.stringify(data.token_type));
    setToken(data.access_token);

  }

  function logout() {
    localStorage.removeItem("token");
    setToken(null);
  }

  return (
    <AuthContext.Provider value={{ token, loading, login, register: registerAccount, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
