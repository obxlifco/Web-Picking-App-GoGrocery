import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BrowserModule } from '@angular/platform-browser';

import { BmscommonModule } from '../../bmscommon.module';
import { WarehouseRoutingModule } from './warehouse-routing.module';

import { WarehouseComponent }  from '../../inventory/warehouse/inventory.warehouse.component';
import { WarehouseAddEditComponent }  from '../../inventory/warehouse/inventory.warehouse.addedit.component';
import { GooglePlaceModule } from "ngx-google-places-autocomplete";
import { NgSelectModule } from '@ng-select/ng-select';
@NgModule({
  imports: [
    CommonModule,
    WarehouseRoutingModule,
    BmscommonModule,
    GooglePlaceModule,
    NgSelectModule
  ],
  declarations: [
    WarehouseComponent,
    WarehouseAddEditComponent
  ],
  entryComponents: [ 
  	WarehouseComponent,
    WarehouseAddEditComponent
  ]
})
export class WarehouseModule { }