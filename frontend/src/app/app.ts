import { Component, inject, signal } from '@angular/core';
import { Router, RouterOutlet } from '@angular/router';
import { ToastModule } from 'primeng/toast';
import { ConfirmDialogModule } from 'primeng/confirmdialog';
import { NavbarComponent } from './layout/navbar/navbar';
import { SidebarComponent } from './layout/sidebar/sidebar';
import { SplashComponent } from './layout/splash/splash';
import { AuthService } from './core/services/auth.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    RouterOutlet,
    ToastModule,
    ConfirmDialogModule,
    NavbarComponent,
    SidebarComponent,
    SplashComponent,
  ],
  templateUrl: './app.html',
  styleUrl: './app.css',
})
export class App {
  private readonly router = inject(Router);
  protected readonly authService = inject(AuthService);

  showSplash = signal<boolean>(!sessionStorage.getItem('tazanorte_intro_seen'));

  onSplashComplete(): void {
    sessionStorage.setItem('tazanorte_intro_seen', 'true');
    this.showSplash.set(false);

    // Si no está autenticado, llevarlo suavemente al login
    if (!this.authService.isAuthenticated()) {
      this.router.navigate(['/login']);
    }
  }
}
