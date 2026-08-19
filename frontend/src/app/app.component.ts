import { Component, OnInit, inject } from '@angular/core';
import { Meta, Title } from '@angular/platform-browser';
import { TranslatorComponent } from './components/translator/translator.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [TranslatorComponent],
  template: `<app-translator></app-translator>`
})
export class AppComponent implements OnInit {
  private title = inject(Title);
  private meta = inject(Meta);

  ngOnInit() {
    this.title.setTitle('Corporate Diplomat — Translate Casual to Corporate & Corporate to Casual');

    this.meta.updateTag({
      name: 'description',
      content: 'Corporate Diplomat is the free online translator that converts casual language into corporate jargon and decodes corporate speak into plain English. Powered by AI and a curated glossary of 80+ business terms.'
    });
    this.meta.updateTag({
      name: 'keywords',
      content: 'corporate diplomat, corporate translator, casual to corporate, corporate to casual, business jargon translator, decode corporate speak, AI translator'
    });

    this.meta.updateTag({ property: 'og:title', content: 'Corporate Diplomat — Casual ↔ Corporate Translator' });
    this.meta.updateTag({
      property: 'og:description',
      content: 'Free AI-powered translator that turns everyday language into polished corporate jargon — and decodes business buzzwords back into plain English.'
    });
    this.meta.updateTag({ property: 'og:url', content: 'https://corporate-diplomat-frontend.onrender.com/' });

    this.meta.updateTag({ name: 'twitter:title', content: 'Corporate Diplomat — Casual ↔ Corporate Translator' });
    this.meta.updateTag({
      name: 'twitter:description',
      content: 'Translate between casual and corporate language instantly. Free AI tool with a curated business glossary.'
    });
  }
}
