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
import { RoleUser, User, Role } from '../../../core/models/rbac.model';

@Component({
  selector: 'app-asignaciones',
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
  templateUrl: './asignaciones.html',
  styleUrl: './asignaciones.css',
})
export class AsignacionesComponent implements OnInit {
  private readonly fb = inject(FormBuilder);
  private readonly rbacService = inject(RbacService);
  private readonly messageService = inject(MessageService);

  loading = signal<boolean>(false);
  roleUsers = signal<RoleUser[]>([]);
  users = signal<User[]>([]);
  roles = signal<Role[]>([]);
  searchTerm = signal<string>('');

  filteredRoleUsers = computed(() => {
    const term = this.searchTerm().toLowerCase().trim();
    if (!term) return this.roleUsers();
    return this.roleUsers().filter(
      (ru) =>
        (ru.username && ru.username.toLowerCase().includes(term)) ||
        (ru.roleName && ru.roleName.toLowerCase().includes(term))
    );
  });

  assignDialog = signal<boolean>(false);

  assignForm: FormGroup = this.fb.group({
    user: [null, [Validators.required]],
    role: [null, [Validators.required]],
  });

  ngOnInit(): void {
    this.loadAll();
  }

  loadAll(): void {
    this.loading.set(true);
    this.rbacService.getRoleUsers().subscribe({
      next: (data) => {
        this.roleUsers.set(data);
        this.loading.set(false);
      },
      error: () => {
        this.loading.set(false);
        this.messageService.add({
          severity: 'error',
          summary: 'Error',
          detail: 'No se pudieron cargar las asignaciones.',
        });
      },
    });

    this.rbacService.getUsers().subscribe({
      next: (data) => this.users.set(data.filter((u) => u.status === 'active')),
    });

    this.rbacService.getRoles().subscribe({
      next: (data) => this.roles.set(data.filter((r) => r.status === 'active')),
    });
  }

  openAssignDialog(): void {
    this.assignForm.reset();
    this.assignDialog.set(true);
  }

  saveAssignment(): void {
    if (this.assignForm.invalid) {
      this.assignForm.markAllAsTouched();
      return;
    }

    const payload = {
      user: Number(this.assignForm.value.user),
      role: Number(this.assignForm.value.role),
      status: 'active',
    };

    this.rbacService.assignRoleToUser(payload).subscribe({
      next: () => {
        this.messageService.add({
          severity: 'success',
          summary: 'Rol Asignado',
          detail: 'Asignación creada exitosamente.',
        });
        this.assignDialog.set(false);
        this.loadAll();
      },
      error: (err) => {
        this.messageService.add({
          severity: 'error',
          summary: 'Error',
          detail: err?.error?.non_field_errors?.[0] || 'Error al asignar rol (posible duplicado).',
        });
      },
    });
  }

  toggleStatus(ru: RoleUser): void {
    const newStatus = ru.status === 'active' ? 'inactive' : 'active';
    const actionText = newStatus === 'inactive' ? 'Retirar' : 'Reactivar';

    this.rbacService.updateRoleUser(ru.id!, { status: newStatus }).subscribe({
      next: () => {
        this.messageService.add({
          severity: newStatus === 'active' ? 'success' : 'warn',
          summary: `Asignación ${actionText}da`,
          detail: `El rol ahora está ${newStatus === 'active' ? 'activo' : 'inactivo'} para este usuario.`,
        });
        this.loadAll();
      },
      error: () => {
        this.messageService.add({
          severity: 'error',
          summary: 'Error',
          detail: `Error al ${actionText.toLowerCase()} asignación.`,
        });
      },
    });
  }
}
