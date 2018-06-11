import { Kalkulator } from './../../shared/services/kal.model';
import { Component, OnInit, NgModule } from '@angular/core';
import { KalService } from '../../shared/services/kal.service';
import { HtmlParser } from '@angular/compiler';
import { NgForm } from '@angular/forms';



@Component({
  selector: 'app-kalkulator',
  templateUrl: './kalkulator.component.html',
  styleUrls: ['./kalkulator.component.css']
})
export class KalkulatorComponent implements OnInit {
  bitbay = {
    BTC: 0.00045,
    LTC: 0.005,
    ETH: 0.00126,
    LSK: 0.2,
    BCC: 0.0006,
    GAME: 0.005,
    DASH: 0.001,
    BTG: 0.0008,
    KZC: 0.0005,
    XIN: 2,
    XRP: 0.1,
  }

  bitbayBids = {
    LTC: [],
    ETH: [],
    LSK: [],
    BCC: [],
    GAME: [],
    DASH: [],
    BTG: [],
    KZC: [],
    XIN: [],
    XRP: [],
  }

  bitbayAsks = {
    LTC: [],
    ETH: [],
    LSK: [],
    BCC: [],
    GAME: [],
    DASH: [],
    BTG: [],
    KZC: [],
    XIN: [],
    XRP: [],
  }

  wynik: any[] = []
  // bitbay:string[] = ['BTC', ]


  bitbayKeys: string[] = Object.keys(this.bitbay);

  poloniexFee: any[];

  bitbayFee;

  polkeys: string[];

  polOrderbook: any[]

  kupWalute: number;





  constructor(private klServ: KalService) {
    // ([aA-zZ]{3,4}:\s[0-9]{0,5}(\.*[0-9]{0,8})


    klServ.getBitbayFee().subscribe(d => this.bitbayFee = this.parseBitbay(d["_body"]));

    klServ.getPoloniexFee().subscribe(d => this.poloniexFee = d.json());

    // pobieram orderbook z poloniex
    klServ.getPoloniexOrderbook().subscribe(d => {
      this.polkeys = Object.keys(d.json());
      this.polOrderbook = d.json();

    })

    for (let i = 0; i < this.bitbayKeys.length; i++) {

      klServ.getBitbayOrderbook(this.bitbayKeys[i]).subscribe(d => {
        if (this.bitbayKeys[i] != "BTC") {
          this.bitbayBids[this.bitbayKeys[i]] = d.json()['bids'][0];
          this.bitbayAsks[this.bitbayKeys[i]] = d.json()['asks'][0];
        }

      })

    }



  }

  polFee() {

  }

  parseBitbay(str) {
    let myRe = /[aA-zZ]{3,4}:\s[0-9]{1,6}(\.*[0-9]{0,8})/g;
    let waluta_fee: string[] = [];
    let myArray: any[];


    let i = 0;
    while ((myArray = myRe.exec(str)) !== null && i < 11) {
      let msg: string = myArray[0];
      if (msg.substring(0, 3) != "NIP") {
        waluta_fee.push(msg);
      }
      i++;
    }
    // return [ "BTC: 0.00045", "LTC: 0.005"]
    return waluta_fee;

  }


  matchAll(str, regex) {
    let res = [];
    let m;
    if (regex.global) {
      while (m = regex.exec(str)) {
        res.push(m[1]);
      }
    } else {
      if (m = regex.exec(str)) {
        res.push(m[1]);
      }
    }
    return res;
  }


  dodajKalk(f: NgForm) {

    if (f.value.bazowa == "Poloniex") {
      this.kupPoloniex(f);
    } else if (f.value.bazowa == "Bitbay") {
      this.kubBitbay(f);
    }

    // f.resetForm();
  }

  kubBitbay(f: NgForm) {
    this.wynik = []
    let ilosc: number = f.value.ilosc;

    for (let i = 0; i < this.polkeys.length; i++) {
      if (this.polkeys[i].substr(0, 3) === "BTC") {
        // this.polOrderbook[this.polkeys[i]]["asks"][0] -- zwraca ["0.00002386", 24.71649195] cene i ilosc
        let waluta_waluta: string[] = this.polkeys[i].split('_');

        if (-1 != this.bitbayKeys.indexOf(waluta_waluta[1]) && this.bitbayKeys[i] != "BTC") {
          this.kupWalute = ilosc / this.bitbayAsks[waluta_waluta[1]][0];
          this.kupWalute -= this.bitbay[waluta_waluta[1]];
          this.kupWalute = this.polOrderbook[this.polkeys[i]]["bids"][0][0] * this.kupWalute
          this.wynik.push([waluta_waluta[1], this.kupWalute])

        } else if (waluta_waluta[1] == 'BCH') {
          console.log(this.bitbayAsks["BCC"][0]);

          this.kupWalute = ilosc / this.bitbayAsks["BCC"][0];
          console.log(this.bitbay[waluta_waluta[1]])
          this.kupWalute -= this.bitbay['BCC'];
          console.log(this.polOrderbook[this.polkeys[i]]["bids"][0][0]);

          this.kupWalute = this.polOrderbook[this.polkeys[i]]["bids"][0][0] * this.kupWalute;
          this.wynik.push(['BCC', this.kupWalute]);

        }
      }
    }
    let withoutWithdraw: number = ilosc - this.bitbay["BTC"];
    this.wynik.push(["BTC", withoutWithdraw]);
    this.wynik.sort((a: any, b: any) => {
      return + b[1] - +a[1];
    });
    // console.log(this.wynik);
    for (let entry of this.wynik) {
      entry[1] = Math.round(entry[1] *100000000)/100000000
      // console.log(entry)
    
  }

  }




  kupPoloniex(f: NgForm) {
    this.wynik = []
    let ilosc: number = f.value.ilosc;

    for (let i = 0; i < this.polkeys.length; i++) {
      if (this.polkeys[i].substr(0, 3) === "BTC") {
        // this.polOrderbook[this.polkeys[i]]["asks"][0] -- zwraca ["0.00002386", 24.71649195] cene i ilosc
        let waluta_waluta: string[] = this.polkeys[i].split('_');

        if (-1 != this.bitbayKeys.indexOf(waluta_waluta[1]) && this.bitbayKeys[i] != "BTC") {

          this.kupWalute = ilosc / this.polOrderbook[this.polkeys[i]]["asks"][0][0];
          this.kupWalute -= this.poloniexFee[waluta_waluta[1]]['txFee'];

          this.kupWalute = this.bitbayBids[waluta_waluta[1]][0] * this.kupWalute
          this.wynik.push([waluta_waluta[1], this.kupWalute])
        } else if (waluta_waluta[1] == 'BCH') {

          this.kupWalute = ilosc / this.polOrderbook[this.polkeys[i]]["asks"][0][0];
          this.kupWalute -= this.poloniexFee[waluta_waluta[1]]['txFee'];
          this.kupWalute = this.bitbayBids["BCC"][0] * this.kupWalute;
          this.wynik.push([waluta_waluta[1], this.kupWalute]);

        }

      }
    }
    let withoutWithdraw: number = ilosc - this.poloniexFee["BTC"]['txFee'];
    this.wynik.push(["BTC", withoutWithdraw]);
    this.wynik.sort((a: any, b: any) => {
      return + b[1] - +a[1];
      
    });
    // console.log(this.wynik);
    // console.log(Math.round(this.wynik[1][1] *10000000)/10000000)
    // Math.round(this.wynik[0][1]*10000000)/10000000
    // Math.round(this.wynik[1][1]*10000000)/10000000
    // Math.round(this.wynik[2][1]*10000000)/10000000
    // Math.round(this.wynik[3][1]*10000000)/10000000
    // Math.round(this.wynik[4][1]*10000000)/10000000
    // Math.round(this.wynik[5][1]*10000000)/10000000
    // Math.round(this.wynik[6][1]*10000000)/10000000
    // Math.round(this.wynik[7][1]*10000000)/10000000

    for (let entry of this.wynik) {
      entry[1] = Math.round(entry[1] *100000000)/100000000
      // console.log(entry)
    
  }
  


  }

  
  






  ngOnInit() {
  }

}
