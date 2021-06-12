import { Component, OnInit,EventEmitter,Output,Input} from '@angular/core';
import {CheckoutService} from '../../../../global/service/checkout.service';
import {GlobalService} from '../../../../global/service/app.global.service';
@Component({
  selector: 'app-promocode',
  templateUrl: './promocode.component.html',
  styleUrls: ['./promocode.component.css']
})
export class PromocodeComponent implements OnInit {
  public promoCode = '';
  public promocodeApplyBoxStatus = 0;
  public appliedPromoCode = {};
  public onApplyPromo = false;
  @Output() onSuccessPromoCode = new EventEmitter();
  @Output() onRemovePromoCode = new EventEmitter();
  @Input() loyaltyData;
  constructor(
    private _checkoutService:CheckoutService,
    private _globalService:GlobalService
  ) {
  }
  ngOnInit() {

  }
  /**
   * Method on applying promocode
   * @access public
  */
  applyPromoCode() {
    if(!this.promoCode) {
      //alert("Please enter promocode");
      this._globalService.showToast("Please enter promocode");
    }

    let promoCodeData = {
      'coupon_code' : this.promoCode,

    }
    if(this.loyaltyData && this.loyaltyData['is_applied']) {
      promoCodeData['redeem_amount'] = this.loyaltyData['usable_loyalty'];
      promoCodeData['rule_id'] = this.loyaltyData['rule_id'];
    }
    this._checkoutService.applyPromoCode(promoCodeData).subscribe(response => {
      if(response && response['data']['applied_coupon'] && response['data']['applied_coupon'][0]['status'] == 1) {
        this.appliedPromoCode = {
          'status' : 1,
          'message' : 'Coupon code applied successfully',
          'coupon_code' : response['data']['applied_coupon'][0]['coupon_code'],
          'disc_type' : response['data']['applied_coupon'][0]['disc_type'],
          'amount' : response['data']['applied_coupon'][0]['amount'],
        }
        let orderAmountDetails = response['data']['orderamountdetails'][0];
        let promocodeInstance = {
          'status' : 200,
          'order_amount_details' : orderAmountDetails,
          'coupon_code' : response['data']['applied_coupon'][0]['coupon_code'],
        }
        this.promocodeApplyBoxStatus = 2;

        this._checkoutService.storeCouponCode(response['data']['applied_coupon'][0]['coupon_code']);
        //alert(this.appliedPromoCode);
        this.onSuccessPromoCode.emit(promocodeInstance);
        // console.log(this.appliedPromoCode);
      } else {
        let invalidPromocodeMessage = response['data']['applied_coupon'][0]['message'];
        this._globalService.showToast(invalidPromocodeMessage);
        this.appliedPromoCode['status'] = 0;
        this.appliedPromoCode['message'] =  response['data']['applied_coupon'][0]['message'];
        this.promoCode = '';
        // console.log(this.appliedPromoCode);
      }
    },
    err => {
      //console.log(err);
      this._globalService.showToast("Something went wrong");
    }
    );
  }
  /**
   * Method request for apply promocode
  */
  requestForApplyPromoCode() {
     this.promocodeApplyBoxStatus = 1;
  }
  /**
   * Method on resetting promo code
   * @access public
  */
  resetPromoCode() {
    this.appliedPromoCode = {};
  }
  removePromocode() {
    this.appliedPromoCode = {};
    let promoCodeData = {};
    if(this.loyaltyData && this.loyaltyData['is_applied']) {
      promoCodeData['redeem_amount'] = this.loyaltyData['usable_loyalty'];
      promoCodeData['rule_id'] = this.loyaltyData['rule_id'];
    }
    this.promocodeApplyBoxStatus = 0;
    this._checkoutService.applyPromoCode(promoCodeData).subscribe(response => {
      if(response && response['status'] == 200) {
        let orderAmountDetails = response['data']['orderamountdetails'][0];
        let promocodeInstance = {
          'status' : 200,
          'order_amount_details' : orderAmountDetails,
          'coupon_code' : '',
        }
        this.onSuccessPromoCode.emit(promocodeInstance);

      }

    });
  }
}
