import { Component, OnInit, inject, signal, computed } from '@angular/core';
import { CommonModule, CurrencyPipe } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { ButtonModule } from 'primeng/button';
import { SelectModule } from 'primeng/select';
import { InputNumberModule } from 'primeng/inputnumber';
import { TableModule } from 'primeng/table';
import { TagModule } from 'primeng/tag';
import { MessageService, SharedModule } from 'primeng/api';
import { SaleService } from '../../../core/services/sale.service';
import { ClientService } from '../../../core/services/client.service';
import { ProductService } from '../../../core/services/product.service';
import { Client } from '../../../core/models/client.model';
import { Product } from '../../../core/models/product.model';
import { Sale, SaleRegisterPayload } from '../../../core/models/sale.model';

export interface CartItem {
  product: Product;
  quantity: number;
}

@Component({
  selector: 'app-sale-form',
  standalone: true,
  imports: [
    CommonModule,
    CurrencyPipe,
    ReactiveFormsModule,
    ButtonModule,
    SelectModule,
    InputNumberModule,
    TableModule,
    TagModule,
    SharedModule,
  ],
  templateUrl: './sale-form.html',
  styleUrl: './sale-form.css',
})
export class SaleFormComponent implements OnInit {
  private readonly saleService = inject(SaleService);
  private readonly clientService = inject(ClientService);
  private readonly productService = inject(ProductService);
  private readonly fb = inject(FormBuilder);
  private readonly messageService = inject(MessageService);
  private readonly router = inject(Router);

  clients = signal<Client[]>([]);
  products = signal<Product[]>([]);
  cart = signal<CartItem[]>([]);
  submitting = signal<boolean>(false);
  lastSale = signal<Sale | null>(null);

  protected readonly Number = Number;

  saleForm: FormGroup = this.fb.group({
    clientId: [null, [Validators.required]],
    discounts: [0, [Validators.min(0)]],
  });

  // Computed signals for cart calculations
  subtotal = computed(() => {
    return this.cart().reduce((acc, item) => {
      const price = Number(item.product.price) || 0;
      return acc + price * item.quantity;
    }, 0);
  });

  discounts = computed(() => {
    return Number(this.saleForm.get('discounts')?.value) || 0;
  });

  tax = computed(() => {
    // DRF backend calculates tax at 19% or uses server logic
    const taxable = Math.max(0, this.subtotal() - this.discounts());
    return Math.round(taxable * 0.19);
  });

  total = computed(() => {
    return this.subtotal() - this.discounts() + this.tax();
  });

  totalItemsCount = computed(() => {
    return this.cart().reduce((acc, item) => acc + item.quantity, 0);
  });

  ngOnInit(): void {
    this.loadClients();
    this.loadProducts();
  }

  loadClients(): void {
    this.clientService.getAll().subscribe({
      next: (clients) => {
        this.clients.set(clients);
        if (clients.length > 0) {
          this.saleForm.patchValue({ clientId: clients[0].id });
        }
      },
    });
  }

  loadProducts(): void {
    this.productService.getAll().subscribe({
      next: (prods) => {
        // Filter active products with positive stock
        this.products.set(prods);
      },
    });
  }

  addToCart(product: Product): void {
    const currentCart = [...this.cart()];
    const existingIndex = currentCart.findIndex((i) => i.product.id === product.id);

    if (existingIndex > -1) {
      if (currentCart[existingIndex].quantity < product.stock) {
        currentCart[existingIndex].quantity += 1;
        this.cart.set(currentCart);
      } else {
        this.messageService.add({
          severity: 'warn',
          summary: 'Stock Máximo',
          detail: `Solo hay ${product.stock} unidades de ${product.name} en inventario.`,
        });
      }
    } else {
      if (product.stock > 0) {
        this.cart.set([...currentCart, { product, quantity: 1 }]);
      } else {
        this.messageService.add({
          severity: 'error',
          summary: 'Sin Stock',
          detail: `${product.name} está agotado.`,
        });
      }
    }
  }

  updateQuantity(productId: number | undefined, delta: number): void {
    if (!productId) return;
    const currentCart = [...this.cart()];
    const index = currentCart.findIndex((i) => i.product.id === productId);
    if (index === -1) return;

    const newQty = currentCart[index].quantity + delta;
    if (newQty <= 0) {
      this.removeFromCart(productId);
    } else if (newQty > currentCart[index].product.stock) {
      this.messageService.add({
        severity: 'warn',
        summary: 'Stock Máximo',
        detail: `No hay más stock disponible para ${currentCart[index].product.name}.`,
      });
    } else {
      currentCart[index].quantity = newQty;
      this.cart.set(currentCart);
    }
  }

  removeFromCart(productId: number | undefined): void {
    if (!productId) return;
    this.cart.set(this.cart().filter((i) => i.product.id !== productId));
  }

  clearCart(): void {
    this.cart.set([]);
  }

  processSale(): void {
    if (this.saleForm.invalid) {
      this.saleForm.markAllAsTouched();
      this.messageService.add({
        severity: 'warn',
        summary: 'Atención',
        detail: 'Por favor seleccione un cliente para la factura.',
      });
      return;
    }

    if (this.cart().length === 0) {
      this.messageService.add({
        severity: 'warn',
        summary: 'Canasta Vacía',
        detail: 'Agregue al menos un producto a la orden antes de procesar.',
      });
      return;
    }

    this.submitting.set(true);

    const payload: SaleRegisterPayload = {
      clientId: this.saleForm.value.clientId,
      saleDate: new Date().toISOString(),
      discounts: Number(this.saleForm.value.discounts) || 0,
      items: this.cart().map((item) => ({
        productId: item.product.id!,
        quantity: item.quantity,
      })),
    };

    this.saleService.createSale(payload).subscribe({
      next: (sale) => {
        this.submitting.set(false);
        this.lastSale.set(sale);
        this.cart.set([]);
        this.messageService.add({
          severity: 'success',
          summary: '¡Venta Transaccional Registrada!',
          detail: `Orden #${sale.id} despachada con éxito por Total: $${Number(sale.total).toLocaleString('es-CO')}.`,
        });
      },
      error: (err) => {
        this.submitting.set(false);
        const detailMsg = err?.error?.detail || err?.error?.message || 'Error procesando la transacción atómica en Django.';
        this.messageService.add({
          severity: 'error',
          summary: 'Error en Venta',
          detail: detailMsg,
        });
      },
    });
  }

  goToSalesHistory(): void {
    this.router.navigate(['/ventas']);
  }
}
