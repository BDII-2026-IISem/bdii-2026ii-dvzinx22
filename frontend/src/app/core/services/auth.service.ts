import { Injectable, inject, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { Observable, tap, catchError, throwError, of } from 'rxjs';
import { environment } from '../../../environments/environment';
import { LoginPayload, TokenPair, UserProfile } from '../models/auth.model';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private readonly http = inject(HttpClient);
  private readonly router = inject(Router);
  private readonly authUrl = `${environment.apiUrl}/auth`;

  private readonly ACCESS_KEY = 'tazanorte_access_token';
  private readonly REFRESH_KEY = 'tazanorte_refresh_token';

  // Signals reactivas de autenticación
  currentUser = signal<UserProfile | null>(null);
  isAuthenticated = signal<boolean>(this.hasValidToken());
  loading = signal<boolean>(false);

  constructor() {
    if (this.hasValidToken()) {
      this.getProfile().subscribe({
        error: () => this.clearLocalSession(),
      });
    }
  }

  getAccessToken(): string | null {
    return localStorage.getItem(this.ACCESS_KEY);
  }

  getRefreshToken(): string | null {
    return localStorage.getItem(this.REFRESH_KEY);
  }

  private hasValidToken(): boolean {
    const token = this.getAccessToken();
    if (!token) return false;
    try {
      const payloadBase64 = token.split('.')[1];
      if (!payloadBase64) return false;
      const decodedJson = atob(payloadBase64);
      const decoded = JSON.parse(decodedJson);
      const isExpired = decoded.exp && decoded.exp * 1000 < Date.now();
      return !isExpired;
    } catch {
      return false;
    }
  }

  login(credentials: LoginPayload): Observable<TokenPair> {
    this.loading.set(true);
    return this.http.post<TokenPair>(`${this.authUrl}/login/`, credentials).pipe(
      tap((res) => {
        localStorage.setItem(this.ACCESS_KEY, res.access);
        localStorage.setItem(this.REFRESH_KEY, res.refresh);
        this.isAuthenticated.set(true);
        this.loading.set(false);
        this.getProfile().subscribe();
      }),
      catchError((err) => {
        this.loading.set(false);
        return throwError(() => err);
      })
    );
  }

  refreshToken(): Observable<TokenPair> {
    const refresh = this.getRefreshToken();
    if (!refresh) {
      this.clearLocalSession();
      return throwError(() => new Error('No refresh token'));
    }

    return this.http.post<TokenPair>(`${this.authUrl}/refresh/`, { refresh }).pipe(
      tap((res) => {
        localStorage.setItem(this.ACCESS_KEY, res.access);
        localStorage.setItem(this.REFRESH_KEY, res.refresh);
        this.isAuthenticated.set(true);
      }),
      catchError((err) => {
        this.clearLocalSession();
        return throwError(() => err);
      })
    );
  }

  getProfile(): Observable<UserProfile> {
    return this.http.get<UserProfile>(`${this.authUrl}/profile/`).pipe(
      tap((user) => this.currentUser.set(user))
    );
  }

  logout(): void {
    const refresh = this.getRefreshToken();
    if (refresh) {
      this.http.post(`${this.authUrl}/logout/`, { refresh }).subscribe({
        next: () => this.clearLocalSession(),
        error: () => this.clearLocalSession(),
      });
    } else {
      this.clearLocalSession();
    }
  }

  clearLocalSession(): void {
    localStorage.removeItem(this.ACCESS_KEY);
    localStorage.removeItem(this.REFRESH_KEY);
    this.currentUser.set(null);
    this.isAuthenticated.set(false);
    this.router.navigate(['/login']);
  }
}

