import React, { useEffect, useState } from "react";
import { View, Text, Pressable, ActivityIndicator, ScrollView } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import { apiRequest, ApiError, isMockMode } from "@/lib/api/client";

interface HealthData {
  status: string;
  service: string;
  version: string;
  database?: string;
}

export default function MobileHomeScreen() {
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
          service: "React Native Mobile Client",
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
    <SafeAreaView className="flex-1 bg-slate-900">
      <ScrollView contentContainerClassName="p-6">
        {/* Header */}
        <View className="flex-row items-center justify-between pb-6 border-b border-slate-800">
          <View>
            <Text className="text-xl font-bold text-white tracking-tight">AI Team Dev</Text>
            <Text className="text-xs text-slate-400">React Native • Expo • NativeWind</Text>
          </View>
          <View className="flex-row items-center">
            <View
              className={`px-3 py-1 rounded-full ${
                isMockMode() ? "bg-amber-900/60" : "bg-emerald-900/60"
              }`}
            >
              <Text
                className={`text-xs font-semibold ${
                  isMockMode() ? "text-amber-300" : "text-emerald-300"
                }`}
              >
                {isMockMode() ? "Mock" : "Live API"}
              </Text>
            </View>
          </View>
        </View>

        {/* Content with 4 UI States */}
        <View className="my-8">
          {/* 1. Loading State */}
          {loading && (
            <View className="rounded-2xl border border-slate-800 bg-slate-800/50 p-8 items-center justify-center">
              <ActivityIndicator size="large" color="#38bdf8" />
              <Text className="text-xs text-slate-400 mt-4">Connecting to FastAPI Backend...</Text>
            </View>
          )}

          {/* 2. Error State */}
          {!loading && error && (
            <View className="rounded-2xl border border-rose-900/50 bg-rose-950/40 p-6">
              <Text className="text-sm font-semibold text-rose-300 mb-1">Connection Issue</Text>
              <Text className="text-xs text-rose-400 mb-4">{error}</Text>
              <Pressable
                onPress={fetchHealth}
                className="bg-rose-600 active:bg-rose-700 py-2.5 px-4 rounded-xl items-center"
              >
                <Text className="text-xs font-semibold text-white">Retry Connection</Text>
              </Pressable>
            </View>
          )}

          {/* 3. Empty State */}
          {!loading && !error && !data && (
            <View className="rounded-2xl border border-dashed border-slate-800 p-8 items-center">
              <Text className="text-sm font-semibold text-slate-400">No Status Available</Text>
              <Pressable onPress={fetchHealth} className="mt-3">
                <Text className="text-xs text-sky-400 font-medium">Tap to refresh</Text>
              </Pressable>
            </View>
          )}

          {/* 4. Success State */}
          {!loading && !error && data && (
            <View className="rounded-2xl border border-slate-800 bg-slate-800/40 p-6">
              <View className="flex-row items-center mb-4">
                <View className="h-2.5 w-2.5 rounded-full bg-emerald-400 mr-2" />
                <Text className="text-sm font-semibold text-emerald-300">Backend Connected</Text>
              </View>

              <View className="space-y-3">
                <View className="p-3 bg-slate-800/80 rounded-xl">
                  <Text className="text-xs text-slate-400">Service</Text>
                  <Text className="text-sm font-semibold text-white mt-0.5">{data.service}</Text>
                </View>
                <View className="p-3 bg-slate-800/80 rounded-xl">
                  <Text className="text-xs text-slate-400">Version</Text>
                  <Text className="text-sm font-semibold text-white mt-0.5">{data.version}</Text>
                </View>
                <View className="p-3 bg-slate-800/80 rounded-xl">
                  <Text className="text-xs text-slate-400">Database Engine</Text>
                  <Text className="text-sm font-semibold text-white mt-0.5">{data.database ?? "connected"}</Text>
                </View>
              </View>

              <Pressable
                onPress={fetchHealth}
                className="mt-6 bg-sky-600 active:bg-sky-700 py-3 rounded-xl items-center shadow-sm"
              >
                <Text className="text-xs font-semibold text-white">Refresh Status</Text>
              </Pressable>
            </View>
          )}
        </View>

        {/* Footer */}
        <View className="pt-6 border-t border-slate-800 items-center">
          <Text className="text-xs text-slate-500">React Native • Tailwind CSS (NativeWind)</Text>
          <Text className="text-[10px] text-slate-600 mt-1">Cross-Platform iOS & Android • Antigravity 2.0</Text>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}
