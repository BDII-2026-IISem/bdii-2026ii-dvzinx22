import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { TableModule } from 'primeng/table';
import { ButtonModule } from 'primeng/button';
import { InputTextModule } from 'primeng/inputtext';
import { DialogModule } from 'primeng/dialog';
import { TagModule } from 'primeng/tag';
import { MessageService, ConfirmationService, SharedModule } from 'primeng/api';
import { RbacService } from '../../../core/services/rbac.service';
import { User, Role, Resource } from '../../../core/models/rbac.model';

@Component({
  selector: 'app-rbac-admin',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    TableModule,
    ButtonModule,
    InputTextModule,
    DialogModule,
    TagModule,
    SharedModule,
  ],
  templateUrl: './rbac-admin.html',
  styleUrl: './rbac-admin.css',
})
export class RbacAdminComponent implements OnInit {
  private readonly rbacService = inject(RbacService);
  private readonly fb = inject(FormBuilder);
  private readonly messageService = inject(MessageService);
  private readonly confirmationService = inject(ConfirmationService);

  activeTab = signal<'users' | 'roles' | 'resources'>('users');
  loading = signal<boolean>(false);

  // Datos
  users = signal<User[]>([]);
  roles = signal<Role[]>([]);
  resources = signal<Resource[]>([]);

  // Modales
  userDialog = signal<boolean>(false);
  roleDialog = signal<boolean>(false);

  // Formularios
  userForm: FormGroup = this.fb.group({
    username: ['', [Validators.required, Validators.minLength(3)]],
    email: ['', [Validators.required, Validators.email]],
    password: ['', [Validators.required, Validators.minLength(6)]],
    firstName: [''],
    lastName: [''],
  });

  roleForm: FormGroup = this.fb.group({
    name: ['', [Validators.required, Validators.minLength(2)]],
    description: [''],
  });

  ngOnInit(): void {
    this.loadAll();
  }

  loadAll(): void {
    this.loading.set(true);
    this.loadUsers();
    this.loadRoles();
    this.loadResources();
  }

  loadUsers(): void {
    this.rbacService.getUsers().subscribe({
      next: (data) => {
        this.users.set(data);
        this.loading.set(false);
      },
      error: () => this.loading.set(false),
    });
  }

  loadRoles(): void {
    this.rbacService.getRoles().subscribe({
      next: (data) => this.roles.set(data),
    });
  }

  loadResources(): void {
    this.rbacService.getResources().subscribe({
      next: (data) => this.resources.set(data),
    });
  }

  setTab(tab: 'users' | 'roles' | 'resources'): void {
    this.activeTab.set(tab);
  }

  openNewUser(): void {
    this.userForm.reset();
    this.userDialog.set(true);
  }

  saveUser(): void {
    if (this.userForm.invalid) {
      this.userForm.markAllAsTouched();
      return;
    }

    const payload = {
      ...this.userForm.value,
      status: 'active',
    };

    this.rbacService.createUser(payload).subscribe({
      next: (created) => {
        this.messageService.add({
          severity: 'success',
          summary: 'Usuario Creado',
          detail: `Usuario ${created.username} registrado en RBAC.`,
        });
        this.userDialog.set(false);
        this.loadUsers();
      },
      error: (err) => {
        this.messageService.add({
          severity: 'error',
          summary: 'Error',
          detail: err?.error?.username ? 'El nombre de usuario ya existe.' : 'Error al registrar usuario.',
        });
      },
    });
  }

  openNewRole(): void {
    this.roleForm.reset();
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

    this.rbacService.createRole(payload).subscribe({
      next: (created) => {
        this.messageService.add({
          severity: 'success',
          summary: 'Rol Creado',
          detail: `Rol ${created.name} registrado en la matriz RBAC.`,
        });
        this.roleDialog.set(false);
        this.loadRoles();
      },
      error: () => {
        this.messageService.add({
          severity: 'error',
          summary: 'Error',
          detail: 'No se pudo crear el rol.',
        });
      },
    });
  }

  getMethodSeverity(method: string): 'success' | 'info' | 'warn' | 'danger' | 'secondary' {
    switch (method.toUpperCase()) {
      case 'GET': return 'info';
      case 'POST': return 'success';
      case 'PUT':
      case 'PATCH': return 'warn';
      case 'DELETE': return 'danger';
      default: return 'secondary';
    }
  }
}

