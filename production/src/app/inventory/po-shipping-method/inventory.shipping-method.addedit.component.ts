import { Component, OnInit, Inject, Optional } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA, MatDialog } from '@angular/material';
import { Router } from '@angular/router';
import { ShippingMethodService } from './inventory.shipping-method.service';
import { GlobalService } from '../../global/service/app.global.service';

@Component({
  templateUrl: './templates/add_shipping_method.html',
  providers: [ShippingMethodService]
})
export class ShippingMethodAddEditComponent implements OnInit { 

	public response: any;
	public errorMsg: string;
	public successMsg: string;
	public formModel: any = {};
	public ipaddress: any;

	constructor(
		private _paymentService:ShippingMethodService,
		private _globalService:GlobalService,
		private _router: Router,
		private dialogRef: MatDialogRef<ShippingMethodAddEditComponent>,
		public dialog: MatDialog,
		@Optional() @Inject(MAT_DIALOG_DATA) public data: any
	) {
		dialog.afterOpen.subscribe(() => {
           let containerElem:HTMLElement = <HTMLElement>document.getElementsByClassName('mat-dialog-container')[0];
           containerElem.classList.remove('pop-box-up');
        });
        this.ipaddress = _globalService.getCookie('ipaddress'); //get user ip from cookie 
	}
	
	ngOnInit(){

		this.formModel.shippingId = this.data;
		if(this.formModel.shippingId>0) {
			this._paymentService.shippingLoad(this.formModel.shippingId).subscribe(
		       	data => {

		       		this.response = data;
		       		if(this.formModel.shippingId>0){
		       			this.formModel.shippingId = this.response.api_status.id;
			            this.formModel.name = this.response.api_status.name;
			            this.formModel.status = this.response.api_status.isblocked; 
		       		}else{
						this.formModel.shippingId = 0;
					}
		       		
		       	},
		       	err => console.log(err),
		       	function(){
		       		//completed callback
		       	}
		    );
		} else {
			this.formModel.status = 'n';
		}
		
	}



    addEditShippingMethod(form: any){

    	this.errorMsg = '';
		
	    var data: any = {};
        data.website_id = 1;
        data.name = this.formModel.name;
        data.isblocked = this.formModel.status;
        if(this.ipaddress){
	        data.ip_address=this.ipaddress;
	        }else{
	        data.ip_address='';
	        }
        if(this.formModel.shippingId<1){
          data.createdby = this._globalService.getUserId();
        }
        data.updatedby = this._globalService.getUserId();
        
        this._paymentService.shippingAddEdit(data,this.formModel.shippingId).subscribe(
           	data => {
               	this.response = data;
              
               	if(this.response.status==1){
                   
                   this.closeDialog();
                   //this._router.navigate(['/brand/reload']);

               	}else{
                   
                   this.errorMsg = this.response.message;
               	}
            },
           	err => console.log(err),
           	function(){
                //completed callback
           	}
        );

    }

    closeDialog(){
		this.dialogRef.close();
	}
}
