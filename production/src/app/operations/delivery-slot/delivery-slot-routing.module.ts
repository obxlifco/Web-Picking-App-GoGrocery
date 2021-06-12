import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { DeliverySlotComponent } from './delivery-slot.component';

const routes: Routes = [
  {
    path:'',component:DeliverySlotComponent
  },

];
@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class DeliverySlotRoutingModule { }
