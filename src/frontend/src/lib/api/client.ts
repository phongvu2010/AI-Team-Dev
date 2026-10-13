/**
 * Typed HTTP Client for communicating with the FastAPI Backend (`frontend/src/lib/api/client.ts`).
 * Supports seamless toggling between Wave 1 Mock Fixtures and Wave 2 Live Backend,
 * with Next.js 15 / React 19 Client Cache Invalidation safeguards and automated port/network alignment.
 */

/**
 * Cross-framework helper to read environment variables across Next.js, Vite, and React Native (Expo).
 */
function getEnvVar(key: "API_URL" | "USE_MOCKS"): string | undefined {
  // 1. Expo (React Native)
  if (typeof process !== "undefined" && process.env) {
    if (key === "API_URL" && process.env.EXPO_PUBLIC_API_URL) {
      return process.env.EXPO_PUBLIC_API_URL;
    }
    if (key === "USE_MOCKS" && process.env.EXPO_PUBLIC_USE_MOCKS) {
      return process.env.EXPO_PUBLIC_USE_MOCKS;
    }
  }

  // 2. Vite (Browser SPA)
  try {
    // @ts-expect-error import.meta is available in Vite environments
    if (typeof import.meta !== "undefined" && import.meta.env) {
      // @ts-expect-error Vite env lookup
      const viteVal = import.meta.env[`VITE_${key}`];
      if (typeof viteVal === "string") return viteVal;
    }
  } catch {
    // import.meta not available
  }

  // 3. Next.js / Node.js
  if (typeof process !== "undefined" && process.env) {
    if (key === "API_URL") {
      return process.env.INTERNAL_API_URL ?? process.env.NEXT_PUBLIC_API_URL;
    }
    if (key === "USE_MOCKS") {
      return process.env.NEXT_PUBLIC_USE_MOCKS;
    }
  }

  return undefined;
}

/**
 * Dynamically resolves the API Base URL:
 * - Next.js: uses INTERNAL_API_URL (SSR) or NEXT_PUBLIC_API_URL (Browser).
 * - Vite: uses VITE_API_URL.
 * - React Native (Expo): uses EXPO_PUBLIC_API_URL.
 * - Fallback: http://localhost:8000
 */
export function getApiBaseUrl(): string {
  const resolved = getEnvVar("API_URL");
  if (resolved) return resolved;

  if (typeof window === "undefined") {
    return "http://127.0.0.1:8000";
  }
  return "http://localhost:8000";
}

/**
 * Returns true if mock mode is explicitly enabled via USE_MOCKS=true (NEXT_PUBLIC / VITE / EXPO).
 * Defaults to false (Live Backend API mode).
 */
export function isMockMode(): boolean {
  return getEnvVar("USE_MOCKS") === "true";
}

export class ApiError extends Error {
  constructor(
    public status: number,
    public detail: string,
  ) {
    super(detail);
    this.name = "ApiError";
  }
}

export interface ApiRequestOptions extends RequestInit {
  mockData?: unknown;
  /** Force cache busting / bypass Next.js 15 fetch and client router cache */
  invalidateCache?: boolean;
}

/**
 * Diagnostics & Network alignment interface
 */
export interface HealthStatus {
  ok: boolean;
  status: number;
  url: string;
  data?: unknown;
  error?: string;
}

/**
 * Utility to clear any persisted client-side cache, localStorage, sessionStorage,
 * and browser CacheStorage when switching between Mock and Live API modes.
 */
export async function clearClientApiCache(): Promise<void> {
  if (typeof window !== "undefined") {
    try {
      // 1. Clear session and local storage keys associated with API responses
      const clearStorage = (storage?: Storage) => {
        if (!storage) return;
        const keysToRemove: string[] = [];
        for (let i = 0; i < storage.length; i++) {
          const key = storage.key(i);
          if (key && (key.startsWith("api_") || key.startsWith("cache_") || key.startsWith("mock_"))) {
            keysToRemove.push(key);
          }
        }
        keysToRemove.forEach((k) => storage.removeItem(k));
      };

      if (typeof sessionStorage !== "undefined") clearStorage(sessionStorage);
      if (typeof localStorage !== "undefined") clearStorage(localStorage);

      // 2. Clear Browser CacheStorage if supported
      if ("caches" in window) {
        const cacheNames = await window.caches.keys();
        await Promise.all(
          cacheNames
            .filter((name) => name.includes("api") || name.includes("fetch"))
            .map((name) => window.caches.delete(name)),
        );
      }
    } catch {
      // Ignore storage errors in restricted iframe/sandbox environments
    }
  }
}

/**
 * Check backend API health and connectivity on configured port.
 */
export async function checkApiHealth(): Promise<HealthStatus> {
  const baseUrl = getApiBaseUrl();
  try {
    const res = await fetch(`${baseUrl}/health`, {
      cache: "no-store",
      headers: {
        "Cache-Control": "no-cache, no-store, must-revalidate",
        Pragma: "no-cache",
      },
    });
    if (res.ok) {
      const data = await res.json();
      return { ok: true, status: res.status, url: baseUrl, data };
    }
    return { ok: false, status: res.status, url: baseUrl, error: `HTTP ${res.status}` };
  } catch (err) {
    return {
      ok: false,
      status: 0,
      url: baseUrl,
      error: err instanceof Error ? err.message : String(err),
    };
  }
}

/**
 * Typed API request wrapper with built-in mock fallback support and Next.js 15 cache invalidation.
 */
export async function apiRequest<T>(
  endpoint: string,
  options?: ApiRequestOptions,
): Promise<T> {
  // Wave 1 Mock Interception: If mock mode is enabled and mockData is provided, return it directly
  if (isMockMode() && options?.mockData !== undefined) {
    return options.mockData as T;
  }

  const { mockData: _, invalidateCache, ...fetchOptions } = options ?? {};

  // Next.js 15 Cache Invalidation: Default to 'no-store' in live mode to avoid stale mock or stale data
  const cacheStrategy: RequestCache =
    fetchOptions.cache ?? (invalidateCache || !isMockMode() ? "no-store" : "default");

  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...((fetchOptions.headers as Record<string, string>) ?? {}),
  };

  if (invalidateCache || !isMockMode()) {
    headers["Cache-Control"] = "no-cache, no-store, must-revalidate";
    headers["Pragma"] = "no-cache";
    headers["Expires"] = "0";
  }

  // If explicit cache bust requested, append timestamp query parameter
  let targetUrl = `${getApiBaseUrl()}${endpoint}`;
  if (invalidateCache) {
    const separator = targetUrl.includes("?") ? "&" : "?";
    targetUrl = `${targetUrl}${separator}_t=${Date.now()}`;
  }

  const response = await fetch(targetUrl, {
    ...fetchOptions,
    cache: cacheStrategy,
    headers,
  });

  if (!response.ok) {
    let detail = `HTTP Error ${response.status}`;
    try {
      const errBody = (await response.json()) as { detail?: string };
      if (typeof errBody.detail === "string") {
        detail = errBody.detail;
      }
    } catch {
      // Fallback to status message if body is not JSON
    }
    throw new ApiError(response.status, detail);
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return (await response.json()) as T;
}
