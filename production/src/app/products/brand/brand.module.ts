import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BrandComponent }  from '../../products/brand/products.brand.component';
import { BmscommonModule } from '../../bmscommon.module';
import { BrandAddEditComponent } from '../../products/brand/products.brand.addedit.component';
import { BrandRoutingModule } from './brand-routing.module';

@NgModule({
  declarations: [
  	BrandComponent,
  	BrandAddEditComponent,

  ],
  imports: [
    CommonModule,
    BrandRoutingModule,
    BmscommonModule,
  ],
  entryComponents: [
  	BrandAddEditComponent
  ]
})
export class BrandModule { }
