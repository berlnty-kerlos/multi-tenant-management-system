const API_BASE =
  (typeof import.meta !== "undefined" && import.meta.env?.VITE_API_URL?.replace(/\/$/, "")) ||
  "http://localhost:8000";


export class ApiError extends Error {
  constructor(message, { status, data } = {}) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.data = data;
  }
}

function normalizeEndpoint(endpoint = "") {
  return endpoint.startsWith("/") ? endpoint : `/${endpoint}`;
}

function buildQuery(params) {
  const usp = new URLSearchParams();
  Object.entries(params || {}).forEach(([k, v]) => {
    if (v !== undefined && v !== null) usp.append(k, String(v));
  });
  const qs = usp.toString();
  return qs ? `?${qs}` : "";
}

async function parseResponse(res) {
  if (res.status === 204) return null;
  const text = await res.text();
  if (!text) return null;
  try {
    return JSON.parse(text);
  } catch {
    return text; 
  }
}

/**
 * apiFetch: tiny wrapper around fetch with:
 * - JWT from localStorage
 * - Query params support
 * - JSON/FormData body support
 * - Consistent errors (ApiError)
 *
 * @param {string} endpoint - e.g. "/projects"
 * @param {object} options
 *   - method: 'GET' | 'POST' | ...
 *   - params: object -> query string
 *   - body: object | FormData
 *   - headers: object
 *   - other fetch options...
 */
export async function apiFetch(
  endpoint,
  { method, params, body, headers, ...rest } = {}
) {
  const token = localStorage.getItem("token");

  const url = `${API_BASE}${normalizeEndpoint(endpoint)}${buildQuery(params)}`;

  const finalMethod = method || (body ? "POST" : "GET");

  const isForm = typeof FormData !== "undefined" && body instanceof FormData;

  const finalHeaders = {
    ...(isForm ? {} : { "Content-Type": "application/json" }),
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
    ...(headers || {}),
  };

  const fetchOptions = {
    method: finalMethod,
    headers: finalHeaders,
    ...rest,
  };

  if (body !== undefined && body !== null) {
    fetchOptions.body = isForm ? body : JSON.stringify(body);
  }
  // console.log('api call', url , fetchOptions)
  let res;
  try {
    res = await fetch(url, fetchOptions);
  } catch (networkErr) {
    throw new ApiError("Network error. Please check your connection.", {
      status: 0,
      data: null,
    });
  }

  let data;
  try {
    data = await res.json();
  } catch {
    data = null;
  }

  if (!res.ok) {
    const message =
      (data && (data.detail || data.message || data.error)) ||
      `${res.status} ${res.statusText}` ||
      "API Error";

    throw new ApiError(message, { status: res.status, data });
  }

  return data;
}


export async function refreshToken() {
  const refresh_token = JSON.parse(localStorage.getItem("refresh_token") || "null");

  if (!refresh_token ) return null;

  try {
    const res = await apiFetch("/auth/refresh", {
      method: "POST",
      body: { refresh_token },
    });

   
    localStorage.setItem("token", res.access_token);
    localStorage.setItem("refresh_token", JSON.stringify(res.refresh_token));
    localStorage.setItem("token_type", JSON.stringify(res.token_type));

    return res.access_token;
  } catch (err) {
   
    localStorage.removeItem("token");
    localStorage.removeItem("refresh_token");
    localStorage.removeItem("token_type");
    return null;
  }
}


export async function apiFetchWithRefresh(endpoint, options = {}) {
  try {
    return await apiFetch(endpoint, options);
  } catch (err) {
    if (err.status === 401) {
      const newToken = await refreshToken();
      if (newToken) {
        return await apiFetch(endpoint, options);
      }
    }

    throw err;
  }
}


export const api = {
  get: (endpoint, opts) => apiFetch(endpoint, { ...opts, method: "GET" }),
  post: (endpoint, body, opts) =>
    apiFetch(endpoint, { ...opts, method: "POST", body }),
  put: (endpoint, body, opts) =>
    apiFetch(endpoint, { ...opts, method: "PUT", body }),
  patch: (endpoint, body, opts) =>
    apiFetch(endpoint, { ...opts, method: "PATCH", body }),
  del: (endpoint, opts) => apiFetch(endpoint, { ...opts, method: "DELETE" }),
};

export { apiFetch as apiRequest };
export { API_BASE as API_URL };
