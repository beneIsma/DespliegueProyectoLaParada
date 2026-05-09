import { Injectable } from '@angular/core';
import { environment } from '../../../../environments/environment';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class ProductosService {

    private url = environment.apiUrl;

    constructor(private http: HttpClient) { }

    obtenerProductos(): Observable<any> {
      return this.http.get<any>(`${this.url}/productos/`);
    }
}
