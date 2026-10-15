export interface SparePart {
  id: string;
  name: string;
  price: number;
  stock_quantity: number;
  is_active: boolean;
}

export interface Appointment {
  id: string;
  item_id: string;
  scheduled_time: string;
  status: string;
  total_amount: number;
  notes?: string;
}

export interface AuthTokenResponse {
  access_token: string;
  token_type: string;
  role: string;
}
