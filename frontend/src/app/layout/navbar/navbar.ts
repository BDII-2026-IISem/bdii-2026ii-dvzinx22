import { Component, signal } from '@angular/core';
import { RouterLink, RouterLinkActive } from '@angular/router';
import { MenubarModule } from 'primeng/menubar';
import { BadgeModule } from 'primeng/badge';
import { MenuItem } from 'primeng/api';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [RouterLink, RouterLinkActive, MenubarModule, BadgeModule],
  templateUrl: './navbar.html',
  styleUrl: './navbar.css',
})
export class NavbarComponent {
  items: MenuItem[] = [
    {
      label: 'Clientes',
      icon: 'pi pi-users',
      routerLink: '/clientes',
    },
    {
      label: 'Tipos de Producto',
      icon: 'pi pi-tags',
      routerLink: '/tipos-producto',
    },
    {
      label: 'Productos',
      icon: 'pi pi-box',
      routerLink: '/productos',
    },
    {
      label: 'Ventas',
      icon: 'pi pi-shopping-bag',
      items: [
        {
          label: 'Historial de Ventas',
          icon: 'pi pi-receipt',
          routerLink: '/ventas',
        },
        {
          label: 'Registrar Venta (POS)',
          icon: 'pi pi-cart-plus',
          routerLink: '/ventas/nueva',
        },
      ],
    },
  ];
}

