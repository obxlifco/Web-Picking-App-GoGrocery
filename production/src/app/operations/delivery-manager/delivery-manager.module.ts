import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DeliveryManagerRoutingModule } from './delivery-manager-routing.module';
import { BmscommonModule } from '../../bmscommon.module';
import { DeliveryManagerComponent } from './delivery-manager.component';
import { ManagerAddeditComponent } from './manager.addedit.component';
import { NgSelectModule } from '@ng-select/ng-select';
@NgModule({
  declarations: [
    ManagerAddeditComponent,
    DeliveryManagerComponent,
  ],
  imports: [
    CommonModule,
    DeliveryManagerRoutingModule,
    BmscommonModule,
    NgSelectModule
  ]
})
export class DeliveryManagerModule { }
