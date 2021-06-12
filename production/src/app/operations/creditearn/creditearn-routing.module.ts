import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { CreditearnAddeditComponent } from './creditearn.addedit.component';
import { CreditearnComponent } from './creditearn.component';
import { CreditearnconditionAddeditComponent } from './creditearncondition.addedit.component';
const routes: Routes = [
  { path: '', component:CreditearnComponent },
  { path: 'add', component:CreditearnAddeditComponent },
  { path: 'edit/:id', component:CreditearnAddeditComponent },
  { path: 'conditions/:id', component:CreditearnconditionAddeditComponent},
  { path: 'conditions/edit/:id', component:CreditearnconditionAddeditComponent},
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class CreditearnRoutingModule { }
