import { Component, OnInit, Inject,Optional } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA, MatDialog } from '@angular/material';
import { Router } from '@angular/router';
import { PresetService } from './order.preset.service';
import { GlobalService } from '../../global/service/app.global.service';

@Component({
  templateUrl: './templates/add_preset.html',
  providers: [PresetService]
})
export class PresetAddEditComponent implements OnInit { 

	public response: any;
	public errorMsg: string;
	public successMsg: string;
	public formModel: any = {};
	public courier_list:any=[];
	public service_list:any=[];
	public package_list:any=[];

	constructor(
		private _presetService:PresetService,
		private _globalService:GlobalService,
		private _router: Router,
		private dialogRef: MatDialogRef<PresetAddEditComponent>,
		public dialog: MatDialog,
		@Optional() @Inject(MAT_DIALOG_DATA) public data: any
	) {
		dialog.afterOpen.subscribe(() => {
           let containerElem:HTMLElement = <HTMLElement>document.getElementsByClassName('mat-dialog-container')[0];
           containerElem.classList.remove('pop-box-up');
        }); 
	}
	
	ngOnInit(){

		this.formModel.presetId = this.data;
			this._presetService.loadPreset(this.formModel.presetId).subscribe(
		       	data => {

		       		this.response = data;
		       		console.log(this.response)
		       		if(this.formModel.presetId>0) {
		       			this.formModel=this.response.api_status;
		       			this.formModel.presetId = this.response.api_status.id;
		       			this.courier_list=this.response.courier_arr;
		       			this.service_list=this.response.services_arr;
		       			this.package_list=this.response.package_arr;
		       			this.formModel.shipping_method_id=this.response.api_status.shipping_method.id;
		       			console.log(this.response);
		       			if(this.response.api_status.service!=null) {
		       				this.formModel.service_id = this.response.api_status.service.id;
		       			} else {
		       				this.formModel.service_id = '';
		       			}
		       			if(this.response.api_status.package!=null) {
		       				this.formModel.package_id = this.response.api_status.package.id;
		       			} else {
		       				this.formModel.package_id = '';	
		       			}		       			
		       		} else {
		       			this.formModel.presetId = 0;
		       			this.courier_list=this.response.courier_arr;
		       		}
		       		
		       	},
		       	err => console.log(err),
		       	function(){
		       		//completed callback
		       	}
		    );
		
	}

	fillServicePackage(courierId:number){
			this._presetService.servicePackageLoad(courierId).subscribe(
		       	data => {
		       		this.response = data;
		       			this.service_list=this.response.services_arr;
		       			this.package_list=this.response.packages_arr;
		       	},
		       	err => console.log(err),
		       	function(){
		       		//completed callback
		       	}
		    );
	}

    addEditPreset(form: any){

    	this.errorMsg = '';
    	var data: any = {};
		if(this.formModel.presetId < 1) {
			data.website_id = this._globalService.getWebsiteId();
			data.name = this.formModel.name;
			data.shipping_method_id = this.formModel.shipping_method_id;
			data.service_id = this.formModel.service_id;
			data.package_id = this.formModel.package_id;
			data.sizel = this.formModel.sizel;
			data.sizew = this.formModel.sizew;
			data.sizeh = this.formModel.sizeh;
			data.weight = this.formModel.weight;
		} else {
			data = Object.assign({}, this.formModel);
	        data.website_id = 1;
	        if(this.formModel.presetId<1){
	          data.createdby = this._globalService.getUserId();
	        }
	        data.updatedby = this._globalService.getUserId();
		}
	   
	   console.log(data);
        
        this._presetService.presetAddEdit(data,this.formModel.presetId).subscribe(
           	data => {
               	this.response = data;
              
               	if(this.response.status==1){
                   
                   this.closeDialog();

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
