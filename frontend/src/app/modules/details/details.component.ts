import { Component, OnInit, Inject, PLATFORM_ID } from '@angular/core';
import {ActivatedRoute,Router} from '@angular/router';
import {DetailsService} from '../../global/service/details.service';
import {CartService} from '../../global/service/cart.service';
import {GlobalVariable, Global} from '../../global/service/global';
import { WarehouseService } from '../../global/service/warehouse.service';
import { GlobalService } from '../../global/service/app.global.service';
import { AuthenticationService } from '../../global/service/authentication.service';
import { LoginComponent } from '../../login/login.component';
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material';
import { MenuService } from '../../global/service/menu.service';
import { isPlatformBrowser } from '@angular/common';
// import { Title, Meta } from '@angular/platform-browser';
declare let fbq:Function;

@Component({
  selector: 'app-details',
  templateUrl: './details.component.html',
  styleUrls: ['./details.component.css']
})
export class DetailsComponent implements OnInit {

  public detailsData = {};
  public is_wishlist:any=0;
  public parentProductId;
  public categoryData;
  public formattedDetailsData = [];
  public productSlug;
  public productDetailsData = [];
  public S3_URL_PRODUCT =  GlobalVariable.S3_URL+'product/400x400/';
  public selectedProductId = 0;
  public owlConfiguration = {
		items: 1,
		dots: false,
		autoWidth:true,
		navigation: false
	};
	public carouselOptions:Object = {
				nav: true,
				responsiveClass: true,
				dots:false,
				items: 1,
				margin : 0,
				center : true,
				autoplay:false,
				navText: [
				        '<i class="fa fa-angle-left" aria-hidden="true"></i>',
				        '<i class="fa fa-angle-right" aria-hidden="true"></i>'
				    ],
				navContainer: '.custom-nav',
				autoplayTimeout:4000,
				autoplayHoverPause:true,
				singleItem: false,
				loop: true,
			};
  public carouselClasses = [
		'owl-theme',
		'row',
		'sliding'
		];
		custom_fields:any;		
  constructor(
    private _route : ActivatedRoute,
    private _detailsService:DetailsService,
    private _router:Router,
	public cartService:CartService,
	private _warehouseservice:WarehouseService,
	private _globalService:GlobalService,
	public authenticationService: AuthenticationService,
	private _global: Global,
	public dialog: MatDialog,
	public _menuservice:MenuService,
	@Inject(PLATFORM_ID) private platformId: Object,
	// private metaTagService: Meta,
	// private titleService: Title,

  ) {

	//fbq('trackCustom', 'GoGroceryDetailsPage', {promotion: 'This is the test message'});
  }
	ngOnInit() {

		this._warehouseservice.warehouseData$.subscribe(res=>{
			this._route.params.subscribe(response => {
				this.productSlug = this._route.snapshot.params['slug'];
				//alert(this.productSlug);
				this._globalService.showLoaderSpinner(true);
				if (isPlatformBrowser(this.platformId)) {
					this.getProductDetails();

				}
			});
		})
	
	}
	/**
	 * Method for getting product details by product slug
	 * @access public
	 */
	getProductDetails() {
		this._detailsService.getProductDetailsByProductSlug(this.productSlug).subscribe(response => {
			if(response && response['status'] == 200) {
				this._globalService.showLoaderSpinner(false);
				this.detailsData = response['data'];
				this.custom_fields=response['data'].custom_field
				console.log(this.custom_fields);
				this.parentProductId = this.detailsData['id'];
				this.categoryData = this.detailsData['category'];	
				if(response['data']['is_wishlist']==1){
					this.is_wishlist=1;
				}else{
					this.is_wishlist=0;
				}


				let logParms:any = {}
				logParms.content_name = this.detailsData["name"];
				logParms.content_category = this.detailsData["category"]["name"]
				logParms.content_ids = this.detailsData["id"];
				logParms.content_type = "product";
				logParms.value = this.detailsData["default_price"];
				logParms.currency = "AED";

				this._globalService.facebookPixelEventLog('track','ViewContent',logParms);

				let googleLogPamrs:any = [];
				let parms:any = {}
				parms.id = this.detailsData["id"];
				parms.name = this.detailsData["name"];
				parms.price = this.detailsData["default_price"]
				
				parms.brand = this.detailsData["brand"]["name"];
				parms.category = this.detailsData["default_price"];
				parms.list_position = "0";
				parms.currency = "AED";
				googleLogPamrs.push(parms);
				this._globalService.googleEventLog("event","ViewContent",googleLogPamrs);
				
				// console.log("**************** Details data *******************");
				// console.log(this.parentProductId);
				this.formatProductDetailsData();

				//////////////  SEO CONTENT //////////////////
				// let seoData: any = {};
				// seoData['metatitle']='Gogrocery: '+this.detailsData["meta_title"]!='' ?  this.detailsData["meta_title"] : this.detailsData["name"];
				// seoData['title']='Gogrocery: '+this.detailsData["name"];
				// seoData['description'] = this.detailsData['meta_description']!='' ?  this.detailsData['meta_description'] : this.detailsData["name"];
				// seoData['keywords'] = this.detailsData["meta_key_word"]!= '' ?  this.detailsData["meta_key_word"] :  this.detailsData["name"];	
				// console.log(seoData);				
				// this._globalService.setAdMetaData(seoData); 				 
			}
		})
	}
	addToWishList(item){
		let data={
			"website_id":this._globalService.getFrontedWebsiteId(),
			"product_id":item.id
		}
		if(this.authenticationService.userFirstName){
			this._global.getWebServiceData('my-wish-list', 'POST', data, '').subscribe(data => {
			if (data.status == 200) {
				let productName = data["data"]["product"]["name"];
				let itemId = data["data"]["product"]["id"];
				this._globalService.showToast(data.message);
				this.is_wishlist=1;

				let logParms:any = {}
				logParms.content_ids = itemId;
				logParms.content_name = productName;
				logParms.content_type = " product"
				this._globalService.facebookPixelEventLog('track','Add_to_wishlist',logParms);

				let googleLogPamrs:any = [];
				let parms:any = {}
				parms.id = itemId;
				parms.name = productName;
				googleLogPamrs.push(parms);
				this._globalService.googleEventLog("event","Add_to_wishlist",googleLogPamrs);

				
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
			}else{
				console.log(data);
				this._globalService.showToast('Somthing wen\'t wrong. Please try again'); 
			}
			}, err => console.log(err), function() {});

		}else{
			// this.openLoginDialog();
			if(!localStorage.getItem('currentUser')) {
				this._menuservice.signinSignuppopup$.next('sign-in');
				return false;
			}
		}
		
	}
	//login dialog
	loginComponent: MatDialogRef<LoginComponent> | null;
	openLoginDialog() {
		this.loginComponent = this.dialog.open(LoginComponent, {
			disableClose: true
		});
	}
	removeFromWishlist(pro_id:number){
		let data:any={};
		data={"product_id":pro_id}
		this._global.getWebServiceData('delete-wishlist', 'POST', data, '').subscribe(data => {
			if (data.status == 200) {
				this._globalService.showToast('Item removed from wishlist');
				this.getProductDetails();
				this.is_wishlist=0;
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
		}, err => console.log(err), function() {});
	}
	/**
	 * Formatting product details
	 * @access public
	 */
	formatProductDetailsData() {
		this.formattedDetailsData['product_list'] = {};
		this.formattedDetailsData['stock_list'] = {};
		this.formattedDetailsData['custom_field_list'] = [];
		//this.selectedProductData = {};
		// Format all variant data
		let clonedProductDetailsData = Object.assign({},this.detailsData);
		delete clonedProductDetailsData['variant_product'];
		this.selectedProductId = clonedProductDetailsData['id'];
		//alert(this.selectedProductId);
		// Configure owl carousel data
		this.configureOwlCarouselItem();
		this.formattedDetailsData['product_list'][clonedProductDetailsData['id']] = clonedProductDetailsData;
		if(this.detailsData['custom_field'] && this.detailsData['custom_field'].length > 0) {
			this.detailsData['custom_field'].forEach(customFieldsData => {
				if(customFieldsData['is_variant'] == 'Yes') {
					customFieldsData['is_parent'] = true;
					this.formattedDetailsData['custom_field_list'].push(customFieldsData);

				}
			});
		}
		// Get all variant product custom field
		if(this.detailsData['variant_product'] && this.detailsData['variant_product'].length > 0) {
			this.detailsData['variant_product'].forEach(variantProductData => {
						this.formattedDetailsData['product_list'][variantProductData['id']] = variantProductData;
						variantProductData['custom_field'].forEach(customFieldData => {
							if(customFieldData['is_variant'] == 'Yes') {
								customFieldData['is_parent'] = false;
								this.formattedDetailsData['custom_field_list'].push(customFieldData);

							}
						});
			});
		}

		this.detailsData['cover_image'] =  {};
		this.detailsData['variant_product'] = [];
		if(this.detailsData['product_image'] && this.detailsData['product_image'].length > 0) {
			this.detailsData['product_image'].forEach(detailsData => {
				if(detailsData['is_cover'] == 1) {
					this.detailsData['cover_image'] = detailsData;
				}
			});
		}
		this.formattedDetailsData['stock_list'] = this.detailsData['stock_data'];
		this.formattedDetailsData['uom'] = this.detailsData['uom'];	
	}
	/**
	 * Method for configuaring owl carousel objetc
	 */
	configureOwlCarouselItem() {
		if(this.formattedDetailsData['product_list'].length > 0 && this.formattedDetailsData['product_list'][this.selectedProductId]['product_image'].length > 0) {
			this.owlConfiguration['items'] = this.formattedDetailsData['product_list'][this.selectedProductId]['product_image'].length;
		} else {
			this.owlConfiguration['items'] = 1;
		}
	}
	/**
	 * Onchnage selected product
	 */
	onChangeSelectedProduct(productId) {
		this.selectedProductId = productId;
	}
	onHoverOverImage() {
		//console.log("**************** Hovering over image ****************")
	}

	imageZoom(imgID, resultID) {
		var img, lens, result, cx, cy;
		img = document.getElementById(imgID);
		result = document.getElementById(resultID);
		lens = document.createElement("DIV");
		lens.setAttribute("class", "img-zoom-lens");
		img.parentElement.insertBefore(lens, img);
		cx = result.offsetWidth / lens.offsetWidth;
		cy = result.offsetHeight / lens.offsetHeight;
		result.style.backgroundImage = "url('" + img.src + "')";
		result.style.backgroundSize = (img.width * cx) + "px " + (img.height * cy) + "px";
		lens.addEventListener("mousemove", moveLens);
		img.addEventListener("mousemove", moveLens);
		lens.addEventListener("touchmove", moveLens);
		img.addEventListener("touchmove", moveLens);
		
		function moveLens(e) {
		var pos, x, y;
		e.preventDefault();
		pos = getCursorPos(e);
		x = pos.x - (lens.offsetWidth / 2);
		y = pos.y - (lens.offsetHeight / 2);
		if (x > img.width - lens.offsetWidth) {x = img.width - lens.offsetWidth;}
		if (x < 0) {x = 0;}
		if (y > img.height - lens.offsetHeight) {y = img.height - lens.offsetHeight;}
		if (y < 0) {y = 0;}
		lens.style.left = x + "px";
		lens.style.top = y + "px";
		result.style.backgroundPosition = "-" + (x * cx) + "px -" + (y * cy) + "px";
	}
		function getCursorPos(e) {
		var a, x = 0, y = 0;
		e = e || window.event;
		a = img.getBoundingClientRect();
		/*calculate the cursor's x and y coordinates, relative to the image:*/
		x = e.pageX - a.left;
		y = e.pageY - a.top;
		/*consider any page scrolling:*/
		x = x - window.pageXOffset;
		y = y - window.pageYOffset;
		return {x : x, y : y};
		}
	}
	navigateToUrl(slug) {
	this._router.navigate(['/details/'+ slug]);

	}

}
