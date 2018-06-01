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
  poloniexFee: any[];
  data: HtmlParser;

  polkeys: string[];

  polOrderbook: any[]

  kupWalute: number;
  constructor(private klServ: KalService) {
    // ([aA-zZ]{3,4}:\s[0-9](\.*[0-9]{0,8})


    klServ.getData().subscribe(d => this.data = d["_body"]);
    // klServ.getPoloniexFee().subscribe(d => this.poloniexFee = [d.json()]);

    klServ.getPoloniexOrderbook().subscribe(d => {
      this.polkeys = Object.keys(d.json());
      this.polOrderbook = d.json();



      //  this.proba =  Array.of(d.json());

    })


  }


  dodajKalk(f: NgForm) {
    // let kalk: Kalkulator  = new Kalkulator();
    // kalk.ilosc = f.value.ilosc;

    // pokauzje pierwsza oferte kupna 
    for (let i = 0; i < this.polkeys.length; i++) {
      if (this.polkeys[i].substr(0, 3) === "BTC") {
        // this.polOrderbook[this.polkeys[i]]["asks"][0] -- zwraca ["0.00002386", 24.71649195] cene i ilosc
        this.kupWalute = f.value.ilosc / this.polOrderbook[this.polkeys[i]]["asks"][0][0];
        console.log(this.kupWalute);
        // console.log(this.polkeys[i].split("_"))
      }
    }



    // f.resetForm();
  }

  ngOnInit() {
  }

}
