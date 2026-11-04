import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ButtonModule } from 'primeng/button';
import { TagModule } from 'primeng/tag';
import { MessageService } from 'primeng/api';
import { AuthService } from '../../../core/services/auth.service';
import { UserProfile } from '../../../core/models/auth.model';

@Component({
  selector: 'app-profile',
  standalone: true,
  imports: [CommonModule, ButtonModule, TagModule],
  templateUrl: './profile.html',
  styleUrl: './profile.css',
})
export class ProfileComponent implements OnInit {
  protected readonly authService = inject(AuthService);
  private readonly messageService = inject(MessageService);

  profile = signal<UserProfile | null>(null);
  loading = signal<boolean>(false);

  ngOnInit(): void {
    this.loadProfile();
  }

  loadProfile(): void {
    this.loading.set(true);
    this.authService.getProfile().subscribe({
      next: (user) => {
        this.profile.set(user);
        this.loading.set(false);
      },
      error: () => {
        this.loading.set(false);
        this.messageService.add({
          severity: 'error',
          summary: 'Error',
          detail: 'No se pudo obtener la información del perfil autenticado.',
        });
      },
    });
  }

  onLogout(): void {
    this.authService.logout();
    this.messageService.add({
      severity: 'info',
      summary: 'Sesión Finalizada',
      detail: 'Has cerrado sesión exitosamente de TazaNorte.',
    });
  }
}

