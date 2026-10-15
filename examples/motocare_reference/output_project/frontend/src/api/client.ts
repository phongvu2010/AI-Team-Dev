import axios from 'axios';
import { SparePart, Appointment, AuthTokenResponse } from '../../types';

const API_BASE_URL = 'http://localhost:8000/api/v1';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: { 'Content-Type': 'application/json' },
});

export const setAuthToken = (token: string | null) => {
  if (token) {
    apiClient.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  } else {
    delete apiClient.defaults.headers.common['Authorization'];
  }
};

export const apiService = {
  async getCatalog(): Promise<SparePart[]> {
    const res = await apiClient.get<SparePart[]>('/catalog');
    return res.data;
  },
  async getOrders(): Promise<Appointment[]> {
    const res = await apiClient.get<Appointment[]>('/orders');
    return res.data;
  },
  async createOrder(itemId: string, scheduledTime: string, notes?: string): Promise<Appointment> {
    const res = await apiClient.post<Appointment>('/orders', {
      item_id: itemId,
      scheduled_time: scheduledTime,
      notes,
    });
    return res.data;
  },
  async login(phone: string, password: string): Promise<AuthTokenResponse> {
    const res = await apiClient.post<AuthTokenResponse>('/auth/login', { phone_number: phone, password });
    return res.data;
  },
  async healthCheck(): Promise<{ status: string }> {
    const res = await apiClient.get('/health');
    return res.data;
  },
};
