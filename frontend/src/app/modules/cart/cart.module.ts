import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BrowserModule } from '@angular/platform-browser';

import { CartRoutingModule } from './cart.routing.module'; 
import { PipeModule} from '../../global/pipes/pipe.module';

import { CartComponent }  from './cart.component';
@NgModule({
  imports: [
    CommonModule,
    CartRoutingModule,
    PipeModule
   ],
  declarations: [
  	CartComponent
  ],
  entryComponents: [
  	CartComponent
  ]
})
export class CartModule { }
