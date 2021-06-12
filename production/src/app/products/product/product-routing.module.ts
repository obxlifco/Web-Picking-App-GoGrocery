import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { ProductComponent, ProductDetailsComponent,ProductPreviewComponent }  from '../../products/product/products.product.component';
import { ProductBasicInfoComponent, ProductAdvanceInfoComponent, ProductPriceSetupComponent, ProductRelatedComponent, ProductSupplierComponent, VariantProductComponent, ProductPricePreviewComponent } from '../../products/product/products.product.addedit.component';

const routes: Routes = [
	  { path:'',component:ProductComponent },
	  { path: 'add', component: ProductBasicInfoComponent },
    { path: 'add/step2', component: ProductAdvanceInfoComponent },
    { path: 'add/step3', component: ProductPriceSetupComponent },
    { path: 'add/step4', component: ProductSupplierComponent },
    { path: 'add/step5', component: VariantProductComponent, }, // variant product
    { path: 'add/step6', component: ProductRelatedComponent, data: { type: 1 } }, 
    { path: 'add/step7', component: ProductRelatedComponent, data: { type: 2 } },
    // { path: 'add/step8', component: ProductRelatedComponent, data: { type: 3 } },
    // { path: 'add/step9', component: ProductRelatedComponent, data: { type: 4 } },

    { path: 'edit/:id', component: ProductBasicInfoComponent },
    { path: 'edit/:id/step2', component: ProductAdvanceInfoComponent },
    { path: 'edit/:id/step3', component: ProductPriceSetupComponent },
    { path: 'edit/:id/step4', component: ProductSupplierComponent },
    { path: 'edit/:id/step5', component: VariantProductComponent },
    { path: 'edit/:id/step6', component: ProductRelatedComponent, data: { type: 1 } },
    { path: 'edit/:id/step7', component: ProductRelatedComponent, data: { type: 2 } },
    // { path: 'edit/:id/step8', component: ProductRelatedComponent, data: { type: 3 } },
    // { path: 'edit/:id/step9', component: ProductRelatedComponent, data: { type: 4 } },
    
    { path: 'details/:id', component: ProductDetailsComponent },
    { path: 'preview_product', component: ProductPreviewComponent },
    { path: 'preview_product_price', component: ProductPricePreviewComponent },

];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [
      RouterModule,
  ]
})
export class ProductRoutingModule { }
