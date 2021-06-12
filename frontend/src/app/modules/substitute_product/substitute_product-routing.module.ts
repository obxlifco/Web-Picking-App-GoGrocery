import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {SubstituteProductComponent} from './substitute_product.component';

const routes: Routes = [
	{path : '',component : SubstituteProductComponent}
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class SubstituteProductRoutingModule { }
