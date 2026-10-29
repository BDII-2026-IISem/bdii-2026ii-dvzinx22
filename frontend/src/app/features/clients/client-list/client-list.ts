import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { TableModule } from 'primeng/table';
import { ButtonModule } from 'primeng/button';
import { InputTextModule } from 'primeng/inputtext';
import { DialogModule } from 'primeng/dialog';
import { TagModule } from 'primeng/tag';
import { MessageService, ConfirmationService } from 'primeng/api';
import { ClientService } from '../../../core/services/client.service';
import { Client } from '../../../core/models/client.model';

@Component({
  selector: 'app-client-list',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    TableModule,
    ButtonModule,
    InputTextModule,
    DialogModule,
    TagModule,
  ],
  templateUrl: './client-list.html',
  styleUrl: './client-list.css',
})
export class ClientListComponent implements OnInit {
  private readonly clientService = inject(ClientService);
  private readonly fb = inject(FormBuilder);
  private readonly messageService = inject(MessageService);
  private readonly confirmationService = inject(ConfirmationService);

  // Signals
  clients = signal<Client[]>([]);
  loading = signal<boolean>(false);
  dialogVisible = signal<boolean>(false);
  isEditing = signal<boolean>(false);
  currentClientId = signal<number | null>(null);

  clientForm: FormGroup = this.fb.group({
    name: ['', [Validators.required, Validators.minLength(2), Validators.maxLength(150)]],
    email: ['', [Validators.email]],
    phone: [''],
    address: [''],
  });

  ngOnInit(): void {
    this.loadClients();
  }

  loadClients(): void {
    this.loading.set(true);
    this.clientService.getAll().subscribe({
      next: (data) => {
        this.clients.set(data);
        this.loading.set(false);
      },
      error: (err) => {
        this.loading.set(false);
        this.messageService.add({
          severity: 'error',
          summary: 'Error de Conexión',
          detail: 'No se pudo conectar con el API Django en :8000',
        });
      },
    });
  }

  openNew(): void {
    this.isEditing.set(false);
    this.currentClientId.set(null);
    this.clientForm.reset();
    this.dialogVisible.set(true);
  }

  editClient(client: Client): void {
    this.isEditing.set(true);
    this.currentClientId.set(client.id ?? null);
    this.clientForm.patchValue({
      name: client.name,
      email: client.email ?? '',
      phone: client.phone ?? '',
      address: client.address ?? '',
    });
    this.dialogVisible.set(true);
  }

  saveClient(): void {
    if (this.clientForm.invalid) {
      this.clientForm.markAllAsTouched();
      return;
    }

    const payload = this.clientForm.value;

    if (this.isEditing() && this.currentClientId()) {
      this.clientService.update(this.currentClientId()!, payload).subscribe({
        next: (updated) => {
          this.messageService.add({
            severity: 'success',
            summary: 'Cliente Actualizado',
            detail: `${updated.name} actualizado con éxito.`,
          });
          this.dialogVisible.set(false);
          this.loadClients();
        },
        error: (err) => {
          this.messageService.add({
            severity: 'error',
            summary: 'Error al Actualizar',
            detail: err?.error?.email ? 'El correo ya está registrado.' : 'Error al actualizar cliente.',
          });
        },
      });
    } else {
      this.clientService.create(payload).subscribe({
        next: (created) => {
          this.messageService.add({
            severity: 'success',
            summary: 'Cliente Creado',
            detail: `${created.name} registrado exitosamente en TazaNorte.`,
          });
          this.dialogVisible.set(false);
          this.loadClients();
        },
        error: (err) => {
          this.messageService.add({
            severity: 'error',
            summary: 'Error al Registrar',
            detail: err?.error?.email ? 'El correo ya está registrado.' : 'Verifique los campos ingresados.',
          });
        },
      });
    }
  }

  deleteClient(client: Client): void {
    this.confirmationService.confirm({
      message: `¿Está seguro de dar de baja lógica al cliente ${client.name}?`,
      header: 'Confirmar Eliminación Segura',
      icon: 'pi pi-exclamation-triangle',
      acceptLabel: 'Sí, Desactivar',
      rejectLabel: 'Cancelar',
      acceptButtonStyleClass: 'p-button-danger',
      accept: () => {
        if (!client.id) return;
        this.clientService.delete(client.id).subscribe({
          next: () => {
            this.messageService.add({
              severity: 'warn',
              summary: 'Cliente Desactivado',
              detail: `Baja lógica procesada en Django para ${client.name}.`,
            });
            this.loadClients();
          },
          error: (err) => {
            this.messageService.add({
              severity: 'error',
              summary: 'Error',
              detail: 'No se pudo dar de baja al cliente.',
            });
          },
        });
      },
    });
  }
}
