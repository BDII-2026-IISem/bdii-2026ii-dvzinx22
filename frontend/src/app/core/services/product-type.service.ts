import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { ProductType } from '../models/product-type.model';

@Injectable({
  providedIn: 'root',
})
export class ProductTypeService {
  private readonly http = inject(HttpClient);
  private readonly baseUrl = `${environment.apiUrl}/product-types/`;

  getAll(): Observable<ProductType[]> {
    return this.http.get<ProductType[]>(this.baseUrl);
  }

  getById(id: number): Observable<ProductType> {
    return this.http.get<ProductType>(`${this.baseUrl}${id}/`);
  }

  create(productType: Partial<ProductType>): Observable<ProductType> {
    return this.http.post<ProductType>(this.baseUrl, productType);
  }

  update(id: number, productType: Partial<ProductType>): Observable<ProductType> {
    return this.http.put<ProductType>(`${this.baseUrl}${id}/`, productType);
  }

  delete(id: number): Observable<void> {
    return this.http.delete<void>(`${this.baseUrl}${id}/`);
  }
}

