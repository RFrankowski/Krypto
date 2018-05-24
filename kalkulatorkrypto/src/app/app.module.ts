import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';


import { AppComponent } from './app.component';
import { NavbarComponent } from './navbar/navbar.component';
import { KalkulatorComponent } from './body/kalkulator/kalkulator.component';


@NgModule({
  declarations: [
    AppComponent,
    NavbarComponent,
    KalkulatorComponent
  ],
  imports: [
    BrowserModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
