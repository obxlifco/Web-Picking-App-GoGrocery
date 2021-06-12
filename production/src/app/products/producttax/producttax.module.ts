import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { BmscommonModule } from '../../bmscommon.module';

import { ProducttaxRoutingModule } from './producttax-routing.module';
import { ProducttaxComponent } from '../../products/producttax/producttax.component';
import { ProducttaxAddeditComponent } from '../../products/producttax/producttax.addedit.component';

@NgModule({
  declarations: [
  	ProducttaxComponent,
  	ProducttaxAddeditComponent,
  ],
  imports: [
    CommonModule,
    ProducttaxRoutingModule,
    BmscommonModule,
  ],
  entryComponents : [
  	ProducttaxAddeditComponent,
  ]
})
export class ProducttaxModule { }
