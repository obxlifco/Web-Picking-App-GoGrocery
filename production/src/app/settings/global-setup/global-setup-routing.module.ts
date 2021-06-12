import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { GlobalSetupComponent } from './settings.global-setup.component';
import { GlobalSetupAddEditComponent } from './settings.global-setup.addedit.component';
const routes: Routes = [
  { path: '', component: GlobalSetupComponent },
  { path: 'add', component: GlobalSetupAddEditComponent },
  { path: 'edit/:id', component: GlobalSetupAddEditComponent }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class GlobalSetupRoutingModule { }
