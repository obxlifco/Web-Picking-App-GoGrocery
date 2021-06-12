import { Component, OnInit,AfterViewInit, Inject, PLATFORM_ID} from '@angular/core';
import { Global } from '../../../global/service/global';
import { AuthenticationService } from '../../../global/service/authentication.service';
import { Router, ActivatedRoute, NavigationEnd } from '@angular/router';
import { GlobalService } from '../../../global/service/app.global.service';
import { DialogsService } from '../../../global/dialog/confirm-dialog.service';
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { LoaderService } from '../../../global/service/loader.service';
import { CartService } from '../../../global/service/cart.service';
import Checkout from '../../../global/checkout/checkout';
import { CancelreasonComponent } from './cancelreason/cancelreason.component';
// var checkout = require('https://test-gateway.mastercard.com/checkout/version/52/checkout.js');
import { isPlatformBrowser } from '@angular/common';
declare var Checkout:any;



@Component({
  selector: 'app-orderhistory',
  templateUrl: './orderhistory.component.html',
  styleUrls: ['./orderhistory.component.css']
})
export class OrderhistoryComponent implements OnInit,AfterViewInit{
  public orders=[];
  public status_class:any;
  public selectedTabIndex:number = 0;
  public isProcessing:boolean;
  public orderStatus:number = 100;
  constructor(
    public global: Global,
		public authenticationService:AuthenticationService,
		private _router: Router,
    public _globalService: GlobalService,
    public dialog: MatDialog,
    private dialogsService: DialogsService,
		private _loader:LoaderService,
    public cartService:CartService,
    @Inject(PLATFORM_ID) private platformId: Object

  ) { 
  }

  private _loadExternalScript(scriptUrl: string,successCallBck,errorCallBck) {
    return new Promise((resolve, reject) => {
      const scriptElement = document.createElement('script')
      scriptElement.src = scriptUrl
      scriptElement.setAttribute('data-error',successCallBck);
       scriptElement.setAttribute('data-cancel',errorCallBck);
      scriptElement.onload = resolve
      document.body.appendChild(scriptElement)
  })
  }

  ngAfterViewInit() {

  }
  ngOnInit() {
    /*this._loadExternalScript("https://test-gateway.mastercard.com/checkout/version/53/checkout.js",
      function(){
        

      },
      function(error) {
        console.log(error);

      }
    );*/

    if (isPlatformBrowser(this.platformId)) {
      this.loadOrders();
    }
  }
  onPaymentSuccess() {
    return 'success';

  }
  onPaymentError(error = '') {
    console.log(error);
    return '';

  }
  onTabChange(event) {
    this.selectedTabIndex = event['index'];
    this.loadOrders();
  }

  loadOrders() {
    this.isProcessing = true;
    let orderType = this.selectedTabIndex==0 ? 'substitute' : this.selectedTabIndex==1 ? 'present' : 'past';
    this._globalService.showLoaderSpinner(true);
    this.global.getWebServiceData('order-history', 'GET', '', '','?req_type='+orderType).subscribe(data => {
        
        if (data.status == 200) {
          this.orders=data.data;
          console.log("********** Order details****************");
          console.log(this.orders);
        } else if(data['status'] == 204) {
          this.orders = [];
        }

        if(this.selectedTabIndex==0){
          if(this.orders.length>0){
            this.orders.forEach(element => {
              element.id = btoa(element.id);
            });
          }
        }
    },
    err => {
      this._globalService.showLoaderSpinner(false);
      this._globalService.showToast("Something went wrong,please try again");
    }, 
    () => {
      this.isProcessing = false;
      this._globalService.showLoaderSpinner(false);
    });
  }
  navigate(data:number, order_id:any=''){
    if(data==0){//Profile
			this._router.navigate(['/home']);
		}else if(data==1){//Profile
			this._router.navigate(['/profile/profiledetails']);
    }else if(data==2){//Delivery  Address
			this._router.navigate(['/profile/delivery-address']);
		}
		if(data==3){//chaange password
			this._router.navigate(['/profile/change-password']);
    }
    if(data==4){//wishlist
			this._router.navigate(['/profile/wishlist']);
    }
  }
  openCheckout() {
    /*console.log(Checkout);
    Checkout.configure({
                merchant: 'TEST900700',
                order: {
                    amount: function() {
                        //Dynamic calculation of amount
                        return 80 + 20;
                    },
                    currency: 'USD',
                    description: 'Ordered goods',
                   id: 'TEST'
                },
                interaction: {
                    operation: 'AUTHORIZE', // set this field to 'PURCHASE' for Hosted Checkout to perform a Pay Operation.
                    merchant: {
                        name: 'MASHREQ TEST',
                        address: {
                            line1: '200 Sample St',
                            line2: '1234 Example Town'            
                        }    
                    }
                                                                }
            });*/
    //Checkout.showPaymentPage();
    if(Checkout) {
      console.log(Checkout);

    }
    
   
  }
  errorCallback(error) {
     //console.log(JSON.stringify(error));
  }
  cancelCallback() {
        console.log('Payment cancelled');
  }
  public cancelComponent: MatDialogRef<CancelreasonComponent> | null;
  
  cancel_now(order_id:number){
    this.cancelComponent = this.dialog.open(CancelreasonComponent, {
			  disableClose: true,
		});
		this.cancelComponent.afterClosed().subscribe(response => {
      if (response) {
        let postdata = response;
        response.order_id = order_id;
        this.global.getWebServiceData('cancel-order/'+order_id, 'POST', postdata, '').subscribe(data => {
          if (data.status == 200) {
            this.loadOrders();
            this._globalService.showToast('Order cancelled successfully');
          }
        }, err => {
            this._globalService.showToast(err['message']);
        });
      }
		},
    err => {
     
    }

    );
  }
  
  //  reorder start here...
  reOrder(order_data) {
    this.cartService.emptyCart();
    order_data.order_products.forEach(order_product => {
      this.cartService.addOrRemoveItem(order_product.product_id,order_product.quantity,order_product.variation);
    });
    // this.cartService.addOrRemoveItem(selectedProductId,1);
    // console.log(order_data.order_products);
    this._router.navigate(['/cart']);
  }
}
