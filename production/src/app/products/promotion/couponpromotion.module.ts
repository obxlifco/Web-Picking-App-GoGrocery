import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CouponpromotionRoutingModule } from './couponpromotion-routing.module';
import { CoupanPromotionComponent }  from '../../products/promotion/products.coupan-promotion.component';
import { PromotioncommonModule } from '../promotioncommon.module';
import { NgSelectModule } from '@ng-select/ng-select';
@NgModule({
  declarations: [
  	CoupanPromotionComponent,
  ],
  imports: [
    CommonModule,
    PromotioncommonModule,
    CouponpromotionRoutingModule,
    NgSelectModule
  ],
  entryComponents:[
  ]
})
export class CouponpromotionModule { }
