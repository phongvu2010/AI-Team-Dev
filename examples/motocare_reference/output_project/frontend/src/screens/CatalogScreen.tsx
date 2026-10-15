import React from 'react';
import { View, Text, FlatList, TouchableOpacity, StyleSheet } from 'react-native';
import { SparePart } from '../../types';

interface CatalogScreenProps {
  items: SparePart[];
  onSelectItem: (item: SparePart) => void;
}

export const CatalogScreen: React.FC<CatalogScreenProps> = ({ items, onSelectItem }) => {
  return (
    <View style={styles.container}>
      <Text style={styles.headerTitle}>Bảng Giá & Danh Mục Phụ tùng & Dịch vụ Sửa chữa Xe</Text>
      <FlatList
        data={items}
        keyExtractor={(item) => item.id}
        renderItem={({ item }) => (
          <View style={styles.card}>
            <View style={styles.info}>
              <Text style={styles.name}>{item.name}</Text>
              <Text style={styles.stock}>Còn lại: {item.stock_quantity} mục</Text>
              <Text style={styles.price}>{item.price.toLocaleString('vi-VN')} VNĐ</Text>
            </View>
            <TouchableOpacity style={styles.selectBtn} onPress={() => onSelectItem(item)}>
              <Text style={styles.btnText}>Đặt lịch</Text>
            </TouchableOpacity>
          </View>
        )}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, padding: 16, backgroundColor: '#F8FAFC' },
  headerTitle: { fontSize: 20, fontWeight: 'bold', marginBottom: 16, color: '#0F172A' },
  card: { backgroundColor: '#FFFFFF', padding: 16, borderRadius: 12, marginBottom: 12, elevation: 2, flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' },
  info: { flex: 1 },
  name: { fontSize: 16, fontWeight: '600', color: '#1E293B' },
  stock: { fontSize: 12, color: '#64748B', marginTop: 4 },
  price: { fontSize: 15, color: '#059669', fontWeight: 'bold', marginTop: 4 },
  selectBtn: { backgroundColor: '#0284C7', paddingHorizontal: 14, paddingVertical: 8, borderRadius: 6 },
  btnText: { color: '#FFFFFF', fontWeight: 'bold', fontSize: 13 },
});
