import React, { useState } from 'react';
import { View, Text, TouchableOpacity, StyleSheet, SafeAreaView } from 'react-native';
import { AuthScreen } from '../screens/AuthScreen';
import { CatalogScreen } from '../screens/CatalogScreen';
import { BookingScreen } from '../screens/BookingScreen';
import { TrackingScreen } from '../screens/TrackingScreen';
import { SparePart, Appointment } from '../../types';

interface AppNavigatorProps {
  initialItems: SparePart[];
  ruleDescription: string;
}

export const AppNavigator: React.FC<AppNavigatorProps> = ({ initialItems, ruleDescription }) => {
  const [activeTab, setActiveTab] = useState<'catalog' | 'booking' | 'tracking' | 'auth'>('catalog');
  const [selectedItem, setSelectedItem] = useState<SparePart | null>(initialItems[0] || null);
  const [orders, setOrders] = useState<Appointment[]>([
    {
      id: 'ORD_INIT01',
      item_id: initialItems[0]?.id || 'item_001',
      scheduled_time: '2026-10-20T10:00:00Z',
      status: 'CONFIRMED',
      total_amount: initialItems[0]?.price || 150000.0,
      notes: 'Đơn hàng mẫu khởi tạo',
    },
  ]);
  const [userToken, setUserToken] = useState<string | null>('mock_token_jwt');

  const handleSelectItem = (item: SparePart) => {
    setSelectedItem(item);
    setActiveTab('booking');
  };

  const handleConfirmBooking = (itemId: string, slot: string, notes: string) => {
    const newOrder: Appointment = {
      id: `ORD_${Math.random().toString(36).substring(2, 8).toUpperCase()}`,
      item_id: itemId,
      scheduled_time: slot,
      status: 'CONFIRMED',
      total_amount: selectedItem ? selectedItem.price : 150000.0,
      notes,
    };
    setOrders([newOrder, ...orders]);
    setActiveTab('tracking');
  };

  return (
    <SafeAreaView style={styles.safeArea}>
      <View style={styles.container}>
        {activeTab === 'auth' && <AuthScreen onLoginSuccess={(token) => { setUserToken(token); setActiveTab('catalog'); }} />}
        {activeTab === 'catalog' && <CatalogScreen items={initialItems} onSelectItem={handleSelectItem} />}
        {activeTab === 'booking' && (
          <BookingScreen
            selectedItem={selectedItem}
            ruleDescription={ruleDescription}
            onConfirmBooking={handleConfirmBooking}
            onCancel={() => setActiveTab('catalog')}
          />
        )}
        {activeTab === 'tracking' && <TrackingScreen orders={orders} />}

        <View style={styles.tabBar}>
          <TouchableOpacity style={[styles.tabItem, activeTab === 'catalog' && styles.tabItemActive]} onPress={() => setActiveTab('catalog')}>
            <Text style={[styles.tabText, activeTab === 'catalog' && styles.tabTextActive]}>Danh Mục</Text>
          </TouchableOpacity>
          <TouchableOpacity style={[styles.tabItem, activeTab === 'booking' && styles.tabItemActive]} onPress={() => setActiveTab('booking')}>
            <Text style={[styles.tabText, activeTab === 'booking' && styles.tabTextActive]}>Đặt Lịch</Text>
          </TouchableOpacity>
          <TouchableOpacity style={[styles.tabItem, activeTab === 'tracking' && styles.tabItemActive]} onPress={() => setActiveTab('tracking')}>
            <Text style={[styles.tabText, activeTab === 'tracking' && styles.tabTextActive]}>Tiến Độ</Text>
          </TouchableOpacity>
          <TouchableOpacity style={[styles.tabItem, activeTab === 'auth' && styles.tabItemActive]} onPress={() => setActiveTab('auth')}>
            <Text style={[styles.tabText, activeTab === 'auth' && styles.tabTextActive]}>{userToken ? 'Tài Khoản' : 'Đăng Nhập'}</Text>
          </TouchableOpacity>
        </View>
      </View>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  safeArea: { flex: 1, backgroundColor: '#FFFFFF' },
  container: { flex: 1 },
  tabBar: { flexDirection: 'row', height: 60, borderTopWidth: 1, borderColor: '#E2E8F0', backgroundColor: '#FFFFFF' },
  tabItem: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  tabItemActive: { borderTopWidth: 2, borderColor: '#0284C7' },
  tabText: { fontSize: 13, color: '#64748B', fontWeight: '500' },
  tabTextActive: { color: '#0284C7', fontWeight: 'bold' },
});
