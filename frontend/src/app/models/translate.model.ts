export interface TranslateRequest {
  text: string;
  direction: 'casual_to_corporate' | 'corporate_to_casual';
}

export interface TranslateResponse {
  translated: string;
  notes?: string;
}