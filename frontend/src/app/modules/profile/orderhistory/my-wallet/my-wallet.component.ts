import { Component, OnInit,ViewChild, Inject, PLATFORM_ID} from '@angular/core';
import { Router, ActivatedRoute, NavigationEnd } from '@angular/router';
import { LoaderService } from '../../../../global/service/loader.service';
import { LoyaltypointService } from '../../../../global/service/loyaltypoint.service';
import {AuthenticationService} from '../../../../global/service/authentication.service';
import {MatPaginator} from '@angular/material/paginator';
import {MatTableDataSource} from '@angular/material/table';
import { isPlatformBrowser } from '@angular/common';

@Component({
  selector: 'app-my-wallet',
  templateUrl: './my-wallet.component.html',
  styleUrls: ['./my-wallet.component.css']
})
export class MyWalletComponent implements OnInit {

  public loyaltyRecord:Object= {};
  public walletDataSource;
  @ViewChild(MatPaginator) paginator: MatPaginator;

  constructor(@Inject(PLATFORM_ID) private platformId: Object,  private _loaderService:LoaderService,private _router: Router,private _loyaltyPoint:LoyaltypointService,private authenticationService:AuthenticationService) { }

   
  ngOnInit() {
    if (isPlatformBrowser(this.platformId)) {
      this.getLoyaltyRecord();
    }

  }
  /**
   * Method for getting wallet data
   * @access public
  */
  getLoyaltyRecord() {
  	//this._loaderService.show();
  	this._loyaltyPoint.getUserLoyaltyData().subscribe(response => {
  		if(response && response['status'] == 200) {
  			this.walletDataSource = response['data'];
        console.log("****************** Wallet data source ******************");
        console.log(this.walletDataSource);
  			//this.loyaltyRecord.paginator = 

  		}
  	});
  	



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
	

}
export interface PeriodicElement {
  name: string;
  position: number;
  weight: number;
  symbol: string;
}
