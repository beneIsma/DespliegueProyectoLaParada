import { Injectable } from '@angular/core';
import { environment } from '../../../../environments/environment';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class AuthServiceService {

  private url = environment.apiUrl;

  constructor(private http: HttpClient) { }

  login(datos:any): Observable<any> {
    return this.http.post<any>(`${this.url}/login/`,datos)
  }

  registro(datos:any): Observable<any> {
    return this.http.post<any>(`${this.url}/registro/`,datos)
  }
}
