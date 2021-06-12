import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { CategoryComponent }  from '../../products/category/products.category.component';
import { CategoryAddEditComponent,CategoryCustomFieldComponent,CategoryAddEditCustomFieldComponent }  from '../../products/category/products.category.addedit.component';


const routes: Routes = [
		{ path: '', component: CategoryComponent },
	    { path: 'add', component: CategoryAddEditComponent },
	    { path: 'edit/:id', component: CategoryAddEditComponent },
	    { path: 'add/step2', component: CategoryCustomFieldComponent },
	    { path: 'edit/:id/step2', component: CategoryCustomFieldComponent },
	    { path: 'edit/:id/step2/reload', component: CategoryCustomFieldComponent }
	];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class CategoryRoutingModule { }
