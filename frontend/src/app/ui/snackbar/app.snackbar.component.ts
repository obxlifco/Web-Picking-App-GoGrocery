import {Component,Inject} from '@angular/core';
import {MAT_SNACK_BAR_DATA} from '@angular/material';


@Component({
  templateUrl: './product_detail_snakbar.html',
})
export class ProductDetailSnakbarComponent {

	constructor(@Inject(MAT_SNACK_BAR_DATA) public data: any) { }

	
}