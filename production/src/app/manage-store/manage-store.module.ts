import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BrowserModule } from '@angular/platform-browser';

import { BmscommonModule } from '../bmscommon.module';
import { ManageStoreRoutingModule } from './manage-store.routing.module';

import { ManageStoreComponent, ManageStoreAddEditComponent }  from './manage-store.component';
@NgModule({
  imports: [
    CommonModule,
    ManageStoreRoutingModule,
    BmscommonModule
  ],
  declarations: [
  	ManageStoreComponent,
  	ManageStoreAddEditComponent,
  ],
  entryComponents: [
  	ManageStoreComponent,
    ManageStoreAddEditComponent,
  ]
})
export class ManageStoreModule { }
