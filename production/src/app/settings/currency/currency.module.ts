import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BrowserModule } from '@angular/platform-browser';

import { ConfirmDialog, AlertDialog } from '../../global/dialog/confirm-dialog.component';

import { BmscommonModule } from '../../bmscommon.module';
import { CurrencyRoutingModule } from './currency-routing.module';

import { CurrencyComponent } from './settings.currency.component';
import { CurrencyManageComponent } from './settings.currency.manage.component';

@NgModule({
  imports: [
    CommonModule,
    CurrencyRoutingModule,
    BmscommonModule,
  ],
  declarations: [
    CurrencyComponent,
    CurrencyManageComponent
  ],
  entryComponents:[
    CurrencyManageComponent,
    ConfirmDialog
  ]
})
export class CurrencyModule { }
