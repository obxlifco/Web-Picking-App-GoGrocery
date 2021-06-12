import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { BmscommonModule } from '../../bmscommon.module';

import { CustomertaxRoutingModule } from './customertax-routing.module';
import { CustomertaxComponent } from '../../products/customertax/customertax.component';
import { CustomertaxAddeditComponent } from '../../products/customertax/customertax.addedit.component';
import { NgSelectModule } from '@ng-select/ng-select';


@NgModule({
  declarations: [
  	CustomertaxComponent,
  	CustomertaxAddeditComponent,
  ],
  imports: [
    CommonModule,
    CustomertaxRoutingModule,
    BmscommonModule,
    NgSelectModule
  ]
})
export class CustomertaxModule { }
