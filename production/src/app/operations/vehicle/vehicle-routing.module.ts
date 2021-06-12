import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { VehicleComponent } from './vehicle.component';
import { vehicleAddEditComponent } from './vehicle.vehicle.addedit.component';
const routes: Routes = [
  {
    path:'',component:VehicleComponent
  },
  {
    path:'add',component:vehicleAddEditComponent
  },
  {
    path:'edit/:id',component:vehicleAddEditComponent
  },

];
@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class VehicleRoutingModule { }
