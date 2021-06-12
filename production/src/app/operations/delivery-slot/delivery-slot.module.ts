import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DeliverySlotRoutingModule } from './delivery-slot-routing.module';
import { DeliverySlotComponent } from './delivery-slot.component';
import { BmscommonModule } from '../../bmscommon.module';
import {NgxMaterialTimepickerModule} from 'ngx-material-timepicker';
import { NgSelectModule } from '@ng-select/ng-select';

@NgModule({
  declarations: [
    DeliverySlotComponent,
  ],
  imports: [
    CommonModule,
    BmscommonModule,
    DeliverySlotRoutingModule,
    NgxMaterialTimepickerModule,
    NgSelectModule
  ]
})
export class DeliverySlotModule { }
