import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { ManageStoreComponent, ManageStoreAddEditComponent }  from './manage-store.component';

const routes: Routes = [	
	{ path: '', component: ManageStoreComponent },
    { path: 'add', component: ManageStoreAddEditComponent },
    { path: 'edit/:id', component: ManageStoreAddEditComponent },
	
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ManageStoreRoutingModule { }
