import { Component, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { AuthService } from '../../core/services/auth.service';

interface NavChild {
  label: string;
  route: string;
  icon: string;
  exact?: boolean;
}

interface NavSection {
  id: string;
  label: string;
  children: NavChild[];
  roles?: string[];
}

@Component({
  selector: 'app-sidebar',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './sidebar.html',
  styleUrl: './sidebar.css',
})
export class SidebarComponent {
  protected readonly authService = inject(AuthService);

  // Secciones desplegadas por defecto
  expandedSections = signal<Record<string, boolean>>({
    operacion: true,
    seguridad: true,
  });

  sections: NavSection[] = [
    {
      id: 'operacion',
      label: 'OPERACIÓN',
      children: [
        { label: 'Dashboard', route: '/', icon: 'pi pi-chart-bar', exact: true },
        { label: 'Clientes', route: '/clientes', icon: 'pi pi-users' },
        { label: 'Tipos de Producto', route: '/tipos-producto', icon: 'pi pi-tags' },
        { label: 'Productos', route: '/productos', icon: 'pi pi-box' },
        { label: 'Ventas (POS)', route: '/ventas/nueva', icon: 'pi pi-shopping-cart' },
        { label: 'Detalle de ventas', route: '/ventas', icon: 'pi pi-receipt', exact: true },
      ],
    },
    {
      id: 'seguridad',
      label: 'SEGURIDAD',
      roles: ['admin', 'seguridad'],
      children: [
        { label: 'Usuarios', route: '/seguridad/usuarios', icon: 'pi pi-users' },
        { label: 'Roles', route: '/seguridad/roles', icon: 'pi pi-id-card' },
        { label: 'Recursos', route: '/seguridad/recursos', icon: 'pi pi-sitemap' },
        { label: 'Asignaciones', route: '/seguridad/asignaciones', icon: 'pi pi-link' },
        { label: 'Concesiones', route: '/seguridad/concesiones', icon: 'pi pi-key' },
        { label: 'Matriz de permisos', route: '/seguridad/matriz-permisos', icon: 'pi pi-th-large' },
      ],
    },
  ];

  canViewSection(section: NavSection): boolean {
    if (!section.roles || section.roles.length === 0) return true;
    const user = this.authService.currentUser();
    if (!user) {
      const token = this.authService.getAccessToken();
      if (token) {
        try {
          const payload = JSON.parse(atob(token.split('.')[1]));
          return payload.username === 'admin';
        } catch {
          return false;
        }
      }
      return false;
    }

    if (user.username === 'admin' || user.isSuperuser) return true;

    const userRoles = user.roles || [];
    return section.roles.some((r) => r === user.username || userRoles.includes(r));
  }

  toggleSection(id: string): void {
    const current = this.expandedSections();
    this.expandedSections.set({
      ...current,
      [id]: !current[id],
    });
  }

  isExpanded(id: string): boolean {
    return !!this.expandedSections()[id];
  }
}
