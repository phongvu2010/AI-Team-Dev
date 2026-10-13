/**
 * Typed HTTP Client for React Native Expo Mobile App (`src/mobile/src/lib/api/client.ts`).
 * Automatically resolves localhost vs 10.0.2.2 (Android Emulator).
 */

import { Platform } from "react-native";

export function getApiBaseUrl(): string {
  // 1. Expo Public Environment Variable (set in .env as EXPO_PUBLIC_API_URL)
  if (process.env.EXPO_PUBLIC_API_URL) {
    return process.env.EXPO_PUBLIC_API_URL;
  }

  // 2. Android Emulator loopback is 10.0.2.2 instead of localhost
  if (Platform.OS === "android") {
    return "http://10.0.2.2:8000";
  }

  // 3. iOS Simulator & Web use localhost
  return "http://localhost:8000";
}

export function isMockMode(): boolean {
  return process.env.EXPO_PUBLIC_USE_MOCKS === "true";
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
}

export async function apiRequest<T>(
  endpoint: string,
  options?: ApiRequestOptions,
): Promise<T> {
  if (isMockMode() && options?.mockData !== undefined) {
    return options.mockData as T;
  }

  const { mockData: _, ...fetchOptions } = options ?? {};

  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...((fetchOptions.headers as Record<string, string>) ?? {}),
  };

  const targetUrl = `${getApiBaseUrl()}${endpoint}`;

  const response = await fetch(targetUrl, {
    ...fetchOptions,
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
      // Non-JSON response
    }
    throw new ApiError(response.status, detail);
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return (await response.json()) as T;
}
