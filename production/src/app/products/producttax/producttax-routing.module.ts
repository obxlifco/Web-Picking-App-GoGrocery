import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { ProducttaxComponent } from '../../products/producttax/producttax.component';

const routes: Routes = [
		{ path: '', component: ProducttaxComponent }
	];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ProducttaxRoutingModule { }
