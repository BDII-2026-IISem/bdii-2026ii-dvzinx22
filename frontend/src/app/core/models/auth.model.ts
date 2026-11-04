export interface LoginPayload {
  username?: string;
  email?: string;
  password: string;
}

export interface TokenPair {
  access: string;
  refresh: string;
  tokenType: string;
  accessExpiresIn: number;
}

export interface UserProfile {
  id: number;
  username: string;
  email: string;
  firstName?: string;
  lastName?: string;
  status: string;
  roles?: string[];
  permissions?: string[];
}

