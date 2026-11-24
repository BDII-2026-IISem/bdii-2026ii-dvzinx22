import { Component, OnInit, inject, signal, computed } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { TableModule } from 'primeng/table';
import { ButtonModule } from 'primeng/button';
import { InputTextModule } from 'primeng/inputtext';
import { MessageService, SharedModule } from 'primeng/api';
import { RbacService } from '../../../core/services/rbac.service';
import { Resource } from '../../../core/models/rbac.model';

@Component({
  selector: 'app-recursos',
  standalone: true,
  imports: [CommonModule, FormsModule, TableModule, SharedModule, ButtonModule, InputTextModule],
  templateUrl: './recursos.html',
  styleUrl: './recursos.css',
})
export class RecursosComponent implements OnInit {
  private readonly rbacService = inject(RbacService);
  private readonly messageService = inject(MessageService);

  loading = signal<boolean>(false);
  resources = signal<Resource[]>([]);
  searchTerm = signal<string>('');

  filteredResources = computed(() => {
    const term = this.searchTerm().toLowerCase().trim();
    if (!term) return this.resources();
    return this.resources().filter(
      (r) =>
        r.name.toLowerCase().includes(term) ||
        r.route.toLowerCase().includes(term) ||
        r.method.toLowerCase().includes(term)
    );
  });

  ngOnInit(): void {
    this.loadResources();
  }

  loadResources(): void {
    this.loading.set(true);
    this.rbacService.getResources().subscribe({
      next: (data) => {
        this.resources.set(data);
        this.loading.set(false);
      },
      error: () => {
        this.loading.set(false);
        this.messageService.add({
          severity: 'error',
          summary: 'Error',
          detail: 'No se pudieron cargar los recursos.',
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
