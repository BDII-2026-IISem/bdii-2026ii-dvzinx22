import { Component, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { InputTextModule } from 'primeng/inputtext';
import { PasswordModule } from 'primeng/password';
import { ButtonModule } from 'primeng/button';
import { MessageService } from 'primeng/api';
import { AuthService } from '../../../core/services/auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    InputTextModule,
    PasswordModule,
    ButtonModule,
  ],
  templateUrl: './login.html',
  styleUrl: './login.css',
})
export class LoginComponent {
  private readonly fb = inject(FormBuilder);
  private readonly authService = inject(AuthService);
  private readonly router = inject(Router);
  private readonly messageService = inject(MessageService);

  loading = signal<boolean>(false);
  errorMessage = signal<string | null>(null);

  loginForm: FormGroup = this.fb.group({
    usernameOrEmail: ['', [Validators.required, Validators.minLength(3)]],
    password: ['', [Validators.required, Validators.minLength(4)]],
  });

  onSubmit(): void {
    if (this.loginForm.invalid) {
      this.loginForm.markAllAsTouched();
      return;
    }

    this.loading.set(true);
    this.errorMessage.set(null);

    const val = this.loginForm.value;
    const isEmail = val.usernameOrEmail.includes('@');
    const payload = {
      ...(isEmail ? { email: val.usernameOrEmail } : { username: val.usernameOrEmail }),
      password: val.password,
    };

    this.authService.login(payload).subscribe({
      next: (tokens) => {
        this.loading.set(false);
        this.messageService.add({
          severity: 'success',
          summary: 'Inicio de Sesión Exitoso',
          detail: 'Bienvenido al Sistema de Gestión TazaNorte.',
        });
        this.router.navigate(['/']);
      },
      error: (err) => {
        this.loading.set(false);
        const detail = err?.error?.detail || 'Credenciales inválidas. Verifique usuario y contraseña.';
        this.errorMessage.set(detail);
        this.messageService.add({
          severity: 'error',
          summary: 'Error de Autenticación',
          detail: detail,
        });
      },
    });
  }
}

