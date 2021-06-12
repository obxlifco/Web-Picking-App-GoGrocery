import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AuthGuard } from '../../global/service/auth-guard.service';

import { AutoResponderComponent }  from '../../order/auto-responder/order.auto-responder.component';
import { AutoResponderAddEditComponent }  from '../../order/auto-responder/order.auto-responder.addedit.component';
const routes: Routes = [	
    { path: '', component: AutoResponderComponent },
    { path: 'add', component: AutoResponderAddEditComponent },
    { path: 'edit/:id', component: AutoResponderAddEditComponent },
 ];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [
      RouterModule
  ]
})
export class AutoResponderRoutingModule { }