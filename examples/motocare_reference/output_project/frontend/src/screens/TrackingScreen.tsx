import React from 'react';
import { View, Text, FlatList, StyleSheet } from 'react-native';
import { Appointment } from '../../types';

interface TrackingScreenProps {
  orders: Appointment[];
}

export const TrackingScreen: React.FC<TrackingScreenProps> = ({ orders }) => {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Tiến Độ Đơn Hàng Theo Thời Gian Thực</Text>
      {orders.length === 0 ? (
        <View style={styles.emptyContainer}>
          <Text style={styles.emptyText}>Chưa có đơn hàng nào.</Text>
        </View>
      ) : (
        <FlatList
          data={orders}
          keyExtractor={(item) => item.id}
          renderItem={({ item }) => (
            <View style={styles.card}>
              <View style={styles.cardHeader}>
                <Text style={styles.orderId}>Mã: {item.id}</Text>
                <View style={styles.badge}>
                  <Text style={styles.badgeText}>{item.status}</Text>
                </View>
              </View>
              <Text style={styles.time}>Khung giờ: {item.scheduled_time}</Text>
              <Text style={styles.amount}>Tổng tiền: {item.total_amount.toLocaleString('vi-VN')} VNĐ</Text>
              {item.notes ? <Text style={styles.notes}>Ghi chú: {item.notes}</Text> : null}
            </View>
          )}
        />
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, padding: 16, backgroundColor: '#F8FAFC' },
  title: { fontSize: 20, fontWeight: 'bold', marginBottom: 16, color: '#0F172A' },
  emptyContainer: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  emptyText: { fontSize: 16, color: '#94A3B8' },
  card: { backgroundColor: '#FFFFFF', padding: 14, borderRadius: 10, marginBottom: 10, elevation: 1 },
  cardHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 6 },
  orderId: { fontSize: 15, fontWeight: 'bold', color: '#1E293B' },
  badge: { backgroundColor: '#DCFCE7', paddingHorizontal: 8, paddingVertical: 4, borderRadius: 4 },
  badgeText: { fontSize: 12, fontWeight: 'bold', color: '#166534' },
  time: { fontSize: 13, color: '#64748B', marginBottom: 4 },
  amount: { fontSize: 14, fontWeight: 'bold', color: '#059669' },
  notes: { fontSize: 12, color: '#64748B', marginTop: 4, fontStyle: 'italic' },
});
