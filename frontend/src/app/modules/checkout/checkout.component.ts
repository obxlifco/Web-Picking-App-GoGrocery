import { Component, OnInit,AfterViewInit,ViewChild,ElementRef,Output,EventEmitter, Inject, PLATFORM_ID, ChangeDetectorRef} from '@angular/core';
import {Router} from '@angular/router';
import {GlobalService} from '../../global/service/app.global.service';
import {CheckoutService} from '../../global/service/checkout.service';
import {CartService} from '../../global/service/cart.service';
import {GlobalVariable, Global} from '../../global/service/global';
import { LoyaltypointService } from '../../global/service/loyaltypoint.service';
import { isPlatformBrowser } from '@angular/common';
import * as moment from 'moment';
import { DomSanitizer } from '@angular/platform-browser';

@Component({
  selector: 'app-checkout',
  templateUrl: './checkout.component.html',
  styleUrls: ['./checkout.component.css']
})
export class CheckoutComponent implements OnInit {
  public slots = [];
  public showDeliveryAddress:boolean = false;
  public deliveryAddressId = '';
  public deliverySlot:Object= {};
  public appliedCouponCode = '';
  public checkoutData = [];
  public orderAmountDetails = {};
  public deliveryAddress = [];
  public allDeliverySlot = [];
  public sliderRange:Array<boolean> = [];
	public showCarouselSlider:boolean = true;
	public sliderId;
  public carouselOptions:Object = {};
  public SelectedAddress:any={};
  public isSelectedAddress:boolean=false;
  public isAddnewAddress:boolean=false;
  public burnLoyaltyData:Object = {};
  public loyaltyDetails:Object = {};
  public orderId = 12;
  public appliedLoyaltyPoint = 0;
  public promoCode = '';
  public promocodeApplyBoxStatus = 0;
  public appliedPromoCode = {};
  public onApplyPromo = false;
  public loyaltyData = {};
  public promocodeAndLoyaltyData = {};
  public isAddressWithinRange:string = 'Yes';
  public rangeErrorMsg:string = '';
  public custom_msg:any = '';
  public delivery_note:any ;

  /* Payment option */
  public placeOrder: any ={};
  public cashOption:number;
  public selectedStartDate:any;
  public paymentFormSampleHtml:any = '';
  public tempSublist: any=[];
  public option: any;
  public paymentOption: any = [];
  public paymentObject: any = {};
  /* Payment option */

  public tomeSlot: any;
  public messageID: any;
  

  @Output() onAddressAdd = new EventEmitter();
  @ViewChild('deliveryAdd') deliveryAdd:ElementRef;
  singleDeliveryAddress: any;
  @ViewChild('paymentForm3D') paymentForm3D : ElementRef;

  constructor(
    private _globalService:GlobalService,
    private _checkoutService:CheckoutService,
    private _router:Router,
    private _cartservice:CartService,
    private _checkout:CheckoutService,
    private _loyaltyservice:LoyaltypointService,
    public global: Global,
    private _domSanitizer:DomSanitizer,
    private _changeDetector:ChangeDetectorRef,
    @Inject(PLATFORM_ID) private platformId: Object

    ) { }

  ngOnInit() {
    if (isPlatformBrowser(this.platformId)) {

      this.syncCartData();
      this.getAllDeliveryLocation();
      this.getDeliverySlot();
    }

    this.getPaymentMethod();

    this.carouselOptions = {
      nav: false,
      responsiveClass: true,
      dots: true,
      items: 1,
      autoplay:false,
      autoplayTimeout:4000,
      autoplayHoverPause:true,
      singleItem: true,
      loop: true,
    }
  }

  getPaymentMethod(){
    this._checkout.getPaymentMethod().subscribe(response => {
      let data: any =[];
      data = response.api_status;
      data.forEach(element => {
        this.paymentOption.push(element.engageboost_paymentgateway_method_id);
      });
    });
  }

  onChangeDeliveryAddress(deliveryAddressId) {
    this.deliveryAddressId = deliveryAddressId;
    let address:any= {};
    address.address_id = +this.deliveryAddressId;
    this._checkout.chekAddressRange(address).subscribe( data=>{
      if(data.warehouseMatch == 'n') {
        this.isAddressWithinRange = 'No';
        this.rangeErrorMsg = data.message;
      } else {
         this.isAddressWithinRange = 'Yes';
      }
    }, err => {

    })
  }
  select_address(deliveryAddress){
    console.log(deliveryAddress);
    this.deliveryAddressId = deliveryAddress.id;
    this.SelectedAddress = deliveryAddress;
    this.isSelectedAddress=true;
  }
  chnange_address(){
    this.isSelectedAddress=false;
    
  }
  add_new(){
    this.isAddnewAddress=true;
    this.singleDeliveryAddress=[];
  }

// delete address function started
  deleteDeliveryAddress(addressId) {
    this._checkout.removeDeliveryAddress(addressId).subscribe(response => {
      if(response && response['status'] == 200) {
        this._globalService.showToast("Your address has been deleted successfully");
        this.getAllDeliveryLocation();
      }
    });
  }
// delete address function ended
// edit address function started

editDeliveryAddress(singleDeliveryAddress){
  this.singleDeliveryAddress=singleDeliveryAddress;
  this.isAddnewAddress =true;  
}

// edit address function ended

  onNewAddressAdded(){
    this.isAddnewAddress=false;
    this.getAllDeliveryLocation();
  }
  onChangeTimeSlot(timeSlotIdObject) {
    console.log('timeSlotIdObject');
    console.log(timeSlotIdObject);
    
    this.deliverySlot = timeSlotIdObject;
  }

  onCashOptionChange(cashOption) {
    this.paymentObject = this.paymentOption.find(eleId =>{
      return eleId.id == cashOption;
    });
    console.log(this.paymentObject)
    this.cashOption = cashOption;
    console.log(this.cashOption)
  }
 
  onPlaceOrder() {
    console.log(this.custom_msg)
    console.log(this.cashOption)
     if(!this.deliveryAddressId) {
       this._globalService.showToast("Please select delivery address");
       return false;
     } else if(Object.keys(this.deliverySlot).length == 0) {
       this._globalService.showToast("Please select delivery time slot");
       return false;
     }
 
     if(this.isAddressWithinRange == 'No') {
       this._globalService.showToast(this.rangeErrorMsg);
       return false;
     }
     if(this.orderAmountDetails['grand_total'] <= 0) {
       this._globalService.showToast("Order amount must be greater that 0");
       return false;
     }
     if(this.orderAmountDetails['minimum_order_amount_check'] == 'no') {
       this._globalService.showToast("Minimum order amount AED "+this.orderAmountDetails['minimum_order_amount']);
       return false;
     }
     if(this.cashOption == undefined){
       this._globalService.showToast("Please select payment option");
       return false;
     }
 
     this._globalService.showLoaderSpinner(true);
    /* console.log("*************************** Delivery slot ********************");
     console.log(this.deliverySlot);*/
     //let timeSlotTime = this.deliverySlot['start_time']+'-'+this.deliverySlot['end_time']
 
      this.placeOrder = {
        'address_book_id' : this.deliveryAddressId,
        'time_slot_date' : this.deliverySlot['delivery_date'],
        'time_slot_time' : this.deliverySlot['start_time']+'-'+this.deliverySlot['end_time'],
        'special_instruction' : this.custom_msg,
        'coupon_code' : this.appliedPromoCode['code'] ? this.appliedPromoCode['code'] : '',
        'redeem_amount' : this.loyaltyDetails['is_applied'] ? this.loyaltyDetails['redeem_amount'] : 0,
        'rule_id'       : this.loyaltyDetails['is_applied'] ? this.loyaltyDetails['rule_id'] : '',
        'payment_method_id': this.paymentObject.id,
        'payment_method_name': this.paymentObject.name,
        'payment_type_id': this.paymentObject.paymentgateway_type_id,
      };
      
      this._checkoutService.placeOrder(this.placeOrder).subscribe(response => {
        if(response && response['status'] == 200) {
           this._globalService.showLoaderSpinner(false);
           let orderId = response['order_id'];
           if(this.paymentObject.id != 51){
             this._cartservice.emptyCart();
           }
           let logParms:any = {}
           logParms.order_id = response['order_id'];
           logParms.gross_amount = response['order_data']['gross_amount'];
           logParms.discount_amount = response['order_data']['discount_amount'];
           logParms.net_amount = response['order_data']['net_amount'];        
           logParms.value = response['order_data']['gross_amount'];
           logParms.currency = 'AED';
           this._globalService.facebookPixelEventLog('track','Purchase',logParms);
   
           let googleLogPamrs:any = [];
           let parms:any = {}
           parms.order_id = response['order_id'];
           parms.gross_amount = response['order_data']['gross_amount'];
           parms.discount_amount = response['order_data']['discount_amount'];
           parms.net_amount = response['order_data']['net_amount'];
           parms.value = response['order_data']['gross_amount'];
           parms.currency = "AED";
           googleLogPamrs.push(parms);
           this._globalService.googleEventLog("event","purchase",googleLogPamrs);     
           console.log(orderId)   
           if(this.paymentObject.id == 51){
             this.payCardPayment(orderId);
           }else{
             this.navigateToUrl('/checkout/success/'+orderId);
           }
      } else {
          this._globalService.showToast(response["message"]);
        }
    });
  }

  payCardPayment(orderID: any){
    this.selectedStartDate = this._checkoutService.convertDate(moment().subtract(0, 'days'), 'dd/MM/yyyy');
    try{
      if(orderID == 0) {
  	  	throw "Invalid amount or Order id";
  	  }
  	  let paymentData = {
  	  	'order_id' : orderID,
  	  	'si_start_date' : this.selectedStartDate
  	  };
  	  this._globalService.showLoaderSpinner(true);
  	  this._checkoutService.do_CcAvenue_Payment(paymentData).subscribe(response => {
  	  	if(response && response['status'] == 200) {
  	  		console.log(response);
  	  		let ccAvenue_Form = `<form id="nonseamless" method="post" name="redirect" action="https://secure.ccavenue.ae/transaction/transaction.do?command=initiateTransaction"/>
								        <input type="hidden" id="encRequest" name="encRequest" value="${response['enc_value']}">
								        <input type="hidden" name="access_code" id="access_code" value="${response['access_code']}">
								        <input type="hidden" name="response_type" id="response_type" value='JSON'>
								        <noscript><div id="msg"><div id="submitButton"><input type="submit" value="Click here to continue" class="button"></div></noscript>
								</form>`;
          this.paymentFormSampleHtml = this._domSanitizer.bypassSecurityTrustHtml(ccAvenue_Form);
          this._changeDetector.detectChanges();
          if(this.paymentForm3D && this.paymentForm3D.nativeElement) {
              this.paymentForm3D.nativeElement.querySelector('form').submit();

          }
  	  	}else{
          this._globalService.showToast(response['message']);
        }
  	  	this._globalService.showLoaderSpinner(false);
  	  },
  	  err => {
  	  	this._globalService.showLoaderSpinner(false);
  	  	console.log("************** Error *******************");
  	  	console.log(err);

  	  }
  	  )
    }
    catch(err) {
  		this._globalService.showLoaderSpinner(false);
  		this._globalService.showToast(err);

  	}
  }
  
  getCheckoutSummary() {
    let checkoutData = {
      'warehouse_id' : this._globalService.getWareHouseId(),
      'address_id' : this.deliveryAddressId,
      'coupon_code' : this.appliedCouponCode
    }
    this._checkoutService.getCheckoutSummary(checkoutData).subscribe(response => {
      console.log("******************* Checkout response ******************");
      console.log(response);
      if(response && response['status'] == 200) {    
        this.orderAmountDetails = response['data'] && response['data']['orderamountdetails'].length > 0 ? response['data']['orderamountdetails'][0] : {};
        this.loyaltyDetails     = response['data'] && response['data']['loyalty_details'] ? response['data']['loyalty_details'] : {};
        this.loyaltyDetails['is_applied'] = false;
        /*console.log("************** Loyalty details ****************");
        console.log(this.loyaltyDetails);*/
        let checkOutItemIds = [];
        let checkOutItemNames:any = [];
        if(response['data']['cartdetails']) {
          response['data']['cartdetails'].forEach(element =>  {
              checkOutItemIds.push(element.id);
              checkOutItemNames.push(element.name);
          }) 
        }

        let logParms:any = {}
        logParms.content_ids = checkOutItemIds;
        logParms.content_name = checkOutItemNames.join(",");
        logParms.content_type = "product"
        logParms.num_items = response['data']['cart_count'];
        logParms.value = response['data']['orderamountdetails']['grand_total'];
        logParms.currency = 'AED';
        this._globalService.facebookPixelEventLog('track','InitiateCheckout',logParms);


        let googleLogPamrs:any = [];
        let parms:any = {}
        parms.content_ids = checkOutItemIds;
        parms.content_name = checkOutItemNames.join(",");
        parms.content_type = "product"
        parms.num_items = response['data']['cart_count'];
        parms.value = response['data']['orderamountdetails']['grand_total'];
        parms.currency = 'AED';
        googleLogPamrs.push(parms);
        this._globalService.googleEventLog("event","InitiateCheckout",googleLogPamrs);


      }
    });
  }
 
  syncCartData() {
    this._cartservice.syncCartData().subscribe(response => {
      if(response && response['status'] == 200) {
        this.getCheckoutSummary();
      }
    });
  }
 /* appliedPromocode(promocodeData) {
    console.log("**************** Promocode data ****************");
    console.log(promocodeData);
    
    if(promocodeData && promocodeData['status'] == 200) {
      this.orderAmountDetails = promocodeData['order_amount_details'];
      this.appliedCouponCode = promocodeData['coupon_code'];
    }

  }*/
  getAllDeliveryLocation() {
    this._checkout.getAllDeliveryAddress().subscribe(response => {
      if(response && response['status'] == 200){
        this.deliveryAddress = response['data'];
        this.deliveryAddress.forEach(element => {
          if(element.set_primary==1){
            this.SelectedAddress = element;
            this.deliveryAddressId = element.id;
          }
        });
        
        // this.setDefaultAddress();
      } else {
        this.deliveryAddress = [];
      }
      console.log(this.deliveryAddress);
      
    });
  }

  getDeliverySlot() {
    this._checkout.getAllDeliverySlot().subscribe(response => {
      if(response && response['status'] == 1) {
        response['delivery_slot'].forEach(slotData => {
          if(slotData && slotData['available_slot'] && slotData['available_slot'].length > 0) {
            slotData['available_slot'].forEach(availableSlotData => {
              if(availableSlotData['is_active'] == 'Yes') {
                let slotName = availableSlotData['based_on'] == 'SameDay' ? 'Same Day' : 'Next Day';
                availableSlotData['slot_name'] = slotName;
                availableSlotData['delivery_date'] = slotData['delivery_date'];
                this.allDeliverySlot.push(availableSlotData);
                this.slots=this.allDeliverySlot;
                this.tomeSlot=this.slots[0];
                // this.onChangeTimeSlot(this.tomeSlot);
              }
            })
          }
        })
      }
    });
  }
  
  
  
  navigateToUrl(url) {
    this._router.navigate([url]);
  }
  onChangeLoyaltyPointOption(event) {
    let promotionOption = event.checked;
    let loyaltyPoint = promotionOption ? this.loyaltyDetails['usable_loyalty'] : 0;
    let loyaltyData = {
      'redeem_amount' : loyaltyPoint,
      'rule_id' : this.loyaltyDetails['rule_id'],
    }
    this.appliedPromoCode && this.appliedPromoCode['code'] ? loyaltyData['coupon_code'] = this.appliedPromoCode['code'] : '';
    console.log("************* Applied coupon code ***************");
    console.log(this.appliedCouponCode);
   /* console.log("************** Loyalty data ***************");
    console.log(loyaltyData);
    return false;*/
    this.applyLoyaltyPoint(loyaltyData);

  }

  applyLoyaltyPoint(loyaltyData) {
    this._checkoutService.applyPromoCode(loyaltyData).subscribe(response => {
      if(response && response['status'] == 200) {
        this.orderAmountDetails = response['data'] && response['data']['orderamountdetails'].length > 0 ? response['data']['orderamountdetails'][0] : {};
        this.loyaltyDetails['redeem_amount'] = loyaltyData['redeem_amount'];
        this.loyaltyDetails['rule_id'] = loyaltyData['rule_id'];
        this.loyaltyDetails['is_applied'] = true;

      }

    });
    /*this._loyaltyservice.applyLoyaltyPoint().subscribe(response => {
      if(response && response['status'] == 200) {
        

      }
    });*/
  }
 
  applyPromoCode() {
    if(!this.promoCode) {
      //alert("Please enter promocode");
      this._globalService.showToast("Please enter promocode");
    }

    let promoCodeData = {
      'coupon_code' : this.promoCode,

    }
    if(this.loyaltyDetails && this.loyaltyDetails['is_applied']) {
      promoCodeData['redeem_amount'] = this.loyaltyDetails['redeem_amount'] ? this.loyaltyDetails['redeem_amount'] : '';
      promoCodeData['rule_id'] = this.loyaltyDetails['rule_id'] ? this.loyaltyDetails['rule_id'] : '';
    }
    this._checkoutService.applyPromoCode(promoCodeData).subscribe(response => {
      if(response && response['data']['applied_coupon'] && response['data']['applied_coupon'].length > 0 && response['data']['applied_coupon'][0]['status'] == 1) {
        this.orderAmountDetails = response['data']['orderamountdetails'][0];
        this.appliedPromoCode['amount'] = response['data']['applied_coupon'][0]['amount'];
        this.appliedPromoCode['code'] = promoCodeData['coupon_code'];
        this.promocodeApplyBoxStatus = 2;

      } else {
        let invalidPromocodeMessage = response['data']['applied_coupon'].length > 0 &&  response['data']['applied_coupon'][0]['message'] ?  response['data']['applied_coupon'][0]['message'] : 'Something went wrong';
        this._globalService.showToast(invalidPromocodeMessage);
        this.appliedPromoCode['status'] = 0;
        this.appliedPromoCode['message'] =  invalidPromocodeMessage;
        this.appliedPromoCode['code'] = '';
        this.promoCode = '';
      }
    },
    err => {
      //console.log(err);
      this._globalService.showToast("Something went wrong");
    }
    );
  }
  
  requestForApplyPromoCode() {
     this.promocodeApplyBoxStatus = 1;
  }
  
  resetPromoCode() {
    this.appliedPromoCode = {};
  }
  removePromocode() {
    this.appliedPromoCode = {};
    let promoCodeData = {};
    if(this.loyaltyDetails && this.loyaltyDetails['is_applied']) {
      promoCodeData['redeem_amount'] = this.loyaltyDetails['redeem_amount'];
      promoCodeData['rule_id'] = this.loyaltyDetails['rule_id'];
    }
    this.promocodeApplyBoxStatus = 0;
    this._checkoutService.applyPromoCode(promoCodeData).subscribe(response => {
      if(response && response['status'] == 200) {
         this.orderAmountDetails = response['data']['orderamountdetails'][0];

        
      }

    });
  }

   
  getMessage(message: string) {
    this.custom_msg = message;
  }
}
