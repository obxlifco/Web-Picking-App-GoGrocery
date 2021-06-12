
import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AuthGuard } from '../../global/service/auth-guard.service';

import { ContactsComponent }  from '../../products/contacts/products.contacts.component';
import { ContactsAddEditComponent }  from '../../products/contacts/products.contacts.addedit.component';
const routes: Routes = [	
    { path: '', component: ContactsComponent },
    { path: 'add', component: ContactsAddEditComponent },
    { path: 'edit/:id', component: ContactsAddEditComponent },
 ];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [
      RouterModule
  ]
})
export class ContactRoutingModule { }