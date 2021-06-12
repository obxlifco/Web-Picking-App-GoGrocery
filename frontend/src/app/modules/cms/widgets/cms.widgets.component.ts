import { Component, OnInit, Input, Inject, Optional, Injectable,ViewChild,AfterViewInit,ElementRef,HostListener} from '@angular/core';
import { Observable } from 'rxjs';
import { Subject } from 'rxjs';
import { Router } from '@angular/router';
import { WidgetComponent } from './widget.component';
import { Global, GlobalVariable } from '../../../global/service/global';
import { GlobalService } from '../../../global/service/app.global.service';
import { CategoryService} from '../../../global/service/category.service';
import {ShoppingCartService } from '../../../global/service/app.cart.service';
import {CartService} from '../../../global/service/cart.service';
import {DealsorsellService} from '../../../global/service/dealsorsell.service';
import { CookieService } from 'ngx-cookie';
import { WINDOW } from '@ng-toolkit/universal';
import { WarehouseService } from '../../../global/service/warehouse.service';
import { ProductService } from '../../../global/service/product.service';
import { AuthenticationService } from '../../../global/service/authentication.service';
import { LoginComponent } from '../../login/login.component';
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material';
import { DialogsService } from '../../../global/dialog/confirm-dialog.service';
import { TranslateService } from '@ngx-translate/core'; //language change module
import { loginTransition } from '../../registration/registration.component';
import { MenuService } from '../../../global/service/menu.service';

@Component({
	templateUrl : './templates/banner/banner.html',
	styleUrls : ['./templates/banner/css/banner.css'],
})
export class BannerComponent implements WidgetComponent, OnInit {
	public widget_data: any = {};
	@Input() data: any;
	@Input() page_data: any;
	@Input() isCMS: boolean = false;
	carouselOptions = {
	nav: false,
	responsiveClass: true,
	dots:true,
	items: 1,
	autoplay:true,
	autoplayTimeout:4000,
	autoplayHoverPause:true,
	singleItem: true,
	loop: true,
	}
	constructor(
		public  _warehouseService:WarehouseService,
		public _productService: ProductService,
	) { }

	ngOnInit() {
		this._warehouseService.warehouseData$.subscribe(response => {
			for (var i = 0; i < this.data.length; i++) {
				for (var j = 0; j < this.data[i].properties.length; j++) {
				this.widget_data[this.data[i].properties[j].selector] = this.data[i].properties[j].value;
				}
			}
		});
	}
}
/**
 * Component for carousel slider
*/
@Component({
	templateUrl : './templates/carousel/carousel.html',
	styleUrls: ['./templates/carousel/css/carousel.css'],

})
export class CarouselComponent implements OnInit,WidgetComponent,AfterViewInit{
	@Input() data:any;
	@Input() page_data:any;
	@Input() isCMS:boolean = false;

	public defaultSlideShow:number = 0;
	public currentSliderIndex:number;
	public sliderRange:Array<boolean> = [];
	public showCarouselSlider:boolean = true;
	public sliderId;
	public carouselOptions:Object = {};
	public innerWidth: any;
	public mobileCarouselData = [];
	public s3Url:string = '';

	constructor(
		public _warehouseService:WarehouseService,
		public _globalService : GlobalService
	) {
	}

	ngOnInit() {
        this.s3Url = GlobalVariable.S3_URL;
		this.innerWidth = window.innerWidth;

		console.log("***************** Inner width data ****************",this.innerWidth);
		
		this._warehouseService.warehouseData$.subscribe(response => {
			this.carouselOptions = {
				nav: false,
				responsiveClass: true,
				dots:true,
				items: 1,
				autoplay:true,
				autoplayTimeout:4000,
				autoplayHoverPause:true,
				singleItem: true,
				loop: true,
			}
		});
		this.getMobileCarouselData();
	}
	ngAfterViewInit() {

	}
	@HostListener('window:resize', ['$event'])
	onresize(event) {
		this.innerWidth = window.innerWidth;
		//console.log("***************** Inner width data ****************",this.innerWidth);
   }
   getMobileCarouselData() {
   	this._globalService.getCarouselBanner().subscribe(response =>{
   		console.log("***************** Mobile carousel data ***************");
   			console.log(response);
   		if(response && response['status'] == 1) {
   			this.mobileCarouselData = response['data'];
   			console.log("***************** Mobile carousel data ***************");
   			console.log(this.mobileCarouselData);
   		}
   	});
   }




}

@Component({
	template: `
				<section class="temp_feature">
				<div class="container container-lg">
					<div class="row">
						<div class="col-md-6 col-lg-3">
							<div class="fech_box">
								<i class="fa {{widget_data.icon1}}"></i>
								<h5>{{widget_data.heading1}}</h5>
								<p>{{widget_data.desc1}}</p>
							</div>
						</div>
						<div class="col-md-6 col-lg-3">
							<div class="fech_box">
								<i class="fa {{widget_data.icon2}}"></i>
								<h5>{{widget_data.heading2}}</h5>
								<p>{{widget_data.desc2}}</p>
							</div>
						</div>
						<div class="col-md-6 col-lg-3">
							<div class="fech_box">
								<i class="fa {{widget_data.icon3}}"></i>
								<h5>{{widget_data.heading3}}</h5>
								<p>{{widget_data.desc3}}</p>
							</div>
						</div>
						<div class="col-md-6 col-lg-3">
							<div class="fech_box">
								<i class="fa {{widget_data.icon4}}"></i>
								<h5>{{widget_data.heading4}}</h5>
								<p>{{widget_data.desc4}}</p>
							</div>
						</div>
					</div>
				</div>
			</section>
	`,
})
export class InfoboxComponent implements WidgetComponent, OnInit {
	@Input() data: any;
	@Input() page_data: any;
	@Input() isCMS: boolean = false;
	constructor() {

	}
	public widget_data: any = {};
	ngOnInit() {
	for (var i = 0; i < this.data.length; i++) {
		for (var j = 0; j < this.data[i].properties.length; j++) {
		this.widget_data[this.data[i].properties[j].selector] = this.data[i].properties[j].value;
		}
	}
	}
}

@Component({
	template: `
				<section>
				<div class="container container-lg">
					<div class="row gutter50">
						<div class="col-sm-4">
							<a [attr.href]="(this.isCMS)?'javascript:void(0)':widget_data.box1_url">
								<div class="catagory">
								<img src="{{widget_data.box1_img}}" alt="">
								<div class="title">
									<div class="title-heading">{{widget_data.box1_heading}}</div>
									{{widget_data.box1_text}}
								</div>
								</div>
							</a>
						</div>
						<div class="col-sm-4">
							<a [attr.href]="(this.isCMS)?'javascript:void(0)':widget_data.box2_url">
								<div class="catagory">
								<img src="{{widget_data.box2_img}}" alt="">
								<div class="title">
									<div class="title-heading">{{widget_data.box2_heading}}</div>
									{{widget_data.box2_text}}
								</div>
								</div>
							</a>
						</div>
						<div class="col-sm-4">
							<a [attr.href]="(this.isCMS)?'javascript:void(0)':widget_data.box3_url">
								<div class="catagory">
								<img src="{{widget_data.box3_img}}" alt="">
								<div class="title">
									<div class="title-heading">{{widget_data.box3_heading}}</div>
									{{widget_data.box3_text}}
								</div>
								</div>
							</a>
						</div>
					</div>
				</div>    
				</section>
	`,
})
export class VFeaturedBoxComponent implements WidgetComponent, OnInit {
	@Input() data: any;
	@Input() page_data: any;
	@Input() isCMS: boolean = false;
	constructor() {
	}
	public widget_data: any = {};
	ngOnInit() {
	for (var i = 0; i < this.data.length; i++) {
		for (var j = 0; j < this.data[i].properties.length; j++) {
		this.widget_data[this.data[i].properties[j].selector] = this.data[i].properties[j].value;
		}
	}
	}
}

@Component({
	template: `
				<section>
				<div class="container">
					<div class="row">
					<div class="col-sm-4">
						<a [attr.href]="(this.isCMS)?'javascript:void(0)':widget_data.box1_url">
						<img src="{{widget_data.box1_img}}" alt="" title="">
						</a>
					</div>
					<div class="col-sm-4">
						<a [attr.href]="(this.isCMS)?'javascript:void(0)':widget_data.box2_url">
						<img src="{{widget_data.box2_img}}" alt="" title="">
						</a>
					</div>
					<div class="col-sm-4">
						<a [attr.href]="(this.isCMS)?'javascript:void(0)':widget_data.box3_url">
						<img src="{{widget_data.box3_img}}" alt="" title="">
						</a>
					</div>
					</div>
				</div>
				</section>
				
	`,
})
export class ThreeSideBannerComponent implements WidgetComponent, OnInit {
	@Input() data: any;
	@Input() page_data: any;
	@Input() isCMS: boolean = false;
	constructor() {
	}

	public widget_data: any = {};
	ngOnInit() {
	for (var i = 0; i < this.data.length; i++) {
		for (var j = 0; j < this.data[i].properties.length; j++) {
		this.widget_data[this.data[i].properties[j].selector] = this.data[i].properties[j].value;
		}
	}
	}
}

@Component({
	template: `
				<section>
				<div class="container container-lg">
					<div class="row gutter50">
						<div class="col-sm-6">
							<div class="catagory1">
								<div class="img-part"><img src="{{widget_data.box1_img}}"></div>
								<div class="text-part">
									<div class="row align-items-center">
										<div class="col">
											<h4>{{widget_data.box1_heading}}</h4>
											<p>{{widget_data.box1_desc}}</p>
										</div>                                
										<div class="col-auto ml-auto">
											<a [attr.href]="(this.isCMS)?'javascript:void(0)':widget_data.box1_link">
												<button class="btn-main mat-raised-button" mat-raised-button>
												<span class="mat-button-wrapper">{{widget_data.box1_btn}}</span>
												<div class="mat-button-ripple mat-ripple"></div>
												<div class="mat-button-focus-overlay"></div>
												</button>
											</a>
										</div>
									</div>
								</div>
							</div>
						</div>
						<div class="col-sm-6">
							<div class="catagory1">
								<div class="img-part"><img src="{{widget_data.box2_img}}"></div>
								<div class="text-part">
									<div class="row align-items-center">
										<div class="col">
											<h4>{{widget_data.box2_heading}}</h4>
											<p>{{widget_data.box2_desc}}</p>
										</div>                                
										<div class="col-auto ml-auto">
											<a [attr.href]="(this.isCMS)?'javascript:void(0)':widget_data.box2_link">
												<button class="btn-main mat-raised-button" mat-raised-button>
												<span class="mat-button-wrapper">{{widget_data.box2_btn}}</span>
												<div class="mat-button-ripple mat-ripple"></div>
												<div class="mat-button-focus-overlay"></div>
												</button>
											</a>
										</div>
									</div>
								</div>
							</div>
						</div>
					</div>
				</div>    
				</section>
	`,
})
export class HFeaturedBoxComponent implements WidgetComponent, OnInit {
	@Input() data: any;
	@Input() page_data: any;
	@Input() isCMS: boolean = false;
	constructor() {

	}
	public widget_data: any = {};
	ngOnInit() {
		for (var i = 0; i < this.data.length; i++) {
			for (var j = 0; j < this.data[i].properties.length; j++) {
			this.widget_data[this.data[i].properties[j].selector] = this.data[i].properties[j].value;
			}
		}
	}
}

@Component({
	providers: [Global],
	template:`<section *ngIf="isCMS">
				<div class="container container-lg">
					<h2 class="pro_title">{{widget_data.heading_text}}</h2>
					<ul class="product-list home">
						<li>
							<div class="product-box">
								<div class="h_pro_img">
									<img src="https://d2vltvjwlghbux.cloudfront.net/frontend/assets/template/images/pro_6.jpg">
									<ul class="home_product_action">
										
										<li><button class="btn-main-ripple mat-icon-button" mat-icon-button=""><span class="mat-button-wrapper"><i class="icon-cart"></i></span><div class="mat-button-ripple mat-ripple mat-button-ripple-round" matripple="" ng-reflect-trigger="[object HTMLButtonElement]" ng-reflect-centered="true" ng-reflect-disabled="false"></div><div class="mat-button-focus-overlay"></div></button></li>
										<li><button class="btn-main-ripple mat-icon-button" mat-icon-button=""><span class="mat-button-wrapper"><i class="icon-heart"></i></span><div class="mat-button-ripple mat-ripple mat-button-ripple-round" matripple="" ng-reflect-trigger="[object HTMLButtonElement]" ng-reflect-centered="true" ng-reflect-disabled="false"></div><div class="mat-button-focus-overlay"></div></button></li>
										<li><button class="btn-main-ripple mat-icon-button" mat-icon-button=""><span class="mat-button-wrapper"><i class="icon-zoom"></i></span><div class="mat-button-ripple mat-ripple mat-button-ripple-round" matripple="" ng-reflect-trigger="[object HTMLButtonElement]" ng-reflect-centered="true" ng-reflect-disabled="false"></div><div class="mat-button-focus-overlay"></div></button></li>
									</ul>
								</div>
								<div class="h_pro_desc">
									<p>Abominable Hoodie</p>
									<h4>$40.00</h4>
								</div>
							</div>
						</li>
						<li>
							<div class="product-box">
								<div class="h_pro_img">
									<img src="https://d2vltvjwlghbux.cloudfront.net/frontend/assets/template/images/pro_7.jpg">
									<ul class="home_product_action">
										<li><button class="btn-main-ripple mat-icon-button" mat-icon-button=""><span class="mat-button-wrapper"><i class="icon-cart"></i></span><div class="mat-button-ripple mat-ripple mat-button-ripple-round" matripple="" ng-reflect-trigger="[object HTMLButtonElement]" ng-reflect-centered="true" ng-reflect-disabled="false"></div><div class="mat-button-focus-overlay"></div></button></li>
										<li><button class="btn-main-ripple mat-icon-button" mat-icon-button=""><span class="mat-button-wrapper"><i class="icon-heart"></i></span><div class="mat-button-ripple mat-ripple mat-button-ripple-round" matripple="" ng-reflect-trigger="[object HTMLButtonElement]" ng-reflect-centered="true" ng-reflect-disabled="false"></div><div class="mat-button-focus-overlay"></div></button></li>
										<li><button class="btn-main-ripple mat-icon-button" mat-icon-button=""><span class="mat-button-wrapper"><i class="icon-zoom"></i></span><div class="mat-button-ripple mat-ripple mat-button-ripple-round" matripple="" ng-reflect-trigger="[object HTMLButtonElement]" ng-reflect-centered="true" ng-reflect-disabled="false"></div><div class="mat-button-focus-overlay"></div></button></li>
									</ul>
								</div>
								<div class="h_pro_desc">
									<p>Abominable Hoodie</p>
									<h4>$29.00</h4>
								</div>
							</div>
						</li>
						<li>
							<div class="product-box">
								<div class="h_pro_img">
									<img src="https://d2vltvjwlghbux.cloudfront.net/frontend/assets/template/images/pro_8.jpg">
									<ul class="home_product_action">
										<li><button class="btn-main-ripple mat-icon-button" mat-icon-button=""><span class="mat-button-wrapper"><i class="icon-cart"></i></span><div class="mat-button-ripple mat-ripple mat-button-ripple-round" matripple="" ng-reflect-trigger="[object HTMLButtonElement]" ng-reflect-centered="true" ng-reflect-disabled="false"></div><div class="mat-button-focus-overlay"></div></button></li>
										<li><button class="btn-main-ripple mat-icon-button" mat-icon-button=""><span class="mat-button-wrapper"><i class="icon-heart"></i></span><div class="mat-button-ripple mat-ripple mat-button-ripple-round" matripple="" ng-reflect-trigger="[object HTMLButtonElement]" ng-reflect-centered="true" ng-reflect-disabled="false"></div><div class="mat-button-focus-overlay"></div></button></li>
										<li><button class="btn-main-ripple mat-icon-button" mat-icon-button=""><span class="mat-button-wrapper"><i class="icon-zoom"></i></span><div class="mat-button-ripple mat-ripple mat-button-ripple-round" matripple="" ng-reflect-trigger="[object HTMLButtonElement]" ng-reflect-centered="true" ng-reflect-disabled="false"></div><div class="mat-button-focus-overlay"></div></button></li>
									</ul>
								</div>
								<div class="h_pro_desc">
									<p>Abominable Hoodie</p>
									<h4>$38.00</h4>
								</div>
							</div>
						</li>
						<li>
							<div class="product-box">
								<div class="h_pro_img">
									<img src="https://d2vltvjwlghbux.cloudfront.net/frontend/assets/template/images/pro_9.jpg">
									<ul class="home_product_action">
										<li><button class="btn-main-ripple mat-icon-button" mat-icon-button=""><span class="mat-button-wrapper"><i class="icon-cart"></i></span><div class="mat-button-ripple mat-ripple mat-button-ripple-round" matripple="" ng-reflect-trigger="[object HTMLButtonElement]" ng-reflect-centered="true" ng-reflect-disabled="false"></div><div class="mat-button-focus-overlay"></div></button></li>
										<li><button class="btn-main-ripple mat-icon-button" mat-icon-button=""><span class="mat-button-wrapper"><i class="icon-heart"></i></span><div class="mat-button-ripple mat-ripple mat-button-ripple-round" matripple="" ng-reflect-trigger="[object HTMLButtonElement]" ng-reflect-centered="true" ng-reflect-disabled="false"></div><div class="mat-button-focus-overlay"></div></button></li>
										<li><button class="btn-main-ripple mat-icon-button" mat-icon-button=""><span class="mat-button-wrapper"><i class="icon-zoom"></i></span><div class="mat-button-ripple mat-ripple mat-button-ripple-round" matripple="" ng-reflect-trigger="[object HTMLButtonElement]" ng-reflect-centered="true" ng-reflect-disabled="false"></div><div class="mat-button-focus-overlay"></div></button></li>
									</ul>
								</div>
								<div class="h_pro_desc">
									<p>Abominable Hoodie</p>
									<h4>$40.00</h4>
								</div>
							</div>
						</li>
					</ul>
				</div>
			</section>

			<section *ngIf="!isCMS && product_list.length">
				<div class="container container-lg">
					<h2 class="pro_title">{{widget_data.heading_text}}</h2>
					<ul class="product-list home">
						<li *ngFor="let product of product_list">
							
							<div class="product-box" [routerLink]="['/product/'+product.slug]">
								<div class="h_pro_img">
									<img *ngIf="product.cover_img" [src]="S3_URL_PRODUCT+product.cover_img">
									<img *ngIf="!product.cover_img" [src]="'https://d2vltvjwlghbux.cloudfront.net/frontend/assets/images/img1.jpg'">
									<div class="outs" *ngIf="product.stock<1 && _globalService.getFrontedWebsiteId()==1"><span>{{ 'GLOBAL.out_of_stock' | translate }}</span></div>
								</div>
								<div class="h_pro_desc">
									<p *ngIf="(lang_code=='th')">{{ ((product.name_th!='' && product.name_th!=null)?product.name_th:product.name) | limitTo:70 }}</p>
									<p *ngIf="(lang_code=='en')">{{ product.name | limitTo:70 }}</p>

									<h4 *ngIf="(product.discount | json) == '{}'; else discountCond">{{_globalService.getCurrencySymbol()}}{{ _globalService.exchangeRate(product.default_price,product.price_marketplace) | number:'1.2-2' }}</h4>
									<ng-template #discountCond>
									<h4>
										<del>{{_globalService.getCurrencySymbol()}}{{ _globalService.exchangeRate(product.default_price,product.price_marketplace) | number:'1.2-2' }}</del>
										{{_globalService.getCurrencySymbol()}}{{ _globalService.exchangeRate(_globalService.calculateProductDiscount(product.discount.disc_type,product.discount.amount,product.default_price),product.price_marketplace) | number:'1.2-2' }} 
										<span class="dis">({{product.discount.name}})</span>
									</h4>
									</ng-template>
									<div class="rating_box" *ngIf="product.review_dict.avg_rating>0">
										<rating [(ngModel)]="product.review_dict.avg_rating" name="review_star" [readonly]="true"></rating>
										 <span class="rev">{{ product.review_dict.total_reviews }} </span>
										<div class="clear"></div>
									</div>
								</div>
							</div>
							<ul class="home_product_action">
								<li><button mat-icon-button class="btn-main-ripple" matTooltip="{{ 'GLOBAL.add_to_cart' | translate }}" (click)="_shoppingCartService.addProductToCart(product, 1)" [disabled]="product.stock<1"><i class="icon-cart"></i></button></li>
								<li><button mat-icon-button class="btn-main-ripple" matTooltip="{{ 'GLOBAL.add_to_wishlist' | translate }}" (click)="_shoppingCartService.addToWishlist(product)"><i class="icon-heart"></i></button></li>
								<li><button mat-icon-button class="btn-main-ripple" matTooltip="{{ 'GLOBAL.view_details' | translate }}" [routerLink]="['/product/'+product.slug]"><i class="icon-zoom"></i></button></li>
							</ul>
						</li>
						
					</ul>
				</div>
			</section>`,
	})
export class FeatureProductComponent implements WidgetComponent, OnInit {
	@Input() data: any;
	@Input() page_data: any;
	@Input() isCMS: boolean = false;
	public product_list: any = [];
	public widget_data: any = {};
	public S3_URL_PRODUCT: string;
	public lang_code: string;
	constructor(
		private _global: Global,
		private _globalService: GlobalService,
		public _shoppingCartService: ShoppingCartService,
		private _cookieService: CookieService
	) {
		let globalData = this._cookieService.getObject('globalData');
		if (globalData['lang_code']) {
			this.lang_code = globalData['lang_code'];
		}
		this._globalService.langChange$.subscribe(value => {
			this.lang_code = value;
		});
	}



	ngOnInit() {
		for (var i = 0; i < this.data.length; i++) {
			for (var j = 0; j < this.data[i].properties.length; j++) {
			this.widget_data[this.data[i].properties[j].selector] = this.data[i].properties[j].value;
			}
		}
		if (!this.isCMS) {
			this.S3_URL_PRODUCT = GlobalVariable.S3_URL + 'product/400x400/';
			this.loadProducts();
		}
	}

	loadProducts() {
	this._global.getFeaturedProducts().subscribe(
		data => {
		if (data.status) {
			this.product_list = data.api_status;
		}
		},
		err => {
		this._globalService.showToast('Something went wrong. Please try again.');
		},
		function () {
		//completed callback
		}
	);
	}
}

//Brands
@Component({
	providers: [Global],
	templateUrl : './templates/brands/brands.html',
	styleUrls : ['./css/carousel_slider.css']
})
export class BrandsWidgetComponent implements WidgetComponent, OnInit {
	@Input() data: any;
	@Input() page_data: any;
	@Input() isCMS: boolean = false;
	public brand_list: any = [];
	public widget_data: any = {};
	public S3_URL_CATEGORY: string;
	public lang_code: string;
	public innerWidth;
	public carouselOptions:Object = {
				nav: true,
				responsiveClass: true,
				items:5,
				dots:false,
				margin : 0,
				autoHeight:false,
				center : false,
				autoplay:false,
				navText: [
				        '<i class="fa fa-angle-left" aria-hidden="true"></i>',
				        '<i class="fa fa-angle-right" aria-hidden="true"></i>'
				    ],
				navContainer: '.custom-nav-brand',
				autoplayTimeout:4000,
				autoplayHoverPause:true,
				singleItem: false,
				loop: true,
			};
	constructor(private _global: Global, private _globalService: GlobalService, public _shoppingCartService: ShoppingCartService, 
	private _cookieService: CookieService,private _categoryService:CategoryService,private _router:Router,public _warehouseService:WarehouseService) {

	let globalData = this._cookieService.getObject('globalData');
	if (globalData['lang_code']) {
		this.lang_code = globalData['lang_code'];
	}

	this._globalService.langChange$.subscribe(value => {
		this.lang_code = value;
	});
	}



	ngOnInit() {
     this.innerWidth = window.innerWidth;
	 
	this._warehouseService.warehouseData$.subscribe(response => {

	for (var i = 0; i < this.data.length; i++) {

		for (var j = 0; j < this.data[i].properties.length; j++) {

		this.widget_data[this.data[i].properties[j].selector] = this.data[i].properties[j].value;
		}
	}
	if (!this.isCMS) {
		
		this.S3_URL_CATEGORY = GlobalVariable.S3_URL + 'brand/200x200/';
		this.loadBrands();
	}
	})
	//this.loadBrands(); 
	}
	@HostListener('window:resize', ['$event'])
	 onresize(event) {
		this.innerWidth = window.innerWidth;	
     }
	loadBrands() {
	let selectedBrandId = [];
	let brandSelector = ['brand_id_1','brand_id_2','brand_id_3','brand_id_4','brand_id_5','brand_id_6','brand_id_7','brand_id_8'];
	for(let brand in this.widget_data) {
		if(brandSelector.includes(brand)) {
		selectedBrandId.push(this.widget_data[brand]);
		}

	}
	/*this._categoryService.getShopByCategoryDataByCategoryId(selectedCategoryId).subscribe(response => {
	 if(response && response['status'] == 1) {
		 this.categories_list = response['data'];
		 
	 }
	});*/
	this._categoryService.getBrandListByBrandId(selectedBrandId).subscribe(
		data => {
		if (data.status) {
			console.log("******************* Brand list ****************");
			console.log(data);
			this.brand_list = data.brands;
			this.brand_list.forEach(item=>{
				item['encr']=btoa(JSON.stringify({'name':item.name,'id':item.id}));
			})
		}
		},
		err => {
			this._globalService.showToast('Something went wrong. Please try again.');
		},
		function () {
		//completed callback
		}
	);
	}
	/**
	 * M
	*/
	navigateToUrl(brandSlug) {
	 if(brandSlug) {
	 this._router.navigate(['/listing/brand/'+brandSlug]);
	 }
	}
}
//Categories
@Component({
	providers: [Global],
	templateUrl : './templates/categories/categories.html',
})
export class CategoriesComponent implements WidgetComponent, OnInit {

	@Input() data: any;
	@Input() page_data: any;
	@Input() isCMS: boolean = false;

	public warehouseidForShopByCategory : any = {};
	public categories_list: any = [];
	public widget_data: any = {};
	public S3_URL_CATEGORY: string;
	public lang_code: string;
	//public category_color:any;
	public category_color:Array<string> = ['cata_color_a','cata_color_b','cata_color_c','cata_color_d','cata_color_e','cata_color_f','cata_color_g','cata_color_h','cata_color_a','cata_color_b','cata_color_c','cata_color_d','cata_color_e','cata_color_f','cata_color_g','cata_color_h','cata_color_a','cata_color_b','cata_color_c','cata_color_d','cata_color_e','cata_color_f','cata_color_g','cata_color_h','cata_color_a','cata_color_b','cata_color_c','cata_color_d','cata_color_e','cata_color_f','cata_color_g','cata_color_h','cata_color_a','cata_color_b','cata_color_c','cata_color_d','cata_color_e','cata_color_f','cata_color_g','cata_color_h','cata_color_a','cata_color_b','cata_color_c','cata_color_d','cata_color_e','cata_color_f','cata_color_g','cata_color_h','cata_color_a','cata_color_b','cata_color_c','cata_color_d','cata_color_e','cata_color_f','cata_color_g','cata_color_h','cata_color_a','cata_color_b','cata_color_c','cata_color_d','cata_color_e','cata_color_f','cata_color_g','cata_color_h','cata_color_a','cata_color_b','cata_color_c','cata_color_d','cata_color_e','cata_color_f','cata_color_g','cata_color_h','cata_color_a','cata_color_b','cata_color_c','cata_color_d','cata_color_e','cata_color_f','cata_color_g','cata_color_h','cata_color_a','cata_color_b','cata_color_c','cata_color_d','cata_color_e','cata_color_f','cata_color_g','cata_color_h','cata_color_a','cata_color_b','cata_color_c','cata_color_d','cata_color_e','cata_color_f','cata_color_g','cata_color_h','cata_color_a','cata_color_b','cata_color_c','cata_color_d','cata_color_e','cata_color_f','cata_color_g','cata_color_h','cata_color_a','cata_color_b','cata_color_c','cata_color_d','cata_color_e','cata_color_f','cata_color_g','cata_color_h'];
    public category_dummy_color:any = ['cata_color_a','cata_color_b','cata_color_c','cata_color_d','cata_color_e','cata_color_f','cata_color_g','cata_color_h'];
    public innerWidth: any;
    public carouselOptions:Object = {
				nav: true,
				responsiveClass: true,
			    items:25,
				dots:false,
				margin : 0,
				autoHeight:false,
				center : false,
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
				rewind : false
			};
	constructor(private _global: Global,
				private _globalService: GlobalService,
				public _shoppingCartService: ShoppingCartService,
				private _cookieService: CookieService,
				private _categoryService:CategoryService,
				public _warehouseService:WarehouseService
			 ) {

	this.innerWidth = window.innerWidth;
	console.log(this.innerWidth,'innerWidth')
	let globalData = this._cookieService.getObject('globalData');
	if (globalData['lang_code']) {
		this.lang_code = globalData['lang_code'];
	}

	this._globalService.langChange$.subscribe(value => {
		this.lang_code = value;
	});
	}


    @HostListener('window:resize', ['$event'])
	onresize(event) {
		this.innerWidth = window.innerWidth;
		console.log("***************** Inner width data ****************",this.innerWidth);
   }
	ngOnInit() {
	this._warehouseService.warehouseData$.subscribe(response => {
	this.warehouseidForShopByCategory = response;
	console.log(this.warehouseidForShopByCategory,'warehouseidForShopByCategory')
	for (var i = 0; i < this.data.length; i++) {

		for (var j = 0; j < this.data[i].properties.length; j++) {

		this.widget_data[this.data[i].properties[j].selector] = this.data[i].properties[j].value;
		}
	}
	if (!this.isCMS) {
		this.S3_URL_CATEGORY = GlobalVariable.S3_URL + 'category/200x200/';
		this.loadCategories();
	}
	})
	//this.loadCategories(); 
	}

	loadCategories() {
		let selectedWarehouseID;
		let selectedCategoryId = [];
		let catgorySelector = ['category_id_1','category_id_2','category_id_3','category_id_4','category_id_5','category_id_6','category_id_7','category_id_8'];
		for(let category in this.widget_data) {
			if(catgorySelector.includes(category)) {
				selectedCategoryId.push(this.widget_data[category]);
			}
		}
		this.carouselOptions['loop'] = true;
		selectedWarehouseID = this.warehouseidForShopByCategory.selected_warehouse_id;
		console.log(selectedWarehouseID,'selectedWarehouseID')
		this._categoryService.getShopByCategoryDataByCategoryId(selectedCategoryId, selectedWarehouseID).subscribe(response => {
			console.log("**************** Shop by category data **************");
			console.log(response);
		 	if(response && response['status'] == 1) {
		 		let category_list_length = response['data'] ? response['data'].length : 0;
		 		console.log("***************** Category list length **************",category_list_length);
                //this.repetedCategoryData(category_list_length);
				 //this.categories_list = response['data'];
				this.categories_list = [];
			 	if(response && response['data'] && response['data'].length > 0) {
			 		response['data'].map(singleCategory => {
			 			if(singleCategory['image']) {
			 				this.categories_list.push(singleCategory);

			 			}
					 });
					console.log(this.categories_list,'******categories_list******')
					console.log(this.categories_list.length,'******categories_list_length******')
					this.carouselOptions['items'] = this.categories_list.length;					 
					if(this.categories_list.length < 8){
						this.carouselOptions['loop'] = false;
					}

			 	}
			 	//this.carouselOptions['items'] = category_list_length;
		 	}
		});
	}
	repetedCategoryData(totalCategoryListLength = 0) {
		if(totalCategoryListLength > 0 && totalCategoryListLength > 8) {
			let totalColorRepeat:any = (totalCategoryListLength/8)+1;
			 totalColorRepeat = parseInt(totalColorRepeat);

			this.category_color = Array(totalColorRepeat).join(this.category_dummy_color).split(', ');
			console.log("****************** Category color *****************");
			console.log(this.category_color);





		}


	}
}



//Parent Categories
@Component({
	providers: [Global],
	templateUrl: './templates/parentcategories/parentcategories.html',
})
export class ParentCategoriesComponent implements WidgetComponent, OnInit {

	@Input() data: any;
	@Input() page_data: any;
	@Input() isCMS: boolean = false;

	public category_wise_product: any = [];
	public widget_data: any = {};
	public S3_URL_CATEGORY: string;
	public lang_code: string;
	public category_id: any;
	public selected_warehouse_id = '';
	public wishlist:any=[];
	public wishlist_ids:any=[]
	public savelist_data = [];
	public formModel:any={};

	constructor(
		private _global: Global,
		private _globalService: GlobalService,
		public _shoppingCartService: ShoppingCartService,
		private _cookieService: CookieService,
		private _categoryService:CategoryService,
		private _router:Router,
		public cartService:CartService,
		public _warehouseService:WarehouseService,
		public authenticationService: AuthenticationService,
		public dialog: MatDialog,
		public _menuservice:MenuService,


		) {

	let globalData = this._cookieService.getObject('globalData');
	if (globalData['lang_code']) {
		this.lang_code = globalData['lang_code'];
	}

	this._globalService.langChange$.subscribe(value => {
		this.lang_code = value;
	});
	}



	ngOnInit() {
		this._warehouseService.warehouseData$.subscribe(response => {
			this.selected_warehouse_id = response && response['selected_warehouse_id'] ? response['selected_warehouse_id'] : GlobalVariable['DEFAULT_WAREHOUSE_DATA']['selected_warehouse_id'];
			console.log("*************** Selected warehouse id ***************",this.selected_warehouse_id);
			for (var i = 0; i < this.data.length; i++) {
				for (var j = 0; j < this.data[i].properties.length; j++) {
					this.widget_data[this.data[i].properties[j].selector] = this.data[i].properties[j].value;
				}
			}
			this.category_id = this.widget_data.category_id;
			if (!this.isCMS) {
				this.S3_URL_CATEGORY = GlobalVariable.S3_URL + 'category/200x200/';
				this.getParentCategoryProductByCategoryId(this.category_id,this.selected_warehouse_id);
			}
		})
		//this.loadParentCategories(this.category_id); 
	}

 /* loadParentCategories(category_id) {
	let data = { 'category_id': category_id };
	this._global.getParentCategories(data).subscribe(
		data => {
		if (data.status) {
			this.categories_list = data.categories;
			console.log("*************** Parent category list data *************");
			console.log(this.categories_list);
		}
		},
		err => {
		this._globalService.showToast('Something went wrong. Please try again.');
		},
		function () {
		//completed callback
		}
	);
	}*/
	/**
	 * Method for getting category wise product
	 * @param categoryId
	 * @access public
	*/
	getParentCategoryProductByCategoryId(categoryId,warehouseId) {
		this._categoryService.getProductByCategoryId(categoryId,warehouseId).subscribe(response => {
			if(response && response['status'] == 1) {
				this.category_wise_product = response['data'].length > 0 && response['data'][0]['product'] ? this.formatProductData(response['data'][0]['product']) : [];
				
			}
		});
	}
	/**
	 * Method for fomatting categories data
	 * @access public
	 * @return formatted data
	*/
	/**
	* Method for formatting deals or sales data
	* @access public
	* @return array
	 */
	 formatProductData(categoriesData = []) {
	 if(categoriesData && categoriesData.length > 0) {

		 let i = 0;
		 categoriesData.forEach(productData => {
		 	try {
		 		/*if(!productData['new_default_price_unit'] && productData['new_default_price_unit'] == 0) {	
		 		 	throw "Invalid product price";
		 		}*/
		 		 
		 		let tempProductData = [];
				 let cloneProductData = Object.assign({},productData);
				 delete cloneProductData.variant_product;
				 categoriesData[i]['selected_product'] = cloneProductData;
				 cloneProductData['is_parent'] = true;
				 tempProductData.push(cloneProductData);
				 if(productData.id){
					 productData.isSaveList=false;
				 }
				 if(productData['variant_product'].length > 0) {
					 tempProductData = tempProductData.concat(productData['variant_product']);

				 }
				 categoriesData[i]['variant_product'] = tempProductData;
				 i++;

		 	}catch(err){
		 		console.log(err);
			 

		    }
		 	}

		);
	 }
	 return categoriesData;
	 }
	 /**
	* Method for navigate to details
	 */
	navigateToDetails(slug) {
	 	this._router.navigate(['/details/'+slug]);
	}

	//  getting save list data after click on icon ....save-list
	getSaveList(product_id, add_new='n') {
		if(this.authenticationService.userFirstName) {
		  let data= {
			"website_id":this._globalService.getFrontedWebsiteId()
		  }
		  if(add_new == 'n') {
			this.category_wise_product.map(x => {
			  if (x.id == product_id) {
				x.isSaveList = !x.isSaveList;
			  } else {
				x.isSaveList = false;
			  }
			});
		  }
	
		  this._global.getWebServiceData('save-list', 'GET', '', '').subscribe(data => {
			if (data.status == 1) {
			  this.savelist_data = data.data;
			  this.savelist_data.forEach(element => {
				var pro_ids=element.product_ids.replace (/"/g,'');
				if(pro_ids.includes(product_id)){
				  element.is_checked=1;
				} else {
				  // 
				}
			  });
			} else {
			  // console.log(data);
			  this._globalService.showToast('Somthing wen\'t wrong. Please try again'); 
			}
		  }, err => console.log(err), function() {});
	
		} else {
		//   this.openLoginDialog();

			if(!localStorage.getItem('currentUser')) {
				this._menuservice.signinSignuppopup$.next('sign-in');
				return false;
			}
		}
	}

	//  add and remove from save list....addremove-from-savelist
	addToSaveList(product_id:number, list_id:number, is_checked) {
	let action = 'add';
	if(is_checked) {
		action = 'del';
	}
	let post_data = {
		"website_id":this._globalService.getFrontedWebsiteId(),
		"product_id":product_id,
		"action": action,
		"list_id":list_id
	}
	if(this.authenticationService.userFirstName) {
		this._global.getWebServiceData('addremove-from-savelist', 'PUT', post_data, '').subscribe(data => {
		if (data.status == 200) {
			// this._globalService.showToast(data.message);
			// this.getSaveList(product_id, 'n');

		} else {
		// console.log(data);
		this._globalService.showToast('Somthing wen\'t wrong. Please try again'); 
		}
		}, err => console.log(err), function() {});
	} else {
		// this.openLoginDialog();
		if(!localStorage.getItem('currentUser')) {
			this._menuservice.signinSignuppopup$.next('sign-in');
			return false;
		}
	}
	}
	//  Add new save list ....save-list
	addNewSaveList(i:number, product_id, savelist_name = '') {
		if(this.authenticationService.userFirstName) {
		  if(savelist_name == '') {
			this._globalService.showToast('Please enter savelist name'); 
		  } else {
			let data= {
			  "website_id":this._globalService.getFrontedWebsiteId(),
			  "product_id":product_id,
			  "name":savelist_name
			}
			this._global.getWebServiceData('save-list', 'POST', data, '').subscribe(data => {
			if (data.status == 200) {
			  this.getSaveList(product_id, 'y');
			  // this._globalService.showToast(data.message);
			} else {
			  // console.log(data);
			  this._globalService.showToast('Somthing wen\'t wrong. Please try again'); 
			}
			}, err => console.log(err), function() {});
		  }
		} else {
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
}


@Component({
	providers: [Global],
	template: `
			
			<section *ngIf="isCMS">
				<div class="container container-lg">
					<h2 class="pro_title">{{widget_data.heading_text}}</h2>
					<ul class="product-list home">
						<li>
							<div class="product-box">
								<div class="h_pro_img">
									<img src="https://d2vltvjwlghbux.cloudfront.net/frontend/assets/template/images/pro_6.jpg">
									<ul class="home_product_action">
										
										<li><button class="btn-main-ripple mat-icon-button" mat-icon-button=""><span class="mat-button-wrapper"><i class="icon-cart"></i></span><div class="mat-button-ripple mat-ripple mat-button-ripple-round" matripple="" ng-reflect-trigger="[object HTMLButtonElement]" ng-reflect-centered="true" ng-reflect-disabled="false"></div><div class="mat-button-focus-overlay"></div></button></li>
										<li><button class="btn-main-ripple mat-icon-button" mat-icon-button=""><span class="mat-button-wrapper"><i class="icon-heart"></i></span><div class="mat-button-ripple mat-ripple mat-button-ripple-round" matripple="" ng-reflect-trigger="[object HTMLButtonElement]" ng-reflect-centered="true" ng-reflect-disabled="false"></div><div class="mat-button-focus-overlay"></div></button></li>
										<li><button class="btn-main-ripple mat-icon-button" mat-icon-button=""><span class="mat-button-wrapper"><i class="icon-zoom"></i></span><div class="mat-button-ripple mat-ripple mat-button-ripple-round" matripple="" ng-reflect-trigger="[object HTMLButtonElement]" ng-reflect-centered="true" ng-reflect-disabled="false"></div><div class="mat-button-focus-overlay"></div></button></li>
									</ul>
								</div>
								<div class="h_pro_desc">
									<p>Abominable Hoodie</p>
									<h4>$40.00</h4>
								</div>
							</div>
						</li>
						<li>
							<div class="product-box">
								<div class="h_pro_img">
									<img src="https://d2vltvjwlghbux.cloudfront.net/frontend/assets/template/images/pro_7.jpg">
									<ul class="home_product_action">
										<li><button class="btn-main-ripple mat-icon-button" mat-icon-button=""><span class="mat-button-wrapper"><i class="icon-cart"></i></span><div class="mat-button-ripple mat-ripple mat-button-ripple-round" matripple="" ng-reflect-trigger="[object HTMLButtonElement]" ng-reflect-centered="true" ng-reflect-disabled="false"></div><div class="mat-button-focus-overlay"></div></button></li>
										<li><button class="btn-main-ripple mat-icon-button" mat-icon-button=""><span class="mat-button-wrapper"><i class="icon-heart"></i></span><div class="mat-button-ripple mat-ripple mat-button-ripple-round" matripple="" ng-reflect-trigger="[object HTMLButtonElement]" ng-reflect-centered="true" ng-reflect-disabled="false"></div><div class="mat-button-focus-overlay"></div></button></li>
										<li><button class="btn-main-ripple mat-icon-button" mat-icon-button=""><span class="mat-button-wrapper"><i class="icon-zoom"></i></span><div class="mat-button-ripple mat-ripple mat-button-ripple-round" matripple="" ng-reflect-trigger="[object HTMLButtonElement]" ng-reflect-centered="true" ng-reflect-disabled="false"></div><div class="mat-button-focus-overlay"></div></button></li>
									</ul>
								</div>
								<div class="h_pro_desc">
									<p>Abominable Hoodie</p>
									<h4>$29.00</h4>
								</div>
							</div>
						</li>
						<li>
							<div class="product-box">
								<div class="h_pro_img">
									<img src="https://d2vltvjwlghbux.cloudfront.net/frontend/assets/template/images/pro_8.jpg">
									<ul class="home_product_action">
										<li><button class="btn-main-ripple mat-icon-button" mat-icon-button=""><span class="mat-button-wrapper"><i class="icon-cart"></i></span><div class="mat-button-ripple mat-ripple mat-button-ripple-round" matripple="" ng-reflect-trigger="[object HTMLButtonElement]" ng-reflect-centered="true" ng-reflect-disabled="false"></div><div class="mat-button-focus-overlay"></div></button></li>
										<li><button class="btn-main-ripple mat-icon-button" mat-icon-button=""><span class="mat-button-wrapper"><i class="icon-heart"></i></span><div class="mat-button-ripple mat-ripple mat-button-ripple-round" matripple="" ng-reflect-trigger="[object HTMLButtonElement]" ng-reflect-centered="true" ng-reflect-disabled="false"></div><div class="mat-button-focus-overlay"></div></button></li>
										<li><button class="btn-main-ripple mat-icon-button" mat-icon-button=""><span class="mat-button-wrapper"><i class="icon-zoom"></i></span><div class="mat-button-ripple mat-ripple mat-button-ripple-round" matripple="" ng-reflect-trigger="[object HTMLButtonElement]" ng-reflect-centered="true" ng-reflect-disabled="false"></div><div class="mat-button-focus-overlay"></div></button></li>
									</ul>
								</div>
								<div class="h_pro_desc">
									<p>Abominable Hoodie</p>
									<h4>$38.00</h4>
								</div>
							</div>
						</li>
						<li>
							<div class="product-box">
								<div class="h_pro_img">
									<img src="https://d2vltvjwlghbux.cloudfront.net/frontend/assets/template/images/pro_9.jpg">
									<ul class="home_product_action">
										<li><button class="btn-main-ripple mat-icon-button" mat-icon-button=""><span class="mat-button-wrapper"><i class="icon-cart"></i></span><div class="mat-button-ripple mat-ripple mat-button-ripple-round" matripple="" ng-reflect-trigger="[object HTMLButtonElement]" ng-reflect-centered="true" ng-reflect-disabled="false"></div><div class="mat-button-focus-overlay"></div></button></li>
										<li><button class="btn-main-ripple mat-icon-button" mat-icon-button=""><span class="mat-button-wrapper"><i class="icon-heart"></i></span><div class="mat-button-ripple mat-ripple mat-button-ripple-round" matripple="" ng-reflect-trigger="[object HTMLButtonElement]" ng-reflect-centered="true" ng-reflect-disabled="false"></div><div class="mat-button-focus-overlay"></div></button></li>
										<li><button class="btn-main-ripple mat-icon-button" mat-icon-button=""><span class="mat-button-wrapper"><i class="icon-zoom"></i></span><div class="mat-button-ripple mat-ripple mat-button-ripple-round" matripple="" ng-reflect-trigger="[object HTMLButtonElement]" ng-reflect-centered="true" ng-reflect-disabled="false"></div><div class="mat-button-focus-overlay"></div></button></li>
									</ul>
								</div>
								<div class="h_pro_desc">
									<p>Abominable Hoodie</p>
									<h4>$40.00</h4>
								</div>
							</div>
						</li>
					</ul>
				</div>
			</section>
			<section *ngIf="!isCMS && product_list.length">
				<div class="container container-lg">
					<h2 class="pro_title">{{widget_data.heading_text}}</h2>
					<ul class="product-list home">
						<li *ngFor="let product of product_list">

							
							<div class="product-box" [routerLink]="['/product/'+product.slug]">
								<div class="h_pro_img">
									<img *ngIf="product.cover_img" [src]="S3_URL_PRODUCT+product.cover_img">
									<img *ngIf="!product.cover_img" [src]="'https://d2vltvjwlghbux.cloudfront.net/frontend/assets/images/img1.jpg'">
									<div class="outs" *ngIf="product.stock<1 && _globalService.getFrontedWebsiteId()==1"><span>{{ 'GLOBAL.out_of_stock' | translate }}</span></div>
								</div>
								<div class="h_pro_desc">
									<p *ngIf="(lang_code=='th')">{{ ((product.name_th!='' && product.name_th!=null)?product.name_th:product.name) | limitTo:70 }}</p>
									<p *ngIf="(lang_code=='en')">{{ product.name | limitTo:70 }}</p>
									
									<h4 *ngIf="(product.discount | json) == '{}'; else discountCond">{{_globalService.getCurrencySymbol()}}{{ _globalService.exchangeRate(product.default_price,product.price_marketplace) | number:'1.2-2' }}</h4>
									<ng-template #discountCond>
									<h4>
										<del>{{_globalService.getCurrencySymbol()}}{{ _globalService.exchangeRate(product.default_price,product.price_marketplace) | number:'1.2-2'}}</del>  
										{{_globalService.getCurrencySymbol()}}{{ _globalService.exchangeRate(_globalService.calculateProductDiscount(product.discount.disc_type,product.discount.amount,product.default_price),product.price_marketplace) | number:'1.2-2' }} 
										<span class="dis">({{product.discount.name}})</span>
									</h4>
									</ng-template>
									<div class="rating_box" *ngIf="product.review_dict.avg_rating>0">
										<rating [(ngModel)]="product.review_dict.avg_rating" name="review_star" [readonly]="true"></rating>
										 <span class="rev">{{ product.review_dict.total_reviews }}  </span>
										<div class="clear"></div>
									</div>
								</div>
							</div>
							<ul class="home_product_action">
							<li><button mat-icon-button class="btn-main-ripple" matTooltip="{{ 'GLOBAL.add_to_cart' | translate }}" (click)="_shoppingCartService.addProductToCart(product, 1)" [disabled]="product.stock<1"><i class="icon-cart"></i></button></li>
							<li><button mat-icon-button class="btn-main-ripple" matTooltip="{{ 'GLOBAL.add_to_wishlist' | translate }}" (click)="_shoppingCartService.addToWishlist(product)"><i class="icon-heart"></i></button></li>
							<li><button mat-icon-button class="btn-main-ripple" matTooltip="{{ 'GLOBAL.view_details' | translate }}" [routerLink]="['/product/'+product.slug]"><i class="icon-zoom"></i></button></li>
							</ul>
						</li>
						
					</ul>
				</div>  
			</section>
	`,
})
export class NewProductComponent implements WidgetComponent, OnInit {

	@Input() data: any;
	@Input() page_data: any;
	@Input() isCMS: boolean = false;

	public product_list: any = [];
	public widget_data: any = {};
	public S3_URL_PRODUCT: string;
	public lang_code: string;

	constructor(private _global: Global, private _globalService: GlobalService, public _shoppingCartService: ShoppingCartService, private _cookieService: CookieService) {
	let globalData = this._cookieService.getObject('globalData');
	if (globalData['lang_code']) {
		this.lang_code = globalData['lang_code'];
	}

	this._globalService.langChange$.subscribe(value => {
		this.lang_code = value;
	});
	}



	ngOnInit() {


	for (var i = 0; i < this.data.length; i++) {

		for (var j = 0; j < this.data[i].properties.length; j++) {

		this.widget_data[this.data[i].properties[j].selector] = this.data[i].properties[j].value;
		}

		if (!this.isCMS) {
		this.S3_URL_PRODUCT = GlobalVariable.S3_URL + 'product/400x400/';
		this.loadProducts();
		}

	}

	}

	loadProducts() {

	this._global.getNewProducts().subscribe(
		data => {
		if (data.status) {
			this.product_list = data.api_status;
		}
		},
		err => {
		this._globalService.showToast('Something went wrong. Please try again.');
		},
		function () {
		//completed callback
		}
	);
	}
}


@Component({
	providers: [Global],
	template: `
			
			<section *ngIf="isCMS">
				<div class="container container-lg">
					<h2 class="pro_title">{{widget_data.heading_text}}</h2>
					<ul class="product-list home">
						<li>
							<div class="product-box">
								<div class="h_pro_img">
									<img src="https://d2vltvjwlghbux.cloudfront.net/frontend/assets/template/images/pro_6.jpg">
									<ul class="home_product_action">
										
										<li><button class="btn-main-ripple mat-icon-button" mat-icon-button=""><span class="mat-button-wrapper"><i class="icon-cart"></i></span><div class="mat-button-ripple mat-ripple mat-button-ripple-round" matripple="" ng-reflect-trigger="[object HTMLButtonElement]" ng-reflect-centered="true" ng-reflect-disabled="false"></div><div class="mat-button-focus-overlay"></div></button></li>
										<li><button class="btn-main-ripple mat-icon-button" mat-icon-button=""><span class="mat-button-wrapper"><i class="icon-heart"></i></span><div class="mat-button-ripple mat-ripple mat-button-ripple-round" matripple="" ng-reflect-trigger="[object HTMLButtonElement]" ng-reflect-centered="true" ng-reflect-disabled="false"></div><div class="mat-button-focus-overlay"></div></button></li>
										<li><button class="btn-main-ripple mat-icon-button" mat-icon-button=""><span class="mat-button-wrapper"><i class="icon-zoom"></i></span><div class="mat-button-ripple mat-ripple mat-button-ripple-round" matripple="" ng-reflect-trigger="[object HTMLButtonElement]" ng-reflect-centered="true" ng-reflect-disabled="false"></div><div class="mat-button-focus-overlay"></div></button></li>
									</ul>
								</div>
								<div class="h_pro_desc">
									<p>Abominable Hoodie</p>
									<h4>$40.00</h4>
								</div>
							</div>
						</li>
						<li>
							<div class="product-box">
								<div class="h_pro_img">
									<img src="https://d2vltvjwlghbux.cloudfront.net/frontend/assets/template/images/pro_7.jpg">
									<ul class="home_product_action">
										<li><button class="btn-main-ripple mat-icon-button" mat-icon-button=""><span class="mat-button-wrapper"><i class="icon-cart"></i></span><div class="mat-button-ripple mat-ripple mat-button-ripple-round" matripple="" ng-reflect-trigger="[object HTMLButtonElement]" ng-reflect-centered="true" ng-reflect-disabled="false"></div><div class="mat-button-focus-overlay"></div></button></li>
										<li><button class="btn-main-ripple mat-icon-button" mat-icon-button=""><span class="mat-button-wrapper"><i class="icon-heart"></i></span><div class="mat-button-ripple mat-ripple mat-button-ripple-round" matripple="" ng-reflect-trigger="[object HTMLButtonElement]" ng-reflect-centered="true" ng-reflect-disabled="false"></div><div class="mat-button-focus-overlay"></div></button></li>
										<li><button class="btn-main-ripple mat-icon-button" mat-icon-button=""><span class="mat-button-wrapper"><i class="icon-zoom"></i></span><div class="mat-button-ripple mat-ripple mat-button-ripple-round" matripple="" ng-reflect-trigger="[object HTMLButtonElement]" ng-reflect-centered="true" ng-reflect-disabled="false"></div><div class="mat-button-focus-overlay"></div></button></li>
									</ul>
								</div>
								<div class="h_pro_desc">
									<p>Abominable Hoodie</p>
									<h4>$29.00</h4>
								</div>
							</div>
						</li>
						<li>
							<div class="product-box">
								<div class="h_pro_img">
									<img src="https://d2vltvjwlghbux.cloudfront.net/frontend/assets/template/images/pro_8.jpg">
									<ul class="home_product_action">
										<li><button class="btn-main-ripple mat-icon-button" mat-icon-button=""><span class="mat-button-wrapper"><i class="icon-cart"></i></span><div class="mat-button-ripple mat-ripple mat-button-ripple-round" matripple="" ng-reflect-trigger="[object HTMLButtonElement]" ng-reflect-centered="true" ng-reflect-disabled="false"></div><div class="mat-button-focus-overlay"></div></button></li>
										<li><button class="btn-main-ripple mat-icon-button" mat-icon-button=""><span class="mat-button-wrapper"><i class="icon-heart"></i></span><div class="mat-button-ripple mat-ripple mat-button-ripple-round" matripple="" ng-reflect-trigger="[object HTMLButtonElement]" ng-reflect-centered="true" ng-reflect-disabled="false"></div><div class="mat-button-focus-overlay"></div></button></li>
										<li><button class="btn-main-ripple mat-icon-button" mat-icon-button=""><span class="mat-button-wrapper"><i class="icon-zoom"></i></span><div class="mat-button-ripple mat-ripple mat-button-ripple-round" matripple="" ng-reflect-trigger="[object HTMLButtonElement]" ng-reflect-centered="true" ng-reflect-disabled="false"></div><div class="mat-button-focus-overlay"></div></button></li>
									</ul>
								</div>
								<div class="h_pro_desc">
									<p>Abominable Hoodie</p>
									<h4>$38.00</h4>
								</div>
							</div>
						</li>
						<li>
							<div class="product-box">
								<div class="h_pro_img">
									<img src="https://d2vltvjwlghbux.cloudfront.net/frontend/assets/template/images/pro_9.jpg">
									<ul class="home_product_action">
										<li><button class="btn-main-ripple mat-icon-button" mat-icon-button=""><span class="mat-button-wrapper"><i class="icon-cart"></i></span><div class="mat-button-ripple mat-ripple mat-button-ripple-round" matripple="" ng-reflect-trigger="[object HTMLButtonElement]" ng-reflect-centered="true" ng-reflect-disabled="false"></div><div class="mat-button-focus-overlay"></div></button></li>
										<li><button class="btn-main-ripple mat-icon-button" mat-icon-button=""><span class="mat-button-wrapper"><i class="icon-heart"></i></span><div class="mat-button-ripple mat-ripple mat-button-ripple-round" matripple="" ng-reflect-trigger="[object HTMLButtonElement]" ng-reflect-centered="true" ng-reflect-disabled="false"></div><div class="mat-button-focus-overlay"></div></button></li>
										<li><button class="btn-main-ripple mat-icon-button" mat-icon-button=""><span class="mat-button-wrapper"><i class="icon-zoom"></i></span><div class="mat-button-ripple mat-ripple mat-button-ripple-round" matripple="" ng-reflect-trigger="[object HTMLButtonElement]" ng-reflect-centered="true" ng-reflect-disabled="false"></div><div class="mat-button-focus-overlay"></div></button></li>
									</ul>
								</div>
								<div class="h_pro_desc">
									<p>Abominable Hoodie</p>
									<h4>$40.00</h4>
								</div>
							</div>
						</li>
					</ul>
				</div>
			</section>
			<section *ngIf="!isCMS && product_list.length"> 
				<div class="container container-lg">
					<h2 class="pro_title">{{widget_data.heading_text}}</h2>
					<ul class="product-list home">
						<li *ngFor="let product of product_list">

							<div class="product-box" [routerLink]="['/product/'+product.slug]">
								<div class="h_pro_img">
									<img *ngIf="product.cover_img" [src]="S3_URL_PRODUCT+product.cover_img">
									<img *ngIf="!product.cover_img" [src]="'https://d2vltvjwlghbux.cloudfront.net/frontend/assets/images/img1.jpg'">
									<div class="outs" *ngIf="product.stock<1 && _globalService.getFrontedWebsiteId()==1"><span>{{ 'GLOBAL.out_of_stock' | translate }}</span></div>
								</div>
								<div class="h_pro_desc">
									<p *ngIf="(lang_code=='th')">{{ ((product.name_th!='' && product.name_th!=null)?product.name_th:product.name) | limitTo:70 }}</p>
									<p *ngIf="(lang_code=='en')">{{ product.name | limitTo:70 }}</p>
									
									<h4 *ngIf="(product.discount | json) == '{}'; else discountCond">{{_globalService.getCurrencySymbol()}}{{ _globalService.exchangeRate(product.default_price,product.price_marketplace) | number:'1.2-2' }}</h4>
									<ng-template #discountCond>
									<h4>
										<del>{{_globalService.getCurrencySymbol()}}{{ _globalService.exchangeRate(product.default_price,product.price_marketplace) | number:'1.2-2' }}</del>
										{{_globalService.getCurrencySymbol()}}{{ _globalService.exchangeRate(_globalService.calculateProductDiscount(product.discount.disc_type,product.discount.amount,product.default_price),product.price_marketplace) | number:'1.2-2' }}
										<span class="dis">({{product.discount.name}})</span>
									</h4>
									</ng-template>
									<div class="rating_box" *ngIf="product.review_dict.avg_rating>0">
										<rating [(ngModel)]="product.review_dict.avg_rating" name="review_star" [readonly]="true"></rating>
										 <span class="rev">{{ product.review_dict.total_reviews }}  </span>
										<div class="clear"></div>
									</div>
								</div>
							</div>
							<ul class="home_product_action">
							<li><button mat-icon-button class="btn-main-ripple" matTooltip="{{ 'GLOBAL.add_to_cart' | translate }}" (click)="_shoppingCartService.addProductToCart(product, 1)" [disabled]="product.stock<1"><i class="icon-cart"></i></button></li>
							<li><button mat-icon-button class="btn-main-ripple" matTooltip="{{ 'GLOBAL.add_to_wishlist' | translate }}" (click)="_shoppingCartService.addToWishlist(product)"><i class="icon-heart"></i></button></li>
							<li><button mat-icon-button class="btn-main-ripple" matTooltip="{{ 'GLOBAL.view_details' | translate }}" [routerLink]="['/product/'+product.slug]"><i class="icon-zoom"></i></button></li>
							</ul>
						</li>
						
					</ul>
				</div>  
			</section>
	`,
})
export class BestSellerProductComponent implements WidgetComponent, OnInit {

	@Input() data: any;
	@Input() page_data: any;
	@Input() isCMS: boolean = false;

	public product_list: any = [];
	public widget_data: any = {};
	public S3_URL_PRODUCT: string;
	public lang_code: string;
	constructor(private _global: Global, private _globalService: GlobalService, public _shoppingCartService: ShoppingCartService, private _cookieService: CookieService) {

	let globalData = this._cookieService.getObject('globalData');
	if (globalData['lang_code']) {
		this.lang_code = globalData['lang_code'];
	}

	this._globalService.langChange$.subscribe(value => {
		this.lang_code = value;
	});
	}

	ngOnInit() {


	for (var i = 0; i < this.data.length; i++) {


		for (var j = 0; j < this.data[i].properties.length; j++) {


		this.widget_data[this.data[i].properties[j].selector] = this.data[i].properties[j].value;
		}
	}

	if (!this.isCMS) {
		this.S3_URL_PRODUCT = GlobalVariable.S3_URL + 'product/400x400/';
		this.loadProducts();
	}

	}

	loadProducts() {

	this._global.getBestSaleProducts().subscribe(
		data => {
		if (data.status) {
			this.product_list = data.api_status;
		}
		},
		err => {
		this._globalService.showToast('Something went wrong. Please try again.');
		},
		function () {
		//completed callback
		}
	);
	}
}


@Component({
	template: `
			<section>
				<div class="container container-lg strongbold" [innerHTML]="widget_data.html_text  | safeHtml"></div>  
			</section>
	`,
})
export class FreeTextComponent implements WidgetComponent, OnInit {

	@Input() data: any;
	@Input() page_data: any;
	@Input() isCMS: boolean = false;
	constructor() {

	}

	public widget_data: any = {};
	ngOnInit() {


	for (var i = 0; i < this.data.length; i++) {

		for (var j = 0; j < this.data[i].properties.length; j++) {


		this.widget_data[this.data[i].properties[j].selector] = this.data[i].properties[j].value;
		}
	}



	}
}


@Component({
	template: `
				<section>
					<div class="container container-lg">
						<div class="row">
							<div class="col-12 col-md-6">
								<h2>{{widget_data.heading_1}}</h2>
								<div [innerHTML]="widget_data.html_text_1 | safeHtml"></div>
							</div>
							
							<div class="col-12 col-md-6">
								<h2>{{widget_data.heading_2}}</h2>
								<div [innerHTML]="widget_data.html_text_2 | safeHtml"></div>
							</div>
						</div>
					</div>
				</section>
	`,
})
export class TwoColumnTextComponent implements WidgetComponent, OnInit {

	@Input() data: any;
	@Input() page_data: any;
	@Input() isCMS: boolean = false;
	constructor() {

	}

	public widget_data: any = {};
	ngOnInit() {

	for (var i = 0; i < this.data.length; i++) {

		for (var j = 0; j < this.data[i].properties.length; j++) {

		this.widget_data[this.data[i].properties[j].selector] = this.data[i].properties[j].value;
		}
	}

	}
}

@Component({
	template: `
				<section>
					<div class="container container-lg">
						<div class="row">
							<div class="col-12 col-md-4">
							<h2>{{widget_data.heading_1}}</h2>
							<div [innerHTML]="widget_data.html_text_1 | safeHtml"></div>
							</div>
							
							<div class="col-12 col-md-4">
							<h2>{{widget_data.heading_2}}</h2>
							<div [innerHTML]="widget_data.html_text_2 | safeHtml"></div>  
							</div>

							<div class="col-12 col-md-4">
							<h2>{{widget_data.heading_3}}</h2>
							<div [innerHTML]="widget_data.html_text_3 | safeHtml"></div>
							</div>
						</div>
					</div>
				</section>
	`,
})
export class ThreeColumnTextComponent implements WidgetComponent, OnInit {

	@Input() data: any;
	@Input() page_data: any;
	@Input() isCMS: boolean = false;
	constructor() {

	}

	public widget_data: any = {};
	ngOnInit() {

	for (var i = 0; i < this.data.length; i++) {

		for (var j = 0; j < this.data[i].properties.length; j++) {

		this.widget_data[this.data[i].properties[j].selector] = this.data[i].properties[j].value;
		}
	}

	}
}


@Component({
	template: `
				<section>
					<div class="container container-lg">
						<div class="row gutter50">
							<div class="col-12 col-md-auto" [class.order-1]="widget_data.img_align=='right' || widget_data.img_align=='Right'">
							 <div class="img-box singel">
								 <img src="{{widget_data.img}}" alt="{{widget_data.img_alt}}">
							 </div>
							</div>
							<div class="col">
								<h2>{{widget_data.heading}}</h2>
								<div [innerHTML]="widget_data.desc_text | safeHtml"></div>
							</div>
						</div>
					</div>
				</section>
	`,
})
export class ImageWithTextComponent implements WidgetComponent, OnInit {

	@Input() data: any;
	@Input() page_data: any;
	@Input() isCMS: boolean = false;
	constructor() {

	}

	public widget_data: any = {};
	ngOnInit() {

	for (var i = 0; i < this.data.length; i++) {

		for (var j = 0; j < this.data[i].properties.length; j++) {

		this.widget_data[this.data[i].properties[j].selector] = this.data[i].properties[j].value;
		}
	}

	}
}


@Component({
	template: `
				<section>
					<div class="container container-lg">
						<div class="row gutter50">
							<div class="col-sm-6">
								<div class="catagory1">
									<a [attr.href]="(this.isCMS)?'javascript:void(0)':widget_data.box1_link">
										<div class="img-part"><img src="{{widget_data.box1_img}}" alt="{{widget_data.box1_alt}}"></div>
									</a>
								</div>
							</div>
							<div class="col-sm-6">
								<div class="catagory1">
									<a [attr.href]="(this.isCMS)?'javascript:void(0)':widget_data.box2_link">
										<div class="img-part"><img src="{{widget_data.box2_img}}" alt="{{widget_data.box2_alt}}"></div>
									</a>
								</div>
							</div>
						</div>
					</div>    
				</section>
	`,
})
export class TwoSideBannerComponent implements WidgetComponent, OnInit {

	@Input() data: any;
	@Input() page_data: any;
	@Input() isCMS: boolean = false;
	constructor() {

	}

	public widget_data: any = {};
	ngOnInit() {

	for (var i = 0; i < this.data.length; i++) {

		for (var j = 0; j < this.data[i].properties.length; j++) {

		this.widget_data[this.data[i].properties[j].selector] = this.data[i].properties[j].value;
		}
	}

	}
}

@Component({
	template: `
				<div class="container container-lg">
					<h2 class="page_title">{{widget_data.heading_text}}</h2>
				</div>
	`,
})
export class HeadingTextComponent implements WidgetComponent, OnInit {

	@Input() data: any;
	@Input() page_data: any;
	@Input() isCMS: boolean = false;
	constructor() {

	}

	public widget_data: any = {};
	ngOnInit() {

	for (var i = 0; i < this.data.length; i++) {

		for (var j = 0; j < this.data[i].properties.length; j++) {

		this.widget_data[this.data[i].properties[j].selector] = this.data[i].properties[j].value;
		}
	}

	}
}



@Component({
	template: `
				<section class="product-intro">
				<div class="container">
					<div class="row">
					<div class="col-sm-6">
						<div class="mobilepadd">
						<h2>{{widget_data.heading}}</h2>
						<h3>{{widget_data.sub_heading}}</h3>
						<div [innerHTML]="widget_data.description | safeHtml"></div>
						<a [attr.href]="(this.isCMS)?'javascript:void(0)':widget_data.button_link">
						<button mat-button class="btn-main-line"><i class="icon-add"></i> {{widget_data.button_text}}</button>
						</a>
					</div>
					</div>
					<div class="col-sm-6">
						<img src="{{widget_data.box_img}}" alt="Image" title="Image">
					</div>
					</div>
				</div>
				</section>
				
	`,
})
export class IntroComponent implements WidgetComponent, OnInit {

	@Input() data: any;
	@Input() page_data: any;
	@Input() isCMS: boolean = false;
	constructor() {

	}

	public widget_data: any = {};
	ngOnInit() {

	for (var i = 0; i < this.data.length; i++) {

		for (var j = 0; j < this.data[i].properties.length; j++) {

		this.widget_data[this.data[i].properties[j].selector] = this.data[i].properties[j].value;
		}
	}

	}
}


@Component({
	template: `
				<section class="about-section">
				<div class="container">
					<div class="row">
					<div class="col-sm-6">
						<div class="smallbanner mb-30">
						<a [attr.href]="(this.isCMS)?'javascript:void(0)':widget_data.box1_img_url">
							<img src="{{widget_data.box1_img}}" alt="image">
						</a>
						</div>
						<div class="bigbanner">
						<a [attr.href]="(this.isCMS)?'javascript:void(0)':widget_data.box2_img_url">
							<img src="{{widget_data.box2_img}}" alt="image">
						</a>
						</div>
					</div>
					<div class="col-sm-6">
						<div class="bigbanner mb-30">
						<div class="about-padding">
							<h2>{{widget_data.box_heading}}</h2>
							<div [innerHTML]="widget_data.box_description | safeHtml"></div>
							<a [attr.href]="(this.isCMS)?'javascript:void(0)':widget_data.btn_link">
							<button mat-button class="btn-main-line text-uppercase">{{widget_data.btn_text}}</button>
							</a>  
						</div>
						</div>
						<div class="smallbanner">
						<a [attr.href]="(this.isCMS)?'javascript:void(0)':widget_data.box3_img_url">
							<img src="{{widget_data.box3_img}}" alt="image">
						</a>
						</div>
					</div>
					</div>

				</div>  
				</section>
				
	`,
})
export class AboutSectionComponent implements WidgetComponent, OnInit {

	@Input() data: any;
	@Input() page_data: any;
	@Input() isCMS: boolean = false;
	constructor() {

	}

	public widget_data: any = {};
	ngOnInit() {

	for (var i = 0; i < this.data.length; i++) {

		for (var j = 0; j < this.data[i].properties.length; j++) {

		this.widget_data[this.data[i].properties[j].selector] = this.data[i].properties[j].value;
		}
	}

	}
}



@Component({
	templateUrl: './form-template.html',
})
export class FormComponent implements WidgetComponent, OnInit {

	@Input() data: any;
	@Input() page_data: any;
	@Input() isCMS: boolean = false;
	constructor(private _global: Global, private _router: Router, private _globalService: GlobalService) { }
	public formModel: any = {};
	public widget_data: any = {};
	ngOnInit() {

	this.widget_data = this.data[0];
	this.widget_data.fields.forEach(field => {


		if ((field.input_type == 'Checkbox' || field.input_type == 'Radio' || field.input_type == 'Dropdown') && typeof field.custom_values == 'string' && field.custom_values && field.custom_values != null && field.custom_values != '') {


		let custom_values: any = field.custom_values.split(',');
		field.custom_values = [];
		field.custom_values = custom_values;
		}

	});

	}

	doFormSubmit(form: any) {

	let form_data: any = {};
	form_data['company_website_id'] = this._globalService.getFrontedWebsiteId();
	form_data['page_name'] = this.page_data.page_name;
	form_data['page_id'] = this.page_data.page_id;
	form_data['form_data'] = JSON.stringify(form.value);
	this._global.cmsFormSubmit(form_data).subscribe(
		data => {
		this._router.navigate([this.widget_data.submit_url]);
		},
		err => {
		this._globalService.showToast('Something went wrong. Please try again.');
		},
		function () {
		//completed callback
		}
	);
	}

	doFormReset(form: any) {
	form.reset();
	}
}



///////// Newsletter ///////////////////


@Component({
	template: `
				<table cellpadding="0" cellspacing="0" width="100%" border="0">
					<tr>
						<td>
							<table cellpadding="0" cellspacing="0" width="600" border="0">
								<tr>
									<td style="padding:5px 0px;">
									<a class="disable-pointer" [attr.href]="widget_data.banner_link+'[[token]]'">
										<img alt="{{widget_data.banner_alt}}" src="{{widget_data.banner_url}}" width="100%" height="auto">
									</a>  
									</td>
								</tr>
							</table>    
						</td>
					</tr>
				</table>
	`,
})
export class EmailBannerComponent implements WidgetComponent, OnInit {

	@Input() data: any;
	@Input() page_data: any;
	@Input() isCMS: boolean = false;
	constructor() {

	}

	public widget_data: any = {};
	ngOnInit() {

	for (var i = 0; i < this.data.length; i++) {

		for (var j = 0; j < this.data[i].properties.length; j++) {

		this.widget_data[this.data[i].properties[j].selector] = this.data[i].properties[j].value;
		}
	}

	}
}


@Component({
	template: `


<table cellpadding="0" cellspacing="0" width="100%" border="0">
	<tr>
		<td>
			<table cellpadding="0" cellspacing="0" width="300" border="0" style="float: left;">
				<tr>
					<td style="padding:5px 5px 5px 0;">
						<a class="disable-pointer" [attr.href]="widget_data.box1_link+'[[token]]'">
						<img src="{{widget_data.box1_img}}" alt="{{widget_data.box1_alt}}" width="100%" height="auto" >
						</a>  
					</td>
				</tr>
			</table>
			<table cellpadding="0" cellspacing="0" width="300" border="0" style="float: right;">
				<tr>
					<td style="padding:5px 0 5px 5px;">
						<a class="disable-pointer" [attr.href]="widget_data.box2_link+'[[token]]'">
						<img src="{{widget_data.box2_img}}" alt="{{widget_data.box2_alt}}" width="100%" height="auto" >
						</a>  
					</td>
				</tr>
			</table>    
		</td>
	</tr>
</table>


	`,
})
export class EmailTwoSideBannerComponent implements WidgetComponent, OnInit {

	@Input() data: any;
	@Input() page_data: any;
	@Input() isCMS: boolean = false;
	constructor() {

	}

	public widget_data: any = {};
	ngOnInit() {

	for (var i = 0; i < this.data.length; i++) {

		for (var j = 0; j < this.data[i].properties.length; j++) {

		this.widget_data[this.data[i].properties[j].selector] = this.data[i].properties[j].value;
		}
	}

	}
}

@Component({
	template: `

<table cellpadding="0" cellspacing="0" width="100%" border="0">
	<tr>
		<td>
			<table cellpadding="0" cellspacing="0" width="600" border="0">
				<tr>
					<td style="padding:15px 0px;" >
						<h1 style="text-align: center;">{{widget_data.heading_text}}</h1>
					</td>
				</tr>
			</table>    
		</td>
	</tr>
</table>

	`,
})
export class EmailHeadingTextComponent implements WidgetComponent, OnInit {

	@Input() data: any;
	@Input() page_data: any;
	@Input() isCMS: boolean = false;
	constructor() {

	}

	public widget_data: any = {};
	ngOnInit() {

	for (var i = 0; i < this.data.length; i++) {

		for (var j = 0; j < this.data[i].properties.length; j++) {

		this.widget_data[this.data[i].properties[j].selector] = this.data[i].properties[j].value;
		}
	}

	}
}


@Component({
	template: `

<table cellpadding="0" cellspacing="0" width="100%" border="0">
	<tr>
		<td style="padding: 15px 10px;background:#f7f7f7" valign="middle">
			<table cellpadding="0" cellspacing="0" width="290" border="0" [style.float]="(widget_data.img_align=='right' || widget_data.img_align=='Right')?'right':'left'">
				<tr>
					<td style="padding:5px;" align="left" valign="middle">
						<img src="{{widget_data.img}}" alt="{{widget_data.img_alt}}" width="100%" height="auto" >
					</td>
				</tr>
			</table>
			<table cellpadding="0" cellspacing="0" width="290" border="0" style="float: right;">
				<tr>
					<td style="padding:5px;">
						<h3 style="color: #444">{{widget_data.heading}}</h3>
						<p style="font-size: 14px;color: #444" [innerHTML]="widget_data.desc_text | safeHtml"></p>
					</td>
				</tr>
			</table>    
		</td>
	</tr>
</table> 


	`,
})
export class EmailImageWithTextComponent implements WidgetComponent, OnInit {

	@Input() data: any;
	@Input() page_data: any;
	@Input() isCMS: boolean = false;
	constructor() {

	}

	public widget_data: any = {};
	ngOnInit() {

	for (var i = 0; i < this.data.length; i++) {

		for (var j = 0; j < this.data[i].properties.length; j++) {

		this.widget_data[this.data[i].properties[j].selector] = this.data[i].properties[j].value;
		}
	}

	}
}


@Component({
	template: `

<table cellpadding="0" cellspacing="0" width="100%" border="0">
	<tr>
		<td>
			<table cellpadding="0" cellspacing="0" width="300" border="0" style="float: left;">
				<tr>
					<td style="padding:5px 5px 5px 0;">
						<a class="disable-pointer" [attr.href]="widget_data.box1_link+'[[token]]'">
						<div style="border: #CCC solid 1px;">
							<img src="{{widget_data.box1_img}}" width="100%" height="auto" >
							<div style="padding:10px 10px 0;">
								<h4 style="color: #444">{{widget_data.box1_heading}}</h4>
								<p style="font-size: 14px;color: #444">{{widget_data.box1_desc}}</p>
							</div>
						</div>
						</a>  
					</td>
				</tr>
			</table>
			<table cellpadding="0" cellspacing="0" width="300" border="0" style="float: right;">
				<tr>
					<td style="padding:5px 0 5px 5px;">
						<a class="disable-pointer" [attr.href]="widget_data.box2_link+'[[token]]'">
						<div style="border: #CCC solid 1px;">
							<img src="{{widget_data.box2_img}}" width="100%" height="auto" >
							<div style="padding:10px 10px 0;">
								<h4 style="color: #444">{{widget_data.box2_heading}}</h4>
								<p style="font-size: 14px;color: #444">{{widget_data.box2_desc}}</p>
							</div>
						</div>
						</a>  
					</td>
				</tr>
			</table>    
		</td>
	</tr>
</table>


	`,
})
export class EmailImageWithTwoTextComponent implements WidgetComponent, OnInit {

	@Input() data: any;
	@Input() page_data: any;
	@Input() isCMS: boolean = false;
	constructor() {

	}

	public widget_data: any = {};
	ngOnInit() {

	for (var i = 0; i < this.data.length; i++) {

		for (var j = 0; j < this.data[i].properties.length; j++) {

		this.widget_data[this.data[i].properties[j].selector] = this.data[i].properties[j].value;
		}
	}

	}
}


@Component({
	template: `


<table cellpadding="0" cellspacing="0" width="100%" border="0">
	<tr>
		<td style="padding: 15px 10px;background:#f7f7f7" valign="middle">
			<table cellpadding="0" cellspacing="0" width="100%" border="0" style="float: right;">
				<tr>
					<td style="padding:5px 0 5px 5px;" class="0-0 container inserted">
						{{widget_data.html_text}}
					</td>
				</tr>
			</table>    
		</td>
	</tr>
</table>

	`,
})
export class EmailFreeTextComponent implements WidgetComponent, OnInit {

	@Input() data: any;
	@Input() page_data: any;
	@Input() isCMS: boolean = false;
	constructor() {

	}

	public widget_data: any = {};
	ngOnInit() {

	for (var i = 0; i < this.data.length; i++) {

		for (var j = 0; j < this.data[i].properties.length; j++) {

		this.widget_data[this.data[i].properties[j].selector] = this.data[i].properties[j].value;
		}
	}



	}
}


@Component({
	template: `

<table cellpadding="0" cellspacing="0" width="100%" border="0">
	<tr>
		<td style="padding: 15px 10px;" valign="middle">
			<table cellpadding="0" cellspacing="0" width="290" border="0" style="float: left;">
				<tr>
					<td style="padding:5px 0 5px 5px;">
						<h3 style="color: #444">{{widget_data.heading_1}}</h3>
						<p style="font-size: 14px;color: #444" [innerHTML]="widget_data.html_text_1 | safeHtml"></p>
					</td>
				</tr>
			</table>
			<table cellpadding="0" cellspacing="0" width="290" border="0" style="float: right;">
				<tr>
					<td style="padding:5px 0 5px 5px;">
						<h3 style="color: #444">{{widget_data.heading_2}}</h3>
						<p style="font-size: 14px;color: #444" [innerHTML]="widget_data.html_text_2 | safeHtml"></p>
					</td>
				</tr>
			</table>    
		</td>
	</tr>
</table>

	`,
})
export class EmailTwoColumnTextComponent implements WidgetComponent, OnInit {

	@Input() data: any;
	@Input() page_data: any;
	@Input() isCMS: boolean = false;
	constructor() {

	}

	public widget_data: any = {};
	ngOnInit() {

	for (var i = 0; i < this.data.length; i++) {

		for (var j = 0; j < this.data[i].properties.length; j++) {

		this.widget_data[this.data[i].properties[j].selector] = this.data[i].properties[j].value;
		}
	}

	}
}

@Component({
	template: `

<table cellpadding="0" cellspacing="0" width="100%" border="0">
	<tr>
	<td>
		<table cellpadding="0" cellspacing="0" width="100%" border="0">
		<tr>
			<td style="padding:5px 5px 5px 0;">
			<div style="border: #CCC solid 1px;">
				<img src="{{widget_data.product1_img}}" alt="{{widget_data.product1_name}}" width="100%" height="auto" >
				<div style="padding:10px; text-align: center;">
				<h4 style="color: #444;text-align: center;">{{widget_data.product1_name}}</h4>
				<del style="text-decoration: line-through;" *ngIf="widget_data.product1_old_price">{{widget_data.product1_old_price}}</del> &nbsp;<strong>{{widget_data.product1_price}}</strong>
				</div>
			</div>
			</td>

			<td style="padding:5px 0 5px 5px;">
			<div style="border: #CCC solid 1px;">
				<img src="{{widget_data.product2_img}}" alt="{{widget_data.product2_name}}" width="100%" height="auto" >
				<div style="padding:10px; text-align: center;">
				<h4 style="color: #444;text-align: center;">{{widget_data.product2_name}}</h4>
				<del style="text-decoration: line-through;" *ngIf="widget_data.product2_old_price">{{widget_data.product2_old_price}}</del> &nbsp;<strong>{{widget_data.product2_price}}</strong>
				</div>
			</div>
			</td>
		</tr>
		</table>  
	</td>
	</tr>
</table>

	`,
})
export class EmailTwoProductComponent implements WidgetComponent, OnInit {

	@Input() data: any;
	@Input() page_data: any;
	@Input() isCMS: boolean = false;
	constructor() {

	}

	public widget_data: any = {};
	ngOnInit() {

	for (var i = 0; i < this.data.length; i++) {

		for (var j = 0; j < this.data[i].properties.length; j++) {

		this.widget_data[this.data[i].properties[j].selector] = this.data[i].properties[j].value;
		}
	}

	}
}


@Component({
	template: `

<table cellpadding="0" cellspacing="0" width="100%" border="0">
	<tr>
	<td>
		<table cellpadding="0" cellspacing="0" width="600" border="0">
		<tr>
			<td style="padding:15px 0px;" >
			<div [ngStyle]="{'width':'100%', 'height': widget_data.height+'px', 'background':widget_data.colorcode }"></div>
			</td>
		</tr>
		</table>  
	</td>
	</tr>
</table>

	`,
})
export class EmailSeparatorComponent implements WidgetComponent, OnInit {

	@Input() data: any;
	@Input() page_data: any;
	@Input() isCMS: boolean = false;
	constructor() {

	}

	public widget_data: any = {};
	ngOnInit() {

	for (var i = 0; i < this.data.length; i++) {

		for (var j = 0; j < this.data[i].properties.length; j++) {

		this.widget_data[this.data[i].properties[j].selector] = this.data[i].properties[j].value;
		}
	}


	}
}


@Component({
	template: `

<table cellpadding="0" cellspacing="0" width="100%" border="0">
	<tr>
	<td>
		<table cellpadding="0" cellspacing="0" width="100%" border="0">
		<tr>
			<td style="padding:5px 5px 5px 0;">
			<div style="border: #CCC solid 1px;">
				<img src="{{widget_data.product1_img}}" alt="{{widget_data.product1_name}}" width="100%" height="auto" >
				<div style="padding:10px; text-align: center;">
				<h4 style="color: #444;text-align: center;">{{widget_data.product1_name}}</h4>
				<del style="text-decoration: line-through;" *ngIf="widget_data.product1_old_price">{{widget_data.product1_old_price}}</del> &nbsp;<strong>{{widget_data.product1_price}}</strong>
				</div>
			</div>
			</td>

			<td style="padding:5px 0 5px 5px;">
			<div style="border: #CCC solid 1px;">
				<img src="{{widget_data.product2_img}}" alt="{{widget_data.product2_name}}" width="100%" height="auto" >
				<div style="padding:10px; text-align: center;">
				<h4 style="color: #444;text-align: center;">{{widget_data.product2_name}}</h4>
				<del style="text-decoration: line-through;" *ngIf="widget_data.product2_old_price">{{widget_data.product2_old_price}}</del> &nbsp;<strong>{{widget_data.product2_price}}</strong>
				</div>
			</div>
			</td>
		</tr>
		</table> 
		<table cellpadding="0" cellspacing="0" width="100%" border="0">
		<tr>
			<td style="padding:5px 5px 5px 0;">
			<div style="border: #CCC solid 1px;">
				<img src="{{widget_data.product3_img}}" alt="{{widget_data.product3_name}}" width="100%" height="auto" >
				<div style="padding:10px; text-align: center;">
				<h4 style="color: #444;text-align: center;">{{widget_data.product3_name}}</h4>
				<del style="text-decoration: line-through;" *ngIf="widget_data.product3_old_price">{{widget_data.product3_old_price}}</del> &nbsp;<strong>{{widget_data.product3_price}}</strong>
				</div>
			</div>
			</td>

			<td style="padding:5px 0 5px 5px;">
			<div style="border: #CCC solid 1px;">
				<img src="{{widget_data.product4_img}}" alt="{{widget_data.product4_name}}" width="100%" height="auto" >
				<div style="padding:10px; text-align: center;">
				<h4 style="color: #444;text-align: center;">{{widget_data.product4_name}}</h4>
				<del style="text-decoration: line-through;" *ngIf="widget_data.product4_old_price">{{widget_data.product4_old_price}}</del> &nbsp;<strong>{{widget_data.product4_price}}</strong>
				</div>
			</div>
			</td>
		</tr>
		</table> 
	</td>
	</tr>
</table>

	`,
})
export class EmailFourProductComponent implements WidgetComponent, OnInit {

	@Input() data: any;
	@Input() page_data: any;
	@Input() isCMS: boolean = false;
	constructor() {

	}

	public widget_data: any = {};
	ngOnInit() {

	for (var i = 0; i < this.data.length; i++) {

		for (var j = 0; j < this.data[i].properties.length; j++) {

		this.widget_data[this.data[i].properties[j].selector] = this.data[i].properties[j].value;
		}
	}

	}
}


@Component({
	template: `

<table cellpadding="0" cellspacing="0" width="100%" border="0">
	<tr>
	<td>
		<table cellpadding="0" cellspacing="0" width="600" border="0">
		<tr>
			<td style="padding:20px 0px;" align="center">
			<a class="disable-pointer" [attr.href]="widget_data.action_link+'[[token]]'">
				<button [ngStyle]="{'background': widget_data.bg_colorcode, 'color': widget_data.text_colorcode, 'border-radius': widget_data.round_px+'px','border': 'none', 'padding': '10px 20px'}">{{widget_data.btn_text}}</button>
			</a>
			</td>
		</tr>
		</table>  
	</td>
	</tr>
</table>

	`,
})
export class EmailButtonComponent implements WidgetComponent, OnInit {

	@Input() data: any;
	@Input() page_data: any;
	@Input() isCMS: boolean = false;
	constructor() {

	}

	public widget_data: any = {};
	ngOnInit() {

	for (var i = 0; i < this.data.length; i++) {

		for (var j = 0; j < this.data[i].properties.length; j++) {

		this.widget_data[this.data[i].properties[j].selector] = this.data[i].properties[j].value;
		}
	}


	}
}


@Component({
	template: `

<table cellpadding="0" cellspacing="0" width="100%" border="0">
	<tr>
	<td>
		<table cellpadding="0" cellspacing="0" width="600" border="0">
		<tr>
			<td style="padding:20px 0px;" align="center">
			<a class="disable-pointer" [attr.href]="widget_data.action_link1+'[[token]]'">
				<button [ngStyle]="{'background': widget_data.bg_colorcode1, 'color': widget_data.text_colorcode1, 'border-radius': widget_data.round_px1+'px','border': 'none', 'padding': '10px 20px'}">{{widget_data.btn_text1}}</button>
			</a>
			</td>
			<td style="padding:20px 0px;" align="center">
			<a class="disable-pointer" [attr.href]="widget_data.action_link2+'[[token]]'">
				<button [ngStyle]="{'background': widget_data.bg_colorcode2, 'color': widget_data.text_colorcode2, 'border-radius': widget_data.round_px2+'px','border': 'none', 'padding': '10px 20px'}">{{widget_data.btn_text2}}</button>
			</a>
			</td>
		</tr>
		</table>  
	</td>
	</tr>
</table>

	`,
})
export class EmailButtonTwoComponent implements WidgetComponent, OnInit {

	@Input() data: any;
	@Input() page_data: any;
	@Input() isCMS: boolean = false;
	constructor() {

	}

	public widget_data: any = {};
	ngOnInit() {

	for (var i = 0; i < this.data.length; i++) {

		for (var j = 0; j < this.data[i].properties.length; j++) {

		this.widget_data[this.data[i].properties[j].selector] = this.data[i].properties[j].value;
		}
	}



	}
}

@Component({
	template: `
	<div class="middle_contain_wrap">
	<section>
		<div class="top_productrow">
			<div class="cus_container">
				<div class="row">
					<div class="col-12 col-lg-4" >
						<div class="top_productbox">
						<a class="disable-pointer" [attr.href]="widget_data.box1_img_url+'[[token]]'">
						<img src="{{widget_data.box1_img}}" width="100%" height="auto" >
						</a>  
						</div>
						</div>
						<div class="col-12 col-lg-4" >
						<div class="top_productbox">
						<a class="disable-pointer" [attr.href]="widget_data.box2_img_url+'[[token]]'">
						<img src="{{widget_data.box2_img}}" width="100%" height="auto" >
						</a>  
						</div>
						</div>
						<div class="col-12 col-lg-4" >
						<div class="top_productbox">
						<a class="disable-pointer" [attr.href]="widget_data.box3_img_url+'[[token]]'">
						<img src="{{widget_data.box3_img}}" width="100%" height="auto" >
						</a>  
						</div>
					</div>
				</div>
			</div>
		</div>
	</section>
	</div>

	`,
})
export class AllProductConditionWise implements WidgetComponent, OnInit {

	@Input() data: any;
	@Input() page_data: any;
	@Input() isCMS: boolean = false;
	constructor() {

	}

	public widget_data: any = {};
	ngOnInit() {

	for (var i = 0; i < this.data.length; i++) {

		for (var j = 0; j < this.data[i].properties.length; j++) {

		this.widget_data[this.data[i].properties[j].selector] = this.data[i].properties[j].value;
		}
	}
	}
}


@Component({
	template: `
			 
	 <section>
		<div class="cus_container">
			<div class="card_add_sec"><img src="{{widget_data.img}}"></div>
		</div>
		
	</section>
	`,
})
export class PaymentImage implements WidgetComponent, OnInit {

	@Input() data: any;
	@Input() page_data: any;
	@Input() isCMS: boolean = false;
	constructor() {

	}

	public widget_data: any = {};
	ngOnInit() {

	for (var i = 0; i < this.data.length; i++) {

		for (var j = 0; j < this.data[i].properties.length; j++) {

		this.widget_data[this.data[i].properties[j].selector] = this.data[i].properties[j].value;
		}
	}

	}
}
/**
 * Component for handle sale or deal products
*/
@Component({
	templateUrl : './templates/bestsellerordeals/bestsellerordeals.html',
	
})
export class BestSellOrDealProduct implements WidgetComponent,OnInit {
	 @Input() data:any;
	 @Input() page_data : any;
	 @Input() isCMS:boolean = false;

	public product_type:string = '';
	public widget_data:any = {};
	public saleorDealsData:any;
	public selectedVariantProduct;
	private S3_URL_PRDUCT = GlobalVariable.S3_URL+'product/200x200/';
	public objectkeys = Object.keys;
	public wishlist:any=[];
	public wishlist_ids:any=[];
	public savelist_data = [];
	public formModel:any={};

	 constructor(
	 	private _sellordeals:DealsorsellService,
	 	private _router:Router,
	 	public cartService:CartService,
		public _wareHouseService:WarehouseService,
		public _producrService:ProductService,
		public _globalService:GlobalService,
		private _global: Global,
		public authenticationService: AuthenticationService,
		private dialogsService: DialogsService,
		private translate: TranslateService,
		public dialog: MatDialog,
		public _menuservice:MenuService,
		
	) {
		
	}
	ngOnInit() {

		this._wareHouseService.warehouseData$.subscribe(response => {
			if(this.data && this.data.length > 0) {
				this.product_type = this.data[0]['product_type'];
				for (var i = 0; i < this.data.length; i++) {
					for (var j = 0; j < this.data[i].properties.length; j++) {
					 	this.widget_data[this.data[i].properties[j].selector] = this.data[i].properties[j].value;
					}
				}
			}
			/*console.log("*********** Product type *********");
			console.log(this.product_type);*/
			if(this.product_type == 'best_sell') {
				this.getSellsData();
			} else if(this.product_type == 'best_deals') {
				this.getDealsData();
			}
			
		});
	}
	 /**
	* Method for getting sells or deals data
	* @access public
	* @return void
	 */
	 getSellsData() {
	 this._sellordeals.getBestSellsOfTheDay().subscribe(response => {
		 if(response && response['status'] == 1) {

			this.saleorDealsData = this.formatProductData(response['data']);
			console.log("**************** Sales or deals data **************");
			console.log(this.saleorDealsData);
		 }

	 });

	 }
	 /**
	* Method for geting deals data
	* @access public
	* @return void
	 */
	 getDealsData() {
	 this._sellordeals.getBestDealsOFtheDay().subscribe(response => {
		 if(response && response['status'] == 1) {
		 let dealsData = response['data'];
		 
		 this.saleorDealsData = this.formatProductData(dealsData);
		}

	 });
	 }
	 /**
	* Method for formatting deals or sales data
	* @access public
	* @return array
	 */
	 formatProductData(saleorDealsData) {
	 if(saleorDealsData.length > 0) {
		 let i = 0;
		 saleorDealsData.forEach(productData => {
		 	try {
		 	 /*if(!productData['new_default_price_unit'] || productData['new_default_price_unit'] == 0) {
		 	 	throw "Invalid product price";
		 	 	

		 	 }*/
		 	 let tempProductData = [];
			 let cloneProductData = Object.assign({},productData);
			 delete cloneProductData.variant_product;
			 saleorDealsData[i]['selected_product'] = cloneProductData;
			 cloneProductData['is_parent'] = true;
			 tempProductData.push(cloneProductData);
			 if(productData.id){
				 productData.isSaveList=false;
			 }
			 if(productData['variant_product'].length > 0) {
				 tempProductData = tempProductData.concat(productData['variant_product']);
			 }
			 saleorDealsData[i]['variant_product'] = tempProductData;
			 i++;

		 	} catch(err){
		 		console.log(err);
			 
		    }
		  }
		 );
		 	
	 }
	 return saleorDealsData;
	 }
	/**
	* Method for navigate to details
	 */
	 navigateToDetails(slug) {
	 this._router.navigate(['/details/'+slug]);

	 }

	//  getting save list data after click on icon ....save-list
	getSaveList(product_id, add_new='n') {
		if(this.authenticationService.userFirstName) {
		  let data= {
			"website_id":this._globalService.getFrontedWebsiteId()
		  }
		  if(add_new == 'n') {
			this.saleorDealsData.map(x => {
			  if (x.id == product_id) {
				x.isSaveList = !x.isSaveList;
			  } else {
				x.isSaveList = false;
			  }
			});
		  }
	
		  this._global.getWebServiceData('save-list', 'GET', '', '').subscribe(data => {
			if (data.status == 1) {
			  this.savelist_data = data.data;
			  this.savelist_data.forEach(element => {
				var pro_ids=element.product_ids.replace (/"/g,'');
				if(pro_ids.includes(product_id)){
				  element.is_checked=1;
				} else {
				  // 
				}
			  });
			} else {
			  // console.log(data);
			  this._globalService.showToast('Somthing wen\'t wrong. Please try again'); 
			}
		  }, err => console.log(err), function() {});
	
		} else {
		//   this.openLoginDialog();
		if(!localStorage.getItem('currentUser')) {
			this._menuservice.signinSignuppopup$.next('sign-in');
			return false;
		}
		}
	}

	//  add and remove from save list....addremove-from-savelist
	addToSaveList(product_id:number, list_id:number, is_checked) {
	let action = 'add';
	if(is_checked) {
		action = 'del';
	}
	let post_data = {
		"website_id":this._globalService.getFrontedWebsiteId(),
		"product_id":product_id,
		"action": action,
		"list_id":list_id
	}
	if(this.authenticationService.userFirstName) {
		this._global.getWebServiceData('addremove-from-savelist', 'PUT', post_data, '').subscribe(data => {
		if (data.status == 200) {
		// this._globalService.showToast(data.message);
		} else {
		// console.log(data);
		this._globalService.showToast('Somthing wen\'t wrong. Please try again'); 
		}
		}, err => console.log(err), function() {});
	} else {
		// this.openLoginDialog();
		if(!localStorage.getItem('currentUser')) {
			this._menuservice.signinSignuppopup$.next('sign-in');
			return false;
		}
	}
	}
	//  Add new save list ....save-list
	addNewSaveList(i:number, product_id, savelist_name = '') {
		if(this.authenticationService.userFirstName) {
		  if(savelist_name == '') {
			this._globalService.showToast('Please enter savelist name'); 
		  } else {
			let data= {
			  "website_id":this._globalService.getFrontedWebsiteId(),
			  "product_id":product_id,
			  "name":savelist_name
			}
			this._global.getWebServiceData('save-list', 'POST', data, '').subscribe(data => {
			if (data.status == 200) {
			  this.getSaveList(product_id, 'y');
			  // this._globalService.showToast(data.message);
			} else {
			  // console.log(data);
			  this._globalService.showToast('Somthing wen\'t wrong. Please try again'); 
			}
			}, err => console.log(err), function() {});
		  }
		} else {
			//   this.openLoginDialog();
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
	
 }
/**
 * Component for subscription section
*/
@Component({
	templateUrl : './templates/subscribenewsletter/subscribenewsletter.html',
})
export class SubscribeNewsLetter implements WidgetComponent,OnInit {
	@Input() data:any;
	@Input() page_data:any;
	@Input() isCMS:boolean = false;
	public subscribeEmail;
	public widget_data:any = {};
	constructor(public _globalService:GlobalService) {
	}
	ngOnInit() {
		if(this.data && this.data.length > 0) {
			for (var i = 0; i < this.data.length; i++) {
				for (var j = 0; j < this.data[i].properties.length; j++) {
					this.widget_data[this.data[i].properties[j].selector] = this.data[i].properties[j].value;
				}
			}
		}
	}
	/**
	 * Method for subscribe to news letter
	 * @access public
	*/
	subscribeNewsLetter() {
		if(!this.subscribeEmail) {
			this._globalService.showToast("Please provide your email address");
			return;
		}
		this._globalService.showLoaderSpinner(true);
		this._globalService.subscribeToNewsLetter(this.subscribeEmail).subscribe(response => {
			this._globalService.showLoaderSpinner(false);
			if(response && response['status'] == 200) {
				let message = response['message'] ? response['message'] : 'You have successfully subscribe to news letter';
				this._globalService.showToast(message);
			}
			
		},
		error => {
			this._globalService.showLoaderSpinner(false);
			this._globalService.showToast("Something went wrong");

		}
		)
	
	}
}
/**
 * Component for OurFeature
*/
@Component({
	templateUrl : './templates/ourfeature/ourfeature.html',
})
export class OurFeature implements WidgetComponent,OnInit{
	@Input() data:any;
	@Input() page_data:any;
	@Input() isCMS:boolean = false;
	public widget_data:any = {};
	public widget_properties_data = [];
	constructor() {
	}
	ngOnInit() {
		if(this.data && this.data.length > 0) {
			for (var i = 0; i < this.data.length; i++) {
				for (var j = 0; j < this.data[i].properties.length; j++) {
				this.widget_data[this.data[i].properties[j].selector] = this.data[i].properties[j].value;
				}
			}
			this.widget_properties_data = this.data[0]['properties'];
		}
	}
}
/**
 * Component for category banner
*/
@Component({
	templateUrl:'./templates/banner/category_banner.html'
})
export class CategoryBanner implements WidgetComponent,OnInit{
	@Input() data:any;
	@Input() page_data:any;
	@Input() isCMS:boolean = false;
	public widget_data:any = {};
	public widget_properties_data = [];
	public widget_data_for_non_cms = [];
	public S3_URL_BANNER = GlobalVariable.S3_URL+'CategoryBanner/800x800';
	public selected_warehouse_id:number = 34;
	constructor(
		private _categoryService:CategoryService,
		private _gs:GlobalService,
		private _router:Router,
		@Inject(WINDOW) private _window: Window,
		public _warehouseService:WarehouseService
	) {
	}
	ngOnInit() {
		this._warehouseService.warehouseData$.subscribe(response => {
			this.selected_warehouse_id = response['selected_warehouse_id'];
			if(this.data && this.data.length > 0) {
				for (var i = 0; i < this.data.length; i++) {
					for (var j = 0; j < this.data[i].properties.length; j++) {
					this.widget_data[this.data[i].properties[j].selector] = this.data[i].properties[j].value;
					}
				 }

			 // Fetch all selected banner for normal pages
			 // This function has been implementd as there some checking made in backend regarding date
			if(!this.isCMS) {
				 this.loadBanner();
			}
			}
		});
	}
	loadBanner() {
		let selectedCategoryBrand = [];
		let categorySelectorList = ['category_banner_id_1','category_banner_id_2','category_banner_id_3'];
		for(let category in this.widget_data) {
			if(categorySelectorList.includes(category)) {
			selectedCategoryBrand.push(this.widget_data[category]);
			}

		}
		this.getBannerWhileForNonCms(selectedCategoryBrand,this.selected_warehouse_id);
	}
	/**
	 * Method for getting banner by banner option
	 * @access public
	*/
	getBannerByBannerId(bannerId,bannerOptions) {
		let selectedBanner = [];
		selectedBanner = bannerOptions.filter(bannerData => {
			if(bannerData['id'] == bannerId) {
				return bannerData;
			}
		});
		return selectedBanner.length > 0 ? selectedBanner[0] : {}; 
	}
	/**
	 * Method for getting banner when iscms is false
	 * @access public
	*/
	getBannerWhileForNonCms(selectedBannerId = [],warehouseId) {
		this._categoryService.getCategoryBannerByBannerId(selectedBannerId,'C',warehouseId).subscribe(bannerData => {
			if(bannerData && bannerData['status'] == 1) {
				this.widget_data_for_non_cms = bannerData['data'];
		 	}
		},
		function () {
			//completed callback
		})
	}
	/**
	 * Method for navigate to url
	 * @access public
	*/
	navigateToUrl(url) {
	 this._router.navigate([url]);
	}
}
/**
 * Component for Promotion Banner
*/
@Component({
	templateUrl:'./templates/banner/promotions_banner.html'

})
export class PromotionBanner implements WidgetComponent,OnInit{
	@Input() data:any;
	@Input() page_data:any;
	@Input() isCMS:boolean = false;
	public widget_data:any = {};
	public widget_properties_data = [];
	public widget_data_for_non_cms = [];
	public S3_URL_BANNER = GlobalVariable.S3_URL+'category_banner/800x800';
	constructor(
		private _categoryService:CategoryService,
		@Inject(WINDOW) private _window: Window,
		public _warehouseService:WarehouseService
	) {
	}
	ngOnInit() {
		this._warehouseService.warehouseData$.subscribe(response => {
			if(this.data && this.data.length > 0) {
			for (var i = 0; i < this.data.length; i++) {
				for (var j = 0; j < this.data[i].properties.length; j++) {
					this.widget_data[this.data[i].properties[j].selector] = this.data[i].properties[j].value;
				}
			 }
			 this.widget_properties_data = this.getFormattedCategoryBannerList(this.data[0]['properties']);
			 // Fetch all selected banner for normal pages
			 // This function has been implementd as there some checking made in backend regarding date
			 if(!this.isCMS) {
				 this.getBannerWhileForNonCms();
			 }
			}
		});
	}
	/**
	 * Method for fomatting category list
	 * @access public
	*/
	getFormattedCategoryBannerList(categoryBanerData = []) {
		if(categoryBanerData.length == 1) {
			return categoryBanerData;
		}
		categoryBanerData.forEach(bannerData => {
			if(bannerData && bannerData['object_for'] && bannerData['object_for'] == 'category_banner') {
				bannerData['selected_banner'] = bannerData['value'] ? this.getBannerByBannerId(bannerData['value'],bannerData['options']) : {};
			}
		});
		return categoryBanerData;
	}
	/**
	 * Method for getting banner by banner option
	 * @access public
	*/
	getBannerByBannerId(bannerId,bannerOptions) {
		let selectedBanner = [];
		selectedBanner = bannerOptions.filter(bannerData => {
			if(bannerData['id'] == bannerId) {
				return bannerData;
			}
		});
		return selectedBanner.length > 0 ? selectedBanner[0] : {}; 
	}
	/**
	 * Method for getting banner when iscms is false
	 * @access public
	*/
	getBannerWhileForNonCms() {
		let selectedBannerId = [];
		this.widget_properties_data.forEach(bannerData => {
			if(bannerData['selected_banner'] )  {
				selectedBannerId.push(bannerData['selected_banner']['id']);
			}
		});
		this._categoryService.getPromotionalBannerByBannerId(selectedBannerId,'C').subscribe(bannerData => {
			if(bannerData && bannerData['status'] == 1) {
			 	this.widget_data_for_non_cms = bannerData['data'];
		 	}
		},
		function () {
			//completed callback
		})
	}
	/**
	 * Method for navigate to url
	 * @access public
	*/
	navigateToUrl(url) {
		url  = (url.indexOf('://') === -1) ? 'http://' + url : url;
		this._window.open(url,'_blank');
	}

	
}

