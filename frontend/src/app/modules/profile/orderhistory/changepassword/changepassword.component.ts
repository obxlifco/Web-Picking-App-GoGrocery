import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute, NavigationEnd } from '@angular/router';
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { Global } from '../../../../global/service/global';
import { AuthenticationService } from '../../../../global/service/authentication.service';
import { GlobalService } from '../../../../global/service/app.global.service';
import { LoaderService } from '../../../../global/service/loader.service';
import { WarehouseService } from '../../../../global/service/warehouse.service';
@Component({
  selector: 'app-changepassword',
  templateUrl: './changepassword.component.html',
  styleUrls: ['./changepassword.component.css']
})
export class ChangepasswordComponent implements OnInit {
  public formModel:any={};

  constructor(
    public global: Global,
		public authenticationService:AuthenticationService,
		private _router: Router,
		public _globalService: GlobalService,
		private _loader:LoaderService,
		private _wareHouseService: WarehouseService,
  ) { }

  ngOnInit() {
  }
  addEdit(formData:any={}){
    let data=formData.value
    this.global.getWebServiceData('change-password', 'PUT', data, '').subscribe(res => {
      console.log(res);
			if(res) {
        if (res.status == 200) {
          this._globalService.showToast('Password Updated successfully'); 
          this.formModel='';         
			  }else{
          
          this._globalService.showToast(res.message);
        }
			}
		}, err => console.log(err), function() {
    });
  }
}
