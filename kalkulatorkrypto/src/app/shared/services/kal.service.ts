import { Injectable } from '@angular/core';
import { Http } from '@angular/http';


@Injectable()
export class KalService {

  constructor(private http: Http) {


  }

  getBitbayFee(){
    return this.http.get("https://bitbay.net/en/fees");

  }


  getPoloniexFee(){
    return this.http.get("https://poloniex.com/public?command=returnCurrencies");

   
  }


  getPoloniexOrderbook(){

    return this.http.get("https://poloniex.com/public?command=returnOrderBook&currencyPair=ALL");

  }

  getBitbayOrderbook(waluta:string){

    return this.http.get("https://bitbay.net/API/Public/"+waluta+"BTC/orderbook.json");
    
  }


}
