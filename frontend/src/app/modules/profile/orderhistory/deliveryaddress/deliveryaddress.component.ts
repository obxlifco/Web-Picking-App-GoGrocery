import { Component, OnInit,EventEmitter,Output,ViewChild,ElementRef,AfterViewInit, Inject, PLATFORM_ID} from '@angular/core';
import {CheckoutService} from '../../../../global/service/checkout.service';
import {GlobalService} from '../../../../global/service/app.global.service';
import { AuthenticationService } from '../../../../global/service/authentication.service';
import { Router, ActivatedRoute, NavigationEnd } from '@angular/router';
import {AddnewdeliveryaddressComponent} from '../../../../modules/checkout/pages/addnewdeliveryaddress/addnewdeliveryaddress.component';
import { isPlatformBrowser } from '@angular/common';

@Component({
  selector: 'app-deliveryaddress',
  templateUrl: './deliveryaddress.component.html',
  styleUrls: ['./deliveryaddress.component.css']
})
export class DeliveryaddressComponent implements OnInit {

  showAddNewDeliveryAddressForm:boolean = false;
  @ViewChild('deliveryAddressContainer') deliveryAddressContainer:ElementRef;
  public selectedAddress;
  public deliveryAddress = [];
  public isProcessing:boolean;
  @Output() chnageDeliveryAddress = new EventEmitter();
  singleDeliveryAddress: any;
  constructor(
    private _checkout:CheckoutService,
    private _globalService:GlobalService,
    public authenticationService:AuthenticationService,
    private _router: Router,
    @Inject(PLATFORM_ID) private platformId: Object

  ) { }

  ngOnInit() {
    if (isPlatformBrowser(this.platformId)) {
      this.getAllDeliveryLocation();
    }
  }
  ngAfterViewInit() {
    //this.onChangeDeliveryAddress(this.selectedAddress);
  }
  /**
   * Method for getting all user location
   * @access public
  */
  getAllDeliveryLocation() {
    this.isProcessing = true;
    this._checkout.getAllDeliveryAddress().subscribe(response => {
      if(response && response['status'] == 200){
        this.deliveryAddress = response['data'];
        /*console.log("*************** All delivery address *****************");
        console.log(this.deliveryAddress);*/
        this.setDefaultAddress();
      } else {
        this.deliveryAddress = [];
      }
      this.isProcessing = false;
    });
  }
  /**
   * Set default address
   * @access public
  */
  setDefaultAddress() {
    let defaultAddress = this.deliveryAddress.filter(address => {
      if(address['set_primary'] == 1) {
        this.selectedAddress = address['id'];
        //alert(this.selectedAddress);
        this.onChangeDeliveryAddress(this.selectedAddress);
        return address;
      }
    })
  }
  /**
   * Method on showing delivery address
  */
  showAddNewDeliveryAddress() {
    this.showAddNewDeliveryAddressForm = !this.showAddNewDeliveryAddressForm;
    this.singleDeliveryAddress = [];
    var divheight = document.getElementById('scroll').clientHeight;

    console.log('scrolled', divheight)
    setTimeout(()=>{
      window.scroll({
        top: divheight,
        behavior: 'smooth'
      });
    },50)

  }

  /**
   * On new delivery address added
   * @access public
  */
  onNewAddressAdded(status) {
    if(status) {
      this.getAllDeliveryLocation();
    }
    this.showAddNewDeliveryAddress();
    this.deliveryAddressContainer.nativeElement.scrollIntoView({behavior: 'smooth',block: 'center'});
  }
  /**
   * Method on deleting delivery address
   * @access public
  */
  deleteDeliveryAddress(addressId) {
    this._checkout.removeDeliveryAddress(addressId).subscribe(response => {
      if(response && response['status'] == 200) {
        this._globalService.showToast("Your address has been deleted successfully");
        this.getAllDeliveryLocation();
      }
    });
  }
  /**
   * Method on chnage delivery address
   * @access public
  */
  onChangeDeliveryAddress(deliveryAddressId) {
    this.chnageDeliveryAddress.emit(deliveryAddressId);
  }
  navigate(data:number,order_id:any='') {
    if(data==0) {//Profile
      this._router.navigate(['/home']);
    }else if(data==1) {//Profile
      this._router.navigate(['/profile/profiledetails']);
    } else if(data==2) {//Delivery  Address
      this._router.navigate(['/profile/delivery-address']);
    } else if(data==3) {//chaange password
      this._router.navigate(['/profile/change-password']);
    } else if(data==4) {//wishlist
      this._router.navigate(['/profile/order-history']);
    }else if(data==5) {//wishlist
      this._router.navigate(['/profile/wishlist']);
    }
  }


  editDeliveryAddress(singleDeliveryAddress) {
    this.singleDeliveryAddress = singleDeliveryAddress;
    console.log(this.singleDeliveryAddress)
    this.showAddNewDeliveryAddressForm = true;
    var divheight = document.getElementById('scroll').clientHeight;

    console.log('scrolled', divheight)
    setTimeout(()=>{
      window.scroll({
        top: divheight,
        behavior: 'smooth'
      });
    },50)
    

  }
}
