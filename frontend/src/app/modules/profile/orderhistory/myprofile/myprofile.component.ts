import { Component, OnInit, Inject, PLATFORM_ID } from '@angular/core';
import { Router, ActivatedRoute, NavigationEnd } from '@angular/router';
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { Global,GlobalVariable} from '../../../../global/service/global';
import { AuthenticationService } from '../../../../global/service/authentication.service';
import { GlobalService } from '../../../../global/service/app.global.service';
import { LoaderService } from '../../../../global/service/loader.service';
import { WarehouseService } from '../../../../global/service/warehouse.service';
import { CartService } from '../../../../global/service/cart.service';
import { isPlatformBrowser } from '@angular/common';

@Component({
  selector: 'app-myprofile',
  templateUrl: './myprofile.component.html',
  styleUrls: ['./myprofile.component.css']
})
export class MyprofileComponent implements OnInit {
  public formModel:any={};
  public gender_list=['Male','Female','Others'];
  public countryCode = GlobalVariable.COUNTRY_CODE;
  public carrierCode =  GlobalVariable.CARRIER_CODE;
  constructor(
    public global: Global,
		public authenticationService:AuthenticationService,
		private _router: Router,
		public _globalService: GlobalService,
		private _loader:LoaderService,
		private _wareHouseService: WarehouseService,
    public cartService:CartService,
    @Inject(PLATFORM_ID) private platformId: Object,
  ) {

   }

  ngOnInit() {
    if (isPlatformBrowser(this.platformId)) {
      this.global.getWebServiceData('my-profile', 'GET', '', '').subscribe(res => {
        if(res) {
          if (res.status == 200) {
            let data=res.data
            console.log(data);
            this.formModel.first_name = data.first_name;
            this.formModel.last_name = data.last_name;
            this.formModel.gender = data.gender;
            this.formModel.location = data.location;
            this.formModel.email = data.email;
            this.formModel.phone = data.phone;
  
          }
        }
      }, err => console.log(err), function() {});
    }
   
  }
  addEdit(formData:any={}){
    console.log(formData.value);
    let data=formData.value
    console.log(data);
    
    this.global.getWebServiceData('my-profile', 'PUT', data, '').subscribe(res => {
      console.log(res);
			if(res) {
        if (res.status == 200) {
          this._globalService.showToast(res.message);                  
			  }else{
          let errorMessage = res && res['error_message'] ? res['error_message'] : 'Something went wrong!';
          this._globalService.showToast(errorMessage);        
        }
			}
		},
    err => {
       this._globalService.showToast("Something went wrong,Please try again");

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
