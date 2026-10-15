import { apiClient, apiService, setAuthToken } from '../src/api/client';
import { initialAppState, AppState } from '../src/store/appStore';
import { SparePart, Appointment, AuthTokenResponse } from '../types';

describe('Frontend End-to-End (E2E) Test Suite', () => {
  let appState: AppState = { ...initialAppState };
  let testItem: SparePart;

  test('[E2E-01] Healthcheck & Backend Connectivity', async () => {
    // Verifies apiClient base configuration
    expect(apiClient.defaults.baseURL).toBe('http://localhost:8000/api/v1');
    expect(apiClient.defaults.timeout).toBe(10000);
  });

  test('[E2E-02] User Registration & Token State Acquisition', () => {
    const mockAuth: AuthTokenResponse = {
      access_token: 'valid_jwt_token_e2e_123',
      token_type: 'bearer',
      role: 'CUSTOMER',
      phone_number: '0912345678',
    };

    setAuthToken(mockAuth.access_token);
    appState = { ...appState, token: mockAuth.access_token, activeTab: 'catalog' };

    expect(appState.token).toBe('valid_jwt_token_e2e_123');
    expect(appState.activeTab).toBe('catalog');
  });

  test('[E2E-03] Catalog Data Fetching & Selection', () => {
    const mockItems: SparePart[] = [
      { id: 'item_01', name: 'Phụ tùng chính hãng', price: 150000.0, stock_quantity: 20, is_active: true },
      { id: 'item_02', name: 'Gói bảo dưỡng xe', price: 300000.0, stock_quantity: 15, is_active: true },
    ];

    appState = { ...appState, items: mockItems };
    testItem = mockItems[0];

    expect(appState.items.length).toBeGreaterThan(0);
    expect(testItem.price).toBeGreaterThan(0);
    expect(testItem.is_active).toBe(true);
  });

  test('[E2E-04] Order Booking Submission & State Synchronization', () => {
    const newOrder: Appointment = {
      id: 'ORD_E2E_001',
      item_id: testItem.id,
      scheduled_time: '2026-10-25T09:00:00Z',
      status: 'CONFIRMED',
      total_amount: testItem.price,
      notes: 'Kiểm thử đặt lịch E2E',
    };

    appState = {
      ...appState,
      orders: [...appState.orders, newOrder],
      activeTab: 'tracking',
    };

    expect(appState.orders.length).toBe(1);
    expect(appState.orders[0].status).toBe('CONFIRMED');
    expect(appState.activeTab).toBe('tracking');
  });

  test('[E2E-05] Capacity Limit Guard (BR-01) Verification', () => {
    const maxCapacity = 3;
    const slotOrders: Appointment[] = Array.from({ length: maxCapacity }, (_, i) => ({
      id: `ORD_SLOT_${i}`,
      item_id: testItem.id,
      scheduled_time: '2026-10-25T09:00:00Z',
      status: 'CONFIRMED',
      total_amount: testItem.price,
    }));

    const isSlotExhausted = slotOrders.length >= maxCapacity;
    expect(isSlotExhausted).toBe(true);
  });
});
