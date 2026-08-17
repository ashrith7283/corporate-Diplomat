import { Component } from '@angular/core';
import { TranslatorComponent } from './components/translator/translator.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [TranslatorComponent],
  template: `<app-translator></app-translator>`
})
export class AppComponent {}
