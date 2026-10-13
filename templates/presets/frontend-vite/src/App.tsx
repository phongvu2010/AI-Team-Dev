import React, { useEffect, useState } from "react";
import { apiRequest, ApiError, isMockMode } from "@/lib/api/client";
import { BaseEntity } from "@/types";
import { Activity, AlertCircle, CheckCircle2, RefreshCw } from "lucide-react";

interface HealthData {
  status: string;
  service: string;
  version: string;
  database?: string;
}

export default function App() {
  const [data, setData] = useState<HealthData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchHealth = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await apiRequest<HealthData>("/health", {
        mockData: {
          status: "ok",
          service: "Vite SPA Mock Client",
          version: "1.0.0",
          database: "healthy (mock)",
        },
      });
      setData(res);
    } catch (err) {
      if (err instanceof ApiError) {
        setError(`API Error (${err.status}): ${err.detail}`);
      } else {
        setError(err instanceof Error ? err.message : "Failed to connect to backend");
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHealth();
  }, []);

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col justify-between p-6">
      <header className="max-w-4xl mx-auto w-full flex items-center justify-between pb-6 border-b border-slate-200">
        <div className="flex items-center gap-3">
          <div className="h-10 w-10 rounded-xl bg-indigo-600 flex items-center justify-center text-white shadow-sm">
            <Activity className="h-5 w-5" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-slate-900 tracking-tight">AI Team Dev — Vite SPA</h1>
            <p className="text-xs text-slate-500">React + Vite + Tailwind CSS</p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <span
            className={`px-2.5 py-1 text-xs rounded-full font-medium ${
              isMockMode()
                ? "bg-amber-100 text-amber-800"
                : "bg-emerald-100 text-emerald-800"
            }`}
          >
            {isMockMode() ? "Mock Mode" : "Live Backend"}
          </span>
          <button
            onClick={fetchHealth}
            disabled={loading}
            className="p-2 rounded-lg text-slate-600 hover:bg-slate-200 transition-colors"
            title="Refresh"
          >
            <RefreshCw className={`h-4 w-4 ${loading ? "animate-spin" : ""}`} />
          </button>
        </div>
      </header>

      <main className="max-w-4xl mx-auto w-full my-12 flex-1">
        {/* 1. Loading State */}
        {loading && (
          <div className="rounded-2xl border border-slate-200 bg-white p-8 animate-pulse shadow-sm">
            <div className="h-6 w-48 bg-slate-200 rounded mb-4" />
            <div className="h-4 w-full bg-slate-100 rounded mb-2" />
            <div className="h-4 w-3/4 bg-slate-100 rounded" />
          </div>
        )}

        {/* 2. Error State */}
        {!loading && error && (
          <div className="rounded-2xl border border-rose-200 bg-rose-50 p-6 text-rose-900 shadow-sm">
            <div className="flex items-center gap-3 mb-2">
              <AlertCircle className="h-5 w-5 text-rose-600" />
              <h3 className="font-semibold text-sm">Connection Warning</h3>
            </div>
            <p className="text-xs text-rose-700 mb-4">{error}</p>
            <button
              onClick={fetchHealth}
              className="px-4 py-2 bg-rose-600 text-white rounded-lg text-xs font-semibold hover:bg-rose-700 transition-colors"
            >
              Retry Connection
            </button>
          </div>
        )}

        {/* 3. Empty State */}
        {!loading && !error && !data && (
          <div className="rounded-2xl border border-dashed border-slate-300 p-12 text-center">
            <h3 className="text-base font-semibold text-slate-900">No Data Available</h3>
            <p className="mt-1 text-xs text-slate-500">Click refresh to fetch backend status.</p>
          </div>
        )}

        {/* 4. Success State */}
        {!loading && !error && data && (
          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
            <div className="flex items-center gap-2 mb-4 text-emerald-600">
              <CheckCircle2 className="h-5 w-5" />
              <h3 className="font-semibold text-sm text-slate-900">Backend System Healthy</h3>
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs">
              <div className="p-3 bg-slate-50 rounded-xl">
                <span className="text-slate-500 block mb-1">Service</span>
                <span className="font-semibold text-slate-800">{data.service}</span>
              </div>
              <div className="p-3 bg-slate-50 rounded-xl">
                <span className="text-slate-500 block mb-1">Version</span>
                <span className="font-semibold text-slate-800">{data.version}</span>
              </div>
              <div className="p-3 bg-slate-50 rounded-xl">
                <span className="text-slate-500 block mb-1">Database</span>
                <span className="font-semibold text-slate-800">{data.database ?? "connected"}</span>
              </div>
            </div>
          </div>
        )}
      </main>

      <footer className="max-w-4xl mx-auto w-full text-center text-xs text-slate-400 pt-6 border-t border-slate-200">
        AI Team Dev • React Vite Preset • Antigravity 2.0
      </footer>
    </div>
  );
}
