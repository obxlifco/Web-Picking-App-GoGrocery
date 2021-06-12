import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReviewComponent } from './review.component';
import { OverallReviewComponent } from './pages/overall-review/overall-review.component';
import { AddReviewComponent } from './pages/add-review/add-review.component';
import {MaterialModule} from '../../global/modules/material.module';
import { ReviewlistComponent } from './pages/reviewlist/reviewlist.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { NgxPaginationModule } from 'ngx-pagination';
@NgModule({
  declarations: [ReviewComponent, OverallReviewComponent, AddReviewComponent, ReviewlistComponent],
  imports: [
    CommonModule,
    FormsModule,
    MaterialModule,
    ReactiveFormsModule,
    NgxPaginationModule
  ],
  exports :[ReviewComponent, OverallReviewComponent, AddReviewComponent, ReviewlistComponent]
  
})
export class ReviewModule { }
