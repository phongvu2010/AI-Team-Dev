import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet } from 'react-native';
import { SparePart } from '../../types';

interface BookingScreenProps {
  selectedItem: SparePart | null;
  ruleDescription: string;
  onConfirmBooking: (itemId: string, slot: string, notes: string) => void;
  onCancel: () => void;
}

export const BookingScreen: React.FC<BookingScreenProps> = ({
  selectedItem,
  ruleDescription,
  onConfirmBooking,
  onCancel,
}) => {
  const [slot, setSlot] = useState('2026-10-20T10:00:00Z');
  const [notes, setNotes] = useState('Yêu cầu xử lý kỹ.');

  if (!selectedItem) {
    return (
      <View style={styles.container}>
        <Text style={styles.warning}>Chưa chọn dịch vụ nào. Vui lòng quay lại danh mục!</Text>
        <TouchableOpacity style={styles.cancelBtn} onPress={onCancel}>
          <Text style={styles.cancelText}>Quay lại</Text>
        </TouchableOpacity>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Xác Nhận Đặt Lịch Hẹn</Text>
      <View style={styles.summaryCard}>
        <Text style={styles.label}>Dịch vụ đã chọn:</Text>
        <Text style={styles.value}>{selectedItem.name}</Text>
        <Text style={styles.price}>{selectedItem.price.toLocaleString('vi-VN')} VNĐ</Text>
        <View style={styles.ruleBadge}>
          <Text style={styles.ruleText}>⚠️ {ruleDescription}</Text>
        </View>
      </View>

      <Text style={styles.inputLabel}>Khung giờ (Slot):</Text>
      <TextInput style={styles.input} value={slot} onChangeText={setSlot} />

      <Text style={styles.inputLabel}>Ghi chú:</Text>
      <TextInput style={[styles.input, { height: 70 }]} value={notes} onChangeText={setNotes} multiline />

      <View style={styles.actions}>
        <TouchableOpacity style={styles.cancelBtn} onPress={onCancel}>
          <Text style={styles.cancelText}>Hủy</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.confirmBtn} onPress={() => onConfirmBooking(selectedItem.id, slot, notes)}>
          <Text style={styles.btnText}>Xác nhận</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20, backgroundColor: '#FFFFFF' },
  title: { fontSize: 22, fontWeight: 'bold', marginBottom: 16, color: '#0F172A' },
  warning: { fontSize: 16, color: '#DC2626', marginBottom: 16 },
  summaryCard: { backgroundColor: '#F1F5F9', padding: 14, borderRadius: 8, marginBottom: 16 },
  label: { fontSize: 13, color: '#64748B' },
  value: { fontSize: 16, fontWeight: '600', color: '#0F172A', marginBottom: 4 },
  price: { fontSize: 16, fontWeight: 'bold', color: '#059669', marginBottom: 8 },
  ruleBadge: { backgroundColor: '#FEF3C7', padding: 6, borderRadius: 4 },
  ruleText: { fontSize: 12, color: '#B45309' },
  inputLabel: { fontSize: 14, fontWeight: '600', color: '#334155', marginBottom: 6 },
  input: { borderWidth: 1, borderColor: '#CBD5E1', borderRadius: 8, padding: 10, marginBottom: 14 },
  actions: { flexDirection: 'row', justifyContent: 'space-between', marginTop: 10 },
  cancelBtn: { flex: 1, padding: 12, borderRadius: 8, borderWidth: 1, borderColor: '#94A3B8', alignItems: 'center', marginRight: 8 },
  cancelText: { color: '#475569', fontWeight: 'bold' },
  confirmBtn: { flex: 1, padding: 12, borderRadius: 8, backgroundColor: '#0284C7', alignItems: 'center', marginLeft: 8 },
  btnText: { color: '#FFFFFF', fontWeight: 'bold' },
});
