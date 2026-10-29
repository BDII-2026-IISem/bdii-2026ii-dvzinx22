import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: '',
    loadComponent: () => import('./features/home/home').then((m) => m.HomeComponent),
  },
  {
    path: 'clientes',
    loadComponent: () =>
      import('./features/clients/client-list/client-list').then((m) => m.ClientListComponent),
  },
  {
    path: 'tipos-producto',
    loadComponent: () =>
      import('./features/product-types/product-type-list/product-type-list').then(
        (m) => m.ProductTypeListComponent,
      ),
  },
  {
    path: '**',
    redirectTo: '',
  },
];
