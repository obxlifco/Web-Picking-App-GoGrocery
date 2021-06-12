import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BmscommonModule } from '../../bmscommon.module';

import { CreditburnRoutingModule } from './creditburn-routing.module';
import { CreditburnAddeditComponent } from './creditburn.addedit.component';
import { CreditburnComponent } from './creditburn.component';
import { CreditburnconditionAddeditComponent } from './creditburncondition.addedit.component';
import { PointburnCategoryListComponent, PointburnProductListComponent, PointburnCustomerListComponent, PointburnCustomerGroupListComponent } from '../../operations/creditburn/creditburncondition.addedit.component';

@NgModule({
  imports: [
    CommonModule,
    CreditburnRoutingModule,
    BmscommonModule
  ],
  declarations: [
    CreditburnAddeditComponent,
    CreditburnComponent,
    CreditburnconditionAddeditComponent,
    PointburnCategoryListComponent, 
    PointburnProductListComponent, 
    PointburnCustomerListComponent, 
    PointburnCustomerGroupListComponent
  ],
  entryComponents: [
    PointburnCategoryListComponent, 
    PointburnProductListComponent,
    PointburnCustomerListComponent,
    PointburnCustomerGroupListComponent
  ]
})
export class CreditburnModule { }
