import { Component, OnInit, Inject, PLATFORM_ID } from '@angular/core';
import { Router, ActivatedRoute, NavigationEnd } from '@angular/router';
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { Global } from '../../../../global/service/global';
import { AuthenticationService } from '../../../../global/service/authentication.service';
import { GlobalService } from '../../../../global/service/app.global.service';
import { LoaderService } from '../../../../global/service/loader.service';
import { WarehouseService } from '../../../../global/service/warehouse.service';
import { CartService } from '../../../../global/service/cart.service';
import { isPlatformBrowser } from '@angular/common';
@Component({
  selector: 'app-wishlist',
  templateUrl: './wishlist.component.html',
  styleUrls: ['./wishlist.component.css']
})
export class WishlistComponent implements OnInit {
	public selectedWareHouseDatails = {};
	public wishlist_ids:any=[];
	public wishlist:any=[];
	constructor(
		public global: Global,
		public authenticationService:AuthenticationService,
		private _router: Router,
		public _globalService: GlobalService,
		private _loader:LoaderService,
		private _wareHouseService: WarehouseService,
		public cartService:CartService,
		@Inject(PLATFORM_ID) private platformId: Object

	) {
		this._wareHouseService.warehouseData$.subscribe(response => {
			this.selectedWareHouseDatails = response;
			this.loadWishlist();
		});
	}

	ngOnInit() {
		if (isPlatformBrowser(this.platformId)) {
			this.loadWishlist();
		}
	}

	loadWishlist() {
		this._loader.show();
		this.global.getWishList('my-wish-list', 'GET', '', '').subscribe(data => {
			this.wishlist=[];
			if(data) {
			  if (data.status == 200) {
				data.data.forEach(element => {
				  //if(element.product.channel_price.channel_price!=''){
					this.wishlist.push(element);
				  //}
				});
				this._loader.hide();
			  }
			}
		}, err => console.log(err), () => this._loader.hide());
	}

	navigate(data:number,order_id:any='') {
		if(data==0) {//Home
			this._router.navigate(['/home']);
		}else if(data==1) {//Profile
			this._router.navigate(['/profile/profiledetails']);
		} else if(data==2) {//Delivery  Address
			this._router.navigate(['/profile/delivery-address']);
		} else if(data==3) {//chaange password
			this._router.navigate(['/profile/change-password']);
		} else if(data==4) {//wishlist
			this._router.navigate(['/profile/order-history']);
		}
	}

	delete_item(pro_id:number) {
		let data:any={};
		data={"product_id":pro_id}
		this.global.getWebServiceData('delete-wishlist', 'POST', data, '').subscribe(data => {
			if (data.status == 200) {
			  this._globalService.showToast('Item removed from wishlist');
			  this.loadWishlist();
			  this.wishlist_count();
			}
		}, err => console.log(err), function() {});
	}

	navigateToDetailPage(productSlug) {
		this._router.navigate(['details/'+productSlug]);
		window.scroll(0,0);
	}

	wishlist_count(){
		this.cartService.saveListCount().subscribe(
			data => {
				if (data.status==200) {
					this.cartService.wishlistCount=data.total_count;
				}
			},
			err => { },
			function () {}
		);
	}
}