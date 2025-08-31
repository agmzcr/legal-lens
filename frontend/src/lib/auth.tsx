import { createContext, useContext, useEffect, useState, type ReactNode } from 'react';
import { apiFetch } from './apiFetch';
import toast from 'react-hot-toast';

interface AuthState {
  isAuthenticated: boolean;
  user: any | null;
  isLoading: boolean;
  logout: () => Promise<void>;
  login: (data: { email: string; password: string }) => Promise<void>;
}

const AuthContext = createContext<AuthState | null>(null);

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const [authState, setAuthState] = useState<AuthState>({
    isAuthenticated: false,
    user: null,
    isLoading: true,
    logout: async () => {},
    login: async () => {},
  });

  const handleLogout = async () => {
    localStorage.clear();
    setAuthState({
      isAuthenticated: false,
      user: null,
      isLoading: false,
      logout: handleLogout,
      login: handleLogin,
    });
    toast.success('Sesión cerrada correctamente.');
  };

  const handleLogin = async (data: { email: string; password: string }) => {
    try {
      const loginResponse = await apiFetch.post('/auth/login', data);
      const { access_token, refresh_token } = loginResponse.data;

      localStorage.setItem('access_token', access_token);
      localStorage.setItem('refresh_token', refresh_token);
      
      const userResponse = await apiFetch.get('/users/me'); 
      
      setAuthState({
        isAuthenticated: true,
        user: userResponse.data,
        isLoading: false,
        logout: handleLogout,
        login: handleLogin,
      });
    } catch (error) {
      localStorage.clear();
      setAuthState({
        isAuthenticated: false,
        user: null,
        isLoading: false,
        logout: handleLogout,
        login: handleLogin,
      });
      throw error;
    }
  };

  useEffect(() => {
    const checkAuthStatus = async () => {
      const accessToken = localStorage.getItem('access_token');
      if (!accessToken) {
        setAuthState({
          isAuthenticated: false,
          user: null,
          isLoading: false,
          logout: handleLogout,
          login: handleLogin,
        });
        return;
      }
      try {
        const response = await apiFetch.get('/users/me');
        setAuthState({
          isAuthenticated: true,
          user: response.data,
          isLoading: false,
          logout: handleLogout,
          login: handleLogin,
        });
      } catch (error) {
        localStorage.clear();
        setAuthState({
          isAuthenticated: false,
          user: null,
          isLoading: false,
          logout: handleLogout,
          login: handleLogin,
        });
      }
    };
    checkAuthStatus();
  }, []); 

  return (
    <AuthContext.Provider value={authState}>
      {children}
    </AuthContext.Provider>
  );
}