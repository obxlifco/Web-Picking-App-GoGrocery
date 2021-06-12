import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BmscommonModule } from '../../bmscommon.module';
import { ContactgroupRoutingModule } from './contactgroup-routing.module';

import { ContactGroupComponent }  from '../../products/contact-group/products.contact-group.component';
import { ContactGroupAddEditComponent }  from '../../products/contact-group/products.contact-group.addedit.component';
@NgModule({
  imports: [
    CommonModule,
    BmscommonModule,
    ContactgroupRoutingModule
  ],
  declarations: [
    ContactGroupComponent,
    ContactGroupAddEditComponent
  ],
  entryComponents: [
    ContactGroupComponent,
    ContactGroupAddEditComponent
  ]
})
export class ContactgroupModule { }
