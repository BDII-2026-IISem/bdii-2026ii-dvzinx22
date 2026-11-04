import { Routes } from '@angular/router';
import { authGuard, guestGuard } from './core/guards/auth.guard';

export const routes: Routes = [
  {
    path: '',
    loadComponent: () => import('./features/home/home').then((m) => m.HomeComponent),
  },
  {
    path: 'clientes',
    canActivate: [authGuard],
    loadComponent: () =>
      import('./features/clients/client-list/client-list').then((m) => m.ClientListComponent),
  },
  {
    path: 'tipos-producto',
    canActivate: [authGuard],
    loadComponent: () =>
      import('./features/product-types/product-type-list/product-type-list').then(
        (m) => m.ProductTypeListComponent,
      ),
  },
  {
    path: 'productos',
    canActivate: [authGuard],
    loadComponent: () =>
      import('./features/products/product-list/product-list').then((m) => m.ProductListComponent),
  },
  {
    path: 'ventas/nueva',
    canActivate: [authGuard],
    loadComponent: () =>
      import('./features/sales/sale-form/sale-form').then((m) => m.SaleFormComponent),
  },
  {
    path: 'ventas',
    canActivate: [authGuard],
    loadComponent: () =>
      import('./features/sales/sale-list/sale-list').then((m) => m.SaleListComponent),
  },
  {
    path: 'perfil',
    canActivate: [authGuard],
    loadComponent: () =>
      import('./features/auth/profile/profile').then((m) => m.ProfileComponent),
  },
  {
    path: 'seguridad/usuarios',
    canActivate: [authGuard],
    loadComponent: () =>
      import('./features/security/rbac-admin/rbac-admin').then((m) => m.RbacAdminComponent),
  },
  {
    path: 'login',
    canActivate: [guestGuard],
    loadComponent: () =>
      import('./features/auth/login/login').then((m) => m.LoginComponent),
  },
  {
    path: '**',
    redirectTo: '',
  },
];
