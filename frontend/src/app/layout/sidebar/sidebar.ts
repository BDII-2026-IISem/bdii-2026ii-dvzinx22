import { Component, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

interface MenuItem {
  id: string;
  label: string;
  icon: string;
  children: {
    label: string;
    route: string;
    icon: string;
  }[];
}

@Component({
  selector: 'app-sidebar',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './sidebar.html',
  styleUrl: './sidebar.css',
})
export class SidebarComponent {
  // Estado de secciones desplegadas
  expandedSections = signal<Record<string, boolean>>({
    catalogo: true,
    ventas: true,
    seguridad: false,
  });

  menuItems: MenuItem[] = [
    {
      id: 'catalogo',
      label: 'Catálogo',
      icon: 'pi pi-file',
      children: [
        { label: 'Clientes', route: '/clientes', icon: 'pi pi-users' },
        { label: 'Tipos de Producto', route: '/tipos-producto', icon: 'pi pi-tags' },
        { label: 'Productos', route: '/productos', icon: 'pi pi-box' },
      ],
    },
    {
      id: 'ventas',
      label: 'Ventas',
      icon: 'pi pi-shopping-cart',
      children: [
        { label: 'Nueva Venta (POS)', route: '/ventas/nueva', icon: 'pi pi-plus-circle' },
        { label: 'Historial de Órdenes', route: '/ventas', icon: 'pi pi-receipt' },
      ],
    },
    {
      id: 'seguridad',
      label: 'Seguridad',
      icon: 'pi pi-shield',
      children: [
        { label: 'Control de Acceso (Fase II)', route: '/clientes', icon: 'pi pi-lock' },
      ],
    },
  ];

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

