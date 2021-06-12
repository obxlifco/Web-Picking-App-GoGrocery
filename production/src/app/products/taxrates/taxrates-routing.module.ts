import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { TaxratesComponent } from '../../products/taxrates/taxrates.component';
import { TaxrateaddeditComponent } from '../../products/taxrates/taxrateaddedit.component';

const routes: Routes = [
	{ path: '', component: TaxratesComponent },
    { path: 'add', component: TaxrateaddeditComponent },
    { path: 'edit/:id', component: TaxrateaddeditComponent },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class TaxratesRoutingModule { }
