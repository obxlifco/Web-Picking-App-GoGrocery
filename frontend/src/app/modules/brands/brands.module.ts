import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BrowserModule } from '@angular/platform-browser';

import { BrandsRoutingModule } from './brands.routing.module'; 

import { BrandsComponent }  from './brands.component';
@NgModule({
  imports: [
    CommonModule,
    BrandsRoutingModule,
      ],
  declarations: [
  	BrandsComponent
  ],
  entryComponents: [
  	BrandsComponent
  ]
})
export class BrandsModule { }
