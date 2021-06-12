import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BrowserModule } from '@angular/platform-browser';

import { BmscommonModule } from '../../bmscommon.module';
import { PresetRoutingModule } from './preset-routing.module';

import { PresetComponent }  from '../../order/preset/order.preset.component';
import { PresetAddEditComponent } from '../../order/preset/order.preset.addedit.component';
@NgModule({
  imports: [
    CommonModule,
    PresetRoutingModule,
    BmscommonModule,
  ],
  declarations: [
    PresetComponent,
    PresetAddEditComponent
  ],
  entryComponents: [ 
  	PresetComponent,
    PresetAddEditComponent
  ]
})
export class PresetModule { }