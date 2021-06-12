import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import {MatTabsModule} from '@angular/material/tabs';
import {PipeModule} from '../../global/pipes/pipe.module';
import {MaterialModule} from '../../global/modules/material.module';
// import { DetailsRoutingModule } from './details-routing.module';
import { SubstituteProductComponent } from './substitute_product.component';
// import { RelatedproductComponent } from './pages/relatedproduct/relatedproduct.component';
import { NgxImgZoomModule} from 'ngx-img-zoom';
import {OwlModule} from 'ngx-owl-carousel';
// import { MostPopularProductComponent } from './pages/most-popular-product/most-popular-product.component';
import {FormsModule} from '@angular/forms';
import { ReviewModule } from '../review/review.module';
import { SubstituteProductRoutingModule } from './substitute_product-routing.module';
import { SuccessSubstituteComponent } from './successSubstituteProduct/successSubstitute.component';


@NgModule({
  declarations: [SubstituteProductComponent],
  imports: [
    CommonModule,
    PipeModule,
    SubstituteProductRoutingModule,
    NgxImgZoomModule,
    OwlModule,
    MatTabsModule,
    FormsModule,
    MaterialModule,
    ReviewModule
  ]
})
export class SubstituteProductModule { }
