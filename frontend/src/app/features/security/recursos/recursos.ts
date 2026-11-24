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
        return 'bg-blue-500/10 text-blue-400 border-blue-500/30';
      case 'POST':
        return 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30';
      case 'PUT':
        return 'bg-amber-500/10 text-amber-400 border-amber-500/30';
      case 'PATCH':
        return 'bg-purple-500/10 text-purple-400 border-purple-500/30';
      case 'DELETE':
        return 'bg-rose-500/10 text-rose-400 border-rose-500/30';
      default:
        return 'bg-slate-500/10 text-slate-400 border-slate-500/30';
    }
  }
}
