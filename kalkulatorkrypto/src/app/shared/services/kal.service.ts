import { Injectable } from '@angular/core';
import { Http } from '@angular/http';


@Injectable()
export class KalService {

  constructor(private http: Http) {


  }

  getData(){
    return this.http.get("https://bitbay.net/en/fees");

  }

}
