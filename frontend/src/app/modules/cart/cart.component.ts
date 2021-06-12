import { Component, OnInit, Inject, PLATFORM_ID } from '@angular/core';
import {CartService} from '../../global/service/cart.service';
import {GlobalService} from '../../global/service/app.global.service';
import {MenuService} from '../../global/service/menu.service';
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material';
import { LoginComponent } from '../../login/login.component';
import {Router} from '@angular/router';
import { isPlatformBrowser } from '@angular/common';
@Component({
  selector: 'app-cart',
  templateUrl: './cart.component.html',
  styleUrls: ['./cart.component.css']
})
export class CartComponent implements OnInit {
    public objectkeys = Object.keys;
    public totalPrice = 0.0;
    public isSyncData = false;
    constructor(
      public cartService:CartService,
      private _router:Router,
      public dialog: MatDialog,
      private _menuservice:MenuService,
      private _globalService:GlobalService,
      @Inject(PLATFORM_ID) private platformId: Object
    ) {
  }
  
  ngOnInit() {

    if (isPlatformBrowser(this.platformId)) {
      // this._globalService.getIpAddress().subscribe(response => {
      //   let ipAddress = response && response['ip'] ? response['ip'] : '';
      //   this.cartService.requestedIp = ipAddress;
        this.cartService.requestedIp = this._globalService.getRequestedIpFromCookie()
        this.cartService.getCartDataAndRestoreItem();
        this.cartService.fetchedAndRestored.subscribe(response => {
          console.log("*************** Response **********************");
          console.log(response);
          
          this.isSyncData = response;
  
        });
  
  
  
      // });
    }
  
    
  }
  /**
   * Method to navigate to url
  */
  navigateToUrl(url) {
    if(this.cartService['cartDetails'] && this.cartService['cartDetails']['minimum_order_amount_check'] == 'no') {
       
      this._globalService.showToast("Minimum order should be above AED "+this.cartService['cartDetails']['minimum_order_amount']);
       return false;
    }
    if(!localStorage.getItem('currentUser')) {
      let userRedirectData = {
        'action' : 'sign-in',
        'redirectUrl' : url,
      }
      this._menuservice.signinSignuppopup$.next(userRedirectData);
      return false;
    }
  	this._router.navigate([url]);
  }
  //login dialog
  /*loginComponent: MatDialogRef<LoginComponent> | null;
  openLoginDialog() {
    this.loginComponent = this.dialog.open(LoginComponent, {
      disableClose: true
    });
    }*/
  /*getTotalPrice() {
    if(Object.keys(this.cartService.cartDetails).length > 0) {
      console.log("***************** Total price ****************");
      alert("hiii");
      for(let productKey in this.cartService.cartDetails) {
        this.totalPrice = this.totalPrice+this.cartService[productKey]['new_default_price'];


      }
    }
  }*/
  navigateToDetailPage(productSlug) {
     this._router.navigate(['details/'+productSlug]);
     window.scroll(0,0);
  }
}
