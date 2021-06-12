import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-successpayment',
  templateUrl: './successpayment.component.html',
  styleUrls: ['./successpayment.component.css']
})
export class SuccesspaymentComponent implements OnInit {
  public orderId = '';
  constructor(
    private _activeRoute:ActivatedRoute
  ) { 
    this.orderId = this._activeRoute.snapshot.params['id'];
  }

  ngOnInit() {
  }

}
