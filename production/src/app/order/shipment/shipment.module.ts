import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BrowserModule } from '@angular/platform-browser';

import { BmscommonModule } from '../../bmscommon.module';
import { ShipmentRoutingModule } from './shipment-routing.module';

import { NgxBarcodeModule } from 'ngx-barcode';
import { NgxDaterangepickerMd } from 'ngx-daterangepicker-material';
import { ColorPickerModule } from 'ngx-color-picker';

import { NgSelectModule } from '@ng-select/ng-select';
import { ShipmentComponent, PicklistComponent }  from '../../order/shipment/order.shipment.component';
import { 
        ShipmentAddEditComponent, ShipmentInvoiceComponent,ShipmentLabelComponent,DeliveryPlannerComponent,
        ShipmentManifestComponent,ManageCrateComponent,GrnOrderProductComponent,AssignVehicleComponent,EditGRNComponent,EditPriceComponent,AddSubstituteProductComponent
    }  from '../../order/shipment/order.shipment.addedit.component';
import { OwlDateTimeModule, OwlNativeDateTimeModule } from 'ng-pick-datetime';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
@NgModule({
  imports: [
    CommonModule,
    ShipmentRoutingModule,
    BmscommonModule,
    NgxBarcodeModule,
    NgxDaterangepickerMd,
    ColorPickerModule,
    OwlDateTimeModule,
    OwlNativeDateTimeModule,
    FormsModule,
    ReactiveFormsModule,
    NgSelectModule,
  ],
  declarations: [
    ShipmentComponent,
    PicklistComponent,
    ShipmentAddEditComponent,
    ShipmentInvoiceComponent,
    ShipmentLabelComponent,
    ShipmentManifestComponent,
    ManageCrateComponent,
    GrnOrderProductComponent,
    DeliveryPlannerComponent,
    AssignVehicleComponent,
    EditGRNComponent,
    EditPriceComponent,
    AddSubstituteProductComponent
  ],
  entryComponents: [ 
  	ShipmentComponent,
    PicklistComponent,
    ShipmentAddEditComponent,
    ShipmentInvoiceComponent,
    ShipmentLabelComponent,
    ShipmentManifestComponent,
    ManageCrateComponent,
    GrnOrderProductComponent,
    AssignVehicleComponent,
    EditGRNComponent,
    EditPriceComponent,
    AddSubstituteProductComponent
  ]
})
export class ShipmentModule { }
