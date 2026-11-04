export interface User {
  id?: number;
  username: string;
  email: string;
  firstName?: string;
  lastName?: string;
  status: string;
  password?: string;
  createdAt?: string;
  updatedAt?: string;
}

export interface Role {
  id?: number;
  name: string;
  description?: string;
  status: string;
  createdAt?: string;
  updatedAt?: string;
}

export interface Resource {
  id?: number;
  name: string;
  method: string;
  route: string;
  status: string;
  createdAt?: string;
  updatedAt?: string;
}

export interface RoleUser {
  id?: number;
  user: number;
  role: number;
  status: string;
  createdAt?: string;
  updatedAt?: string;
}

export interface ResourceRole {
  id?: number;
  role: number;
  resource: number;
  status: string;
  createdAt?: string;
  updatedAt?: string;
}

