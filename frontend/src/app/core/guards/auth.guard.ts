import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { AuthService } from '../services/auth.service';

export const authGuard: CanActivateFn = (route, state) => {
  const authService = inject(AuthService);
  const router = inject(Router);

  if (authService.isAuthenticated()) {
    return true;
  }

  // Si no está autenticado, redirige al login guardando la URL a la que quería entrar
  return router.createUrlTree(['/login'], {
    queryParams: { returnUrl: state.url },
  });
};

export const guestGuard: CanActivateFn = () => {
  const authService = inject(AuthService);
  const router = inject(Router);

  if (authService.isAuthenticated()) {
    // Si ya está autenticado e intenta ir a /login, redirige al inicio
    return router.createUrlTree(['/']);
  }

  return true;
};

export const adminGuard: CanActivateFn = () => {
  const authService = inject(AuthService);
  const router = inject(Router);

  if (!authService.isAuthenticated()) {
    return router.createUrlTree(['/login']);
  }

  const user = authService.currentUser();
  if (user) {
    const isAdmin =
      user.username === 'admin' ||
      !!user.isSuperuser ||
      (user.roles && (user.roles.includes('admin') || user.roles.includes('seguridad')));

    if (isAdmin) {
      return true;
    }
    // Usuario normal: no tiene acceso a seguridad, redirigir al inicio
    return router.createUrlTree(['/']);
  }

  // Comprobación de respaldo leyendo el token si el perfil aún se está cargando
  const token = authService.getAccessToken();
  if (token) {
    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      if (payload.username === 'admin') return true;
    } catch {}
  }

  return true;
};

