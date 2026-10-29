export interface Client {
  id?: number;
  identification: string;
  names: string;
  surnames: string;
  email: string;
  phone: string;
  address?: string;
  status?: string;
  createdAt?: string;
  updatedAt?: string;
}

