import {Component, signal} from '@angular/core';
import {Login} from './components/admin/login/login';
import {BarraMenuMovil} from './components/menuHome-movil/barra-menu-movil';
import {NgClass} from '@angular/common';
import {RouterLink} from '@angular/router';
import {CookieService} from 'ngx-cookie-service';
import {AlertasServices} from '../../core/utils/alertas/alertas.services';
import {BaseModal} from '../../shared/components/modals/base-modal/base-modal';
import {CategoriaInterface} from '../../core/interfaces/categoriaInterface';
import {CajaNotis} from './components/caja-notis/caja-notis';
import {ClicOutside} from '../../shared/directives/clic-outside';

@Component({
  selector: 'app-main-layout',
  imports: [
    Login,
    BarraMenuMovil,
    NgClass,
    RouterLink,
    CajaNotis,
    ClicOutside,
  ],
  templateUrl: './main-layout.html',
  styleUrl: './main-layout.scss',
  standalone: true,
})
export class MainLayout {


  constructor(
    private cookieService: CookieService,
    private alertasServises: AlertasServices,
  ) {}

  openLogin = signal<boolean>(false);

  toggleLogin = () => {
    this.openLogin.update(state => !state);
  }
  openCajitaNotis = signal<boolean>(false);

  toggleCajitaNotis() {
    this.openCajitaNotis.update(state => !state);
  }
  openBarra = signal<boolean>(false);
  toggleBarra = () => {
    this.openBarra.update(state => !state);
  }

  existeToken() {
    let existe = false
    const cookie = this.cookieService.get('token_usuario');
    if (cookie) {
      existe = true;
      return existe;
    }
    return existe;
  }

  verProductos(event: Event) {
    if (!this.existeToken()) {
      event.preventDefault();
      // this.alertasServises.alert("ERROR","Ántes debes loguearte","info")
      this.alertasServises.mensajeFaltaLogin("Oops...","Para acceder debes loguearte", "/icons/iconErr.svg")
    }
  }

}
