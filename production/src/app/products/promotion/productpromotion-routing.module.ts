import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { ProductPromotionComponent }  from '../../products/promotion/products.product-promotion.component';
import { PromotionAddEditComponent, PromotionPreviewComponent }  from '../../products/promotion/products.promotion.addedit.component';
import { PromotionConditionsComponent }  from '../../products/promotion/products.promotion.conditions.component';

const routes: Routes = [
	{ path: '', component: ProductPromotionComponent },
    { path: 'add', component: PromotionAddEditComponent },
    { path: 'edit/:id', component: PromotionAddEditComponent },
    { path: 'conditions', component: PromotionConditionsComponent },
    { path: 'edit/:id/conditions', component: PromotionConditionsComponent },
    { path: 'preview_promotion', component: PromotionPreviewComponent },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ProductpromotionRoutingModule { }
