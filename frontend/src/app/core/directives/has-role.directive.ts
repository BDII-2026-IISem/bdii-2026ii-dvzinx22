import { Directive, Input, TemplateRef, ViewContainerRef, inject, effect } from '@angular/core';
import { AuthService } from '../services/auth.service';

@Directive({
  selector: '[appHasRole]',
  standalone: true,
})
export class HasRoleDirective {
  private readonly templateRef = inject(TemplateRef<unknown>);
  private readonly viewContainer = inject(ViewContainerRef);
  private readonly authService = inject(AuthService);

  private requiredRoles: string[] = [];
  private isRendered = false;

  constructor() {
    effect(() => {
      const isAuth = this.authService.isAuthenticated();
      const user = this.authService.currentUser();
      this.evaluatePermission(isAuth, user?.username);
    });
  }

  @Input() set appHasRole(roles: string | string[]) {
    this.requiredRoles = Array.isArray(roles) ? roles : [roles];
    const isAuth = this.authService.isAuthenticated();
    const user = this.authService.currentUser();
    this.evaluatePermission(isAuth, user?.username);
  }

  private evaluatePermission(isAuth: boolean, username?: string): void {
    if (!isAuth) {
      this.clear();
      return;
    }

    // El superusuario/admin siempre tiene acceso completo
    if (username === 'admin' || this.requiredRoles.length === 0) {
      this.render();
      return;
    }

    // Comprobación de rol
    const hasRole = this.requiredRoles.includes(username || '');
    if (hasRole) {
      this.render();
    } else {
      this.clear();
    }
  }

  private render(): void {
    if (!this.isRendered) {
      this.viewContainer.createEmbeddedView(this.templateRef);
      this.isRendered = true;
    }
  }

  private clear(): void {
    if (this.isRendered) {
      this.viewContainer.clear();
      this.isRendered = false;
    }
  }
}

