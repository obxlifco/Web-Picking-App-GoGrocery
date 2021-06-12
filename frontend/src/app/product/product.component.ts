import { Component, OnInit } from '@angular/core';
import { Router,ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-product',
  templateUrl: './product.component.html',
  styleUrls: ['./product.component.css']
})
export class ProductComponent implements OnInit {

  constructor( private _route: ActivatedRoute) { }
  public product_id:any;
  ngOnInit() {
  	// get id or slug from the  url
  	this._route.params.subscribe(params => { 
        this.product_id = params['id_slug']; 
        
    });
  }

}
