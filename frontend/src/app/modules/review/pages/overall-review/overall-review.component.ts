import { Component, OnInit, Output, EventEmitter, Input, Inject, PLATFORM_ID } from '@angular/core';
import { AuthenticationService } from '../../../../global/service/authentication.service';
import {MenuService} from '../../../../global/service/menu.service';
import { ReviewService } from "../../review.service";
import { isPlatformBrowser } from '@angular/common';
@Component({
  selector: 'app-overall-review',
  templateUrl: './overall-review.component.html',
  styleUrls: ['./overall-review.component.css']
})
export class OverallReviewComponent implements OnInit {
  @Input('productId') public product_id ;
  @Output() formEvent = new EventEmitter();
  public rating;
  public rating_data:any=[];
  public review_data:any=[];
  constructor(
    public authenticationService: AuthenticationService,
    private _menuservice:MenuService,
    public reviewService:ReviewService,
    @Inject(PLATFORM_ID) private platformId: Object

  ) { 
    this.reviewService.reviewData.subscribe(data=>{
      this.review_data = data;
    });
    this.reviewService.rating.subscribe(data=>{
      this.rating = data;
    });
    this.reviewService.ratingData.subscribe(data=>{
      this.rating_data = data;
    });
  }
  
  ngOnInit() {
    if (isPlatformBrowser(this.platformId)) {
      this.getReview();
    }
  
  }
  showrateForm(){
    if(this.authenticationService.userFirstName){
      this.formEvent.emit(true);
		}else{
			this._menuservice.signinSignuppopup$.next('sign-in');
		}
  }
  getReview(){
    this.reviewService.getProductReviewByProductID(this.product_id).subscribe(response => {
      this.rating = response['review_avg'];
      this.rating_data = response.rating_data;
      this.review_data = response.review_data;
		})
  }
  
}
