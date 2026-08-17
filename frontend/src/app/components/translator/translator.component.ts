import { Component, signal, OnInit, PLATFORM_ID, inject } from '@angular/core';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { TranslateService } from '../../services/translate.service';
import { TranslateResponse } from '../../models/translate.model';

@Component({
  selector: 'app-translator',
  standalone: true,
  templateUrl: './translator.component.html',
  imports: [CommonModule]
})
export class TranslatorComponent implements OnInit {
  direction = signal<'casual_to_corporate' | 'corporate_to_casual'>('casual_to_corporate');
  inputText = signal('');
  outputText = signal('');
  notes = signal('');
  error = signal('');
  loading = signal(false);
  darkMode = signal(false);

  private platformId = inject(PLATFORM_ID);

  constructor(private translateService: TranslateService) {}

  ngOnInit() {
    if (isPlatformBrowser(this.platformId)) {
      this.darkMode.set(document.documentElement.classList.contains('dark'));
    }
  }

  toggleTheme() {
    const next = !this.darkMode();
    this.darkMode.set(next);
    if (isPlatformBrowser(this.platformId)) {
      if (next) {
        document.documentElement.classList.add('dark');
        localStorage.setItem('theme', 'dark');
      } else {
        document.documentElement.classList.remove('dark');
        localStorage.setItem('theme', 'light');
      }
    }
  }

  onInput(event: Event) {
    this.inputText.set((event.target as HTMLTextAreaElement).value);
  }

  setDirection(direction: 'casual_to_corporate' | 'corporate_to_casual') {
    this.direction.set(direction);
  }

  translate() {
    if (!this.inputText().trim()) {
      this.error.set('Please enter some text to translate.');
      return;
    }
    this.error.set('');
    this.notes.set('');
    this.loading.set(true);
    this.translateService.translate({ text: this.inputText(), direction: this.direction() }).subscribe({
      next: (response: TranslateResponse) => {
        this.outputText.set(response.translated);
        this.notes.set(response.notes ?? '');
        this.loading.set(false);
      },
      error: () => {
        this.error.set('Translation failed. Please check that the backend is running and try again.');
        this.loading.set(false);
      }
    });
  }

  swap() {
    if (!this.outputText()) {
      return;
    }
    this.inputText.set(this.outputText());
    this.outputText.set('');
    this.notes.set('');
    this.direction.set(this.direction() === 'casual_to_corporate' ? 'corporate_to_casual' : 'casual_to_corporate');
  }

  copy() {
    if (!this.outputText()) {
      return;
    }
    navigator.clipboard.writeText(this.outputText());
  }
}