import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { DeliveryManagerComponent } from './delivery-manager.component';
import { ManagerAddeditComponent } from './manager.addedit.component';

const routes: Routes = [
  {
    path:'',component:DeliveryManagerComponent
  },
  {
    path:'add',component:ManagerAddeditComponent
  },
  {
    path:'edit/:id',component:ManagerAddeditComponent
  },

];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class DeliveryManagerRoutingModule { }
