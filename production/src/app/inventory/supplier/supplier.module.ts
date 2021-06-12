import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BrowserModule } from '@angular/platform-browser';

import { BmscommonModule } from '../../bmscommon.module';
import { SupplierRoutingModule } from './supplier-routing.module';

import { SupplierComponent }  from '../../inventory/supplier/inventory.supplier.component';
import { SupplierPOComponent } from '../../inventory/supplier/inventory.supplier.po.component';
import { SupplierAddEditComponent }  from '../../inventory/supplier/inventory.supplier.addedit.component';
import { NgSelectModule } from '@ng-select/ng-select';
@NgModule({
  imports: [
    CommonModule,
    SupplierRoutingModule,
    BmscommonModule,
    NgSelectModule
  ],
  declarations: [
    SupplierComponent,
    SupplierPOComponent,
    SupplierAddEditComponent
  ],
  entryComponents: [ 
  	SupplierComponent,
    SupplierPOComponent,
    SupplierAddEditComponent
  ]
})
export class SupplierModule { }