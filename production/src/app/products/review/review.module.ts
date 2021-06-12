import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BmscommonModule } from '../../bmscommon.module';

import { ReviewRoutingModule } from './review-routing.module';
import { ReviewComponent }  from '../../products/review/products.review.component';
import { ReviewAddeditComponent } from '../../products/review/review.addedit.component';
import { RatingModule } from 'ng-starrating';
import { NgSelectModule } from '@ng-select/ng-select';

@NgModule({
  imports: [
    CommonModule,
    BmscommonModule,
    ReviewRoutingModule,
    RatingModule,
    NgSelectModule
  ],
  declarations: [
    ReviewComponent,
    ReviewAddeditComponent
  ],
  entryComponents: [
    ReviewComponent
  ]
})
export class ReviewModule { }
