/**
 * API client: base URL and helpers for auth requests.
 * Uses Vite proxy: /api -> backend (localhost:5000).
 */

const API_BASE = '/api';

function getAuthHeaders() {
  const token = localStorage.getItem('token');
  return token ? { Authorization: `Bearer ${token}` } : {};
}

/**
 * POST /api/auth/register
 * @param {{ email: string, password: string, name: string }} payload
 * @returns {{ access_token: string, user: { id, email, name, created_at } }}
 */
export async function register(payload) {
  const res = await fetch(`${API_BASE}/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    const msg = Array.isArray(data.detail) ? data.detail.map((d) => d.msg || JSON.stringify(d)).join(', ') : (data.detail || 'Registration failed');
    throw new Error(msg);
  }
  return data;
}

/**
 * POST /api/auth/login
 * @param {{ email: string, password: string }} payload
 * @returns {{ access_token: string, user: { id, email, name, created_at } }}
 */
export async function login(payload) {
  const res = await fetch(`${API_BASE}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    const msg = Array.isArray(data.detail) ? data.detail.map((d) => d.msg || JSON.stringify(d)).join(', ') : (data.detail || 'Login failed');
    throw new Error(msg);
  }
  return data;
}

/**
 * GET /api/auth/me - current user (requires token).
 */
export async function getMe() {
  const res = await fetch(`${API_BASE}/auth/me`, {
    headers: getAuthHeaders(),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.detail || 'Not authenticated');
  return data;
}
