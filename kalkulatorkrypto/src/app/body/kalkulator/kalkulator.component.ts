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
        // d.json()['bids'][0];
        if (this.bitbayKeys[i] != "BTC") {
          this.bitbayBids[this.bitbayKeys[i]] = d.json()['bids'][0]

          // console.log( d.json()['bids'][0]);;
          //  console.log(d.json()['bids'][0]);  
        }

      })

    }



  }

  polFee() {

  }

  parseBitbay(str) {
    // re = /\s*([^[:]+):\"([^"]+)"/g;
    var myRe = /[aA-zZ]{3,4}:\s[0-9]{1,6}(\.*[0-9]{0,8})/g;
    // var str = "abbcdefabh";
    let waluta_fee: string[] = [];
    let myArray: any[];


    let i = 0;
    while ((myArray = myRe.exec(str)) !== null && i < 11) {
      var msg: string = myArray[0];
      if (msg.substring(0, 3) != "NIP") {
        // let wal_cena :string[] =msg.split(':')
        // console.log(msg.split(':'));
        waluta_fee.push(msg);
      }
      // msg += "Next match starts at " + myRe.lastIndex;
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

    // let kalk: Kalkulator  = new Kalkulator();
    // kalk.ilosc = f.value.ilosc;

    // bez przewalutowania

    // pokauzje pierwsza oferte kupna 
    this.kupPoloniex(f);


    // f.resetForm();
  }





  kupPoloniex(f: NgForm) {
    let ilosc: number = f.value.ilosc;
    // console.log(this.bitbayKeys);
    // console.log(this.polkeys);
    // ilosc -= this.poloniexFee['BTC']['txFee'];

    for (let i = 0; i < this.polkeys.length; i++) {
      if (this.polkeys[i].substr(0, 3) === "BTC") {
        // this.polOrderbook[this.polkeys[i]]["asks"][0] -- zwraca ["0.00002386", 24.71649195] cene i ilosc
        // odejmuje fee
        let waluta_waluta: string[] = this.polkeys[i].split('_');

        if (-1 != this.bitbayKeys.indexOf(waluta_waluta[1]) && this.bitbayKeys[i] != "BTC") {

          this.kupWalute = ilosc / this.polOrderbook[this.polkeys[i]]["asks"][0][0];
          this.kupWalute -= this.poloniexFee[waluta_waluta[1]]['txFee'];

          this.kupWalute = this.bitbayBids[waluta_waluta[1]][0] * this.kupWalute
          // console.log(this.kupWalute);
          console.log(this.bitbayBids[waluta_waluta[1]][0]);
        }

        // console.log(waluta_waluta[1]);

        console.log(this.kupWalute);
      }
    }
  }






  ngOnInit() {
  }

}
