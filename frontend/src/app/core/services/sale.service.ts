import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { Sale, SaleRegisterPayload } from '../models/sale.model';

@Injectable({
  providedIn: 'root',
})
export class SaleService {
  private readonly http = inject(HttpClient);
  private readonly baseUrl = `${environment.apiUrl}/sales/`;

  getAll(): Observable<Sale[]> {
    return this.http.get<Sale[]>(this.baseUrl);
  }

  getById(id: number): Observable<Sale> {
    return this.http.get<Sale>(`${this.baseUrl}${id}/`);
  }

  createSale(payload: SaleRegisterPayload): Observable<Sale> {
    return this.http.post<Sale>(this.baseUrl, payload);
  }

  voidSale(id: number): Observable<void> {
    return this.http.delete<void>(`${this.baseUrl}${id}/`);
  }
}

