import { Component, OnInit, Inject, Optional } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA, MatDialog } from '@angular/material';
import { Router } from '@angular/router';
import { PaymentMethodService } from './inventory.payment-method.service';
import { GlobalService } from '../../global/service/app.global.service';
@Component({
  templateUrl: './templates/add_payment_method.html',
  providers: [PaymentMethodService]
})
export class PaymentMethodAddEditComponent implements OnInit {
	public response: any;
	public errorMsg: string;
	public successMsg: string;
	public formModel: any = {};
	public ipaddress: any;
	constructor(
		private _paymentService:PaymentMethodService,
		private _globalService:GlobalService,
		private _router: Router,
		private dialogRef: MatDialogRef<PaymentMethodAddEditComponent>,
		public dialog: MatDialog,
		@Optional() @Inject(MAT_DIALOG_DATA) public data: any
	) {
		dialog.afterOpen.subscribe(() => {
           let containerElem:HTMLElement = <HTMLElement>document.getElementsByClassName('mat-dialog-container')[0];
           containerElem.classList.remove('pop-box-up');
        }); 
        this.ipaddress = _globalService.getCookie('ipaddress'); //get user ip from cookie
	}
	
	ngOnInit() {
		this.formModel.paymentId = this.data;
		if(this.formModel.paymentId>0){
			this._paymentService.paymentLoad(this.formModel.paymentId).subscribe(
		       	data => {
		       		this.response = data;
		       		if(this.formModel.paymentId>0){
		       			this.formModel.paymentId = this.response.api_status.id;
			            this.formModel.name = this.response.api_status.name;
			            this.formModel.status = this.response.api_status.isblocked; 
		       		}else{
					   this.formModel.paymentId = 0;
					}
		       	},
		       	err => console.log(err),
		       	function(){
		       		//completed callback
		       	}
		    );
		} else{
			this.formModel.status = 'n';
		}
	}

    addEditPaymentMethod(form: any){
    	this.errorMsg = '';
	    var data: any = {};
        data.website_id = this._globalService.getWebsiteId();
        data.name = this.formModel.name;
        data.isblocked = this.formModel.status;
        if(this.ipaddress){
	        data.ip_address=this.ipaddress;
	    } else {
	        data.ip_address = '';
	    }
        if(this.formModel.paymentId<1){
          data.createdby = this._globalService.getUserId();
        }
        data.updatedby = this._globalService.getUserId();
        this._paymentService.paymentAddEdit(data,this.formModel.paymentId).subscribe(
           	data => {
               	this.response = data;
               	if(this.response.status==1){
                   this.closeDialog();
               	} else {
                   this.errorMsg = this.response.message;
               	}
            },
           	err => console.log(err),
           	function(){
                //completed callback
           	}
        );
    }

    closeDialog() {
		this.dialogRef.close();
	}
}