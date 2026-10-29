import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule, CurrencyPipe, DatePipe } from '@angular/common';
import { Router } from '@angular/router';
import { TableModule } from 'primeng/table';
import { ButtonModule } from 'primeng/button';
import { DialogModule } from 'primeng/dialog';
import { TagModule } from 'primeng/tag';
import { ConfirmDialogModule } from 'primeng/confirmdialog';
import { ConfirmationService, MessageService, SharedModule } from 'primeng/api';
import { SaleService } from '../../../core/services/sale.service';
import { Sale, ProductSale } from '../../../core/models/sale.model';

@Component({
  selector: 'app-sale-list',
  standalone: true,
  imports: [
    CommonModule,
    CurrencyPipe,
    DatePipe,
    TableModule,
    ButtonModule,
    DialogModule,
    TagModule,
    ConfirmDialogModule,
    SharedModule,
  ],
  templateUrl: './sale-list.html',
  styleUrl: './sale-list.css',
})
export class SaleListComponent implements OnInit {
  private readonly saleService = inject(SaleService);
  private readonly messageService = inject(MessageService);
  private readonly confirmationService = inject(ConfirmationService);
  private readonly router = inject(Router);

  sales = signal<Sale[]>([]);
  loading = signal<boolean>(false);
  detailVisible = signal<boolean>(false);
  selectedSale = signal<Sale | null>(null);

  ngOnInit(): void {
    this.loadSales();
  }

  loadSales(): void {
    this.loading.set(true);
    this.saleService.getAll().subscribe({
      next: (data) => {
        this.sales.set(data);
        this.loading.set(false);
      },
      error: () => {
        this.loading.set(false);
        this.messageService.add({
          severity: 'error',
          summary: 'Error',
          detail: 'No se pudo cargar el historial de ventas de TazaNorte.',
        });
      },
    });
  }

  viewDetail(sale: Sale): void {
    this.selectedSale.set(sale);
    this.detailVisible.set(true);
  }

  voidSale(sale: Sale): void {
    this.confirmationService.confirm({
      message: `¿Está seguro de anular la Venta #${sale.id} de ${sale.clientName} por valor de $${Number(sale.total).toLocaleString('es-CO')}? Esta acción revertirá la transacción.`,
      header: 'Confirmar Anulación de Venta',
      icon: 'pi pi-exclamation-triangle',
      acceptLabel: 'Sí, Anular Venta',
      rejectLabel: 'Conservar',
      acceptButtonStyleClass: 'p-button-danger',
      accept: () => {
        if (!sale.id) return;
        this.saleService.voidSale(sale.id).subscribe({
          next: () => {
            this.messageService.add({
              severity: 'warn',
              summary: 'Venta Anulada',
              detail: `La venta #${sale.id} ha sido anulada con éxito en Django.`,
            });
            this.loadSales();
          },
          error: (err) => {
            this.messageService.add({
              severity: 'error',
              summary: 'Error al Anular',
              detail: err?.error?.detail || 'No se pudo anular la orden seleccionada.',
            });
          },
        });
      },
    });
  }

  newSale(): void {
    this.router.navigate(['/ventas/nueva']);
  }
}

