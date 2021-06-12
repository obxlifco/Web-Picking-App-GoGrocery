import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AuthGuard } from '../../global/service/auth-guard.service';

import { CourierComponent }  from '../../order/courier/order.courier.component';
import { CourierAddEditComponent }  from '../../order/courier/order.courier.addedit.component';
const routes: Routes = [	
    { path: '', component: CourierComponent },
	{ path: 'add' ,component : CourierAddEditComponent},
	{ path: 'edit/:id' ,component : CourierAddEditComponent },
 ];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [
      RouterModule
  ]
})
export class CourierRoutingModule { }