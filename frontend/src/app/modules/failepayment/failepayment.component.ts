import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-failepayment',
  templateUrl: './failepayment.component.html',
  styleUrls: ['./failepayment.component.css']
})
export class FailepaymentComponent implements OnInit {
  public orderId = '';
  public paymentStatus = '';
  public responseMessage = '';
  constructor(
    private _activeRoute:ActivatedRoute
  ) { 
    this.orderId = this._activeRoute.snapshot.params['id'];
    this.paymentStatus = this._activeRoute.snapshot.params['status'];
    this.responseMessage = this._activeRoute.snapshot.params['message'];
  }

  ngOnInit() {
  }

}
