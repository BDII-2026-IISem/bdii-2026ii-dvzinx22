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
    path: '**',
    redirectTo: '',
  },
];
