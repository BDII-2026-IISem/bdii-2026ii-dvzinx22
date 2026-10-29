import { Client } from './client.model';
import { Product } from './product.model';

export interface ProductSale {
  id?: number;
  productId: number;
  product?: Product;
  productName?: string;
  quantity: number;
  unitPrice?: number;
  subtotal?: number;
}

export interface Sale {
  id?: number;
  clientId: number;
  client?: Client;
  clientName?: string;
  total?: number;
  status?: string;
  items?: ProductSale[];
  createdAt?: string;
  updatedAt?: string;
}

export interface CreateSaleItemPayload {
  productId: number;
  quantity: number;
}

export interface CreateSalePayload {
  clientId: number;
  items: CreateSaleItemPayload[];
}

