import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { VehicleRoutingModule } from './vehicle-routing.module';
import { VehicleComponent } from './vehicle.component';
import { vehicleAddEditComponent } from './vehicle.vehicle.addedit.component';
import { BmscommonModule } from '../../bmscommon.module';
import { NgSelectModule } from '@ng-select/ng-select';
@NgModule({
  declarations: [ 
  	vehicleAddEditComponent,
  	VehicleComponent,
 ],
  imports: [
    CommonModule,
    VehicleRoutingModule,
    BmscommonModule,
    NgSelectModule
  ]
})
export class VehicleModule { }

