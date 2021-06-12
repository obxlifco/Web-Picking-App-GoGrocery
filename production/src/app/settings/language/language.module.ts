import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BrowserModule } from '@angular/platform-browser';

import { ConfirmDialog, AlertDialog } from '../../global/dialog/confirm-dialog.component';

import { BmscommonModule } from '../../bmscommon.module';
import { LanguageRoutingModule } from './language-routing.module';

import { LanguageComponent } from './settings.language.component';
import { LanguageManageComponent, LanguageAddEditComponent } from './settings.language.manage.component';

@NgModule({
  imports: [
    CommonModule,
    LanguageRoutingModule,
    BmscommonModule,
  ],
  declarations: [
    LanguageComponent,
    LanguageManageComponent,
    LanguageAddEditComponent
  ],
  entryComponents:[
    LanguageAddEditComponent
  ]
})
export class LanguageModule { }
