import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute, NavigationEnd } from '@angular/router';

@Component({
  selector: 'app-success',
  templateUrl: './successSubstitute.component.html',
  styleUrls: ['./successSubstitute.component.css']
})
export class SuccessSubstituteComponent implements OnInit {
  public sub:any;
  public orderId = '';
  public pageData:any={}
  constructor(
    private _activeRoute:ActivatedRoute
  ) {
    // this.orderId = this._activeRoute.snapshot.params['id'];
    this.orderId = '2841';
    /*console.log("***************** Order id ****************");
    console.log(this.orderId);*/

   }

  ngOnInit() {
    
    this.sub = this._activeRoute.data.subscribe(v => {
      if(v.page=='thank-you'){
        let pageData:any={}
        pageData.name='Thank You';
        pageData.link='thank-you';
        this.pageData=pageData;
      }
    });

  }

}