import { Component, Input, OnInit, ElementRef, Inject, ViewChild, Output, EventEmitter, PLATFORM_ID } from '@angular/core';
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material';
import { Router, ActivatedRoute, NavigationEnd } from '@angular/router';
import { TranslateService } from '@ngx-translate/core'; //language change module
import { CookieService } from 'ngx-cookie';
import { Global, GlobalVariable } from '../../global/service/global';
import { GlobalService } from '../../global/service/app.global.service';
import { MenuService } from '../../global/service/menu.service';
import { ShoppingCartService } from '../../global/service/app.cart.service';
import { DialogsService } from '../../global/dialog/confirm-dialog.service';

// import { LoginComponent } from '../../modules/login/login.component';
import { UtillService } from '../../global/service/utill.service';
import { WarehouseService } from '../../global/service/warehouse.service';
import { CartService } from '../../global/service/cart.service';
import { WINDOW } from '@ng-toolkit/universal';
import { LoginComponent } from '../../login/login.component';
import { SignUpComponent } from '../../modules/sign-up/sign-up.component';
import {ForgetPasswordComponent  } from '../../forget-password/forget-password.component';
import { AuthenticationService } from "../../global/service/authentication.service";
import {SearchService} from "../../global/service/search.service";
import { AuthService } from "angularx-social-login";
import { isPlatformBrowser } from '@angular/common';

@Component({
	selector: 'header-part',
	templateUrl: './header.component.html',
	styleUrls: ['./header.component.css'],
	providers: [Global],
	host: {
		'(document:click)': 'onClick($event)',
	},
})
export class HeaderComponent implements OnInit {
	@Input() isCMS: boolean = false;
	@Input() pageType: number = 1;
	@Output() chnageWareHouse = new EventEmitter();
	@Output() chnageStoreType = new EventEmitter();
	@Output() chnageLocation = new EventEmitter();
	@Output() selectDropdownOption = new EventEmitter();

	@ViewChild('navSec') navSec: ElementRef;
	@ViewChild('topSearchBox') topSearchBox: ElementRef;
	@ViewChild('topSearchMobileBox') topSearchMobileBox: ElementRef;
	@ViewChild('wishList') wishList: ElementRef;
	@ViewChild('mobBag') mobBag: ElementRef;
	@ViewChild('toggleProfileMenu') toggleProfileMenu: ElementRef;
	public isMobileSearch = false;
	public facebookStore: boolean = false;
	public clientData: any = {};
	public menu_list: any = [];
	public searchIds:any = [];
	public encoded_id_data = '';
	public is_dist: boolean = false;
	public itemCount: number = 0;
	public ipaddress: any;
	public errorMsg: string;

	public cart: any = {};
	public isLoggedIn: boolean = false;
	public is_facebook: boolean = false;
	public showMobMenu: boolean = false;
	public showMobMenuStatic: boolean = false;
	public sub_q: any;
	public globalData: any = {};
	public logo: string = '';
	public page_uri: string;
	public global_search: any = [];
	//selected="7";
	show_result = '';
	public base_url: string = '';
	public followers_count: number = 0;
	public follow_unfollow: string = 'Follow';
	public distributor_type: string = 'retail';
	// CMS To logo and facebbok link changes..
	public img_base: string = GlobalVariable.S3_URL + 'cms/';
	public customer_data: any = {};
	public showBagPopup: boolean = false;
	public showBagPopupMob: boolean = false;
	////shabnam
	public header_list = [];
	public header_menu_group_list = [];

	public addedCartList = {};
	public objectKeys = Object.keys;
	public userData: any = {};
	public showUserMenu: boolean = false;
	public showMobileMenu:boolean = false;
	public submenuItemList = [];
	public showSubmenuList:boolean = false;
	public showUserMenuMob: boolean = false;
	public subMenu: boolean = false;
	public subMenuProfile: boolean = false;
	public headerMenu_child:any=[];
	public headerMenu_child_name:any;
	public showSearchBox:any;
	public searchKeyword:any;
	//public showFrontEndMenuItem = ['Bakery','Healthy','Household','Baby','Personal Care','Fruits & Vegetables','Dairy & Eggs'];
	public showFrontEndMenuItem = ['Water','Food Cupboard','Baby Care','Personal Care','Fruits & Vegetables','Dairy & Eggs'];
	public selectedWareHouseDatails = {};
	public defaultWareHouse:any = GlobalVariable.DEFAULT_WAREHOUSE_DATA;


	constructor(@Inject(WINDOW) private window: Window,
		private elRef: ElementRef,
		private _global: Global,
		private _router: Router,
		public dialog: MatDialog,
		public _shoppingCartService: ShoppingCartService,
		private _cookieService: CookieService,
		private _globalService: GlobalService,
		private activatedRoute: ActivatedRoute,
		private translate: TranslateService,
		private dialogsService: DialogsService,
		private _menuService: MenuService,
		private _wareHouseService: WarehouseService,
		public us: UtillService,
		public cartService: CartService,
		public authenticationService: AuthenticationService,
		private authService: AuthService,
		private _searchService : SearchService,
		@Inject(PLATFORM_ID) private platformId: Object

	) {
		
		this.ipaddress = _globalService.getCookie('ipaddress');

		let facebook_store = +this._cookieService.get('facebookStore');
		if (facebook_store && facebook_store == 1) {
			this.facebookStore = true;
		} else {
			this.facebookStore = false;
		}

		this.isLoggedIn = this._globalService.isLoggedInFrontend();
		
		
		this.clientData = this._cookieService.getObject('clientData');
		if (this.clientData && this.clientData['user_type'] == 'merchant') {
			this.is_dist = true;
		} else {
			this.is_dist = false;
		}
		this._globalService.isLoginChange$.subscribe(
			(value) => {
				this.isLoggedIn = value;
				this.clientData = this._cookieService.getObject('clientData');

				if (this.clientData && this.clientData['user_type'] == 'merchant') {
					this.is_dist = true;
				} else {
					this.is_dist = false;
				}
				if (value) {
					this.saveTempCart();
				}
			}
		);

		this.is_facebook = false;
		this.sub_q = this.activatedRoute.queryParams.subscribe(params => {
			if (params['isfacebook'] !== undefined) {
				this.is_facebook = true;
			}
		});

		this._globalService.isFollowSource.subscribe(
			(value) => {
				this.follow_unfollow = value;
			}
		);
		// catch route uri changes 
		this._router.events.subscribe(event => {
			if (event instanceof NavigationEnd) {
				this.page_uri = event.url;
			}
		});

		// catch global data changes
		this.globalData = this._cookieService.getObject('globalData');
		this._globalService.globalDataChange$.subscribe(value => {

			this.logo = GlobalVariable.S3_URL + 'companylogo/250x185/' + this.globalData['website_logo'];
			if (this.globalData['lang_code']) {
				//this.setLang(this.globalData['lang_code'].match(/en|th/) ? this.globalData['lang_code'] : 'en');
			} else {
				//let browserLang = this.translate.getBrowserLang();
				//this.setLang(browserLang.match(/en|th/) ? browserLang : 'en');
			}
		},
			err => {
				console.log(err);
			});

		this.base_url = GlobalVariable.COMPANY_URL;

		// Onchnaging warehouse data
		this._wareHouseService.warehouseData$.subscribe(response => {
			this.selectedWareHouseDatails = response;

		});
		let userData = this.authenticationService.currentUserVal();
		if (userData) {
			// console.log(userData);
			this.authenticationService.userFirstName = userData.first_name;
			this.authenticationService.userLastName = userData.last_name;
		}
		this._menuService.signinSignuppopup$.subscribe(response => {
			if(response) {
				let action = typeof response == 'object' ? response['action'] : response;
                let actionData = {
                	'action' : action
                }
                typeof response == 'object' ? actionData['redirectUrl'] = response['redirectUrl'] : '';
				if(action == 'sign-in') {
					this.openLoginDialog(actionData);
				} else if(action == 'sign-up') {
					this.openSignupDialog(actionData);
				}
				/*if(typeof response == 'object') {


				} else {
					if(response == 'sign-in') {
						this.openLoginDialog();
					} else if(response == 'sign-up') {
						this.openSignupDialog();
					}
				}*/

			}
		})
		if(this.authenticationService.userFirstName){
			this.getSaveListCount();
		}else{
			this.cartService.wishlistCount=0;
		}

		this.checkSocialAuthenticate();

	}
	
	/**
	 * Method for check if social authenticate exists
	 * @access public
	*/
	checkSocialAuthenticate() {
		 this.authService.authState.subscribe((user) => {
           if(user) {
               this.authenticationService.isSocialLogin = true;
               let userData = {
                   'user_email' : user['email'] ? user['email'] : '',
                   'first_name' : user['firstName'] ? user['firstName'] : '',
                   'last_name'  : user['lastName'] ? user['lastName'] : '',
                   'image_name'  : user['photoUrl'] ? user['photoUrl'] : '',
                   'google_login_id' : user['provider'] == 'GOOGLE' ? user['id'] : '',
                   'facebook_id' : user['provider'] == 'FACEBOOK' ? user['id'] : '',
                   'phone' : '',
                   'device_id' : this._globalService.getCookie('client_ip') ? this._globalService.getCookie('client_ip') : '',

               }
               this.authenticationService.socialLogin(userData).subscribe(response => {
                   if(response && response['status'] == 200) {
                       localStorage.setItem('userData', JSON.stringify(response['data']));

                       this.dialog.closeAll();

                        /*if(Object.keys(this.actionData).length > 0 && this.actionData['redirectUrl']) {
                            this.router.navigate([this.actionData['redirectUrl']]);
                        } */
                   }

               },
               (err) => {
               	 this._globalService.showToast("Something went wrong,Please try again");
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
        );
	}
	onToggleMobileMenu() {
		this.showMobileMenu = true;
	}
	hideMobileMenu() {
		this.showMobileMenu = false;
	}
	parentMenuClick() {
		
	}
	backToParentMenu() {
		this.submenuItemList = [];
        this.showSubmenuList = false;

	}
    mobileNavigateToUrl(url,hideMobileMenu = false) {
    	
    	this._router.navigate([url]);
    	if(hideMobileMenu) {
    		this.hideMobileMenu();

    	}


    }
    /*onMouseHover(){

    }*/


	openSubmenuOrRoutingToLink(headerMenuData) {
		/*console.log("********************** header menu data ****************");
		console.log(headerMenuData);*/
		if(headerMenuData && headerMenuData['child'].length > 0) {
			this.submenuItemList = headerMenuData;
			this.showSubmenuList = true;

		} else {
			// If there are no submenu item then navigate to the listing page
			console.log("****************** Header menu data **************");
			console.log(headerMenuData);
			this.mobileNavigateToUrl('/listing/'+headerMenuData['slug'],true);



		}

	}
	toggle_menu() {
		this.showUserMenu = !this.showUserMenu;
	}
	toggle_menu_mob() {
		this.showUserMenuMob = !this.showUserMenuMob;
	}
	open_submenu(item:any=[]){
		if(item=="profile"){
			this.subMenuProfile = !this.subMenuProfile;
		}else{
			this.subMenu = !this.subMenu;
			this.headerMenu_child=item['child'];
			this.headerMenu_child_name=item['name'];
		}
	}
	navigateTolist(link:any){
		if(link!=''){
			this._router.navigate(['/listing/',link]);
			this.showUserMenuMob = !this.showUserMenuMob;
			this.subMenu = !this.subMenu;
		}
	}
	navigateTolistMob(link:any){
		if(link!=''){
			this._router.navigate([link]);
			this.showUserMenuMob = !this.showUserMenuMob;
		}
	}
	navigate(data: number) {
		if (data == 1) {
			this._router.navigate(['/profile/profiledetails']);
		}
		if (data == 2) {
			this._router.navigate(['/profile/order-history']);
		}
		if (data == 3) {
			//Open login popup
			if(this.authenticationService.userFirstName) {

				this._router.navigate(['/profile/wishlist']);
			}
			else {
				//   this.openLoginDialog();
				//RAJAT
					if(!localStorage.getItem('currentUser')) {
						this._menuService.signinSignuppopup$.next('sign-in');
						return false;
					}
				}
		}
	}
	toggleBagPopup() {

		this.showBagPopup = !this.showBagPopup;
		
	}
	toggleBagPopupMob() {
		this.showBagPopupMob = !this.showBagPopupMob;
	}
	checkCart(productId, quantity) {
		
	}
	open_serchbox(){

		this.showSearchBox = !this.showSearchBox;
	}
	/*getWarehouseValue(e){
		this.selected=e;
		this._cookieService.putObject('warehouse_id',e);
		window.location.reload()

	}*/

	onSearchChange(value,isMobile = false) {

		this.isMobileSearch = isMobile;
		this.searchKeyword = value;
		this.searchIds = [];
		this.encoded_id_data = '';
		this.global_search = [];
		let warehouse_data = '';
		


		this._wareHouseService.warehouseData$.subscribe(response => {
			warehouse_data = response['selected_warehouse_id'];
		})
		let name = this.activatedRoute.snapshot.paramMap.get('slug');
		if (value != '') {
			document.querySelector('.topserchbox').classList.add('search_active')
			if (value.length > 1) {
				this.show_result = value;
				let filter_set = {};

				filter_set = {
					"query": {
						"bool": {
							"must": [
								{

									"query_string": {

										"query": "\""+value+"\"",
										

									},

								},
								/*{
							    	"match_all": {}
							    },*/
								{
									"match": {
										"visibility_id": { "query": "Catalog Search", "operator": "and" }
									}
								}
							],
							"filter" : [
							  {'nested' : {
							            "path" : "inventory",
							            "query" : {
							                "bool" : {
							                    "must" : [
							                    { "term" : {"inventory.id" : warehouse_data} },
							                    { "range" : {"inventory.stock" : {"gt" : 0}} }
							                    ]
							                }
							            },
							            "score_mode" : "avg"
							      }
							     },
							     {
							       'nested' : {
							         "path" : "channel_currency_product_price",
							         "query" : {
							           "bool" : {
							             "must" : [
							               { 
							                 "range": {
							                  "channel_currency_product_price.new_default_price": {
							                    "gt": 0,
							             
							                 }
							               }
							              },
							              { "term": { "channel_currency_product_price.warehouse_id": warehouse_data } }
							             ]
							           }
							         }
							       }
							     },
							      {
							       'nested' : {
							         "path" : "product_images",
							         "query" : {
							           "bool" : {
							             "must" : [
							            
							              { "term": { "product_images.is_cover": 1 } }
							             ]
							           }
							         }
							       }
							     }
							],
							

						},

					},
					"from" : 0,
                    "size" : 10000
				}


				let remainingValue = [];
				// document.querySelector('.topserchbox').classList.add('active');
				this._global.doSearchServer(filter_set).subscribe(
					data => {
						
						if (data.hits.hits.length > 0) {
							
							remainingValue = data.hits.hits;
							let img: any;
							let variations = [];
							let is_parent_variation: any;


							remainingValue.map(item => {

								if (item._source.product_images) {
									item._source.product_images.forEach(im => {
										if (im.is_cover == 1) {
											img = im.link + im.img;
										}
									})
								}
								if (item._source.variations) {
									item._source.variations.forEach(im => {
										if (im.is_parent == "y") {
											is_parent_variation = im.field_value[0];
										}
									})
								}
								let price;
								if (item._source.channel_currency_product_price.length > 0) {
									item._source.channel_currency_product_price.forEach(pr=> {
										/*// if (pr.is_parent == "y") {
											price = pr[0].price
										// }*/
										if(pr['warehouse_id'] == warehouse_data && pr['new_default_price'] > 0) {
											price = pr['new_default_price'];
										}
									})
								}
								/*if (item._source.channel_currency_product_price.length > 0)
									price = item._source.channel_currency_product_price[0].price;*/
							   if(price) {
							   	    this.searchIds.push(item['_id']);
							   		this.global_search.push({
									_id: item._id,
									brand: item._source.brand,
									category: item._source.category,
									channel_currency_product_price: price,
									default_price: item._source.default_price,
									description: item._source.description,
									hsn_id: item._source.hsn_id,
									id: item._source.id,
									name: item._source.name,
									product_images: img,
									sku: item._source.sku,
									slug: item._source.slug,
									unit: item._source.sku,
									url: item._source.sku,
									variation: is_parent_variation,
									max_order_unit: item._source.max_order_unit,
									IsCart: false,
									quantity: item._source.quantity,

								});

							   } 
							
							})
							// console.log("this.global_search");
							// console.log(this.global_search);
						}
						
					    this.encoded_id_data = this._searchService.getEncodedId(this.searchIds);
					    if(this.elRef.nativeElement.querySelector('.serch_dropbox')) {
					    	this.elRef.nativeElement.querySelector('.serch_dropbox').style.display = "block";

					    }
						



						// this.global_search = data.hits.hits;

					},
					err => console.log(err),
					function () { }
				);

			} else {
				if(this.elRef.nativeElement.querySelector('.serch_dropbox')) {
					this.elRef.nativeElement.querySelector(' .serch_dropbox').style.display = "none";
			    }
			    //this._globalService.showToast('Search Value should be greater than two');

					
				
			}

		} else {
			if(this.elRef.nativeElement.querySelector('.serch_dropbox')) {
				this.elRef.nativeElement.querySelector('.serch_dropbox').style.display = "none";
		    }
			document.querySelector('.topserchbox').classList.remove('search_active');

		}
		//}

	}

	ngOnInit() {
		/*alert("hiii");*/
		/*if(this._cookieService.getObject('warehouse_id')){
			this.selected=this._cookieService.getObject('warehouse_id').toString();
		}*/
		this.selectedWareHouseDatails = this._cookieService.getObject('current_user_location') ? this._cookieService.getObject('current_user_location') : {};
		/*if (this._router.url && this._router.url.indexOf('/base') > -1) {
			this.page_uri = '/base';
		}*/
		this.globalData = this._cookieService.getObject('globalData');
		this.logo = GlobalVariable.S3_URL + 'companylogo/250x185/' + this.globalData['website_logo'];
		//console.log('Yes coming...');
		//console.log(this.globalData);
		if (this.globalData && this.globalData['lang_code']) {
			//this.setLang(this.globalData['lang_code'].match(/en|th/) ? this.globalData['lang_code'] : 'en');
		} else {
			/*let browserLang = this.translate.getBrowserLang();
			this.globalData['lang_code'] = browserLang.match(/en|th/) ? browserLang : 'en';*/
			//this.setLang(this.globalData['lang_code']);
		}
		if (isPlatformBrowser(this.platformId)) {
		this.cart = this._shoppingCartService.retrieve();
		this.itemCount = this.cart.items.map((x) => x.quantity).reduce((p, n) => p + n, 0);
		this._shoppingCartService.cartChange$.subscribe((cart) => {
			this.itemCount = cart.items.map((x) => x.quantity).reduce((p, n) => p + n, 0);
		});
		this._wareHouseService.warehouseData$.subscribe(response => {
			if(response['selected_warehouse_id'] == undefined) { // load defualt warehouse data . if no warehouse selected.
				response['selected_warehouse_id'] = GlobalVariable['DEFAULT_WAREHOUSE_DATA']['selected_warehouse_id']
			}
			this._menuService.getHeaderMenu(response['selected_warehouse_id']).subscribe(response => {
				if (response && response['status'] == 1) {
					this.header_list = response['menu_bar'];
					let clone_header_list = this.header_list.slice(0);
					this.header_menu_group_list = this.groupingArray(clone_header_list,4);
					console.log("******************** Header menu group list ********************");
					console.log(this.header_menu_group_list);
					this.header_list.forEach(item => {
						item.child.map(x => {
							if (x.id) {
								x['encr'] = btoa(JSON.stringify({ 'name': item.slug, 'id': item.id }));
							}
						})
					})
				}
			},
				err => {
					this._globalService.showToast('Something went wrong.Please try again');
				}
			);
		})
		// On warehouse change
	}
   }
	groupingArray(array = [],chunk) {
		
		var i,j,temparray,groupedArray = [];
		if(array.length == 0) {
			return array;
		}
		for (i=0,j=array.length; i<j; i+=chunk) {
		    temparray = array.slice(i,i+chunk);
		    groupedArray.push(temparray);

		    // do whatever
		}
		return groupedArray;
	}

	saveTempCart() {
		this.cart = this._shoppingCartService.retrieve();
		let customer_id = this._globalService.getCustomerId();
		let website_id: number = this._globalService.getFrontedWebsiteId();
		if (this.cart.items.length) {
			let cart_product_ids: any = [];
			this.cart.items.forEach(item => {
				//this._shoppingCartService.addTempCart(item.product_id, item.quantity);
				let cat_prod: any = {};
				cat_prod.website_id = website_id;
				cat_prod.company_id = 1;
				cat_prod.device_id = '';
				cat_prod.customer_id = customer_id;
				cat_prod.product_id = item.product_id;
				cat_prod.quantity = item.quantity;
				// Add and update in caret table will go here...
				cart_product_ids.push(cat_prod);
			});
			//console.log(cart_product_ids);
			let data: any = { products: cart_product_ids, website_id: website_id, customer_id: customer_id };
			this._shoppingCartService.addTempCartAfterLogin(data).subscribe(
				data => {
					if (data.status) {
						for (let result of data.api_status) {
							this._shoppingCartService.addItem(result, result.quantity, true, false, 0, 1);
						}
					}
				},
				err => { },
				function () {
					//completed callback
				}
			);
		} else {
			this.getCartProducts();
		}
	}


	getCartProducts() {
		let saved_products: any = [];
		let website_id = this._globalService.getFrontedWebsiteId();
		if (this.clientData['products']) {
			saved_products = this.clientData['products'];
			//console.log(saved_products)
			let product_ids: any = [];
			saved_products.forEach(item => {
				let prod: any = {};
				let product_exist: any = this.cart.items.filter((cartItem) => cartItem.merchant_product_id === item.products);
				if (this.cart.items.length && product_exist.length == 0) {
					prod.product_id = item.products;
					prod.website_id = website_id;
					product_ids.push(prod);
				} else {
					prod.product_id = item.products;
					prod.website_id = website_id;
					product_ids.push(prod);
				}
			});
			let data: any = { products: product_ids, website_id: website_id };
			//console.log(product_ids)
			this._shoppingCartService.getCartProducts(data).subscribe(
				data => {
					if (data.status) {
						data.api_status.forEach(item => {
							let select_item: any = saved_products.find((p) => p.products === item.id);
							if (item.stock) {
								this._shoppingCartService.addItem(item, select_item.quantity, true, false);
							}
						});
					}
				},
				err => { },
				function () {
					//completed callback
				}
			);
		}
	}

	openMobMenu() {
		this.showMobMenu = !this.showMobMenu;
	}

	openMobMenuStatic() {
		this.showMobMenuStatic = !this.showMobMenuStatic;
	}

	onClick(event: any) {

		let siblings;
		event.stopPropagation();
		/*let allHeaderMenu = document.querySelectorAll('li a.header_menu');
		allHeaderMenu.forEach(headerElementNode => {
			if (headerElementNode.classList.contains('active')) {
				headerElementNode.classList.remove('active');
			}
		})
		if ((this.navSec.nativeElement as HTMLElement).contains(event.target)) {
			let target = event.target || event.srcElement || event.currentTarget;
			if (target.classList.contains('active')) {
				target.classList.remove('active');
			} else {
				target.classList.add('active');
			}
			//let parentNode = target.parentElement;
		}*/
		if (!(this.topSearchBox.nativeElement as HTMLElement).contains(event.target) && !this.isMobileSearch) {

			this.topSearchBox.nativeElement.querySelector('.topserchbox .search').value = "";
			this.global_search = [];
		}
		if (!(this.topSearchMobileBox.nativeElement as HTMLElement).contains(event.target) && this.isMobileSearch) {
			this.topSearchMobileBox.nativeElement.querySelector('.serchbox .search').value = "";
			this.global_search = [];
		}
		if (!(this.wishList.nativeElement as HTMLElement).contains(event.target)) {
			this.showBagPopup = false;
		}
		if (!(this.mobBag.nativeElement as HTMLElement).contains(event.target)) {
			this.showBagPopupMob = false;
		}
		if (!(this.toggleProfileMenu.nativeElement as HTMLElement).contains(event.target)) {
			this.showUserMenu = false;
		}

		// if (this.elRef.nativeElement.querySelector('megamenu_wrap ul li a.active') != null) {
		// 		if (this.elRef.nativeElement.querySelector('.red_nav ul li .megamenu_wrap') != null) {
		// 			this.elRef.nativeElement.querySelector('.red_nav ul li .megamenu_wrap').style.display = "none";
		// 			document.querySelector('.red_nav ul li a').classList.remove('active');
		// 			document.querySelector('.red_nav ul li a').classList.add("no-class");
		// 			let all_value = document.querySelectorAll('.red_nav ul li a');
		// 			for (let i = 0; i < all_value.length; i++) {
		// 				if (all_value[i].classList.contains("active")) {
		// 					all_value[i].classList.remove('active');
		// 					all_value[i].classList.add("no-class");
		// 				}
		// 			}
		//this.child_header_list = [];
		// }
		//this.close_search_div('desk');
		// }
	}
	onMouseHover(event:any) {
		console.log("******************* Mouser hover enter *****************");
		event.stopPropagation();
		let allHeaderMenu = document.querySelectorAll('li a.header_menu');
		allHeaderMenu.forEach(headerElementNode => {
			if (headerElementNode.classList.contains('active')) {
				headerElementNode.classList.remove('active');
			}
		})
		if ((this.navSec.nativeElement as HTMLElement).contains(event.target)) {
			alert("hiii");
			let target = event.target || event.srcElement || event.currentTarget;
			target.classList.add('active');
			/*if (target.classList.contains('active')) {
				target.classList.remove('active');
			} else {
				target.classList.add('active');
			}*/
			//let parentNode = target.parentElement;
		}
	}

	close_search_div(type: string) {
		// if (this.elRef.nativeElement.querySelector('.mob-search .dropdownsearch') != null) {
		// 	if (type == 'mob') {
		// 		this.elRef.nativeElement.querySelector('.mob-search .dropdownsearch').style.display = "none";
		// 		this.elRef.nativeElement.querySelector('.mob-search .search').value = "";
		// 		document.querySelector('.mob-search .search').classList.remove('active');
		// 	} else {

		// 		this.elRef.nativeElement.querySelector('.search-box .dropdownsearch').style.display = "none";
		// 		this.elRef.nativeElement.querySelector('.search-box .search').value = "";
		// 		document.querySelector('.search-box .search').classList.remove('active');
		// 		this.elRef.nativeElement.querySelector('.serch_dropbox').style.display = "none";
		// 		this.elRef.nativeElement.querySelector('.topserchbox .search').value = "";
		// 		// document.querySelector('.serch_dropbox .search').classList.remove('active');
		// 		this.elRef.nativeElement.querySelector('.topserchbox').remove('active');
		// 	}

		// }
		if (this.elRef.nativeElement.querySelectorAll('.topserchbox.search_active').length == 1) {
			this.elRef.nativeElement.querySelector('.topserchbox .search').value = "";
			// this.elRef.nativeElement.querySelector('.topserchbox').remove('active');
			this.global_search = [];
		}

	}
	globalSearch(txt: string, type: string) {
		this.global_search = [];
		if (txt != '') {
			document.querySelector('.search').classList.add('active');
			this._global.doSearch(txt).subscribe(
				data => {
					this.global_search = data.hits.hits;
					if (this.global_search.length > 0) {
						if (type == 'mob') {
							this.elRef.nativeElement.querySelector('.mob-search .dropdownsearch').style.display = "block";
						} else {
							this.elRef.nativeElement.querySelector('.search-box .dropdownsearch').style.display = "block";
						}
					}
				},
				err => console.log(err),
				function () { }
			);
		} else {
			document.querySelector('.search').classList.remove('active');
		}
	}

	logout() {
		this._globalService.showLoaderSpinner(true);
		setTimeout(() => {
			//console.log('After cookie deleted...');
			//const allCookiesafter: {} = this._cookieService.getAll();
			//this._cookieService.removeAll();
			//console.log(allCookiesafter);
			this._shoppingCartService.local_storage_empty();
			this._shoppingCartService.empty();
			this._cookieService.remove('clientData', this._globalService.getCookieOption());
			this._cookieService.remove('guestCustomerData', this._globalService.getCookieOption());
			this._cookieService.remove('facebookStore');
			this._cookieService.remove('is_facebook');
			this._cookieService.remove('disc_type');
			this._cookieService.remove('distributorBusinessType');
			if (this._cookieService.get('referred_unique_code')) {
				this._cookieService.remove('referred_unique_code');
			}
			if (this._cookieService.get('cid_edit')) {
				this._cookieService.remove('cid_edit');
			}
			if (this._cookieService.get('coupon_edit')) {
				this._cookieService.remove('coupon_edit');
			}
			if (this._cookieService.get('coupon_code')) {
				this._cookieService.remove('coupon_code');
			}
			if (this._cookieService.get('pid_edit')) {
				this._cookieService.remove('pid_edit');
			}
			if (this._cookieService.get('temp_order_id')) {
				this._cookieService.remove('temp_order_id');
			}
			if (this._cookieService.get('after_login_redirect')) {
				this._cookieService.remove('after_login_redirect');
			}
			//this.countFollowers();	    	
			if (this._globalService.getFrontedWebsiteId() > 1) {
				this._router.navigate(['/page/home']);
			} else {
				this._router.navigate(['/']);
			}
			this._globalService.isLoginSource.next(false);
			this._globalService.showLoaderSpinner(false);
			location.reload();
		}, 1000);
	}


	setCurrency(currency_id: number) {
		let curr: any = this.globalData.currency_master.find((c) => c.currency_id === currency_id);
		this._shoppingCartService.currecnyExchange(currency_id).subscribe(
			data => {
				if (data.status) {
					this.globalData['currency_code'] = curr.currency_code;
					this.globalData['currency_symbol'] = curr.currency_symbol;
					this.globalData['currency_id'] = curr.currency_id;
					this.globalData['currency_exchange'] = data.rate;
					this._cookieService.putObject('globalData', this.globalData, this._globalService.getCookieOption());
				}
			},
			err => { },
			function () {
				//completed callback
			}
		);
	}

	setLang(lang: any) {
		//alert(lang);
		console.log("******************** Language data ******************",lang);
		this.globalData['lang_code'] = lang;
		this._cookieService.putObject('globalData', this.globalData, this._globalService.getCookieOption());
		this.translate.use(lang);
		this._globalService.langChangeSource.next(lang);
	}

	// Followrs and unfollowers start here....
	updateFollowers(activity_status: any) {
		if (this.isLoggedIn) {
			let user_id = this.clientData['uid'];
			let data: any = { user_id: user_id, activity_status: activity_status, company_website_id: this._globalService.getFrontedWebsiteId() };
			this._global.updateFollowers(data).subscribe(
				data => {
					if (data.status) {
						this.followers_count = data.count;
						if (data.activity_status == 'subscribed') {
							this.follow_unfollow = 'Unfollow';
						} else {
							this.follow_unfollow = 'Follow';
						}
						this.setFollowers(this.follow_unfollow)
					}
				},
				err => { },
				function () {
					//completed callback
				}
			);
		} else {
			this._router.navigate(['/login']);
		}
	}

	countFollowers() {
		let data: any = { user_id: this._globalService.getClientId(), company_website_id: this._globalService.getFrontedWebsiteId() };
		this._global.countFollowers(data).subscribe(
			data => {
				if (data.status) {
					this.followers_count = data.api_status;
					if (data.activity_status == 'subscribed') {
						this.follow_unfollow = 'Unfollow';
					} else {
						this.follow_unfollow = 'Follow';
					}
					this.setFollowers(this.follow_unfollow)
				}
			},
			err => { },
			function () {
				//completed callback
			}
		);
	}

	setFollowers(follow_unfollow: any) {
		this.globalData['follow_unfollow'] = follow_unfollow;
		this._cookieService.putObject('globalData', this.globalData, this._globalService.getCookieOption());
		//this._globalService.isFollowSource.next(follow_unfollow);
	}

	redirectHelpDetailPage(page_slug: any) {
		let currentUrl = this._router.url;
		if (page_slug && page_slug != '') {
			let page_url = '/help/details/' + page_slug
			this._router.navigate([page_url]);
			if (currentUrl.match("/details/")) {
				//console.log(currentUrl);
				location.reload();
			}
		} else {
			return false;
		}
	}

	redirectMobileMenuLink(page_slug: any) {
		let page_url = '/' + page_slug
		this._router.navigate([page_url]);
	}

	go_moodle() {
		let userData: any;
		userData = this._cookieService.getObject('clientData');
		let username = userData.email;
		let password = userData.moodle_password;
		let queryString = btoa('username=' + username + '&password=' + password);
		// this.window.open('https://lc.khaliworld.com/moodle/login/angular_login.php?data=' + queryString, "_blank");
		//52.221.222.57
	}
	/**
	 * Method for search page request
	 * @access public
	*/
	onSearchPageReq(event) {
		if(!this.encoded_id_data) {
			return;
		}
        // this.showSearchBox = false;
         if(this.elRef.nativeElement.querySelector('.serch_dropbox')) {
			 this.elRef.nativeElement.querySelector('.serch_dropbox').style.display = "none";
		}
		if(this.isMobileSearch) {
			this.showSearchBox = false;
		}
        this._router.navigate(['/search'],{
							     relativeTo: this.activatedRoute,
							      queryParams: {
							      	q : this.searchKeyword ? encodeURI(this.searchKeyword) : '',
							        v: this.encoded_id_data
							       
							      },
							      queryParamsHandling: 'merge',
							      // preserve the existing query params in the route
							      skipLocationChange: false
							      // do not trigger navigation
							    });


		
	}

	redirectToPanel() {
		let userData: any;
		userData = this._cookieService.getObject('clientData');
		//console.log(userData);
		// logout from company store when moving to distributor store..admin...
		this._cookieService.remove('clientData', this._globalService.getCookieOption());
		this._cookieService.remove('temp_order_id');
		// logout from company store when moving to distributor store..admin...
		userData['uid'] = userData.uid;
		userData['first_name'] = userData.first_name;
		userData['last_name'] = userData.last_name;
		userData['email'] = userData.email;
		userData['is_otp'] = false;
		userData['isLoggedIn'] = true;
		userData['auth_token'] = userData.auth_token;
		userData['user_type'] = userData.user_type;
		userData['company_id'] = userData.company_id;
		userData['website_id'] = userData.website_id;
		userData['business_name'] = userData.business_name;
		userData['currency'] = userData.currency;
		userData['currency_id'] = userData.currency_id;
		userData['usd_exchange_rate'] = userData.usd_exchange_rate;
		userData['role_id'] = userData.role_id;
		if (userData['user_type'] === 'merchant') {
			userData['distributor_type'] = userData.distributor_type;
			userData['distributor_user_type'] = userData.distributor_user_type;
			userData['default_warehouse_type'] = userData.default_warehouse_type;
			userData['moodle_password'] = userData.learning_center_password;
		}
		this._cookieService.putObject('userData', userData, this._globalService.getCookieOption());
		// this.window.location.href = GlobalVariable.BASE_Backend_URL + 'welcome';
	}


	userUpgradeAgent() {
		//console.log(this.clientData);
		this.dialogsService.confirm('Upgrade Customer to Agent !', 'Do you really want to upgrade from Customer to Agent?').subscribe(res => {
			if (res) {
				var userRegData = {};
				if (this.ipaddress) {
					userRegData['ip_address'] = this.ipaddress;
				} else {
					userRegData['ip_address'] = '';
				}
				userRegData['role_id'] = 320;
				userRegData['website_id'] = this._globalService.getFrontedWebsiteId();
				var usergeo = this._cookieService.getObject('userGeo');
				userRegData['country_id'] = (usergeo['country_id']) ? usergeo['country_id'] : 209;
				userRegData['city'] = (usergeo['city']) ? usergeo['city'] : '';
				userRegData['company_id'] = this._globalService.getFrontedCompanyId();
				userRegData['postcode'] = (usergeo['zip']) ? usergeo['zip'] : '';
				userRegData['state'] = (usergeo['region_name']) ? usergeo['region_name'] : '';
				userRegData['last_name'] = this.clientData['last_name'];
				userRegData['first_name'] = this.clientData['first_name'];
				userRegData['email'] = this.clientData['email'];
				userRegData['phone'] = '';
				userRegData['password'] = '';
				this._globalService.showLoaderSpinner(true);
				let that = this;
				this._global.agentRegister(userRegData).subscribe(
					data => {
						if (data.status) {
							this.clientData['user_type'] = data.user_type;
							this.clientData['role_id'] = 320;
							//console.log('After update this data will go to cookie...');
							//console.log(this.clientData);
							this.dialogsService.alert('Upgrade Customer to Agent', 'You are successfully upgraded to Agent.').subscribe(res => { });
							this._cookieService.putObject('clientData', this.clientData, this._globalService.getCookieOption());
							this._globalService.showLoaderSpinner(false);
							this._globalService.isLoginSource.next(true);
							this._router.navigate(['/category/shop-now/']);
						} else {
							this.errorMsg = data.message;
							this.window.scrollTo(0, 0);
						}
						this._globalService.showLoaderSpinner(false);
					},
					err => {
						this._globalService.showLoaderSpinner(false);
						this.errorMsg = "Something went wrong. Please try again."
					},
					function () {
						that._globalService.showLoaderSpinner(false);
						//completed callback
					}
				);
			}
		});
	}

	// dialogNotifyPaymentRef: MatDialogRef<NotifyPaymentsComponent> | null;
	// notifyPayment() {
	// 	let address_data: any = {}
	// 	let data: any = {};
	// 	if (Object.keys(address_data).length > 0) {
	// 		data = Object.assign({}, address_data);
	// 	} else {
	// 		data.delivery_firstname = this.customer_data.first_name;
	// 		data.delivery_lastname = this.customer_data.last_name;
	// 		data.delivery_phone = this.customer_data.phone;
	// 		data.delivery_email_address = this.customer_data.email;
	// 	}
	// 	this.dialogNotifyPaymentRef = this.dialog.open(NotifyPaymentsComponent, { data: data, width: '600px' });
	// 	this.dialogNotifyPaymentRef.afterClosed().subscribe(result => {
	// 		if (result) {
	// 			this.dialogsService.alert('Notification Payment', 'Payment notification send successfully.').subscribe(res => { });
	// 		}
	// 	});
	// }
	/**
	 * Method on chnaging warehouse
	 * @access public
	*/
	onChangeWareHouse() {

		this.chnageWareHouse.emit(this.selectedWareHouseDatails);
	}
 
	/**
	 * Method on chnaging Store Type
	 * @access public
	*/
	onChangeStoreType() {

		this.chnageStoreType.emit(this.selectedWareHouseDatails);
	}
	/**
	 * Method on chnaging location
	 * @access public
	*/
	onChangeLocation(){
		this.chnageLocation.emit(this.selectedWareHouseDatails);
	}
	/**
	 * Method on show popup to change location, store type, store
	 * @access public
	*/
	onChangeSelectOption(){
		this.selectDropdownOption.emit(this.selectedWareHouseDatails);
	}

	/**
	 * Method for navigating to url
	 * @access public
	*/
	navigateToUrl(url) {
		this.showBagPopup = false;
		this.showBagPopupMob = false;
		this._router.navigate([url]);

	}

	//login dialog
	loginComponent: MatDialogRef<LoginComponent> | null;
	openLoginDialog(actionData = {}) {
		this.loginComponent = this.dialog.open(LoginComponent, {
			disableClose: true,
			data : actionData,
		});
		this.loginComponent.afterClosed().subscribe(response => {
			//console.log(actionData);
			// alert(response);
			if (response == 'sign-up') {
				//alert("hiii");
				this.openSignupDialog(actionData);
			}
			if (response == 'forget-password') {
				this.openForgetPasswordDialog();
			}
		});
	}
	openSignupDialog(actionData = {}) {
		/*this.dialogRef.close('sign-up');*/
		let signupRef = this.dialog.open(SignUpComponent, {
			disableClose: true,
			data : actionData
		});
		signupRef.afterClosed().subscribe(response => {
			if (response == 'sign-in') {
				this.openLoginDialog(actionData);
			}
		});
	}
	openForgetPasswordDialog() {
		/*this.dialogRef.close('sign-up');*/
		let forgetRef = this.dialog.open(ForgetPasswordComponent, {
			disableClose: true
		});
		forgetRef.afterClosed().subscribe(response => {
			if (response == 'sign-in') {
				this.openLoginDialog();
			}
		});
	}
	onMouseEnterOnMenu(event:any) {
		//let siblings;
		event.stopPropagation();
		/*let allHeaderMenu = document.querySelectorAll('li a.header_menu');
		allHeaderMenu.forEach(headerElementNode => {
			if (headerElementNode.classList.contains('active')) {
				headerElementNode.classList.remove('active');
			}
		})*/
		if ((this.navSec.nativeElement as HTMLElement).contains(event.target)) {
			let target = event.target || event.srcElement || event.currentTarget;
				target.classList.add('active');
	
			
		}
		
    	
    }
    onMouseOutFromMenu(event:any,element) {
    	event.stopPropagation();
    	if (!element.contains(event.relatedTarget)) {
			element.querySelector('a.header_menu').classList.remove('active');
			
		}
		
	}
	
	getSaveListCount(){
		this.cartService.saveListCount().subscribe(
			data => {
				// alert(JSON.stringify(data));
				if (data.status==200) {
					this.cartService.wishlistCount=data.total_count;
				}
			},
			err => { },
			function () {
				//completed callback
			}
		);
	}

	navigateToDetailPage(productSlug) {
		this._router.navigate(['details/'+productSlug]);
		window.scroll(0,0);
		this.showBagPopup=false;
		this.showBagPopupMob=false;
	 }

}