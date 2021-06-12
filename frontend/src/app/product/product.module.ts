import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BrowserModule } from '@angular/platform-browser';

import { ProductRoutingModule } from './product.routing.module'; 

import { ProductComponent }  from './product.component';
@NgModule({
  imports: [
    CommonModule,
    ProductRoutingModule,
      ],
  declarations: [
  	ProductComponent
  ],
  entryComponents: [
  	ProductComponent
  ]
})
export class ProductModule { }
