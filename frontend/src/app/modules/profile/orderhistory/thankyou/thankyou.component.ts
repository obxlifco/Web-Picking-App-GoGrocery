import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute, NavigationEnd } from '@angular/router';

@Component({
  selector: 'app-thankyou',
  templateUrl: './thankyou.component.html',
  styleUrls: ['./thankyou.component.css']
})
export class ThankyouComponent implements OnInit {
  public sub:any;
  public orderId = '';
  constructor(
    private _activeRoute:ActivatedRoute,
    public router:Router

  ) {
    // this.orderId = this._activeRoute.snapshot.params['id'];
    let data=this._activeRoute.snapshot.params;
    this.orderId = data['order_id'];

   }

  ngOnInit() {
  }

}
