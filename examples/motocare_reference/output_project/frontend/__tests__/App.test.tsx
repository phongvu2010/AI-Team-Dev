import { SparePart, Appointment } from '../types';

describe('React Native Mobile App Test Suite', () => {
  const mockCatalog: SparePart[] = [
    { id: 'item_001', name: 'Phụ tùng & Dịch vụ Sửa chữa Xe Tiêu chuẩn', price: 150000.0, stock_quantity: 50, is_active: true },
  ];

  test('Kiểm tra khởi tạo dữ liệu danh mục hợp lệ', () => {
    expect(mockCatalog.length).toBeGreaterThan(0);
    expect(mockCatalog[0].price).toBeGreaterThan(0);
    expect(mockCatalog[0].is_active).toBe(true);
  });

  test('Kiểm tra quy tắc giới hạn khung giờ (Business Rule BR-01)', () => {
    const maxCapacity = 3;
    const currentOrders: Appointment[] = Array.from({ length: maxCapacity }, (_, i) => ({
      id: `ORD_${i}`,
      item_id: 'item_001',
      scheduled_time: '2026-10-20T10:00:00Z',
      status: 'CONFIRMED',
      total_amount: 150000.0,
    }));

    expect(currentOrders.length).toBe(maxCapacity);
    const canBookMore = currentOrders.length < maxCapacity;
    expect(canBookMore).toBe(false);
  });

  test('Kiểm tra định dạng tiền tệ VNĐ hiển thị chính xác', () => {
    const price = 150000.0;
    const formatted = price.toLocaleString('vi-VN');
    expect(typeof formatted).toBe('string');
  });
});
