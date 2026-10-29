import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { TableModule } from 'primeng/table';
import { ButtonModule } from 'primeng/button';
import { InputTextModule } from 'primeng/inputtext';
import { DialogModule } from 'primeng/dialog';
import { MessageService, ConfirmationService } from 'primeng/api';
import { ProductTypeService } from '../../../core/services/product-type.service';
import { ProductType } from '../../../core/models/product-type.model';

@Component({
  selector: 'app-product-type-list',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    TableModule,
    ButtonModule,
    InputTextModule,
    DialogModule,
  ],
  templateUrl: './product-type-list.html',
  styleUrl: './product-type-list.css',
})
export class ProductTypeListComponent implements OnInit {
  private readonly productTypeService = inject(ProductTypeService);
  private readonly fb = inject(FormBuilder);
  private readonly messageService = inject(MessageService);
  private readonly confirmationService = inject(ConfirmationService);

  // Signals
  productTypes = signal<ProductType[]>([]);
  loading = signal<boolean>(false);
  dialogVisible = signal<boolean>(false);
  isEditing = signal<boolean>(false);
  currentId = signal<number | null>(null);

  typeForm: FormGroup = this.fb.group({
    name: ['', [Validators.required, Validators.minLength(2), Validators.maxLength(100)]],
    description: [''],
  });

  ngOnInit(): void {
    this.loadProductTypes();
  }

  loadProductTypes(): void {
    this.loading.set(true);
    this.productTypeService.getAll().subscribe({
      next: (data) => {
        this.productTypes.set(data);
        this.loading.set(false);
      },
      error: () => {
        this.loading.set(false);
        this.messageService.add({
          severity: 'error',
          summary: 'Error de Conexión',
          detail: 'No se pudo cargar los tipos de producto desde Django.',
        });
      },
    });
  }

  openNew(): void {
    this.isEditing.set(false);
    this.currentId.set(null);
    this.typeForm.reset();
    this.dialogVisible.set(true);
  }

  editType(type: ProductType): void {
    this.isEditing.set(true);
    this.currentId.set(type.id ?? null);
    this.typeForm.patchValue({
      name: type.name,
      description: type.description ?? '',
    });
    this.dialogVisible.set(true);
  }

  saveType(): void {
    if (this.typeForm.invalid) {
      this.typeForm.markAllAsTouched();
      return;
    }

    const payload = this.typeForm.value;

    if (this.isEditing() && this.currentId()) {
      this.productTypeService.update(this.currentId()!, payload).subscribe({
        next: (updated) => {
          this.messageService.add({
            severity: 'success',
            summary: 'Categoría Actualizada',
            detail: `${updated.name} actualizada con éxito.`,
          });
          this.dialogVisible.set(false);
          this.loadProductTypes();
        },
        error: () => {
          this.messageService.add({
            severity: 'error',
            summary: 'Error',
            detail: 'No se pudo actualizar la categoría.',
          });
        },
      });
    } else {
      this.productTypeService.create(payload).subscribe({
        next: (created) => {
          this.messageService.add({
            severity: 'success',
            summary: 'Categoría Creada',
            detail: `${created.name} registrada en TazaNorte.`,
          });
          this.dialogVisible.set(false);
          this.loadProductTypes();
        },
        error: () => {
          this.messageService.add({
            severity: 'error',
            summary: 'Error',
            detail: 'Verifique los datos o nombre de la categoría.',
          });
        },
      });
    }
  }

  deleteType(type: ProductType): void {
    this.confirmationService.confirm({
      message: `¿Está seguro de dar de baja la categoría "${type.name}"?`,
      header: 'Confirmar Baja Lógica',
      icon: 'pi pi-exclamation-triangle',
      acceptLabel: 'Sí, Desactivar',
      rejectLabel: 'Cancelar',
      acceptButtonStyleClass: 'p-button-danger',
      accept: () => {
        if (!type.id) return;
        this.productTypeService.delete(type.id).subscribe({
          next: () => {
            this.messageService.add({
              severity: 'warn',
              summary: 'Categoría Desactivada',
              detail: `Baja lógica realizada para ${type.name}.`,
            });
            this.loadProductTypes();
          },
          error: () => {
            this.messageService.add({
              severity: 'error',
              summary: 'Error',
              detail: 'No se pudo desactivar la categoría (puede tener productos asociados).',
            });
          },
        });
      },
    });
  }
}

