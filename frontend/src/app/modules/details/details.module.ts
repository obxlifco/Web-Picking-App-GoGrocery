import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import {MatTabsModule} from '@angular/material/tabs';
import {PipeModule} from '../../global/pipes/pipe.module';
import {MaterialModule} from '../../global/modules/material.module';
import { DetailsRoutingModule } from './details-routing.module';
import { DetailsComponent } from './details.component';
import { RelatedproductComponent } from './pages/relatedproduct/relatedproduct.component';
import { NgxImgZoomModule} from 'ngx-img-zoom';
import {OwlModule} from 'ngx-owl-carousel';
import { MostPopularProductComponent } from './pages/most-popular-product/most-popular-product.component';
import {FormsModule} from '@angular/forms';
import { ReviewModule } from '../review/review.module';


@NgModule({
  declarations: [DetailsComponent, RelatedproductComponent,MostPopularProductComponent],
  imports: [
    CommonModule,
    PipeModule,
    DetailsRoutingModule,
    NgxImgZoomModule,
    OwlModule,
    MatTabsModule,
    FormsModule,
    MaterialModule,
    ReviewModule
  ]
})
export class DetailsModule { }
