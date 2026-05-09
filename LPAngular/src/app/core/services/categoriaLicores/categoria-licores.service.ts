import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../../environments/environment';

@Injectable({
  providedIn: 'root',
})
export class CategoriaLicoresService {
  private url = environment.apiUrl;

  constructor(private http: HttpClient) { }

  getCategorias(): Observable<any> {
    return this.http.get<any>(`${this.url}/secciones/`);
  }
}
