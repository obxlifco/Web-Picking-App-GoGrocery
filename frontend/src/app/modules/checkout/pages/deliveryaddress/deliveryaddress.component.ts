import { Component, OnInit, EventEmitter, Output, ViewChild, ElementRef, AfterViewInit, Input, Inject, PLATFORM_ID } from '@angular/core';
import { CheckoutService } from '../../../../global/service/checkout.service';
import { GlobalService } from '../../../../global/service/app.global.service';
import { isPlatformBrowser } from '@angular/common';

declare var $;
@Component({
  selector: 'app-deliveryaddress',
  templateUrl: './deliveryaddress.component.html',
  styleUrls: ['./deliveryaddress.component.css']
})
export class DeliveryaddressComponent implements OnInit, AfterViewInit {
  showAddNewDeliveryAddressForm: boolean = false;
  @ViewChild('deliveryAddressContainer') deliveryAddressContainer: ElementRef;
  public selectedAddress;
  public deliveryAddress = [];
  @Output() chnageDeliveryAddress = new EventEmitter();
  singleDeliveryAddress: any;
  constructor(
    private _checkout: CheckoutService,
    private _globalService: GlobalService,
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
    this._checkout.getAllDeliveryAddress().subscribe(response => {
      if (response && response['status'] == 200) {
        this.deliveryAddress = response['data'];
        /*console.log("*************** All delivery address *****************");
        console.log(this.deliveryAddress);*/
        this.setDefaultAddress();
      } else {
        this.deliveryAddress = [];
      }
    });
  }
  /**
   * Set default address
   * @access public
  */
  setDefaultAddress() {
    let defaultAddress = this.deliveryAddress.filter(address => {
      if (address['set_primary'] == 1) {
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
  }
  /**
   * On new delivery address added
   * @access public
  */
  onNewAddressAdded(status) {
    if (status) {
      this.getAllDeliveryLocation();
    }
    this.showAddNewDeliveryAddress();
    this.deliveryAddressContainer.nativeElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
  /**
   * Method on deleting delivery address
   * @access public
  */
  deleteDeliveryAddress(addressId) {
    this._checkout.removeDeliveryAddress(addressId).subscribe(response => {
      if (response && response['status'] == 200) {
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
  editDeliveryAddress(singleDeliveryAddress) {
    this.singleDeliveryAddress = singleDeliveryAddress;
    this.showAddNewDeliveryAddressForm = true;
    var divheight = document.getElementById('scrollred').clientHeight;

    console.log('scrolled', divheight)
    setTimeout(()=>{
      window.scroll({
        top: divheight,
        behavior: 'smooth'
      });
    },50)
    

  }


}