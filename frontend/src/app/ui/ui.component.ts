import { Component, OnInit, AfterViewInit, NgZone, Inject,OnChanges} from '@angular/core';
import { HeaderComponent } from './header/header.component';
import { FooterComponent } from './footer/footer.component';
import { mergeMap, map, filter } from 'rxjs/operators';
import { Router, NavigationEnd, ActivatedRoute } from '@angular/router';
import { DOCUMENT } from '@angular/platform-browser';
// import { Title, DOCUMENT } from '@angular/platform-browser';
import { CookieService } from 'ngx-cookie';
import {HttpClient} from '@angular/common/http';
import { Global, GlobalVariable } from '../global/service/global';
import { GlobalService } from '../global/service/app.global.service';
import { DialogsService } from '../global/dialog/confirm-dialog.service';
import { WarehouseService } from '../global/service/warehouse.service';
import { AuthenticationService } from '../global/service/authentication.service';
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { WarehouselistComponent } from '../global/dialog/warehouselist/warehouselist.component';
import { LocationdialogComponent } from '../global/dialog/locationdialog/locationdialog.component';
import { FinetuninglocationComponent } from '../global/dialog/finetuninglocation/finetuninglocation.component';
import { NowarehousefoundComponent } from '../global/dialog/nowarehousefound/nowarehousefound.component';
import { CartService } from '../global/service/cart.service';
import { WINDOW,LOCAL_STORAGE} from '@ng-toolkit/universal';
import { isPlatformBrowser, isPlatformServer } from '@angular/common';
import { PLATFORM_ID } from '@angular/core';
import { storecategorylistComponent } from '../global/dialog/storecategorylist/storecategorylist.component';
import { StoreCategoryService } from '../global/service/storecategory.service';
import { SelectOptionComponent } from '../global/dialog/selectoption/selectoption.component';



@Component({
  selector: 'app-ui',
  templateUrl: './ui.component.html',
  styleUrls: ['./ui.component.css']
})
export class UiComponent implements OnInit{
  public is_facebook: boolean = false;
  public sub_q: any;
  public isCMS: boolean = false;
  public isPromotion:boolean = false;
  public showSpinnerLoaded: boolean = false;
  public isLoaded: boolean = false;
  public is_dist: boolean = false;
  public facebookStore: boolean = false;
  public pageType: number = 1;
  public dstore: any;
  public userGlobalLocation: Object;
  public ipAddress;
  public isBrowser;
  public postdata : any ={};
  constructor(
    @Inject(WINDOW) private window: Window,
    @Inject(LOCAL_STORAGE) private localStorage: any,
    @Inject(PLATFORM_ID) platformId: Object,
    private _cookieService: CookieService,
    private global: Global,
    private globalService: GlobalService,
    public router: Router,
    private activatedRoute: ActivatedRoute,
    // private titleService: Title,
    private zone: NgZone,
    private dialogsService: DialogsService,
    private _warehouse: WarehouseService,
    private _cartService: CartService,
    private _storeCategoryServise: StoreCategoryService,
    public dialog: MatDialog,
    private http: HttpClient,
    private _authService:AuthenticationService,
    @Inject(DOCUMENT) private document: any
  ) {
    this.isBrowser = isPlatformBrowser(platformId);
    console.log("************** Is browser ******************",this.isBrowser);
    this.router.events.subscribe((ev) => {
      if (ev instanceof NavigationEnd) { 
        this.getCartData();

      }
    });
    // Sub domain setup for staging....
    let site_url = this.router.url;
    
    // console.log("************** Site url **************");
    // console.log(site_url);
    if (site_url.includes('?dstore')) {
      this.dstore = site_url.split('?dstore=')[1];
      if (this.dstore !== undefined && this.dstore != '') {
        this._cookieService.putObject('dstore', this.dstore, this.globalService.getCookieOption());
      } else if (this.dstore == '1') {
        this._cookieService.putObject('dstore', this.dstore, this.globalService.getCookieOption());
      }
    }
    //console.log('Called Constructor' + this.dstore);
    // Sub domain setup for staging....
    this.is_facebook = false;
    this.sub_q = this.activatedRoute.queryParams.subscribe(params => {
      if (params['isfacebook'] !== undefined) {
          this.is_facebook = true;
      }

      if (params['token'] !== undefined) {
        let decoded_token = JSON.parse(atob(params['token']));
        this._cookieService.putObject('campaign_token', decoded_token);
        if (decoded_token && decoded_token['type'] == 'unsubscribed') {
          setTimeout(() => {
            this.dialogsService.confirm('Warning', 'Do you really want to unsubscribe newsletter?').subscribe(res => {
              if (res) {
                this.updateSubscribe(decoded_token['email'], decoded_token['campaign_id'], decoded_token['company_website_id']);
              }
            });
          });
        } else if (decoded_token && decoded_token['type'] == 'clicked') {
          this.updateUserClick(decoded_token['email'], decoded_token['campaign_id'], decoded_token['company_website_id']);
        }
      }
    });


  }

  ngOnInit() {
    this.userGlobalLocation = this.globalService.getCookie('current_user_location') != '' ? JSON.parse(this.globalService.getCookie('current_user_location')) : {};
  
    if(this.isBrowser && !this.router.url.includes('payment-options-approved') && !this.router.url.includes('approved-order') && !this.router.url.includes('reset-password') && !this.router.url.includes('contact-us') && !this.router.url.includes('promotion') && !this.router.url.includes('substitute-product') && !this.router.url.includes('success-substitute')) {
      this.checkIfUserLocationExists();

    }
    
    this.isLoaded = false;
    // set global data in cookie
    this.is_dist = false;
    
    this.global.globalData().subscribe(
      data => {
        if (data.status) {
          data['pagesize'] = "15";
          this._cookieService.putObject('globalData', data, this.globalService.getCookieOption());
          this.is_dist = false;
          this.isLoaded = true;
          this.isPromotion = false;
          this.globalService.globalDataSource.next(true);
          // Get all cart data
          //this.getCartData(data['requested_ip']);
        } else {
          this.router.navigate(['/404']);
          this.isLoaded = true;
          this.isPromotion = false;
        }
      }
    );
    

    if (this.router.url.includes('editor')) {

      this.isCMS = true;
      this.isLoaded = false;
      this.isPromotion = false;
      // alert(this.isCMS);
    }

    if (this.router.url.includes('promotion')) {
      this.isCMS = false;
      this.isLoaded = false;
      this.isPromotion = true;
      // alert(this.isCMS);
    }

    // set user ip address in cookie
    // this.global.Ipaddress().subscribe(
    //     data => {
    //       this._cookieService.put('ipaddress', data.ip, this.globalService.getCookieOption());
    //       let userGeo: any = {};
    //       userGeo['city'] = data.city;
    //       userGeo['country_code'] = data.country_code;
    //       userGeo['country_name'] = data.country_name;
    //       userGeo['ip'] = data.ip;
    //       userGeo['region_code'] = data.region_code;
    //       userGeo['region_name'] = data.region_name;
    //       userGeo['zip'] = data.zip;
    //       this._cookieService.putObject('userGeo', userGeo, this.globalService.getCookieOption());
    //     }
    // );
    // route state change event
    // this.router.events.pipe(
    //  		 filter((event) => event instanceof NavigationEnd)
    //  		).pipe(map(() => this.activatedRoute))
    //  		.pipe(map((route) => {
    //    		while (route.firstChild) route = route.firstChild;
    //    		return route;
    //  		})).pipe(
    //  		 filter((route) => route.outlet === 'primary'))
    //  		.mergeMap((route) => route.data)
    //  		.subscribe((event) => { 
    //            this.pageType = event['pageType'];
    //            this.facebookStore = event['facebook_store'];
    //            if(this.facebookStore) {
    //                 this._cookieService.put( 'facebookStore', '1' );
    //            }
    //            window.scrollTo(0, 0);
    //            if(event['is_cms']) { //check if current route is before logged in
    //          	    this.isCMS = true; //hide sidebar from the page layout 
    //         	} else { // current route is after logged in
    //             this.isCMS = false; //show sidebar on the page layout if route is after logged in
    //             this.zone.run(() => {
    //                this.isCMS = false;
    //             });
    //        	}
    //  		});

    this.globalService.loadSpinnerChange$.subscribe(
      (value) => {
        this.showSpinnerLoaded = value;
      }
    );
    this._authService.currentUser.subscribe(response => {
      console.log("**************** Current user data *************");
      console.log(response);

    });


    // Auth service
    /* this.authService.authState.subscribe((user) => {
           if(user) {
     
               let userData = {
                   'user_email' : user['email'] ? user['email'] : '',
                   'first_name' : user['firstName'] ? user['firstName'] : '',
                   'last_name'  : user['lastName'] ? user['lastName'] : '',
                   'photo_url'  : user['photoUrl'] ? user['photoUrl'] : '',
                   'google_login_id' : user['provider'] == 'GOOGLE' ? user['id'] : '',
                   'facebook_id' : user['provider'] == 'FACEBOOK' ? user['id'] : '',
                   'phone' : '',
                   'device_id' : clientIp,

               }
               console.log("************ User data ************");
               console.log(userData);
               this.authenticationService.socialLogin(userData).subscribe(response => {
                   if(response && response['status'] == 200) {
                       localStorage.setItem('userData', JSON.stringify(response['data']));
                        if(Object.keys(this.actionData).length > 0 && this.actionData['redirectUrl']) {
                            this.router.navigate([this.actionData['redirectUrl']]);
                        } 


                   }

               },
               (err) => {
                   this.isError = true;
                   this.error = "Something went wrong";

               }
              );
               


           }
        },
        (err) => {
            console.log("*************** Error occurred in social login *****************");
            console.log(err);

        },
        () => {
            
        }
        );*/
  }

  /**
   * Method for getting cart list
   * @access public
  */
  // getCartData() {

  //  this._cartService.initiateCartData();
  //   this.http.get<{ip:string}>('https://api6.ipify.org?format=json')
  //   .subscribe( data => {
  //     this.ipAddress = data && data['ip'] ? data['ip'] : '';
  //     this._cookieService.put('client_ip',this.ipAddress);
  //     console.log("*************** Client ip address ***************");
  //     console.log(this.ipAddress);
  //     this.fetchCardDetails(this.ipAddress);

  //   })
    
  // }

  getCartData() {
    // this._cartService.initiateCartData();
    // this.http.get<{ip:string}>('https://api6.ipify.org?format=json')
    // .subscribe( data => {
    //   this.ipAddress = data && data['ip'] ? data['ip'] : '';
    //   this._cookieService.put('client_ip',this.ipAddress);
    //   console.log("************** Client ip address **************");
    //   console.log(this.ipAddress);
    //   this.fetchCardDetails(this.ipAddress);

    // })
    
    this._cartService.initiateCartData();
    if (localStorage) {
      if(localStorage.getItem('client_ip')){
        this.ipAddress = localStorage.getItem('client_ip');
      }else{
        this.ipAddress = Math.floor(Math.random() * 1000000000);
        }
      localStorage.setItem('client_ip', this.ipAddress);
      console.log("************* Client ip address *************");
      console.log(this.ipAddress);
      this.fetchCardDetails(this.ipAddress);
    }
  }

  fetchCardDetails(requestedIp) {
    //alert(requestedIp);
    this._cartService.requestedIp = requestedIp;

    this._cartService.getCartDetails().subscribe(response => {
      // console.log("***************** Cart response *****************");
      // console.log(response);
      // console.log("***************** Cart response *****************");
      if (response && response['status'] == 200) {
        let cartListForStorage = {};
        let cartData = {};
        response['data'].forEach(cartData => {
          let productId = cartData['product_id']['id'];
          cartListForStorage[productId] = {
            'product_id': productId,
            'quantity': cartData['quantity'],
            'price': cartData['new_default_price'] ? cartData['new_default_price'].toFixed(2) : 0,
            'default_price': cartData['default_price'] ? cartData['default_price'].toFixed(2) : 0,
            'new_default_price': cartData['new_default_price'] ? cartData['new_default_price'].toFixed(2) : 0,
            'new_default_price_unit': cartData['new_default_price_unit'] ? cartData['new_default_price_unit'].toFixed(2) : 0,
            'product_image': cartData['product_id']['product_image'],
            'product_name': cartData['product_name'],
            'product_slug': cartData['product_slug']
          }
        });
        cartData['cart_list'] = Object.keys(cartListForStorage).length > 0 ? cartListForStorage : {};
        cartData['total_amount'] = response['total_amount'];
        cartData['minimum_order_amount'] = response['minimum_order_amount'];
        cartData['minimum_order_amount_check'] = response['minimum_order_amount_check'];
        let stringifyData = JSON.stringify(cartData);
        if (localStorage) {
          localStorage.setItem('cart_details', stringifyData);
        }
        //this._cookieService.putObject('cart_details',cartData);
        this._cartService.cartDetails = cartData;
      }
    });
  }

  ngAfterViewInit() {
    
  }

  updateSubscribe(email: string, campaign_id: number, website_id: number) {
    let request_data: any = { email: email, website_id: website_id, campaign_id: campaign_id }
    // this.global.updateSubscribe(request_data).subscribe(
    //        data => {
    //          if(data.status){
    //            this.dialogsService.alert('Notification','You have successfully unsubscribed');
    //          }else{
    //            this.dialogsService.alert('Error',data.message);
    //          }
    //        },
    //        err => console.log(err),
    //        function(){
    //        }
    //   );
  }

  updateUserClick(email: string, campaign_id: number, website_id: number) {
    let request_data: any = { email: email, website_id: website_id, campaign_id: campaign_id }
    this.global.updateClick(request_data).subscribe(
      data => {
      },
      err => console.log(err),
      function () {
      }
    );
  }
  /**
 * Method checking user location
 * @access public
*/
  checkIfUserLocationExists() {

    if (Object.keys(this.userGlobalLocation).length > 0) {

      if (this.userGlobalLocation['latitude'] && this.userGlobalLocation['longitude'] && (!this.userGlobalLocation['selected_warehouse_id'] || this.userGlobalLocation['selected_warehouse_id'] == '')) {
        this.getUserMapPopUp(this.userGlobalLocation);
      }
    } else {
      this.getUserDeliveryLocation();
    }
  }

  /**
   * Method for tracing user delivery location
   * @access public
  */
  getUserDeliveryLocation() {
    let locationDialog = this.dialog.open(LocationdialogComponent, {
      disableClose: true
    });

    locationDialog.afterClosed().subscribe(response => {
      // Call user location fine tuning
      if (response && response['latitude'] && response['longitude']) {
        this.userGlobalLocation['latitude'] = response['latitude'];
        this.userGlobalLocation['longitude'] = response['longitude'];
        this.globalService.updateCookieByKeyAndData(this.userGlobalLocation, 'current_user_location');
      }
      this.getUserMapPopUp(this.userGlobalLocation);
    });
  }
  /**
   * Method for pop up current user map
   * @access public
  */
  getUserMapPopUp(userLocation = {}) {
    console.log('************** User location popup called *****************');
    console.log(userLocation);
    let mapLocationDialogRef = this.dialog.open(FinetuninglocationComponent, {
      disableClose: true,
      data: userLocation
    });
    mapLocationDialogRef.afterClosed().subscribe(response => {
      if(response) {
        this.userGlobalLocation['latitude'] = response['latitude'];
        this.userGlobalLocation['longitude'] = response['longitude'];
        this.globalService.updateCookieByKeyAndData(this.userGlobalLocation, 'current_user_location');
        // this.getNearestWareHouse(this.userGlobalLocation);
        this.getStoreCategoryList(this.userGlobalLocation);

      }
      
    });
  }

   /**
   * Method for getting store category
   * @access public
  */
  getStoreCategoryList(latitudeLongitudeObject: Object = {}){
    console.log('************** Store Category List load *****************');
    console.log(latitudeLongitudeObject);
    console.log(latitudeLongitudeObject['website_id'],'website_id')
    this.postdata = latitudeLongitudeObject;
    console.log(this.postdata, 'postdata')
    this.postdata.website_id = latitudeLongitudeObject['website_id'] ? latitudeLongitudeObject['website_id'] : 1;
    console.log(this.postdata, 'postdata');
    this._storeCategoryServise.getAllStoreCategory(this.postdata).subscribe(response => {
      if (response && response['status'] == 1){
        let storeCategoryDialogRef = this.dialog.open(storecategorylistComponent, {
          disableClose: true,
          data: response['data']
        });
        storeCategoryDialogRef.afterClosed().subscribe(response =>{
          if(response){
            let storecategoryData = response;
            latitudeLongitudeObject['storetype_id']= storecategoryData.storecategoryID;
            console.log(latitudeLongitudeObject)
            this.getNearestWareHouse(latitudeLongitudeObject);
          }else if(latitudeLongitudeObject['storetype_id'] == undefined){
            console.log('No Store Type Selected')
            console.log(latitudeLongitudeObject,'latitudeLongitudeObject')
            this.getUserMapPopUp(latitudeLongitudeObject);
          }else if(latitudeLongitudeObject['storetype_id'] && latitudeLongitudeObject['selected_warehouse_id'] == undefined){
            console.log('No warehouse Selected')
            this.getUserMapPopUp(latitudeLongitudeObject);
          }
        });
      }
    });
  }

  /**
   * Method for getting warehose
   * @access public
  */
  getNearestWareHouse(latitudeLongitudeObject: Object = {}) {
    if (Object.keys(latitudeLongitudeObject).length == 0 || latitudeLongitudeObject['latitude'] == '' || latitudeLongitudeObject['longitude'] == '') {
      this.openUpNoWarehouseFound();
      return false;

    }
    latitudeLongitudeObject['website_id'] = 1;
    this.userGlobalLocation['latitude'] = latitudeLongitudeObject['latitude'];
    this.userGlobalLocation['longitude'] = latitudeLongitudeObject['longitude'];
    this.userGlobalLocation['storetype_id'] = latitudeLongitudeObject['storetype_id'];
    this._warehouse.getWareHouseList(latitudeLongitudeObject).subscribe(response => {
      if (response && response['status'] == 200) {
        let dialogRef = this.dialog.open(WarehouselistComponent, {
          disableClose: true,
          data: response['data']
        });
        dialogRef.afterClosed().subscribe(response => {
          if(response){
            this.userGlobalLocation['selected_warehouse_id'] = response['warehouseId'];
            this.userGlobalLocation['selected_warehouse_name'] = response['warehouseName'];
            this.globalService.updateCookieByKeyAndData(this.userGlobalLocation, 'current_user_location');
            this._warehouse.onWareHouseChangeData(this.userGlobalLocation);
            // this.window.location.reload();
          }else if(latitudeLongitudeObject['selected_warehouse_id'] == undefined){
            this.getUserMapPopUp(latitudeLongitudeObject);
          }
        });
      } else {
        this.openUpNoWarehouseFound();
      }
    });
  }
  /**
   * Popup no warehouse found
   * @access public
  */
  openUpNoWarehouseFound() {
    let openWareHoueseDialogRef = this.dialog.open(NowarehousefoundComponent, {
      data: 'TEST'
    });
    openWareHoueseDialogRef.afterClosed().subscribe(response => {
      console.log(this.userGlobalLocation,'userGlobalLocation')
      this.getStoreCategoryList(this.userGlobalLocation);
    });
  }
  /**
   * Method on chnaging warehouse data
   * @access public
  */
  onChangeWareHouse(warehouseData = {}) {
    // this.getUserMapPopUp(warehouseData);
    this.getNearestWareHouse(warehouseData)
  }
  /**
   * Method on chnaging store type
   * @access public
  */
  onChangeStoreType(wareouseData = {}) {
    this.getStoreCategoryList(wareouseData);
  }
   /**
   * Method on chnaging location
   * @access public
  */
  onChangeLocation(warehouseData = {}){
    this.getUserMapPopUp(warehouseData);
  }

  onselectDropdownOption(warehouseData = {}) {
    let openSelectOptionDialogRef = this.dialog.open(SelectOptionComponent, {
      data: 'TEST'
    });
    openSelectOptionDialogRef.afterClosed().subscribe(response => {
      if(response){
        if(response.selectedOptionId == 1){
          this.getUserMapPopUp(warehouseData);
        }else if(response.selectedOptionId == 2){
          this.getStoreCategoryList(warehouseData);
        }else {
          this.getNearestWareHouse(warehouseData)
        }
      }else{
        this.getUserMapPopUp(warehouseData);
      }
    });
  }
}