import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule, CurrencyPipe } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { TableModule } from 'primeng/table';
import { ButtonModule } from 'primeng/button';
import { InputTextModule } from 'primeng/inputtext';
import { DialogModule } from 'primeng/dialog';
import { SelectModule } from 'primeng/select';
import { TagModule } from 'primeng/tag';
import { MessageService, ConfirmationService, SharedModule } from 'primeng/api';
import { ProductService } from '../../../core/services/product.service';
import { ProductTypeService } from '../../../core/services/product-type.service';
import { Product } from '../../../core/models/product.model';
import { ProductType } from '../../../core/models/product-type.model';

@Component({
  selector: 'app-product-list',
  standalone: true,
  imports: [
    CommonModule,
    CurrencyPipe,
    ReactiveFormsModule,
    TableModule,
    SharedModule,
    ButtonModule,
    InputTextModule,
    DialogModule,
    SelectModule,
    TagModule,
  ],
  templateUrl: './product-list.html',
  styleUrl: './product-list.css',
})
export class ProductListComponent implements OnInit {
  private readonly productService = inject(ProductService);
  private readonly productTypeService = inject(ProductTypeService);
  private readonly fb = inject(FormBuilder);
  private readonly messageService = inject(MessageService);
  private readonly confirmationService = inject(ConfirmationService);

  // Signals
  products = signal<Product[]>([]);
  productTypes = signal<ProductType[]>([]);
  loading = signal<boolean>(false);
  dialogVisible = signal<boolean>(false);
  isEditing = signal<boolean>(false);
  currentId = signal<number | null>(null);

  productForm: FormGroup = this.fb.group({
    name: ['', [Validators.required, Validators.minLength(2), Validators.maxLength(120)]],
    productTypeId: [null, [Validators.required]],
    price: [null, [Validators.required, Validators.min(100)]],
    stock: [0, [Validators.required, Validators.min(0)]],
    description: [''],
  });

  ngOnInit(): void {
    this.loadProducts();
    this.loadProductTypes();
  }

  loadProducts(): void {
    this.loading.set(true);
    this.productService.getAll().subscribe({
      next: (data) => {
        this.products.set(data);
        this.loading.set(false);
      },
      error: () => {
        this.loading.set(false);
        this.messageService.add({
          severity: 'error',
          summary: 'Error',
          detail: 'No se pudo cargar el catálogo de productos de TazaNorte.',
        });
      },
    });
  }

  loadProductTypes(): void {
    this.productTypeService.getAll().subscribe({
      next: (types) => this.productTypes.set(types),
    });
  }

  openNew(): void {
    this.isEditing.set(false);
    this.currentId.set(null);
    this.productForm.reset({ stock: 0 });
    this.dialogVisible.set(true);
  }

  editProduct(prod: Product): void {
    this.isEditing.set(true);
    this.currentId.set(prod.id ?? null);
    this.productForm.patchValue({
      name: prod.name,
      productTypeId: prod.productTypeId,
      price: prod.price,
      stock: prod.stock,
      description: prod.description ?? '',
    });
    this.dialogVisible.set(true);
  }

  saveProduct(): void {
    if (this.productForm.invalid) {
      this.productForm.markAllAsTouched();
      return;
    }

    const formValues = this.productForm.value;
    const payload = {
      ...formValues,
      status: 'active',
    };

    if (this.isEditing() && this.currentId()) {
      this.productService.update(this.currentId()!, payload).subscribe({
        next: (updated) => {
          this.messageService.add({
            severity: 'success',
            summary: 'Producto Actualizado',
            detail: `${updated.name} actualizado exitosamente.`,
          });
          this.dialogVisible.set(false);
          this.loadProducts();
        },
        error: () => {
          this.messageService.add({
            severity: 'error',
            summary: 'Error',
            detail: 'No se pudo actualizar el producto.',
          });
        },
      });
    } else {
      this.productService.create(payload).subscribe({
        next: (created) => {
          this.messageService.add({
            severity: 'success',
            summary: 'Producto Creado',
            detail: `${created.name} agregado al menú de cafetería.`,
          });
          this.dialogVisible.set(false);
          this.loadProducts();
        },
        error: () => {
          this.messageService.add({
            severity: 'error',
            summary: 'Error',
            detail: 'Verifique los datos o campos requeridos.',
          });
        },
      });
    }
  }

  deleteProduct(prod: Product): void {
    this.confirmationService.confirm({
      message: `¿Está seguro de dar de baja el producto "${prod.name}" del catálogo?`,
      header: 'Confirmar Baja Lógica',
      icon: 'pi pi-exclamation-triangle',
      acceptLabel: 'Sí, Desactivar',
      rejectLabel: 'Cancelar',
      acceptButtonStyleClass: 'p-button-danger',
      accept: () => {
        if (!prod.id) return;
        this.productService.delete(prod.id).subscribe({
          next: () => {
            this.messageService.add({
              severity: 'warn',
              summary: 'Producto Desactivado',
              detail: `Baja lógica aplicada para ${prod.name}.`,
            });
            this.loadProducts();
          },
          error: () => {
            this.messageService.add({
              severity: 'error',
              summary: 'Error',
              detail: 'No se pudo desactivar el producto.',
            });
          },
        });
      },
    });
  }
}
