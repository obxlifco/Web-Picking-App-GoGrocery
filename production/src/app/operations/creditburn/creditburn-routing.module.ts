import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { CreditburnAddeditComponent } from './creditburn.addedit.component';
import { CreditburnComponent } from './creditburn.component';
import { CreditburnconditionAddeditComponent } from './creditburncondition.addedit.component';
const routes: Routes = [
  { path: '', component:CreditburnComponent },
  { path: 'add', component:CreditburnAddeditComponent },
  { path: 'edit/:id', component:CreditburnAddeditComponent },
  { path: 'conditions/:id', component:CreditburnconditionAddeditComponent},
  { path: 'conditions/edit/:id', component:CreditburnconditionAddeditComponent},
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class CreditburnRoutingModule { }
