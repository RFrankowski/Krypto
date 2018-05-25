import { Component, OnInit } from '@angular/core';
import { KalService } from '../../shared/services/kal.service';
import { HtmlParser } from '@angular/compiler';

@Component({
  selector: 'app-kalkulator',
  templateUrl: './kalkulator.component.html',
  styleUrls: ['./kalkulator.component.css']
})
export class KalkulatorComponent implements OnInit {

  data:HtmlParser;
  constructor(private klServ:KalService) {
    // ([aA-zZ]{3,4}:\s[0-9](\.*[0-9]{0,8})
    klServ.getData().subscribe(d =>  this.data = d["_body"]);
    
   }

  ngOnInit() {
  }

}
