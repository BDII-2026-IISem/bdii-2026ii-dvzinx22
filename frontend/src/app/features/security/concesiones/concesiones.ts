import { Component, OnInit, inject, signal, computed } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators, FormsModule } from '@angular/forms';
import { TableModule } from 'primeng/table';
import { ButtonModule } from 'primeng/button';
import { InputTextModule } from 'primeng/inputtext';
import { DialogModule } from 'primeng/dialog';
import { TagModule } from 'primeng/tag';
import { SelectModule } from 'primeng/select';
import { MessageService, SharedModule } from 'primeng/api';
import { RbacService } from '../../../core/services/rbac.service';
import { ResourceRole, Role, Resource } from '../../../core/models/rbac.model';

@Component({
  selector: 'app-concesiones',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
    TableModule,
    SharedModule,
    ButtonModule,
    InputTextModule,
    DialogModule,
    TagModule,
    SelectModule,
  ],
  templateUrl: './concesiones.html',
  styleUrl: './concesiones.css',
})
export class ConcesionesComponent implements OnInit {
  private readonly fb = inject(FormBuilder);
  private readonly rbacService = inject(RbacService);
  private readonly messageService = inject(MessageService);

  loading = signal<boolean>(false);
  resourceRoles = signal<ResourceRole[]>([]);
  roles = signal<Role[]>([]);
  resources = signal<Resource[]>([]);
  searchTerm = signal<string>('');

  filteredResourceRoles = computed(() => {
    const term = this.searchTerm().toLowerCase().trim();
    if (!term) return this.resourceRoles();
    return this.resourceRoles().filter(
      (rr) =>
        (rr.roleName && rr.roleName.toLowerCase().includes(term)) ||
        (rr.resourceRoute && rr.resourceRoute.toLowerCase().includes(term)) ||
        (rr.resourceMethod && rr.resourceMethod.toLowerCase().includes(term))
    );
  });

  grantDialog = signal<boolean>(false);

  grantForm: FormGroup = this.fb.group({
    role: [null, [Validators.required]],
    resource: [null, [Validators.required]],
  });

  ngOnInit(): void {
    this.loadAll();
  }

  loadAll(): void {
    this.loading.set(true);
    this.rbacService.getResourceRoles().subscribe({
      next: (data) => {
        this.resourceRoles.set(data);
        this.loading.set(false);
      },
      error: () => {
        this.loading.set(false);
        this.messageService.add({
          severity: 'error',
          summary: 'Error',
          detail: 'No se pudieron cargar las concesiones.',
        });
      },
    });

    this.rbacService.getRoles().subscribe({
      next: (data) => this.roles.set(data.filter((r) => r.status === 'active')),
    });

    this.rbacService.getResources().subscribe({
      next: (data) => this.resources.set(data.filter((res) => res.status === 'active')),
    });
  }

  openGrantDialog(): void {
    this.grantForm.reset();
    this.grantDialog.set(true);
  }

  saveGrant(): void {
    if (this.grantForm.invalid) {
      this.grantForm.markAllAsTouched();
      return;
    }

    const payload = {
      role: Number(this.grantForm.value.role),
      resource: Number(this.grantForm.value.resource),
      status: 'active',
    };

    this.rbacService.assignResourceToRole(payload).subscribe({
      next: () => {
        this.messageService.add({
          severity: 'success',
          summary: 'Concesión Creada',
          detail: 'Permiso asignado exitosamente al rol.',
        });
        this.grantDialog.set(false);
        this.loadAll();
      },
      error: (err) => {
        this.messageService.add({
          severity: 'error',
          summary: 'Error',
          detail: err?.error?.non_field_errors?.[0] || 'Error al conceder permiso (posible duplicado).',
        });
      },
    });
  }

  toggleStatus(rr: ResourceRole): void {
    const newStatus = rr.status === 'active' ? 'inactive' : 'active';
    const actionText = newStatus === 'inactive' ? 'Retirar' : 'Reactivar';

    this.rbacService.updateResourceRole(rr.id!, { status: newStatus }).subscribe({
      next: () => {
        this.messageService.add({
          severity: newStatus === 'active' ? 'success' : 'warn',
          summary: `Concesión ${actionText}da`,
          detail: `Permiso ahora está ${newStatus === 'active' ? 'activo' : 'inactivo'}.`,
        });
        this.loadAll();
      },
      error: () => {
        this.messageService.add({
          severity: 'error',
          summary: 'Error',
          detail: `Error al ${actionText.toLowerCase()} concesión.`,
        });
      },
    });
  }

  getMethodClass(method?: string): string {
    switch (method?.toUpperCase()) {
      case 'GET':
        return 'bg-sky-100 text-sky-800 border-sky-200';
      case 'POST':
        return 'bg-emerald-100 text-emerald-800 border-emerald-200';
      case 'PUT':
        return 'bg-orange-100 text-orange-800 border-orange-200';
      case 'PATCH':
        return 'bg-amber-100 text-amber-800 border-amber-200';
      case 'DELETE':
        return 'bg-rose-100 text-rose-800 border-rose-200';
      default:
        return 'bg-stone-100 text-stone-700 border-stone-200';
    }
  }
}
