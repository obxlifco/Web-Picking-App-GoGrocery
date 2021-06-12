import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { CustomertaxComponent } from '../../products/customertax/customertax.component';
import { CustomertaxAddeditComponent } from '../../products/customertax/customertax.addedit.component';

const routes: Routes = [
	{ path: '', component: CustomertaxComponent },
    { path: 'add', component: CustomertaxAddeditComponent },
    { path: 'edit/:id', component: CustomertaxAddeditComponent },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class CustomertaxRoutingModule { }
