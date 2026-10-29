import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { ToastModule } from 'primeng/toast';
import { ConfirmDialogModule } from 'primeng/confirmdialog';
import { NavbarComponent } from './layout/navbar/navbar';
import { SidebarComponent } from './layout/sidebar/sidebar';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, ToastModule, ConfirmDialogModule, NavbarComponent, SidebarComponent],
  templateUrl: './app.html',
  styleUrl: './app.css',
})
export class App {}
