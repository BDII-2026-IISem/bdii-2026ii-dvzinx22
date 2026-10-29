import { ProductType } from './product-type.model';

export interface Product {
  id?: number;
  code: string;
  name: string;
  description?: string;
  productTypeId: number;
  productType?: ProductType;
  productTypeName?: string;
  price: number;
  stock: number;
  isAvailable?: boolean;
  status?: string;
  createdAt?: string;
  updatedAt?: string;
}

