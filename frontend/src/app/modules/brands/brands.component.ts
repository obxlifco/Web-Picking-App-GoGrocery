import { Component, OnInit } from '@angular/core';
import { Router,ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-brands',
  templateUrl: './brands.component.html',
  styleUrls: ['./brands.component.css']
})
export class BrandsComponent implements OnInit {

  constructor(private _route:ActivatedRoute) { }
  public brand_id:any;

  ngOnInit() {
  // get category id from the  url
  	this._route.params.subscribe(params => { 
        this.brand_id = params['id']; 

    });
  }

}
