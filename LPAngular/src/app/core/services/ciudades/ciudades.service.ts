import { Injectable } from '@angular/core';
import { environment } from '../../../../environments/environment';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class CiudadesService {
  private url = environment.apiUrl;

  constructor(private http: HttpClient) { }

  get():Observable<any> {
    return this.http.get<any>(`${this.url}/ciudades/`)
  }
}
