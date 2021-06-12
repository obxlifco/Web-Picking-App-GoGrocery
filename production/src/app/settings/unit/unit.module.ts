import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BrowserModule } from '@angular/platform-browser';

import { BmscommonModule } from '../../bmscommon.module';
import { UnitRoutingModule } from './unit-routing.module';

import { UnitComponent }  from '../../settings/unit/settings.unit.component';
import { UnitAddEditComponent } from '../../settings/unit/settings.unit.addedit.component';
@NgModule({
  imports: [
    CommonModule,
    UnitRoutingModule,
    BmscommonModule,
  ],
  declarations: [
    UnitComponent,
    UnitAddEditComponent
  ],
  entryComponents: [
    UnitComponent,
  	UnitAddEditComponent
  ]
})
export class UnitModule { }