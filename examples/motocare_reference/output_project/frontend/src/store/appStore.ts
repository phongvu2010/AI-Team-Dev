import { SparePart, Appointment } from '../../types';

export interface AppState {
  token: string | null;
  items: SparePart[];
  orders: Appointment[];
  activeTab: 'catalog' | 'booking' | 'tracking' | 'auth';
}

export const initialAppState: AppState = {
  token: null,
  items: [],
  orders: [],
  activeTab: 'catalog',
};
