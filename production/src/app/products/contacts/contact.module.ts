import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BmscommonModule } from '../../bmscommon.module';
import { ContactRoutingModule } from './contact-routing.module';

import { ContactsComponent }  from '../../products/contacts/products.contacts.component';
import { ContactsAddEditComponent }  from '../../products/contacts/products.contacts.addedit.component';
@NgModule({
  imports: [
    CommonModule,
    ContactRoutingModule,
    BmscommonModule
  ],
  declarations: [
    ContactsComponent,
    ContactsAddEditComponent
  ],
  entryComponents: [
    ContactsComponent,
  	ContactsAddEditComponent
  ]
})
export class ContactModule { }