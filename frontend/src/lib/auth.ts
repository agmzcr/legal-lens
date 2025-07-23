/**
 * Check if the user is authenticated.
 */
export function isAuthenticated(): boolean {
  return !!localStorage.getItem('token');
}

/**
 * Log out the current user.
 */
export function logout(): void {
  localStorage.removeItem('token');
}