import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { HttpModule } from '@angular/http';


import { AppComponent } from './app.component';
import { NavbarComponent } from './navbar/navbar.component';
import { KalkulatorComponent } from './body/kalkulator/kalkulator.component';
import { KalService } from './shared/services/kal.service';


@NgModule({
  declarations: [
    AppComponent,
    NavbarComponent,
    KalkulatorComponent
  ],
  imports: [
    BrowserModule,
    HttpModule
  ],
  providers: [KalService],
  bootstrap: [AppComponent]
})
export class AppModule { }
