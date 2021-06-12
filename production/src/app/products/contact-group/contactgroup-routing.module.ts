import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AuthGuard } from '../../global/service/auth-guard.service';

import { ContactGroupComponent }  from '../../products/contact-group/products.contact-group.component';
import { ContactGroupAddEditComponent }  from '../../products/contact-group/products.contact-group.addedit.component';
const routes: Routes = [	
    { path: '', component: ContactGroupComponent },
    { path: 'add', component: ContactGroupAddEditComponent },
    { path: 'edit/:id', component: ContactGroupAddEditComponent },
 ];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [
      RouterModule
  ]
})
export class ContactgroupRoutingModule { }