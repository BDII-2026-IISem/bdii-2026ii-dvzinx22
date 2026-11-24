import { Component, OnInit, inject, signal, computed } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators, FormsModule } from '@angular/forms';
import { TableModule } from 'primeng/table';
import { ButtonModule } from 'primeng/button';
import { InputTextModule } from 'primeng/inputtext';
import { DialogModule } from 'primeng/dialog';
import { TagModule } from 'primeng/tag';
import { MessageService, ConfirmationService, SharedModule } from 'primeng/api';
import { RbacService } from '../../../core/services/rbac.service';
import { Role } from '../../../core/models/rbac.model';

@Component({
  selector: 'app-roles',
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
  ],
  templateUrl: './roles.html',
  styleUrl: './roles.css',
})
export class RolesComponent implements OnInit {
  private readonly fb = inject(FormBuilder);
  private readonly rbacService = inject(RbacService);
  private readonly messageService = inject(MessageService);
  private readonly confirmationService = inject(ConfirmationService);

  loading = signal<boolean>(false);
  roles = signal<Role[]>([]);
  searchTerm = signal<string>('');

  filteredRoles = computed(() => {
    const term = this.searchTerm().toLowerCase().trim();
    if (!term) return this.roles();
    return this.roles().filter(
      (r) =>
        r.name.toLowerCase().includes(term) ||
        (r.description && r.description.toLowerCase().includes(term))
    );
  });

  roleDialog = signal<boolean>(false);
  isEditing = signal<boolean>(false);
  currentRoleId = signal<number | null>(null);

  roleForm: FormGroup = this.fb.group({
    name: ['', [Validators.required, Validators.minLength(2)]],
    description: [''],
  });

  ngOnInit(): void {
    this.loadRoles();
  }

  loadRoles(): void {
    this.loading.set(true);
    this.rbacService.getRoles().subscribe({
      next: (data) => {
        this.roles.set(data);
        this.loading.set(false);
      },
      error: () => {
        this.loading.set(false);
        this.messageService.add({
          severity: 'error',
          summary: 'Error',
          detail: 'No se pudieron cargar los roles.',
        });
      },
    });
  }

  openNewRole(): void {
    this.isEditing.set(false);
    this.currentRoleId.set(null);
    this.roleForm.reset();
    this.roleDialog.set(true);
  }

  editRole(role: Role): void {
    this.isEditing.set(true);
    this.currentRoleId.set(role.id || null);
    this.roleForm.patchValue({
      name: role.name,
      description: role.description || '',
    });
    this.roleDialog.set(true);
  }

  saveRole(): void {
    if (this.roleForm.invalid) {
      this.roleForm.markAllAsTouched();
      return;
    }

    const payload = {
      ...this.roleForm.value,
      status: 'active',
    };

    if (this.isEditing() && this.currentRoleId()) {
      this.rbacService.updateRole(this.currentRoleId()!, payload).subscribe({
        next: (updated) => {
          this.messageService.add({
            severity: 'success',
            summary: 'Rol Actualizado',
            detail: `Rol ${updated.name} modificado exitosamente.`,
          });
          this.roleDialog.set(false);
          this.loadRoles();
        },
        error: () => {
          this.messageService.add({
            severity: 'error',
            summary: 'Error',
            detail: 'Error al actualizar rol.',
          });
        },
      });
    } else {
      this.rbacService.createRole(payload).subscribe({
        next: (created) => {
          this.messageService.add({
            severity: 'success',
            summary: 'Rol Creado',
            detail: `Rol ${created.name} registrado en RBAC.`,
          });
          this.roleDialog.set(false);
          this.loadRoles();
        },
        error: () => {
          this.messageService.add({
            severity: 'error',
            summary: 'Error',
            detail: 'Error al crear rol.',
          });
        },
      });
    }
  }

  toggleRoleStatus(role: Role): void {
    const newStatus = role.status === 'active' ? 'inactive' : 'active';
    const actionText = newStatus === 'inactive' ? 'Retirar' : 'Reactivar';

    this.rbacService.updateRole(role.id!, { status: newStatus }).subscribe({
      next: () => {
        this.messageService.add({
          severity: newStatus === 'active' ? 'success' : 'warn',
          summary: `Rol ${actionText}do`,
          detail: `El rol ${role.name} ahora está ${newStatus === 'active' ? 'activo' : 'inactivo'}.`,
        });
        this.loadRoles();
      },
      error: () => {
        this.messageService.add({
          severity: 'error',
          summary: 'Error',
          detail: `Error al ${actionText.toLowerCase()} el rol.`,
        });
      },
    });
  }
}
