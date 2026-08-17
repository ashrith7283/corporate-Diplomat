import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { TranslateRequest, TranslateResponse } from '../models/translate.model';

@Injectable({
  providedIn: 'root'
})
export class TranslateService {
  private apiUrl = 'http://localhost:8000/api/translate';

  constructor(private http: HttpClient) {}

  translate(request: TranslateRequest): Observable<TranslateResponse> {
    return this.http.post<TranslateResponse>(this.apiUrl, request);
  }
}
