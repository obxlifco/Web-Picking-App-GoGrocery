import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ProductpromotionRoutingModule } from './productpromotion-routing.module';
import { ProductPromotionComponent }  from '../../products/promotion/products.product-promotion.component';
import { PromotioncommonModule } from '../promotioncommon.module';
import { NgSelectModule } from '@ng-select/ng-select';

@NgModule({
  declarations: [
  	ProductPromotionComponent,
  ],
  imports: [
    PromotioncommonModule,
    CommonModule,
    ProductpromotionRoutingModule,
    NgSelectModule
  ],
  entryComponents : [
  ]
})
export class ProductpromotionModule { }
