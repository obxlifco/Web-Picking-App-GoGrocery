import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AuthGuard } from '../../global/service/auth-guard.service';

import { StoreCategoryComponent }  from '../../settings/store-category_type/settings.store-category.component';
import { storeCategoryAddEditComponent }  from '../../settings/store-category_type/settings.store-category.addedit.component';
const routes: Routes = [	
    { path: '', component: StoreCategoryComponent },
    { path: 'add', component: storeCategoryAddEditComponent },
    { path: 'edit/:id', component: storeCategoryAddEditComponent },
 ];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [
      RouterModule
  ]
})
export class StoreCategoryRoutingModule { }