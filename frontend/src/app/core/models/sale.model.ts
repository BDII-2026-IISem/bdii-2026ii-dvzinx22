import { Client } from './client.model';
import { Product } from './product.model';

export interface ProductSale {
  id?: number;
  product?: number | Product;
  productId?: number;
  productName?: string;
  quantity: number;
  unitPrice?: number | string;
  lineTotal?: number | string;
  subtotal?: number | string;
  status?: string;
  createdAt?: string;
  updatedAt?: string;
}

export interface Sale {
  id?: number;
  client?: number | Client;
  clientId?: number;
  clientName?: string;
  saleDate?: string;
  subtotal?: number | string;
  tax?: number | string;
  discounts?: number | string;
  total?: number | string;
  status?: string;
  lines?: ProductSale[];
  items?: ProductSale[];
  createdAt?: string;
  updatedAt?: string;
}

export interface CreateSaleItemPayload {
  productId: number;
  quantity: number;
}

export interface SaleRegisterPayload {
  clientId: number;
  saleDate: string;
  discounts?: number;
  items: CreateSaleItemPayload[];
}
