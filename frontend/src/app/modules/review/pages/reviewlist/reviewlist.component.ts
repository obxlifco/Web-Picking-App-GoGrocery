import { Component, OnInit, Input, Inject, PLATFORM_ID } from '@angular/core';
import { ReviewService } from "../../review.service";
import { isPlatformBrowser } from '@angular/common';


@Component({
  selector: 'app-reviewlist',
  templateUrl: './reviewlist.component.html',
  styleUrls: ['./reviewlist.component.css']
})
export class ReviewlistComponent implements OnInit {
  @Input('productId') public product_id ;
  public review_data:any=[];
  p: Number = 1;
  count: Number = 5;
  constructor(
    public reviewService:ReviewService,    @Inject(PLATFORM_ID) private platformId: Object

  ) {
    this.reviewService.reviewData.subscribe(data=>{
      this.review_data = data;
      
    });  
    
  }

  ngOnInit() {
    if (isPlatformBrowser(this.platformId)) {
      this.getReview();

    }
  }
  getReview(){
    this.reviewService.getProductReviewByProductID(this.product_id).subscribe(response => {
      this.review_data = response.review_data;
		})
  }
}
