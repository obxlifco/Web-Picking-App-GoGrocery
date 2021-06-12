import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AuthGuard } from '../../global/service/auth-guard.service';

import { PresetComponent }  from '../../order/preset/order.preset.component';
const routes: Routes = [	
    { path: '', component: PresetComponent }
 ];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [
      RouterModule
  ]
})
export class PresetRoutingModule { }