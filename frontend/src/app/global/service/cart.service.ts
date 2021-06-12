import { CartoptionpopupComponent } from './../dialog/cartoptionpopup/cartoptionpopup.component';
import { Injectable,Inject} from '@angular/core';
import { throwError as observableThrowError,  Observable,BehaviorSubject} from 'rxjs';
import { catchError, map} from 'rxjs/operators';
import { Http, Response, Headers, RequestOptions} from '@angular/http';
/*import { BehaviorSubject, Observable } from 'rxjs';*/
import {MatDialog, MatSnackBar} from '@angular/material';
import {GlobalService} from './app.global.service';
import {GlobalVariable} from './global';
import { CookieService} from 'ngx-cookie';
import { WarehouseService } from './warehouse.service';
import { WINDOW,LOCAL_STORAGE} from '@ng-toolkit/universal';
import {DialogsService} from '../dialog/confirm-dialog.service'

@Injectable({
  providedIn: 'root'
})
export class CartService {
  readonly apiBaseUrl = GlobalVariable.BASE_API_URL;
  private _websiteId = 1;
  public cartDetails = {};
  public warehouse_id:number;
  public requestedIp = '';
  public fetchedAndRestored = new BehaviorSubject<boolean>(false);
  public isCartFetched = this.fetchedAndRestored.asObservable();
  public cardUpdated = new BehaviorSubject<boolean>(false);
  public isCardUpdated = this.cardUpdated.asObservable();
  public wishlistCount :any= 0;
  selected_preparion_unit : any;
  prepearation_lable:any;
  confirm:any;
  confirmCartData:any;

  //public requestedIpData = this._globalServ


  constructor(
	private _http:Http,
	private _globalService:GlobalService,
	private _cookieService:CookieService,
	private _warehouseService:WarehouseService,
	private dialogsService: DialogsService,
	public dialog: MatDialog,
	@Inject(LOCAL_STORAGE) private localStorage: any,
	) {
	//this.getCartDetails();
	//alert("hiii");

	}
	addData(confirm){
		this.confirm=confirm;
	}
	confirmAddToCart(productId,quantity){
		this._globalService.showLoaderSpinner(true);
		let addedQuanity = parseInt(quantity);
		//let cartItem = this._cookieService.getObject('cart_details') ? this._cookieService.getObject('cart_details') : {};
		let cartItem = this.localStorage.getItem('cart_details') ? JSON.parse(this.localStorage.getItem('cart_details')) : {};
		let cartData = {
			 'device_id' : this._globalService.getRequestedIpFromCookie(),
			 'product_id' : productId,
			 'quantity' : addedQuanity,
			 'warehouse_id' : this.warehouse_id,
			 'year_check' : this.localStorage.getItem("year_check")
		 }
		 console.log(cartData)
		 this._warehouseService.warehouseData$.subscribe(res=>{
			this.warehouse_id=res['selected_warehouse_id']
		  })
		let headersData = {'WAREHOUSE' : this.warehouse_id};
		if(this.localStorage.getItem('currentUser')) {
			  let userData = JSON.parse(this.localStorage.getItem('currentUser'));
			  headersData['Authorization'] = 'Token '+userData['token'];
		 }
		 console.log(cartData)
		  let headers = new Headers(headersData);
		  let requestOptions = new RequestOptions({ headers: headers });
		  this._http.post(this.apiBaseUrl+'add-to-cart/',cartData,requestOptions).pipe(
			  map(res =>  res.json()),
			  catchError(this.handleError)).subscribe(response => {
				  if(response && response['status'] == 1) {
					  console.log(response)
					  let cartDetails = response['cart_data']['cartdetails'];
					  let addedCartDetails = cartDetails.filter(singleCartData => {
						  return singleCartData['id'] == productId;
					  });
					  // console.log("*********************** Cart Response  *****************");
					  // console.log(response);
					  if(cartDetails.length == 0) {
						  cartData['quantity'] = 0;
	  
					  }
					  cartData['price'] = (cartDetails && cartDetails.length > 0) ?  addedCartDetails[0]['new_default_price'] : '';
					  cartData['product_image'] = (cartDetails && cartDetails.length > 0) ? addedCartDetails[0]['product_images'] : '';
					  cartData['product_name'] = (cartDetails && cartDetails.length > 0) ? addedCartDetails[0]['name'] : '';
					  cartData['product_slug'] = (cartDetails && cartDetails.length > 0) ? addedCartDetails[0]['slug'] : '';
					  cartData['default_price'] = (cartDetails && cartDetails.length > 0 && addedCartDetails[0]['default_price']) ? addedCartDetails[0]['default_price'].toFixed(2) : 0;
					  cartData['new_default_price'] = (cartDetails && cartDetails.length > 0 && addedCartDetails[0]['new_default_price']) ? addedCartDetails[0]['new_default_price'].toFixed(2) : 0;
					  cartData['new_default_price_unit'] = (cartDetails && cartDetails.length > 0 && addedCartDetails[0]['new_default_price_unit']) ? addedCartDetails[0]['new_default_price_unit'].toFixed(2) : 0;
					  cartData['total_amount'] = (response['cart_data'] && response['cart_data']['orderamountdetails'].length > 0) ? response['cart_data']['orderamountdetails'][0]['sub_total'] : 0;
					  cartData['minimum_order_amount'] = (response['cart_data'] && response['cart_data']['orderamountdetails'].length > 0) ? response['cart_data']['orderamountdetails'][0]['minimum_order_amount'] : 0;
					  cartData['minimum_order_amount_check'] = (response['cart_data'] && response['cart_data']['orderamountdetails'].length > 0) ? response['cart_data']['orderamountdetails'][0]['minimum_order_amount_check'] : 0;
					  console.log(cartData)
					  this.storeCartDataInCookie(cartData);
	  
					  let logParms:any = {}
					  logParms.content_ids = productId;
					  logParms.content_type = "product";
					  logParms.value = addedQuanity;				
					  this._globalService.facebookPixelEventLog('track','AddToCart',logParms);
	  
					  let googleLogPamrs:any = [];
					  let parms:any = {}
					  parms.id = productId;
					//   parms.name = addedCartDetails[0]['name'];
					  googleLogPamrs.push(parms);
					  this._globalService.googleEventLog("event","add_to_cart",googleLogPamrs);
	  
				  } else if(response && response['status'] == 0) {
					  if(response['is_age_verification'] == "False") {
						  this.dialogsService.confirm('Age Verification', response['msg']).subscribe(res => {
						  if (res) {
							  this.localStorage.setItem('year_check',"Y");
						  }
					  });
					  } else {
						  this._globalService.showToast(response['msg']);	
					  }
				  }
				  this._globalService.showLoaderSpinner(false);
			  },
			  error => {
				  this._globalService.showLoaderSpinner(false);
			  }
			  );
	}
  /**
   * Method for adding an item into cart
   * @access public
  */
  addOrRemoveItem(productId,quantity,custom_fields) {
	  console.log(custom_fields)
	  console.log(productId,quantity)
	  let addedQuanity = parseInt(quantity);
		  if(custom_fields && custom_fields.length>0){
				const dialogRef = this.dialog.open(CartoptionpopupComponent, {
					disableClose: true,
					data: custom_fields
				});
				dialogRef.afterClosed().subscribe(result => {
					if(this.confirm==='confirm'){
					// NOW ADD TO CART TO FUNCTION WILL GOES HERE.
					var cartData = {
						'device_id' : this._globalService.getRequestedIpFromCookie(),
						'product_id' : productId,
						'quantity' : addedQuanity,
						'warehouse_id' : this.warehouse_id,
						'year_check' : this.localStorage.getItem("year_check"),
						'custom_field_name': result.prepearation_lable,
						'custom_field_value' : result.selected_preparion_unit,
					}
					this._warehouseService.warehouseData$.subscribe(res=>{
						this.warehouse_id=res['selected_warehouse_id']
					  })
					let headersData = {'WAREHOUSE' : this.warehouse_id};
					if(this.localStorage.getItem('currentUser')) {
						  let userData = JSON.parse(this.localStorage.getItem('currentUser'));
						  headersData['Authorization'] = 'Token '+userData['token'];
					 }
					let headers = new Headers(headersData);
					let requestOptions = new RequestOptions({ headers: headers });
					this._http.post(this.apiBaseUrl+'add-to-cart/',cartData,requestOptions).pipe(
						map(res =>  res.json()),
						catchError(this.handleError)).subscribe(response => {
							if(response && response['status'] == 1) {
								console.log(response)
								let cartDetails = response['cart_data']['cartdetails'];
								let addedCartDetails = cartDetails.filter(singleCartData => {
									return singleCartData['id'] == productId;
								});
								// console.log("*********************** Cart Response  *****************");
								// console.log(response);
								if(cartDetails.length == 0) {
									cartData['quantity'] = 0;
				
								}
								cartData['price'] = (cartDetails && cartDetails.length > 0) ?  addedCartDetails[0]['new_default_price'] : '';
								cartData['product_image'] = (cartDetails && cartDetails.length > 0) ? addedCartDetails[0]['product_images'] : '';
								cartData['product_name'] = (cartDetails && cartDetails.length > 0) ? addedCartDetails[0]['name'] : '';
								cartData['product_slug'] = (cartDetails && cartDetails.length > 0) ? addedCartDetails[0]['slug'] : '';
								cartData['default_price'] = (cartDetails && cartDetails.length > 0 && addedCartDetails[0]['default_price']) ? addedCartDetails[0]['default_price'].toFixed(2) : 0;
								cartData['new_default_price'] = (cartDetails && cartDetails.length > 0 && addedCartDetails[0]['new_default_price']) ? addedCartDetails[0]['new_default_price'].toFixed(2) : 0;
								cartData['new_default_price_unit'] = (cartDetails && cartDetails.length > 0 && addedCartDetails[0]['new_default_price_unit']) ? addedCartDetails[0]['new_default_price_unit'].toFixed(2) : 0;
								cartData['total_amount'] = (response['cart_data'] && response['cart_data']['orderamountdetails'].length > 0) ? response['cart_data']['orderamountdetails'][0]['sub_total'] : 0;
								cartData['minimum_order_amount'] = (response['cart_data'] && response['cart_data']['orderamountdetails'].length > 0) ? response['cart_data']['orderamountdetails'][0]['minimum_order_amount'] : 0;
								cartData['minimum_order_amount_check'] = (response['cart_data'] && response['cart_data']['orderamountdetails'].length > 0) ? response['cart_data']['orderamountdetails'][0]['minimum_order_amount_check'] : 0;
								console.log(cartData)
								this.storeCartDataInCookie(cartData);
				
								let logParms:any = {}
								logParms.content_ids = productId;
								logParms.content_type = "product";
								logParms.value = addedQuanity;				
								this._globalService.facebookPixelEventLog('track','AddToCart',logParms);
				
								let googleLogPamrs:any = [];
								let parms:any = {}
								parms.id = productId;
								parms.name = addedCartDetails[0]['name'];
								googleLogPamrs.push(parms);
								this._globalService.googleEventLog("event","add_to_cart",googleLogPamrs);
				
							} else if(response && response['status'] == 0) {
								if(response['is_age_verification'] == "False") {
									this.dialogsService.confirm('Age Verification', response['msg']).subscribe(res => {
									if (res) {
										this.localStorage.setItem('year_check',"Y");
									}
								});
								} else {
									this._globalService.showToast(response['msg']);	
								}
							}
							this._globalService.showLoaderSpinner(false);
						},
						error => {
							this._globalService.showLoaderSpinner(false);
						}
						);
					console.log(cartData)
					this.confirmCartData=cartData;
					
					}
				});
			  }else{
				this.confirmAddToCart(productId,quantity)
			  }

	}
  /**
   * Method for removiing item from cart
   * @access public
  */

  /**
   * Method for getting  all cart details
   * @access public
  */
  	getCartDetails() {
      //alert(this.requestedIp);
		let warehouseId = this._globalService.getWareHouseId();
		let requestedIp = this._globalService.getRequestedIpFromCookie();
		let headersData = {
			'Content-Type' : 'application/json',
			'DEVICEID' : requestedIp,
			'WAREHOUSE' : warehouseId,
		}
    if(this.localStorage.getItem('currentUser')) {
        let userData = JSON.parse(this.localStorage.getItem('currentUser'));
        headersData['Authorization'] = 'Token '+userData['token'];
      }
		const headers = new Headers(headersData);
		let requestOptions = new RequestOptions({ headers: headers });
		return this._http.get(this.apiBaseUrl+'view-cart/',requestOptions).pipe(
			   map(res =>  res.json()),
			   catchError(this.handleError));
	}
	/**
	 * Method for store data in cookie
	 * @access public
	*/
	storeCartDataInCookie(productData) {
	  	console.log("**************** Product data *******************");
	  	console.log(productData);
		let localcartData = this.localStorage.getItem('cart_details') ? JSON.parse(this.localStorage.getItem('cart_details')) : {};
		if(productData['quantity'] == 0) {
			delete localcartData['cart_list'][productData['product_id']];
			localcartData['total_amount'] =  productData['total_amount'];
			localcartData['minimum_order_amount'] = productData['minimum_order_amount'];
            localcartData['minimum_order_amount_check'] = productData['minimum_order_amount_check'];

		} else {
			let newCartData  = {
				'prodcut_id' : productData['product_id'],
				'quantity' : productData['quantity'],
				'price' : productData['price'].toFixed(2),
				'default_price' : productData['default_price'],
				'new_default_price' : productData['new_default_price'],
				'new_default_price_unit' : productData['new_default_price_unit'],
				'product_image' : productData['product_image'],
				'product_name' : productData['product_name'],
				'product_slug':productData['product_slug'],
			};
			localcartData['total_amount'] =  productData['total_amount'];
			localcartData['minimum_order_amount'] = productData['minimum_order_amount'];
            localcartData['minimum_order_amount_check'] = productData['minimum_order_amount_check'];

			if(localcartData['cart_list'] == undefined) {
				localcartData['cart_list'] = {};
			}
			if(localcartData['cart_list'][productData['product_id']] == undefined) {
				localcartData['cart_list'][productData['product_id']] = {};
			}
			localcartData['cart_list'][productData['product_id']] = newCartData;
		}
		this.localStorage.setItem('cart_details',JSON.stringify(localcartData));
		//this._cookieService.putObject('cart_details',localcartData);
		this.cartDetails = localcartData;
		console.log("********************* Cart details ******************");
		console.log(this.cartDetails);
	}
	/**
	 * Method to remove cart item from local storage
	*/
	removeCartItem(productId) {

		let headersData = {};
    if(this.localStorage.getItem('currentUser')) {
        let userData = JSON.parse(this.localStorage.getItem('currentUser'));
        headersData['Authorization'] = 'Token '+userData['token'];
      }
    const headers = new Headers(headersData);
    let requestOptions = new RequestOptions({ headers: headers });
		let removeCartData = {
			'device_id' : this._globalService.getRequestedIpFromCookie(),
			'product_id' : productId,
			'website_id' : this._websiteId,
			'warehouse_id' : this.warehouse_id
		}
        this._globalService.showLoaderSpinner(true);
		this._http.post(this.apiBaseUrl+'remove-cart/',removeCartData,requestOptions).pipe(
		  map(res =>  res.json()),
		  catchError(this.handleError)).subscribe(response => {
			if(response && response['status'] == 200) {
				let removeCartData = {
					'product_id' : productId,
					'quantity' : 0,
					'total_amount' : response['data'] && response['data']['orderamountdetails'].length > 0 ? response['data']['orderamountdetails'][0]['grand_total'] : 0,
					'minimum_order_amount' : response['data'] && response['data']['orderamountdetails'].length > 0 ? response['data']['orderamountdetails'][0]['minimum_order_amount'] : 0,
					'minimum_order_amount_check' : response['data'] && response['data']['orderamountdetails'].length > 0 ? response['data']['orderamountdetails'][0]['minimum_order_amount_check'] : 0,

				}
				this.storeCartDataInCookie(removeCartData);
			}
			this._globalService.showLoaderSpinner(false);
		},
		error => {
			this._globalService.showLoaderSpinner(false);

		}
		);
	}
	/**
	 * Method for empty cart details
	 * @access public
	*/
	emptyCart() {
	  let emptyCartData = {
		'website_id' : this._websiteId,
		'device_id'  : this._globalService.getRequestedIpFromCookie(),
	  }
    let headersData = {};
    if(this.localStorage.getItem('currentUser')) {
        let userData = JSON.parse(this.localStorage.getItem('currentUser'));
        headersData['Authorization'] = 'Token '+userData['token'];
      }
    const headers = new Headers(headersData);
    let requestOptions = new RequestOptions({ headers: headers });
    this._globalService.showLoaderSpinner(true);
	  this._http.post(this.apiBaseUrl+'empty-cart/',emptyCartData,requestOptions).pipe(
		  map(res =>  res.json()),
		  catchError(this.handleError)).subscribe(response => {
			if(response && response['status'] == 200){
			  this.cartDetails['cart_list'] = {};
			  this.cartDetails['total_amount'] = 0;
			   this.localStorage.setItem('cart_details',JSON.stringify(this.cartDetails));
			   //localStorage.removeItem('cart_details');
			 }
			 this._globalService.showLoaderSpinner(false); 
		  },
		  error => {
		  	this._globalService.showLoaderSpinner(false);

		  }
		  );
	}

	private handleError(error: Response) { 
		return Observable.throw(error || "Server err"); 
	}
	/**
	  * Method for getting total cart count
	*/
	getTotalCartCount() {
	   let cartCount = 1;
	   if(this.localStorage.getItem('cart_details')) {
		 let cartDetails = this.localStorage.getItem('cart_details');
		 let cartList = cartDetails['cart_list'] ? JSON.parse(cartDetails['cart_list']) : {};
		 if(Object.keys(cartList).length > 0 ) {
		   cartList.forEach(cartData => {
			 cartCount= cartCount+parseInt(cartData['quantity']);
		   })
		 }
	   }
	   return cartCount;
	}
  /**
    * Method for syncing cart data
    * @access public
   */
   syncCartData() {
     let headersData = {
      'Content-Type' : 'application/json',
      'DEVICEID' : this._globalService.getRequestedIpFromCookie(),
    }
    if(this.localStorage.getItem('currentUser')) {
        let userData = JSON.parse(this.localStorage.getItem('currentUser'));
        headersData['Authorization'] = 'Token '+userData['token'];
     }
    const headers = new Headers(headersData);
    let requestOptions = new RequestOptions({ headers: headers });
    return this._http.get(this.apiBaseUrl+'sync-cart/',requestOptions).pipe(
              map(res => res.json()),
              catchError(this. handleError)
            )
   }
   syncCartDataAndRestoreItem() {
     this.syncCartData().subscribe(response => {
       if(response && response['status'] == 200) {
         this.getCartDetails().subscribe(response => {
         	console.log("**************** Cart response **************");
         	console.log(response);
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
				'product_slug': cartData['product_slug'],
				
              }
            });
            cartData['cart_list'] = Object.keys(cartListForStorage).length > 0 ? cartListForStorage : {};
            cartData['minimum_order_amount'] = response['minimum_order_amount'];
            cartData['minimum_order_amount_check'] = response['minimum_order_amount_check'];
            cartData['total_amount'] = response['total_amount'];
            let stringifyData = JSON.stringify(cartData);
            if (this.localStorage) {
              this.localStorage.setItem('cart_details', stringifyData);
            }
            //this._cookieService.putObject('cart_details',cartData);
            this.cartDetails = cartData;
            
          }


         });

       }

     });
   }
   getCartDataAndRestoreItem() {
     this._globalService.showLoaderSpinner(true);
      this.getCartDetails().subscribe(response => {
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
				'product_slug': cartData['product_slug'],
				'custom_field_name':cartData['custom_field_name'],
				'custom_field_value':cartData['custom_field_value']
              }
            });
            cartData['cart_list'] = Object.keys(cartListForStorage).length > 0 ? cartListForStorage : {};
            cartData['minimum_order_amount'] = response['minimum_order_amount'];
            cartData['minimum_order_amount_check'] = response['minimum_order_amount_check'];
            cartData['total_amount'] = response['total_amount'];
            cartData['total_amount'] = response['total_amount'];
            let stringifyData = JSON.stringify(cartData);
            if (this.localStorage) {
              this.localStorage.setItem('cart_details', stringifyData);
            }
            //this._cookieService.putObject('cart_details',cartData);
            this.cartDetails = cartData;
            
            
          }
          this._globalService.showLoaderSpinner(false);
          this.fetchedAndRestored.next(true);


         });

   }
   /**
    * Method for initiate cart data
    * @access public
   */
   initiateCartData() {
   	this.cartDetails = {};
   	if(this.localStorage) {
   		this.localStorage.removeItem('cart_details');
   	}

   }

   saveListCount(){
	let headersData = {
		'Content-Type' : 'application/json',
	  }
	  if(this.localStorage.getItem('currentUser')) {
		let userData = JSON.parse(this.localStorage.getItem('currentUser'));
		headersData['Authorization'] = 'Token '+userData['token'];
		}
	  const headers = new Headers(headersData);
	  let requestOptions = new RequestOptions({ headers: headers });
	  return this._http.get(this.apiBaseUrl+'get-wishlist-count/',requestOptions).pipe(
			map(res => res.json()),
			catchError(this. handleError)
		)
	}

  }