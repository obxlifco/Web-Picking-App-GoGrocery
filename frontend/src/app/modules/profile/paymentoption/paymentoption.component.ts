import { Component, OnInit,ElementRef,ViewChild,AfterViewInit,ChangeDetectorRef, Inject, PLATFORM_ID} from '@angular/core';
import {DomSanitizer} from '@angular/platform-browser';
import {Http} from '@angular/http';
import {FormControl,FormBuilder,FormGroup,Validators,AbstractControl,ValidatorFn} from '@angular/forms';
import { Global } from '../../../global/service/global';
import { GlobalService } from '../../../global/service/app.global.service';
import { CheckoutService } from '../../../global/service/checkout.service';
import { Router, ActivatedRoute, NavigationEnd } from '@angular/router';
import { CreditCardValidator } from 'angular-cc-library';
import { isPlatformBrowser } from '@angular/common';
declare let PaymentSession:any;


@Component({
  selector: 'app-paymentoption',
  templateUrl: './paymentoption.component.html',
  styleUrls: ['./paymentoption.component.css']
})
export class PaymentoptionComponent implements OnInit {
  public orders:any=[];
  public orderId:number;
  public formModel: any = {};
  public prev_data:any;
  public order_data:any;
  public cashOption:number = 1;
  public paymenyForm:FormGroup;
  public isPaymentFormSubmitted:boolean = false;
  public paymentFormSampleHtml:any = '';

  @ViewChild('paymentForm3D') paymentForm3D : ElementRef;

  constructor(
    public global: Global,
    public _globalService: GlobalService,
		private _router: Router,
    private _activeRoute:ActivatedRoute,
    private _paymentFormBuilder:FormBuilder,
    private _checkoutService:CheckoutService,
    private _http:Http,
    private _changeDetector:ChangeDetectorRef,
    private _domSanitizer:DomSanitizer,
    @Inject(PLATFORM_ID) private platformId: Object

  ) {
    let data=this._activeRoute.snapshot.params;
    this.order_data = data['order_id'];
    console.log(this.order_data)
    console.log(data.slug)
    this.orderId=+data.slug;

    this._activeRoute.url.subscribe(() => {
      this.prev_data = this._activeRoute.snapshot.data['page'];
      // alert(this.prev_data);
      // alert(this.order_data);
    });
    // alert(+data.slug)
    // this.orderId=76;
   }
   ngAfterViewInit() {
     console.log("*************** Payment form **************");
     console.log(this.paymentForm3D);
   }

  ngOnInit() {

    //this.initiateForm();
    //this.loadScripts();
   // this.processCardPayment();
   
   if (isPlatformBrowser(this.platformId)) {
    this.get_order_details(this.orderId);

   }
    //this.formModel.pament_type=3;

  }
  initiateForm() {
    this.paymenyForm = this._paymentFormBuilder.group({
      name_on_card : ['',this.conditionalValidator(this.cashOption,Validators.required)],
      card_number: ['', this.conditionalValidator(this.cashOption,<any>CreditCardValidator.validateCCNumber)],
      expiry_date: ['', this.conditionalValidator(this.cashOption,<any>CreditCardValidator.validateExpDate)],
      sec_code: ['', this.conditionalValidator(this.cashOption,<any>Validators.required)] //<any>Validators.minLength(3), <any>Validators.maxLength(4)]
    })

  }
  conditionalValidator(condition, validator: ValidatorFn): ValidatorFn {
    return (control: AbstractControl): {[key: string]: any} => {
     //alert(condition);
      if (condition == '1') {
        return validator(control);
      }
      return null;
      
    }
  }
   

  get_order_details(id:any){
    var url:any;
    if(this.prev_data=='approved'){
      url='order-details-payment';
      id=this.order_data;
      let idArr = id.split("?");
      id = idArr[0];
    }else{
      url='order-details';
    }
    if(id){
      this.global.getWebServiceData(url, 'GET', '', id).subscribe(data => {
        console.log(data);
        if (data.status == 200) {

          this.orders=data.data;
          this.orderId = this.orders['id'];

         // this.burnLoyaltyData = data['data']['loyalty_details'] && data['data']['loyalty_details'].length > 0 ? data['data']['loyalty_details'][0]['burn_loyalty'] : {};
        }else{
          console.log(data);
          this._globalService.showToast('Something went wrong. Please try again.');        
        }
      }, err => console.log(err), function() {});
    }else{
      this._globalService.showToast('Order details not available for this order');        
    }
  }
  onCashOptionChange(cashOption) {
    this.cashOption = cashOption;
    
    //this.initiateForm();
    
  }

  palce_order(){
  	/*alert(this.cashOption);
  	return false;*/
    let data:any={};
    if(!this.cashOption) {
      this._globalService.showToast("Please choose payment option");
      return false;
    }
    if(this.orders['applied_loyalty_amount'] > 0) {
      data['loyalty_amount'] = this.orders['applied_loyalty_amount'];
      data['rule_id'] = this.orders['rule_id'];
    }

    data.order_id=this.orders.custom_order_id;
    var id=data.order_id
    if(this.cashOption == 1) {
      this.payCardPayment(this.orders['gross_amount'],this.orders['id']);
      return false;
    }
    if(this.cashOption==2){
      data.payment_method_id=16;
      data.payment_method_name='Cash On Delivery';
      data.payment_type_id=4;

    } else if(this.cashOption == 3) {
      data.payment_method_id = 59;
      data.payment_method_name = 'Card on Delivery';
      data.payment_type_id = 4;

    }
    // this._router.navigate(['/approved-order/thank-you/'+id]);
    this._globalService.showLoaderSpinner(true);
    this.global.getWebServiceData('checkout', 'PUT', data, '').subscribe(data => {
      if (data.status == 200) {
        this.orders=data.data;
        let url = this.prev_data == 'approved' ? '/approved-order/thank-you' : '/profile/thank-you';
        url = url+'/'+id;
        this._router.navigate([url]);
        this._globalService.showToast(data.msg);
        
      }else{
        this._globalService.showToast('Something went wrong. Please try again'); 
        
      }
      this._globalService.showLoaderSpinner(false);
    }, err => console.log(err), function() {
      this._globalService.showLoaderSpinner(false);


    });
    // this._router.navigate(['/approved-order/thank-you']);
  }
  payCardPayment(amount = 0,orderId = 0) {
  	try {
  	  if(amount == 0 || orderId == 0) {
  	  	throw "Invalid amount or Order id";
  	  }
  	  let paymentData = {
  	  	'order_id' : orderId,
  	  	'order_amount' : amount
  	  };
  	  this._globalService.showLoaderSpinner(true);
  	  this._checkoutService.doCcAvenuePayment(paymentData).subscribe(response => {
  	  	if(response && response['status'] == 200) {
  	  		console.log(response);
  	  		let ccAvenueForm = `<form id="nonseamless" method="post" name="redirect" action="https://secure.ccavenue.ae/transaction/transaction.do?command=initiateTransaction"/>
								        <input type="hidden" id="encRequest" name="encRequest" value="${response['enc_value']}">
								        <input type="hidden" name="access_code" id="access_code" value="${response['access_code']}">
								        <input type="hidden" name="response_type" id="response_type" value='JSON'>
								        <noscript><div id="msg"><div id="submitButton"><input type="submit" value="Click here to continue" class="button"></div></noscript>
								</form>`;
			this.paymentFormSampleHtml = this._domSanitizer.bypassSecurityTrustHtml(ccAvenueForm);
            this._changeDetector.detectChanges();
            if(this.paymentForm3D && this.paymentForm3D.nativeElement) {
               this.paymentForm3D.nativeElement.querySelector('form').submit();

            }
  	  	}
  	  	this._globalService.showLoaderSpinner(false);
  	  },
  	  err => {
  	  	this._globalService.showLoaderSpinner(false);
  	  	console.log("************** Error *******************");
  	  	console.log(err);

  	  }
  	  )
  	} catch(err) {
  		this._globalService.showLoaderSpinner(false);
  		this._globalService.showToast(err);

  	}
  	


  }
  /**
   * This method has been deprecated as previously we used mastercard payment
   * Now we are using ccavenue payment gateway
   * @date 17-01-2020
  */
  onPaymentFormSubmit(paymentForm) {
    try {
      if(!this.cashOption) {
        this._globalService.showToast("Please choose payment option");
        return false;
      }
      if(this.cashOption == 2) {
        this.palce_order();
        return;
      }
      if(this.paymenyForm.status == 'INVALID') {
        return false;
      }
      let paymentFormValue = {};
      paymentFormValue = this.paymenyForm.value;
      let expiryDate = paymentFormValue['expiry_date'].split('/');
      paymentFormValue['order_id'] = this.orderId;
      paymentFormValue['card_number'] = paymentFormValue['card_number'].replace(/ /g,'');
      paymentFormValue['payment_method_id'] = 51;
      paymentFormValue['payment_type_id'] = 2;
      paymentFormValue['payment_method_name'] = "Credit / Debit Card";
      paymentFormValue['exp_month'] = expiryDate[0].replace(/ /g,'');
      paymentFormValue['exp_year'] = expiryDate[1].replace(/ /g,'');
      // Do payment
      this._globalService.showLoaderSpinner(true);
      let url = this.prev_data == 'approved' ? '/approved-order' : '/profile';
      this._checkoutService.doCardPayment(paymentFormValue).subscribe(response => {
        console.log("************ Payment response ************");
        console.log(response);
        if(response && response['response'] && response['response']['acs_result'] && response['response']['acs_result']['status'] == 1) {
          let secure3dData = response['response']['acs_result']['response_data'];
          let secure3dFormData = `<form name="echoForm" method="POST" action="${secure3dData['3DSecure']['authenticationRedirect']['customized']['acsUrl']}" accept-charset="UTF-8">
                                   <input type="hidden" name="PaReq" value="${secure3dData['3DSecure']['authenticationRedirect']['customized']['paReq']}">
                                   <input type="hidden" name="TermUrl" value="http://gogrocery.ae:8062/api/front/v1/payment-req/">
                                   <input type="hidden" name="MD" value="">
                                   <noscript><div id="msg"><div id="submitButton"><input type="submit" value="Click here to continue" class="button"></div></noscript></form>`;
          
            this.paymentFormSampleHtml = this._domSanitizer.bypassSecurityTrustHtml(secure3dFormData);
            this._changeDetector.detectChanges();
            if(this.paymentForm3D && this.paymentForm3D.nativeElement) {
               this.paymentForm3D.nativeElement.querySelector('form').submit();

            }

        
        }
        if(response && response['response'] && response['response']['enroll_data']) {

          let secure3dData = response['response']['enroll_data'];
          let secure3dFormData = `<form name="echoForm" method="POST" action="${secure3dData['3DSecure']['authenticationRedirect']['customized']['acsUrl']}" accept-charset="UTF-8">
                                   <input type="hidden" name="PaReq" value="${secure3dData['3DSecure']['authenticationRedirect']['customized']['paReq']}">
                                   <input type="hidden" name="TermUrl" value="http://gogrocery.ae:8062/api/front/v1/payment-req/">
                                   <input type="hidden" name="MD" value="${secure3dData['3DSecureId']}">
                                   <noscript><div id="msg"><div id="submitButton"><input type="submit" value="Click here to continue" class="button"></div></noscript></form>`;
          
            this.paymentFormSampleHtml = this._domSanitizer.bypassSecurityTrustHtml(secure3dFormData);
            this._changeDetector.detectChanges();
            if(this.paymentForm3D && this.paymentForm3D.nativeElement) {
               this.paymentForm3D.nativeElement.querySelector('form').submit();
               
            }

        
        }
       /* if(response && response['response'] && response['response']['response_data']) {
           let secureHtml = this._domSanitizer.bypassSecurityTrustHtml(response['response']['response_data']['3DSecure']['authenticationRedirect']['simple']['htmlBodyContent']);
           this.paymentFormSampleHtml = secureHtml;
          this._changeDetector.detectChanges();
          if(this.paymentForm3D && this.paymentForm3D.nativeElement) {
            this.paymentForm3D.nativeElement.querySelector('form').submit();
            
          }
        }*/
        this._globalService.showLoaderSpinner(false);
        /*this._globalService.showLoaderSpinner(false);
        if(response && response['status'] == 200) {
          let receiptId = response['response']['transaction']['receipt'];
          this._router.navigate([url+'/thank-you/'+receiptId]);
        }*/

      },
      err => {
        console.log(err);
        this._globalService.showLoaderSpinner(false);
        let responseMessage = 'Something went wrong,please try again';
        if(err && err['status'] && err['status'] == 500) {
          this._globalService.showToast(responseMessage);
          return;
        }
        if(err && err['response'] && err['response']['result'] && err['response']['result'] == 'ERROR') {
          responseMessage = err['response'] && err['response']['error'] ? err['response']['error']['explanation'] : 'something went wrong';
        }
        this._globalService.showToast(responseMessage);

        this._router.navigateByUrl(url+'/failed-order/'+this.orderId+'?message='+responseMessage);
        
        
      }
      )

    }catch(err) {
      console.log("******************* Error *****************",err);
    }
  }
  
}
