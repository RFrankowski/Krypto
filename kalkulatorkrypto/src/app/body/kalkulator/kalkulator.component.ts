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

  bitbayKeys =  Object.keys(this.bitbay);

  poloniexFee: any[];

  bitbayFee;

  polkeys: string[];

  polOrderbook: any[]

  kupWalute: number;
  constructor(private klServ: KalService) {
    // ([aA-zZ]{3,4}:\s[0-9]{0,5}(\.*[0-9]{0,8})


    klServ.getBitbayFee().subscribe(d => this.bitbayFee = this.matchAll(d["_body"], /[aA-zZ]{3,4}:\s[0-9](\.*[0-9]{0,8})/));
    // klServ.getPoloniexFee().subscribe(d => this.poloniexFee = [d.json()]);

    // pobieram orderbook z poloniex
    klServ.getPoloniexOrderbook().subscribe(d => {
      this.polkeys = Object.keys(d.json());
      this.polOrderbook = d.json();

    })


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

    // pokauzje pierwsza oferte kupna 
    
    this.kupPoloniex(f);


    // f.resetForm();
  }

  kupBitbay(){
    

  }



  kupPoloniex(f :NgForm){
    for (let i = 0; i < this.polkeys.length; i++) {
      if (this.polkeys[i].substr(0, 3) === "BTC") {
        // this.polOrderbook[this.polkeys[i]]["asks"][0] -- zwraca ["0.00002386", 24.71649195] cene i ilosc
        this.kupWalute = f.value.ilosc / this.polOrderbook[this.polkeys[i]]["asks"][0][0];
        console.log(this.kupWalute);
        // console.log(this.polkeys[i].split("_"))
      }
    }
  }

  ngOnInit() {
  }

}
