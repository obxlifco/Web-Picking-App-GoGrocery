import { SubstitutioncartoptionComponent } from './../../global/dialog/substitutioncartoption/substitutioncartoption.component';
import { Component, OnInit, Inject, PLATFORM_ID } from '@angular/core';
import {ActivatedRoute,Router} from '@angular/router';
import {DetailsService} from '../../global/service/details.service';
import {CartService} from '../../global/service/cart.service';
import {GlobalVariable, Global} from '../../global/service/global';
import { WarehouseService } from '../../global/service/warehouse.service';
import { GlobalService } from '../../global/service/app.global.service';
import { AuthenticationService } from '../../global/service/authentication.service';
import { LoginComponent } from '../../login/login.component';
import {MatDialogRef, MAT_DIALOG_DATA, MatDialog} from '@angular/material/dialog';
import { MenuService } from '../../global/service/menu.service';
import { isPlatformBrowser } from '@angular/common';
import { ProductService } from '../../global/service/product.service';
import * as moment from 'moment';
declare let fbq:Function;

@Component({
  selector: 'app-substitute',
  templateUrl: './substitute_product.component.html',
  styleUrls: ['./substitute_product.component.css']
})
export class SubstituteProductComponent implements OnInit {

	public S3_URL_PRODUCT =  GlobalVariable.S3_URL+'product/400x400/';
	public productSlug;
	public detailsData = {};
	public parentProductId;
	public categoryData;
	public is_wishlist:any=0;
	public formattedDetailsData = [];
	public selectedProductId = 0;
	public owlConfiguration = {
			items: 1,
			dots: false,
			autoWidth:true,
			navigation: false
	};																

	public shortageProducts: any = [];
	public currency_code: any;
	public categories_list: any = [];
	public item : any = {};
	public client_id: any;
	public approvalDetails: any = [];
	public currentItemIndex = 0 ;
	public allOrderProducts: any = [];
	public customer_id: any;
	public grnQuantity = 0;
	public showConformationBox=0;	
	public createdDate;
	public orderId;
	public itemIndex;
	public substituteTime;
	public substituteApprovalTime;
	public expiryDate;
	public currentTime;
	public RemainingTime;
	public minute;
	public second;
	public custom_fields:any=[];
	selected_preparion_unit:any;
	prepearation_lable:any;
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
		private _ps:ProductService,
		@Inject(PLATFORM_ID) private platformId: Object,
	){

	}

	ngOnInit() {
		this._warehouseservice.warehouseData$.subscribe(res=>{
				this._route.params.subscribe(response => {
					this.productSlug = this._route.snapshot.params['slug'];
				});
			})
		this.orderId = atob(this.productSlug);
		console.log(this.orderId)
		this.orderId = parseInt(this. orderId)
		console.log(this.orderId)
		this.customer_id = this._globalService.getCustomerId();
		this.client_id = this._globalService.getClientId()
		this.getSubstituteProductByOrderId();	
	}

	getSubstituteProductByOrderId(){
		let data={
			"website_id" : this._globalService.getWebsiteId(),
			"order_id" : this.orderId
		}

		this._ps.getSubstituteProduct(data).subscribe(response => {
			this.selectedProductId = response.response[0].id;
			this.allOrderProducts = response.response[0].order_products;
			this.shortageProducts = this.allOrderProducts.filter(element => element.substitute_products.length > 0)
			this.item = this.shortageProducts[0];
			if(this.item.send_approval == 'action_taken'){
				this.showConformationBox = 4;
			}
			let created = this.item.substitute_products[0].created;
			console.log(created, 'created')
			let require = new Date(created)
			console.log(require.toString(), 'require')
			this.substituteApprovalTime = response.response[0].substitute_approval_time;
			this.expiryDate = moment(created).add(this.substituteApprovalTime, 'minutes');
			let date = moment(this.expiryDate).toDate();
			console.log(date,'expiryDate')
			this.substituteTime = this._globalService.convertDate(date, 'yyyy-MM-dd HH:mm:ss');
			console.log(this.substituteTime, 'substituteTime')
			this.currency_code = response.response[0].currency_code;
			let currentDate = moment().format();
			this.currentTime = this._globalService.convertDate(currentDate, 'yyyy-MM-dd HH:mm:ss');
			console.log(this.currentTime,'currentTime')
			let startDate = moment(this.currentTime);
			let endDate = moment(this.substituteTime);
			console.log(startDate, endDate)
			let boolean = startDate.isBefore(endDate);
			if(boolean){
				this.RemainingTime = moment.utc(moment(this.substituteTime, "HH:mm:ss").diff(moment(this.currentTime, "HH:mm:ss"))).format("mm:ss");
			}else{
				this.showConformationBox = 3;
			}
			// this.RemainingTime = moment.utc(moment(this.substituteTime, "HH:mm:ss").diff(moment(this.currentTime, "HH:mm:ss"))).format("mm:ss");
			console.log(this.RemainingTime)
			if(this.RemainingTime){
				let timeArray = this.RemainingTime.split(':');
				if(timeArray){
					this.minute = +timeArray[0];
					this.second = +timeArray[1];
					// this.minute = 0;
					// this.second = 30;
				}
				this.countDown();
			}
		});
	}

	countDown(){
		let interval = setInterval(() => {
			if(this.second){
				this.second -= 1;
			}else if(this.second == 0 && this.minute == 0){
				clearInterval(interval);
				this.showConformationBox = 3;
			}else {
				if(this.second == 0){
					this.second = 59;
					if(this.minute){
						this.minute -= 1;
					}
				}
			}
		}, 1000);
		
	}

	getMinutes(minute){
		if(minute < 10){
			return "0" + minute;
		}else{
			return minute;
		}
	}

	getSeconds(second){
		if(second < 10){
			return "0" + second;
		}else{
			return second;
		}
	}

	submitReplacement(){
		if(this.getSelectedQauantity() && this.getSelectedQauantity() < this.item.shortage){
			this.showConformationBox = 2;
		}else if(this.getSelectedQauantity() == this.item.shortage){
			this.showConformationBox = 5;
			// let postdata = {
			// 	"website_id":this._globalService.getWebsiteId(),
			// 	"order_id":this.orderId,
			// 	"user_id" : this.customer_id,
			// 	"approval_details" : []
			// }
			// if(this.item && this.item.substitute_products){
			// 	this.item.substitute_products.forEach(element => {
			// 		let approval = {
			// 			"product_id": this.item.product.id,
			// 			"substitute_product_id": element.product.id,
			// 			"order_product_id": element.id,
			// 			"quantity": element.quantity,
			// 			"grn_quantity": element.selectedQuantity ? element.selectedQuantity : 0
			// 		}
			// 		postdata.approval_details.push(approval);
			// 	});
			// }
			// console.log(postdata)	
			// this._ps.submitReplacementProduct(postdata).subscribe(response => {
			// 	if(this.itemIndex == this.shortageProducts.length-1){
			// 		this.orderId = btoa(this.productSlug);
			// 		console.log(this.orderId)
			// 		this.navigateToUrl('success-substitute/'+this.orderId)
			// 	}
			// });
			// this.showNext();
		}else{
			this._globalService.showToast('Please select substitute product');
		}

	}

	showNext(){
		if(this.shortageProducts && this.item){
			let index = this.shortageProducts.findIndex(ele =>  ele.id == this.item.id );
			this.itemIndex = index;
			if(index !=-1 && index < this.shortageProducts.length-1){
				this.item = this.shortageProducts[index+1];
				this.currentItemIndex = index + 1;
			}
		}
	}

	showWarning(){
		this.showConformationBox = 1;
	}

	showPrevious(){
		if(this.shortageProducts && this.item){
			let index = this.shortageProducts.findIndex(ele =>  ele.id == this.item.id );
			this.itemIndex = index;
			if(index !=-1 && index > 0){
				this.item = this.shortageProducts[index-1];
				this.currentItemIndex = index-1;
			}else{
				this.item = this.shortageProducts[0];
			}
		}
	}


	addItem(product: any,string){
		console.log(product)
		this.custom_fields= product.product.custom_fields
		console.log(this.custom_fields)
		if(this.custom_fields && this.custom_fields.length>0 && string==='addItem'){
			const dialogRef = this.dialog.open(SubstitutioncartoptionComponent, {
				disableClose: true,
				data: this.custom_fields
			});
			dialogRef.afterClosed().subscribe(result => {
				this.selected_preparion_unit= result.custom_field_value
				this.prepearation_lable = result.fieldlabel;
				console.log(this.prepearation_lable,this.selected_preparion_unit)
				if(this.getSelectedQauantity() < this.item.shortage){
					if(product.selectedQuantity){
						product.selectedQuantity = product.selectedQuantity + 1;
					}else{
						product.selectedQuantity = 1;
					}
				}else{
					this._globalService.showToast('You reached maximum number of Substitute Product');
				}
				this.grnQuantity = product.selectedQuantity;
			})
		}
		else{
			if(this.getSelectedQauantity() < this.item.shortage){
				if(product.selectedQuantity){
					product.selectedQuantity = product.selectedQuantity + 1;
				}else{
					product.selectedQuantity = 1;
				}
			}else{
				this._globalService.showToast('You reached maximum number of Substitute Product');
			}
			this.grnQuantity = product.selectedQuantity;
		}
	}

	getSelectedQauantity(){
		let count = 0;
		this.item.substitute_products.forEach(element => {
			if(element.selectedQuantity > 0){  
				count += element.selectedQuantity;
			}
		});
		return count;
	}

	RemoveItem(product: any){
		if(product.selectedQuantity){
			product.selectedQuantity = product.selectedQuantity - 1;
		}
	}

	navigateToUrl(url) {
		this._router.navigate([url]);
	}

	reSubstitute(type:number=0){
		if(type == 1){
			this.showConformationBox = 0;
			this.submit_Replacement();
		}else if(type == 2){
			this.showConformationBox = 0;
			this.submitForceReplacement();
		}else{
			this.showConformationBox = 0;
		}
	}

	submitForceReplacement(){
		let postdata = {
			"website_id":this._globalService.getWebsiteId(),
			"order_id":this.orderId,
			"user_id" : this.customer_id,
			"approval_details" : []
		}
		if(this.item && this.item.substitute_products){
			this.item.substitute_products.forEach(element => {
				let approval = {
					"product_id": this.item.product.id,
					"substitute_product_id": element.product.id,
					"order_product_id": element.id,
					"quantity": element.quantity,
					"grn_quantity": element.selectedQuantity ? element.selectedQuantity : 0
				}
				postdata.approval_details.push(approval);
			});
		}
		console.log(postdata)	
		this._ps.submitReplacementProduct(postdata).subscribe(response => {
			if(this.itemIndex == this.shortageProducts.length-1){
				this.orderId = btoa(this.productSlug);
					console.log(this.orderId)
				this.navigateToUrl('success-substitute/'+this.orderId)
			}
		});
		this.showNext();
	}

	submit_Replacement(){
		let postdata = {
			"website_id":this._globalService.getWebsiteId(),
			"order_id":this.orderId,
			"user_id" : this.customer_id,
			"approval_details" : []
		}
		if(this.item && this.item.substitute_products){
			if(this.prepearation_lable === undefined){
				this.prepearation_lable = ''
			}
			if(this.selected_preparion_unit === undefined){
				this.selected_preparion_unit = ''
			}
			this.item.substitute_products.forEach(element => {
				let approval = {
					"product_id": this.item.product.id,
					"substitute_product_id": element.product.id,
					"order_product_id": element.id,
					"quantity": element.quantity,
					"grn_quantity": element.selectedQuantity ? element.selectedQuantity : 0,
					"custom_field_name":this.prepearation_lable,
					"custom_field_value":this.selected_preparion_unit
				}
				postdata.approval_details.push(approval);
			});
		}
		console.log(postdata)
		this._ps.submitReplacementProduct(postdata).subscribe(response => {
			if(this.itemIndex == this.shortageProducts.length-1){
				this.orderId = btoa(this.productSlug);
					console.log(this.orderId)
				this.navigateToUrl('success-substitute/'+this.orderId)
			}
		});
		this.showNext();
	}
}