import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { TaxrulesComponent } from '../../products/taxrules/taxrules.component';
import { TaxruleaddeditComponent } from '../../products/taxrules/taxruleaddedit.component';


const routes: Routes = [
	{ path: '', component: TaxrulesComponent },
    { path: 'add', component: TaxruleaddeditComponent },
    { path: 'edit/:id', component: TaxruleaddeditComponent },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class TaxrulesRoutingModule { }
