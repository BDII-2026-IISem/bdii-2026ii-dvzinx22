import { Component, OnInit, inject, signal, computed } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { TableModule } from 'primeng/table';
import { ButtonModule } from 'primeng/button';
import { InputTextModule } from 'primeng/inputtext';
import { MessageService } from 'primeng/api';
import { forkJoin, of } from 'rxjs';
import { RbacService } from '../../../core/services/rbac.service';
import { Role, Resource, ResourceRole } from '../../../core/models/rbac.model';

export interface MatrixRow {
  key: string;
  label: string;
  route: string;
  postResource?: Resource;
  getResource?: Resource;
  putResource?: Resource;
  deleteResource?: Resource;
}

@Component({
  selector: 'app-matriz-permisos',
  standalone: true,
  imports: [CommonModule, FormsModule, TableModule, ButtonModule, InputTextModule],
  templateUrl: './matriz-permisos.html',
  styleUrl: './matriz-permisos.css',
})
export class MatrizPermisosComponent implements OnInit {
  private readonly rbacService = inject(RbacService);
  private readonly messageService = inject(MessageService);

  loading = signal<boolean>(false);
  saving = signal<boolean>(false);

  roles = signal<Role[]>([]);
  resources = signal<Resource[]>([]);
  allConcessions = signal<ResourceRole[]>([]);

  selectedRole = signal<Role | null>(null);
  roleSearch = signal<string>('');
  tableSearch = signal<string>('');

  // Estado mutable de permisos concedidos: Map de resourceId -> boolean
  permissionState = signal<Record<number, boolean>>({});
  originalState: Record<number, boolean> = {};

  // Definición de las tablas del negocio TazaNorte
  matrixDefinitions: { key: string; label: string; baseRoute: string }[] = [
    { key: 'products', label: 'Productos', baseRoute: 'api/products/' },
    { key: 'products_available', label: 'Productos disponibles', baseRoute: 'api/products/available/' },
    { key: 'product_types', label: 'Tipos de Producto', baseRoute: 'api/product-types/' },
    { key: 'clients', label: 'Clientes', baseRoute: 'api/clients/' },
    { key: 'sales', label: 'Ventas (POS)', baseRoute: 'api/sales/' },
    { key: 'users', label: 'Usuarios', baseRoute: 'api/users/' },
    { key: 'roles', label: 'Roles', baseRoute: 'api/roles/' },
    { key: 'role_users', label: 'Asignaciones', baseRoute: 'api/role-users/' },
    { key: 'resource_roles', label: 'Concesiones', baseRoute: 'api/resource-roles/' },
    { key: 'resources', label: 'Recursos', baseRoute: 'api/resources/' },
    { key: 'profile', label: 'Perfil JWT', baseRoute: 'api/auth/profile/' },
  ];

  filteredRoles = computed(() => {
    const term = this.roleSearch().toLowerCase().trim();
    if (!term) return this.roles();
    return this.roles().filter((r) => r.name.toLowerCase().includes(term));
  });

  matrixRows = computed<MatrixRow[]>(() => {
    const allRes = this.resources();
    const term = this.tableSearch().toLowerCase().trim();

    const rows: MatrixRow[] = this.matrixDefinitions.map((def) => {
      const post = allRes.find(
        (r) => r.method === 'POST' && (r.route === def.baseRoute || r.route.startsWith(def.baseRoute))
      );
      const get = allRes.find(
        (r) => r.method === 'GET' && (r.route === def.baseRoute || r.route.startsWith(def.baseRoute))
      );
      const put = allRes.find(
        (r) => (r.method === 'PUT' || r.method === 'PATCH') && (r.route === def.baseRoute || r.route.startsWith(def.baseRoute))
      );
      const del = allRes.find(
        (r) => r.method === 'DELETE' && (r.route === def.baseRoute || r.route.startsWith(def.baseRoute))
      );

      return {
        key: def.key,
        label: def.label,
        route: '/' + def.baseRoute,
        postResource: post,
        getResource: get,
        putResource: put,
        deleteResource: del,
      };
    });

    if (!term) return rows;
    return rows.filter(
      (row) =>
        row.label.toLowerCase().includes(term) ||
        row.route.toLowerCase().includes(term)
    );
  });

  totalGranted = computed(() => {
    const state = this.permissionState();
    return Object.values(state).filter((val) => val === true).length;
  });

  ngOnInit(): void {
    this.loadData();
  }

  loadData(): void {
    this.loading.set(true);
    forkJoin({
      roles: this.rbacService.getRoles(),
      resources: this.rbacService.getResources(),
      concessions: this.rbacService.getResourceRoles(),
    }).subscribe({
      next: ({ roles, resources, concessions }) => {
        this.roles.set(roles);
        this.resources.set(resources);
        this.allConcessions.set(concessions);
        this.loading.set(false);

        if (!this.selectedRole() && roles.length > 0) {
          const admin = roles.find((r) => r.name === 'admin') || roles[0];
          this.selectRole(admin);
        } else if (this.selectedRole()) {
          this.rebuildRoleState(this.selectedRole()!.id!);
        }
      },
      error: () => {
        this.loading.set(false);
        this.messageService.add({
          severity: 'error',
          summary: 'Error',
          detail: 'No se pudieron cargar los datos de RBAC.',
        });
      },
    });
  }

  selectRole(role: Role): void {
    this.selectedRole.set(role);
    if (role.id) {
      this.rebuildRoleState(role.id);
    }
  }

  rebuildRoleState(roleId: number): void {
    const state: Record<number, boolean> = {};
    const roleConcessions = this.allConcessions().filter(
      (c) => c.role === roleId && c.status === 'active'
    );

    for (const res of this.resources()) {
      if (res.id) {
        state[res.id] = roleConcessions.some((c) => c.resource === res.id);
      }
    }

    this.permissionState.set({ ...state });
    this.originalState = { ...state };
  }

  isGranted(resourceId?: number): boolean {
    if (!resourceId) return false;
    return !!this.permissionState()[resourceId];
  }

  togglePermission(resourceId?: number): void {
    if (!resourceId) return;
    const current = this.permissionState();
    this.permissionState.set({
      ...current,
      [resourceId]: !current[resourceId],
    });
  }

  // Column helpers: Todo / Nada por verbo
  toggleColumn(verb: 'POST' | 'GET' | 'PUT' | 'DELETE', grant: boolean): void {
    const current = { ...this.permissionState() };
    for (const row of this.matrixRows()) {
      let targetRes: Resource | undefined;
      if (verb === 'POST') targetRes = row.postResource;
      if (verb === 'GET') targetRes = row.getResource;
      if (verb === 'PUT') targetRes = row.putResource;
      if (verb === 'DELETE') targetRes = row.deleteResource;

      if (targetRes && targetRes.id) {
        current[targetRes.id] = grant;
      }
    }
    this.permissionState.set(current);
  }

  // Row helper: marcar o desmarcar toda la fila
  toggleRow(row: MatrixRow, grant: boolean): void {
    const current = { ...this.permissionState() };
    const resList = [row.postResource, row.getResource, row.putResource, row.deleteResource];
    for (const r of resList) {
      if (r && r.id) {
        current[r.id] = grant;
      }
    }
    this.permissionState.set(current);
  }

  markAll(): void {
    const current = { ...this.permissionState() };
    for (const res of this.resources()) {
      if (res.id) current[res.id] = true;
    }
    this.permissionState.set(current);
  }

  unmarkAll(): void {
    const current = { ...this.permissionState() };
    for (const res of this.resources()) {
      if (res.id) current[res.id] = false;
    }
    this.permissionState.set(current);
  }

  discard(): void {
    this.permissionState.set({ ...this.originalState });
    this.messageService.add({
      severity: 'info',
      summary: 'Cambios descartados',
      detail: 'Se restauró el estado previo de los permisos.',
    });
  }

  saveChanges(): void {
    const role = this.selectedRole();
    if (!role || !role.id) return;

    this.saving.set(true);
    const roleId = role.id;
    const currentState = this.permissionState();
    const concessions = this.allConcessions().filter((c) => c.role === roleId);

    const ops: any[] = [];

    for (const res of this.resources()) {
      if (!res.id) continue;
      const shouldBeActive = !!currentState[res.id];
      const existing = concessions.find((c) => c.resource === res.id);

      if (shouldBeActive) {
        if (!existing) {
          // Crear concesión
          ops.push(this.rbacService.assignResourceToRole({ role: roleId, resource: res.id, status: 'active' }));
        } else if (existing.status !== 'active') {
          // Reactivar
          ops.push(this.rbacService.updateResourceRole(existing.id!, { status: 'active' }));
        }
      } else {
        if (existing && existing.status === 'active') {
          // Retirar
          ops.push(this.rbacService.updateResourceRole(existing.id!, { status: 'inactive' }));
        }
      }
    }

    if (ops.length === 0) {
      this.saving.set(false);
      this.messageService.add({
        severity: 'info',
        summary: 'Sin cambios',
        detail: 'No se detectaron modificaciones en los permisos.',
      });
      return;
    }

    forkJoin(ops).subscribe({
      next: () => {
        this.saving.set(false);
        this.messageService.add({
          severity: 'success',
          summary: 'Permisos guardados',
          detail: `Matriz de permisos actualizada exitosamente para «${role.name}».`,
        });
        // Recargar concesiones desde BD
        this.rbacService.getResourceRoles().subscribe((updatedConcessions) => {
          this.allConcessions.set(updatedConcessions);
          this.rebuildRoleState(roleId);
        });
      },
      error: () => {
        this.saving.set(false);
        this.messageService.add({
          severity: 'error',
          summary: 'Error',
          detail: 'Ocurrió un error al guardar los permisos en la base de datos.',
        });
      },
    });
  }
}
