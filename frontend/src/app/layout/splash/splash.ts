import { Component, EventEmitter, Output, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-splash',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './splash.html',
  styleUrl: './splash.css',
})
export class SplashComponent implements OnInit {
  @Output() completed = new EventEmitter<void>();

  progress = signal<number>(0);
  statusText = signal<string>('Moliendo granos de origen...');
  fadingOut = signal<boolean>(false);

  private readonly phrases = [
    'Moliendo granos de origen...',
    'Calentando el agua a 92°C...',
    'Extrayendo espresso con crema dorada...',
    'Cargando catálogo gourmet y seguridad RBAC...',
    '¡Listo para servir!',
  ];

  ngOnInit(): void {
    let currentProgress = 0;
    const interval = setInterval(() => {
      currentProgress += 2;
      this.progress.set(currentProgress);

      const phraseIdx = Math.min(
        Math.floor((currentProgress / 100) * this.phrases.length),
        this.phrases.length - 1
      );
      this.statusText.set(this.phrases[phraseIdx]);

      if (currentProgress >= 100) {
        clearInterval(interval);
        setTimeout(() => this.finish(), 400);
      }
    }, 40); // 100 * 40ms = 4 segundos de experiencia fluida
  }

  finish(): void {
    this.fadingOut.set(true);
    setTimeout(() => {
      this.completed.emit();
    }, 600);
  }
}
