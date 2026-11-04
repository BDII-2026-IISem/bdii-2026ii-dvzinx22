import { HttpInterceptorFn, HttpErrorResponse } from '@angular/common/http';
import { inject } from '@angular/core';
import { catchError, switchMap, throwError } from 'rxjs';
import { AuthService } from '../services/auth.service';
import { environment } from '../../../environments/environment';

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const authService = inject(AuthService);
  const isApiUrl = req.url.startsWith(environment.apiUrl);
  const isAuthAuthEndpoint = req.url.includes('/auth/login/') || req.url.includes('/auth/refresh/');

  let authReq = req;
  const token = authService.getAccessToken();

  if (isApiUrl && !isAuthAuthEndpoint && token) {
    authReq = req.clone({
      setHeaders: {
        Authorization: `Bearer ${token}`,
      },
    });
  }

  return next(authReq).pipe(
    catchError((error: HttpErrorResponse) => {
      // Si recibimos 401 y no es login/refresh, intentamos refrescar el token
      if (error.status === 401 && isApiUrl && !isAuthAuthEndpoint && authService.getRefreshToken()) {
        return authService.refreshToken().pipe(
          switchMap((newTokenPair) => {
            const retryReq = req.clone({
              setHeaders: {
                Authorization: `Bearer ${newTokenPair.access}`,
              },
            });
            return next(retryReq);
          }),
          catchError((refreshErr) => {
            authService.clearLocalSession();
            return throwError(() => refreshErr);
          })
        );
      }
      return throwError(() => error);
    })
  );
};

