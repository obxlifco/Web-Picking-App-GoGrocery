import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CreditearnRoutingModule } from './creditearn-routing.module';
import { CreditearnAddeditComponent } from './creditearn.addedit.component';
import { CreditearnComponent } from './creditearn.component';
import { CreditearnconditionAddeditComponent } from './creditearncondition.addedit.component';
import { BmscommonModule } from '../../bmscommon.module';
import { OwlDateTimeModule, OwlNativeDateTimeModule } from 'ng-pick-datetime';

import { PointCategoryListComponent, PointProductListComponent, PointCustomerListComponent, PointCustomerGroupListComponent } from '../../operations/creditearn/creditearncondition.addedit.component';


@NgModule({
   imports: [
    CommonModule,
    CreditearnRoutingModule,
    BmscommonModule,
    OwlDateTimeModule,
    OwlNativeDateTimeModule,
  ],
  declarations: [
    CreditearnAddeditComponent,
    CreditearnComponent,
    CreditearnconditionAddeditComponent,
    PointCategoryListComponent, 
    PointProductListComponent,
    PointCustomerListComponent,
    PointCustomerGroupListComponent
  ],
  entryComponents: [
    PointCategoryListComponent, 
    PointProductListComponent,
    PointCustomerListComponent,
    PointCustomerGroupListComponent
  ]
})
export class CreditearnModule { }
