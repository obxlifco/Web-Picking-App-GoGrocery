import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AuthGuard } from '../../global/service/auth-guard.service';

import { UnitComponent }  from '../../settings/unit/settings.unit.component';
const routes: Routes = [	
    { path: '', component: UnitComponent },
    { path: 'reload', component: UnitComponent },
 ];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [
      RouterModule
  ]
})
export class UnitRoutingModule { }