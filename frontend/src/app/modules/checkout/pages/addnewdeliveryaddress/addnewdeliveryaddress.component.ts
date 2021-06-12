import { Component, OnInit, AfterViewInit, ViewChild, ElementRef, Output, EventEmitter, Input, SimpleChanges, Inject, PLATFORM_ID } from '@angular/core';
import { CheckoutService } from '../../../../global/service/checkout.service';
import { GlobalVariable } from '../../../../global/service/global';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { GlobalService } from '../../../../global/service/app.global.service';
import { isPlatformBrowser } from '@angular/common';

@Component({
  selector: 'app-addnewdeliveryaddress',
  templateUrl: './addnewdeliveryaddress.component.html',
  styleUrls: ['./addnewdeliveryaddress.component.css']
})
export class AddnewdeliveryaddressComponent implements OnInit, AfterViewInit {
  public countryList = [];
  public stateList = [];
  public addNewAddress: FormGroup;
  public isSubmitted: boolean = false;
  public state = null;
  public countryCode = GlobalVariable.COUNTRY_CODE;
  public carrierCode = GlobalVariable.CARRIER_CODE;
  customers_addressId: any;
  @ViewChild('deliveryAddressForm') deliveryAddressForm: ElementRef;
  @Output() onAddressAdd = new EventEmitter();
  @Input() displayIn: string;
  @Input() deleveryeditaddress: any;
  formmode: string = '';
  carrier_code: any;
  constructor(
    private _checkout: CheckoutService,
    private _formBuilder: FormBuilder,
    private _GlobalService: GlobalService,
    @Inject(PLATFORM_ID) private platformId: Object

  ) {

  }
  ngOnChanges(changes: SimpleChanges) {
    this.addNewAddress = this._formBuilder.group({
      'name': ['', Validators.required],
      // 'last_name' : ['',Validators.required],
      'apartment_name': ['', Validators.required],
      // 'nearest_landmark' : [''],
      // 'country' : ['',Validators.required],
      'state': ['', Validators.required],
      'area': ['', Validators.required],
      // 'pincode' : [''],
      'mobile_no': ['', Validators.required],
      'carrier_code': ['', Validators.required],
      // 'alternative_mobile_no' : [''],
      'is_default': ['']
    },
      {

      }
    );
    if (changes.deleveryeditaddress.currentValue.length==0) {
      this.formmode = 'new'
      this.addNewAddress.reset();
    }
    else {
          
      this.setformdata(changes.deleveryeditaddress.currentValue);
      this.formmode = 'edit'
    }

    // this.setformdata()
    // You can also use categoryId.previousValue and 
    // categoryId.firstChange for comparing old and new values
  }

  setformdata(deleveryeditaddress) {
    
    this.addNewAddress.controls['name'].setValue(deleveryeditaddress.delivery_name);
    this.addNewAddress.controls['apartment_name'].setValue(deleveryeditaddress.delivery_street_address);
    this.addNewAddress.controls['state'].setValue(deleveryeditaddress.billing_state);
    this.state = +deleveryeditaddress.billing_state;
    this.addNewAddress.controls['area'].setValue(deleveryeditaddress.billing_landmark);
    this.addNewAddress.controls['mobile_no'].setValue(deleveryeditaddress.delivery_phone % 10000000);
    this.carrier_code = deleveryeditaddress.delivery_phone.substring(deleveryeditaddress.delivery_phone.length - 9, deleveryeditaddress.delivery_phone.length - 7)
    // this.addNewAddress.controls['carrier_code'].setValue(this.carrier_code);
    this.addNewAddress.get('carrier_code').setValue(parseInt(this.carrier_code));
    this.addNewAddress.controls['is_default'].setValue(deleveryeditaddress.set_primary);
    this.customers_addressId = deleveryeditaddress.id
  }
  ngOnInit() {
    if (isPlatformBrowser(this.platformId)) {
      this.getCountryList();
      this.getStateByCountryId(221);
    }

    //On chnaging country selecte corrosponding city
    // this.f['country'].valueChanges.subscribe(countryId => {
    // 	this.getStateByCountryId(countryId);
    // });
  }
  ngAfterViewInit() {
    if (this.displayIn == 'desktop') {
      var divheight = document.getElementById('scrollred').clientHeight;

      console.log('scrolled', divheight)
      setTimeout(()=>{
        window.scroll({
          top: divheight,
          behavior: 'smooth'
        });
      },50)
      // this.deliveryAddressForm.nativeElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  }

  get f() {
    return this.addNewAddress.controls;
  }

  /**
   * On form submit
  */
  onAddNewAddressSubmit() {
    this.isSubmitted = true;
    for (let controller in this.addNewAddress.controls) {
      this.addNewAddress.get(controller).markAsTouched();
    }

    if (this.addNewAddress.invalid) {
      return;
    }
    let addNewAddress = this.addNewAddress.value;
    addNewAddress['mobile_no'] = (GlobalVariable.COUNTRY_CODE.toString() + addNewAddress['carrier_code'].toString() + addNewAddress['mobile_no'].toString()).trim();

    if (this.formmode == 'edit') {

      this._checkout.EditDeliveryAddress(addNewAddress, this.customers_addressId).subscribe(response => {
        if (response && response['status'] == 200) {
          this._GlobalService.showToast('Addess has beed edited successfully!')
          this.onAddressAdd.emit(true);
        }
      });

    }
    else {
      this._checkout.addNewDeliveryAddress(addNewAddress).subscribe(response => {
        if (response && response['status'] == 200) {
          this.onAddressAdd.emit(true);
        }
      });
    }
  }

  cancelAddNewAddress() {
    this.onAddressAdd.emit(true);
  }



  /**
   * Get country list
   * @access public
  */
  getCountryList() {
    this._checkout.getCountryList().subscribe(response => {
      if (response && response['status'] == 200) {
        this.countryList = response['data'];
      }
    });
  }
  /**
   * Method for getting city by country id
   * @access public
  */
  getStateByCountryId(countryId = 221) {
    this._checkout.getStateListByCountryId(countryId).subscribe(response => {
      if (response && response['status'] == 200) {

        this.stateList = response['data'];
      }
    });
  }
}
