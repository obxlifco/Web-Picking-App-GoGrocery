import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BrowserModule } from '@angular/platform-browser';
import { CKEditorModule } from 'ng2-ckeditor';

import { BmscommonModule } from '../../bmscommon.module';
import { AutoResponderRoutingModule } from './autoresponder-routing.module';

import { AutoResponderComponent }  from '../../order/auto-responder/order.auto-responder.component';
import { AutoResponderAddEditComponent }  from '../../order/auto-responder/order.auto-responder.addedit.component';
@NgModule({
  imports: [
    CommonModule,
    AutoResponderRoutingModule,
    BmscommonModule,
    CKEditorModule
  ],
  declarations: [
    AutoResponderComponent,
    AutoResponderAddEditComponent
  ],
  entryComponents: [ 
  	AutoResponderComponent,
    AutoResponderAddEditComponent
  ]
})
export class AutoResponderModule { }