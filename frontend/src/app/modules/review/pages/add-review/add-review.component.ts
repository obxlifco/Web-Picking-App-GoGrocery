import { Component, OnInit, Input, Output, EventEmitter} from '@angular/core';
import { FormGroup, FormControl, FormBuilder, NgForm, Validators} from '@angular/forms'
import { ReviewService } from "../../review.service";
import {GlobalService} from '../../../../global/service/app.global.service';
@Component({
  selector: 'app-add-review',
  templateUrl: './add-review.component.html',
  styleUrls: ['./add-review.component.css']
})
export class AddReviewComponent implements OnInit {
  @Input('productId') public product_id;
  @Output() showclass = new EventEmitter();
  public reviewForm : FormGroup;
  public rating:number = 0;
  public rateText = 'Rate this product';
  public ratevalid:boolean=false;
  constructor(
    private  _reviewService:ReviewService,
    private formbuilder:FormBuilder,
    private _gs:GlobalService
  ) { 
    this.reviewForm = formbuilder.group({
      review_title :  ['',Validators.required],
      review_message : ['',Validators.required],
    });
  }

  ngOnInit() {
    // let error = this.reviewForm.invalid;
    // console.log(error);
    // this.reviewForm.statusChanges.subscribe(response => {
    //   console.log(response);
    // })
  }
  
  addReview(reviewForm:any){
    if(this.rating == 0 ){
      this.ratevalid = true;
    }else{
      this.ratevalid = false;
      let formData = reviewForm.value;
      formData['product_id'] = this.product_id;
      formData['review_star'] = this.rating;
      this._reviewService.addProductReview(formData).subscribe(response => {
        if(response.status == 1){
          this._gs.showToast(response.msg);
          this._reviewService.reviewData.next(response.review_data);
          this._reviewService.ratingData.next(response.rating_data);
          this._reviewService.rating.next(response.review_avg);
          this.reviewForm.reset();
          this.showclass.emit(false);
        }
      },
      err => {
        this._gs.showToast("Something went wrong");

      });
    }
    
  }
  chageRating(rate){
    this.rating = rate;
    if(this.rating >= 3){
      this.rateText = 'Good';
    }else if(this.rating ==2 ){
      this.rateText = 'Avarage';
    }else if(this.rating == 1){
      this.rateText = 'Worst';
    }else{
      this.rateText = 'Rate this product';
    }
  }
  onReset(){
    this.rating = 0;
    this.rateText = 'Rate this product';
    this.reviewForm.reset();
    this.showclass.emit(false);
  }
  
}
