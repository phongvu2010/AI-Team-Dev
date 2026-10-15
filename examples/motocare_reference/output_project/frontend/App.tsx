import React from 'react';
import { AppNavigator } from './src/navigation/AppNavigator';
import { SparePart } from './types';

const defaultCatalog: SparePart[] = [
  { id: 'item_001', name: 'Phụ tùng & Dịch vụ Sửa chữa Xe Tiêu chuẩn', price: 150000.0, stock_quantity: 50, is_active: true },
  { id: 'item_002', name: 'Phụ tùng & Dịch vụ Sửa chữa Xe Cao cấp', price: 225000.0, stock_quantity: 30, is_active: true }
];

export default function App() {
  return <AppNavigator initialItems={defaultCatalog} ruleDescription="Giới hạn tối đa 3 xe mỗi khung giờ (BR-01)" />;
}
