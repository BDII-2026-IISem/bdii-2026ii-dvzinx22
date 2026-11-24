import { Component, inject, signal } from '@angular/core';
import { Router, RouterOutlet, NavigationEnd } from '@angular/router';
import { filter } from 'rxjs';
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
  isLoginRoute = signal<boolean>(false);

  constructor() {
    this.checkLogin(this.router.url);
    this.router.events
      .pipe(filter((e): e is NavigationEnd => e instanceof NavigationEnd))
      .subscribe((e) => {
        this.checkLogin(e.urlAfterRedirects || e.url);
      });
  }

  private checkLogin(url: string): void {
    const isLogin = url.includes('/login') || (typeof window !== 'undefined' && window.location.pathname.includes('/login'));
    this.isLoginRoute.set(isLogin);
  }

  onSplashComplete(): void {
    sessionStorage.setItem('tazanorte_intro_seen', 'true');
    this.showSplash.set(false);

    // Si no está autenticado, llevarlo suavemente al login
    if (!this.authService.isAuthenticated()) {
      this.router.navigate(['/login']);
    }
  }
}
