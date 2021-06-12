import { Component, OnInit, OnDestroy, ViewChild, AfterViewInit, Inject, Optional } from '@angular/core';

import { Router, ActivatedRoute } from '@angular/router';
import { BasicSetupService } from './settings.basic-setup.service';
import { GlobalService } from '../../global/service/app.global.service';
import { Global } from '../../global/service/global';
import { GlobalVariable } from '../../global/service/global';
import { AddEditTransition } from '../.././addedit.animation';
import { PopupImgDirective, ImageUploadUrlDialog } from '../.././global/directive/popup-image.directive';
import { MatAutocompleteSelectedEvent, MatAutocompleteTrigger, MatDialog, MatDialogRef, MAT_DIALOG_DATA, MatTabsModule } from '@angular/material';
import {MatCardModule} from '@angular/material/card';
import { DialogsService } from '../../global/dialog/confirm-dialog.service';
import { CookieService } from 'ngx-cookie';
//import { connectableObservableDescriptor } from 'rxjs';

@Component({
  templateUrl: './templates/add-basicsetup.html',
  providers: [BasicSetupService,Global],
  animations: [ AddEditTransition ],
  host: {
    '[@AddEditTransition]': ''
  },
})
export class BasicSetupAddEditComponent implements OnInit,OnDestroy,AfterViewInit { 

	public response: any;
	public errorMsg: string;
	public successMsg: string;

	public settingList: any = {};

	public formModel: any = {};
	public industrylist:any = [];
	private sub: any;
	public tabIndex: number;
	public parentId: number = 0;
	public ipaddress: any;
	public imgsubscriber:any;
	
	public country_list:any = [];
	public state_list:any = [];
	S3_URL: string;

	@ViewChild(MatAutocompleteTrigger) trigger;	

	constructor(
		private _basicSetupService:BasicSetupService,
		public _globalService:GlobalService,
		private _global:Global,
		public dialog: MatDialog,
		private _router: Router,
		private _cookieService: CookieService,
		private _route: ActivatedRoute 
	) {
		this.ipaddress = _globalService.getCookie('ipaddress');
		let userData = this._cookieService.getObject('userData');
		this.S3_URL = GlobalVariable.S3_URL + userData['company_name'] + '/' + userData['s3folder_name'] + '/'; 
	}
		
	ngOnInit() {
		
		this.tabIndex = +this._globalService.getCookie('active_tabs');
		this.parentId = this._globalService.getParentTab(this.tabIndex);
		this.sub = this._route.params.subscribe(params => {
	       this.formModel.settingsId = +params['id']; // (+) converts string 'id' to a number
		});
		this.loadCountry();
		if(this.formModel.settingsId > 0) {
			this._basicSetupService.settingsLoad(this.formModel.settingsId).subscribe(
				data => {
				 this.response = data;
				 	this.industrylist = this.response.industrylist;
					if(this.formModel.settingsId>0) {
						this.formModel = Object.assign(this.formModel,this.response.api_status);
						if(this.response.country){
							this.formModel['country_id'] = this.response.country[0].id;
							this.loadState(this.formModel['country_id']);
						}
 
						let img_base = this.S3_URL+'companylogo/250x185/';
					 if(this.formModel.website_logo){
						 this.formModel.website_logo = {};
						 this.formModel.website_logo['name'] = this.response.api_status.website_logo;
						 this.formModel.website_logo['url'] = img_base+this.response.api_status.website_logo;
					 }
					 
					 if(this.formModel.id_proof){
						 this.formModel.id_proof = {};
						 this.formModel.id_proof['name'] = this.response.api_status.id_proof;
						 this.formModel.id_proof['url'] = this.S3_URL+'id_proof/'+this.response.api_status.id_proof;
					 }
					 if(this.formModel.address_proof){
						 this.formModel.address_proof = {};
						 this.formModel.address_proof['name'] = this.response.api_status.address_proof;
						 this.formModel.address_proof['url'] = this.S3_URL+'address_proof/'+this.response.api_status.address_proof;
					 }
					 if(this.formModel.other_document){
						 this.formModel.other_document = {};
						 this.formModel.other_document['name'] = this.response.api_status.other_document;
						 this.formModel.other_document['url'] = this.S3_URL+'other_document/'+this.response.api_status.other_document;
					 }
					} 
					
				},
				err => {
					this._globalService.showToast('Something went wrong. Please try again.');
				},
				function(){
					//completed callback
				}
		 );			
		} else { // geting the industries list from the add page 
			this._basicSetupService.getIndustriesList().subscribe(data => {
				this.response = data;
				this.industrylist = this.response.Industry;
			}, 
		err => {
			this._globalService.showToast('Something went wrong. Please try again.');
		})
		}
			
	}

	loadCountry() {
		this._basicSetupService.loadCountry().subscribe(
			data => {
				this.country_list = data.countrylist;
			},
			err => console.log(err),
			function () {
				//completed callback
			}
		);
	}

	ngAfterViewInit() {
		// this.trigger.panelClosingActions
        // .subscribe(e => {
          
        //   if (this.trigger.activeOption) {
        //     this.formModel.country_id = this.trigger.activeOption;
        //     this.trigger.closePanel();
        //   }else{
        //     if(typeof this.formModel.country_id != 'object'){
        //     	this.formModel.country_id = null;
	    //         this.country_list = [];
	    //     }
        //   }
        // });

        this.imgsubscriber =this._globalService.libArrayChange$.subscribe(result => {

        	for (let key in result) {
			    let value = result[key][0];
			    value['name'] = value['url'];
			    if(key=='website_logo'){
		  			value['url'] = this.S3_URL+'companylogo/250x185/'+value['url'];
		  		}
		  		else{
		  			value['url'] = this.S3_URL+'companylogo/250x185/'+value['url'];
		  		}	
			    value['type'] = 3;  // image upload type - 3 i.e upload from s3 library
			    this.formModel[key] = value;
			}
		});

    }
		
	ngOnDestroy(){
		this.sub.unsubscribe();
		this.imgsubscriber.unsubscribe();
	}

  	displayFn(obj: any){
    	return obj ? obj.country_name : obj;
  	}

  	// get countries
  	filter_countries(val:any){
		  console.log(val);
	    let filterValue: string = '';
			if (val.term) {
				filterValue = val.term.toLowerCase();
	      if(typeof val === 'object'){
			  filterValue = val.term.toLowerCase();
	      } else {
			  filterValue = val.term.toLowerCase();
	      }
	    }
	    let data = {
	      "table_name": "EngageboostCountries",
	      "search": filterValue,
	      "company_id": this._globalService.getCompanyId(),
		  "website_id": this.formModel.settingsId
	    }
	    this._global.globalAutocomplete(data).subscribe(
	      data => {
			//console.log(this.country_list);
			this.country_list = data.filter_data;
	      },
	      err => {
	        this._globalService.showToast('Something went wrong. Please try again.');
	      },
	      function(){
	      //completed callback
	      }
	    );
	}	

	getFilename(url:string){
		let filename:string = url.substring(url.lastIndexOf('/')+1);
		return filename;
	}

	loadState(country_id){
		this._basicSetupService.loadStates(country_id,'').subscribe(
			data => {
				this.state_list = data.states;
			},
			err => console.log(err),
			function () {
			}
		);
	}

    fileChoose(e: Event,imgFor: string, file_type:number) {
        let files: any = {};
        let target: HTMLInputElement = e.target as HTMLInputElement;
        let file_arr: any = [];
        for(let i=0;i < target.files.length; i++) {
            if(!this.check_file_ext(target.files[i].type,file_type) && file_type==1){
                this._globalService.showToast('Only jpeg/png/gif files are allowed');
            }else if(!this.check_file_ext(target.files[i].type,file_type) && file_type==2){
                this._globalService.showToast('Only pdf files are allowed');
            }else if(!this.check_file_size(target.files[i].size)){
                this._globalService.showToast('Maximum 2MB of file size is allowed');
            }else{
                let temp_arr = {};
                let reader = new FileReader();
                reader.readAsDataURL(target.files[i]);
                reader.onload = (event) => {
                    temp_arr['url'] = event.srcElement['result'];
                }
                temp_arr['_file'] = target.files[i]; 
                file_arr.push(temp_arr); 
            }
        }
        files[imgFor] = file_arr;
        for (let key in files) {
		    let value = files[key][0];
		    if(value){
		    	value['type'] = 2; // image upload type - 2 i.e upload from browse file
		   		this.formModel[key] = value;
		    }
		}
    }

    check_file_ext(type: string,file_type: number){
        let return_result = 0;
        switch (type) {
            case "image/png":
            	if(file_type==1)
                	return_result= 1;
                break;
            case "image/gif":
            	if(file_type==1)
                	return_result= 1;
                break;
            case "image/jpeg":
            	if(file_type==1)
                	return_result= 1;
                break;
            case "application/pdf":
                if(file_type==2)
                	return_result= 1;
                break;    
            default:
                return_result= 0;
                break;
        }

        return return_result;
    }

    check_file_size(size: number){
        let return_result: boolean;
        size = (size)/(1024*1024); // in MB
        if(size>2){
            return_result = false;
        }else{
            return_result = true;
        }
        return return_result;
    }

	delImg(is_remove: number,scope_var: string,file_var: string,is_arr: number,index: number){
		if(is_remove>0){
			let form_data: any = {};
			form_data.id = is_remove;
			form_data.field = file_var;
			form_data.file_name = this[scope_var][file_var]['name'];
			if(form_data.file_name){
				this._basicSetupService.imageDelete(form_data).subscribe(
		           	data => {
		               	this.response = data;
		               	if(this.response.status==1){
		               		this._globalService.showToast('Successfully Deleted!');
		               	} else {
		                   this.errorMsg = this.response.message;
		               	}
		            },
		           	err => {
		           		this._globalService.showToast('Something went wrong. Please try again.');
		           	},
		           	function(){
		                //completed callback
		           	}
		        );
			} else {
				this._globalService.showToast('Successfully Deleted!');
			}	
		}

      	if(is_arr){
	        if(scope_var!=''){
	          this[scope_var][file_var].splice(index,1); 
	        }else{
	          this[file_var].splice(index,1); 
	        }
      	}else{
	        if(scope_var!=''){
	          this[scope_var][file_var] = ''; 
	        }else{
	          this[file_var] = ''; 
	        }  
      	}
    };    
 
    addEditBasicSetup(form: any){
    	this._globalService.showLoaderSpinner(true);
    	this.errorMsg = '';
    	let data: any = {};
    	data = Object.assign({}, this.formModel);
		data.company_id = this._globalService.getCompanyId();
    	data.website_id = this.formModel.settingsId;

		data.engageboost_company_id = 1 ; //this._globalService.getCompanyId();
	    if(this.ipaddress) {
	    	data.ip_address=this.ipaddress;
	    } else {
	    	data.ip_address="";
	    }
	    if(this.formModel.settingsId<1){
				data.createdby = this._globalService.getUserId();
			}
	    data.updatedby = this._globalService.getUserId();
	    data.country_id = this.formModel.country_id

	    if(this.formModel.banner_image && this.formModel.banner_image.hasOwnProperty("name")){
      		data.banner_image = this.formModel.banner_image.name;
      	}else{
      		data.banner_image = '';
      	}

      	if(this.formModel.website_logo && this.formModel.website_logo.hasOwnProperty("name")){
      		data.website_logo = this.formModel.website_logo.name;
      	}else{
      		data.website_logo = '';
      	}

      	if(this.formModel.id_proof && this.formModel.id_proof.hasOwnProperty("name")){
      		data.id_proof = this.formModel.id_proof.name;
      	} else {
      		data.id_proof = '';
      	}

      	if(this.formModel.address_proof && this.formModel.address_proof.hasOwnProperty("name")){
      		data.address_proof = this.formModel.address_proof.name;
      	} else {
      		data.address_proof = '';
      	}

      	if(this.formModel.other_document && this.formModel.other_document.hasOwnProperty("name")){
      		data.other_document = this.formModel.other_document.name;
      	}else{
      		data.other_document = '';
      	}

	    let form_data = new FormData();
      	form_data.append('data', JSON.stringify(data));
      	if(this.formModel.website_logo){
      		if(this.formModel.website_logo.type==1){
      			form_data.append('website_logo', this.formModel.website_logo.url);  
      		}else{
      			if(this.formModel.website_logo._file){
      				form_data.append('website_logo', this.formModel.website_logo._file);
      			}else{
      				form_data.append('website_logo', '');
      			}
      		}
      	} else {
      		form_data.append('website_logo', '');
      	}

      	if(this.formModel.id_proof){
      		if(this.formModel.id_proof.type==1){
      			form_data.append('id_proof', this.formModel.id_proof.url);  
      		}else{
      			if(this.formModel.id_proof._file){
      				form_data.append('id_proof', this.formModel.id_proof._file);
      			} else {
      				form_data.append('id_proof', '');
      			}
      		}
      	} else {
      		form_data.append('id_proof', '');
      	}

      	if(this.formModel.address_proof){
      		if(this.formModel.address_proof.type==1){
      			form_data.append('address_proof', this.formModel.address_proof.url);  
      		}else{
      			if(this.formModel.address_proof._file){
      				form_data.append('address_proof', this.formModel.address_proof._file);
      			}else{
      				form_data.append('address_proof', '');
      			}
      		}
      	}else {
      		form_data.append('address_proof', '');  
      	}

      	if(this.formModel.other_document){
      		if(this.formModel.other_document.type==1){
      			form_data.append('other_document', this.formModel.other_document.url);  
      		}else{
      			if(this.formModel.other_document._file){
      				form_data.append('other_document', this.formModel.other_document._file);
      			}else{
      				form_data.append('other_document', '');
      			}   
      		}	
      	} else {
      		form_data.append('other_document', '');
		}
		console.log(form_data);
		
		this._basicSetupService.settingsAddEdit(form_data,this.formModel.id).subscribe(
           	data => {
               	this.response = data;
              	if(this.response.status==1) {
									 this.formModel.id=this.response.api_status;
                   this._router.navigate(['/basicsetup/edit/'+this.formModel.id+'/payment_gateway']);
               	} else {
                   this.errorMsg = this.response.message;
               	}
               	this._globalService.showLoaderSpinner(false);
            },
           	err => {
           		this._globalService.showToast('Something went wrong. Please try again.');
           		this._globalService.showLoaderSpinner(false);
           	},
           	function(){
                //completed callback
           	}
        );
    }
}


@Component({
  templateUrl: 'templates/select-template.html',
  providers: [BasicSetupService],
  animations: [AddEditTransition],
  host: {
  	'[@AddEditTransition]': ''
  },
})
export class BasicSetupTemplateComponent implements OnInit { 

	public response: any;
	public errorMsg: string;
	public successMsg: string;

	public formModel: any = {};
	public template_list: any = [];

	private sub: any;
	public tabIndex: number;
	public parentId: number = 0;
	public ipaddress: any;
	
	constructor(
		private _basicSetupService:BasicSetupService,
		public _globalService:GlobalService,
		private _global:Global,
		public dialog: MatDialog,
		private _router: Router,
		private _route: ActivatedRoute 
	) {

	this.ipaddress = _globalService.getCookie('ipaddress');
	}

	ngOnInit(){
		this.tabIndex = +this._globalService.getCookie('active_tabs');
		this.parentId = this._globalService.getParentTab(this.tabIndex);
		this.sub = this._route.params.subscribe(params => {
	       this.formModel.settingsId = +params['id']; // (+) converts string 'id' to a number
		});
		
		this._basicSetupService.templatesLoad(this.formModel.settingsId).subscribe(
	       	data => {

				this.response = data;
				this.formModel.engageboost_template_master_id = this.response.webstore_data[0].engageboost_template_master_id;
	       		this.template_list = this.response.api_status;
	       		
	       	},
	       	err => {
	       		this._globalService.showToast('Something went wrong. Please try again.');
	       	},
	       	function(){
	       		//completed callback
	       	}
	    );
	}

	setTemplate(index:number) {
		this.formModel.engageboost_template_master_id = index;
	}

	saveTemplate(form: any){
		let data:any = {};
		data = { engageboost_template_master_id: this.formModel.engageboost_template_master_id }
		this._basicSetupService.templatesEdit(data,this.formModel.settingsId).subscribe(
           	data => {
               	this.response = data;
               	if(this.response.status==1){
                   this._router.navigate(['/basicsetup/edit/'+this.formModel.settingsId+'/payment_gateway']);
               	}else{
                   this.errorMsg = this.response.message;
               	}
            },
           	err => {
           		this._globalService.showToast('Something went wrong. Please try again.');
           	},
           	function() {
                //completed callback
           	}
        );		
	}
}


@Component({
  templateUrl: 'templates/payment-gateway.html',
	providers: [BasicSetupService],
	animations: [AddEditTransition],
	host: {
		'[@AddEditTransition]': ''
	},
})
export class BasicSetupPaymentGatewayComponent { 

	public response: any;
	public errorMsg: string;
	public successMsg: string;

	public formModel: any = {};

	private sub: any;
	public tabIndex: number;
	public parentId: number = 0;
	public ipaddress: any;
	
	public payment_list:any = [];

	constructor(
		private _basicSetupService:BasicSetupService,
		public _globalService:GlobalService,
		public _dialogsService:DialogsService,
		private _global:Global,
		public dialog: MatDialog,
		private _router: Router,
		private _route: ActivatedRoute 
	) {

	this.ipaddress = _globalService.getCookie('ipaddress');
	}

	ngOnInit() {
		this.tabIndex = +this._globalService.getCookie('active_tabs');
		this.parentId = this._globalService.getParentTab(this.tabIndex);
		this.sub = this._route.params.subscribe(params => {
	       this.formModel.settingsId = +params['id']; // (+) converts string 'id' to a number
		});
		this._basicSetupService.paymentLoad(this.formModel.settingsId).subscribe(
	       	data => {
						this.response = data;
						this.payment_list = this.response.api_status;
	       	},
	       	err => {
	       		this._globalService.showToast('Something went wrong. Please try again.');
	       	},
	       	function(){
	       		//completed callback
	       	}
	    );
	}

	savePayment(form: any){
		let payment_method_data: any = {};
		let data:any = [];
		let that = this;
		let enabled_methods: any = [];
		this.payment_list.forEach(function(type:any){
			if(type.payment_method && type.payment_method.length>0){
				type.payment_method.forEach(function(method:any){
	
					if(method.is_checked){
						enabled_methods.push(method.id);
						method.payment_field.forEach(function(field:any){
							let result_item : any = {};
							result_item['website_id'] = that._globalService.getWebsiteId();
							result_item['paymentgateway_type_id'] = field.paymentgateway_type_id;
							result_item['paymentgateway_method_id'] = field.paymentgateway_method_id;
							result_item['setting_key'] = field.setting_key;
							result_item['setting_val'] = field.values;
							result_item['paymentgateway_setting_id'] = field.id;
							data.push(result_item);
						});	
					}
					
				});
			}

		});
		payment_method_data['data'] = data;
		payment_method_data['enabled_methods'] = enabled_methods.join(',');
		payment_method_data['website_id'] = this.formModel.settingsId;
		
		if(enabled_methods.length){
			console.log(payment_method_data);
			this._basicSetupService.paymentSave(payment_method_data,this.formModel.settingsId).subscribe(
		       	data => {
		       		if(data.status==1){
								this._router.navigate(['/basicsetup/edit/'+this.formModel.settingsId+'/shipping']);
							}else{
									
								this.errorMsg = this.response.message;
							}
		       	},
		       	err => {
		       		this._globalService.showToast('Something went wrong. Please try again.');
		       	},
		       	function(){
		       		//completed callback
		       	}
		    );
		}else{
			this._dialogsService.alert('Settings Error', 'Please choose atleast one payment method!');
		}
		
	}
}

@Component({
  templateUrl: 'templates/tax-rate.html',
	providers: [BasicSetupService],
	animations: [AddEditTransition],
	host: {
		'[@AddEditTransition]': ''
	},
})
export class BasicSetupTaxRateComponent { 

	public response: any;
	public errorMsg: string;
	public successMsg: string;

	public formModel: any = {};

	private sub: any;
	public tabIndex: number;
	public parentId: number = 0;
	public ipaddress: any;
	
	constructor(
		private _basicSetupService:BasicSetupService,
		public _globalService:GlobalService,
		private _global:Global,
		public dialog: MatDialog,
		private _router: Router,
		private _route: ActivatedRoute 
	) {

	this.ipaddress = _globalService.getCookie('ipaddress');
	}

	ngOnInit(){
		this.tabIndex = +this._globalService.getCookie('active_tabs');
		this.parentId = this._globalService.getParentTab(this.tabIndex);
		this.sub = this._route.params.subscribe(params => {
	       this.formModel.settingsId = +params['id']; // (+) converts string 'id' to a number
		});
		
		this._basicSetupService.taxLoad(this.formModel.settingsId).subscribe(
	       	data => {

	       		this.response = data;
	       		if(this.formModel.settingsId>0){
	       			this.formModel = Object.assign(this.formModel,this.response.api_status);
	       			this.formModel.international_tax = parseFloat(this.formModel.international_tax).toFixed(2);
	       			this.formModel.domestic_tax = parseFloat(this.formModel.domestic_tax).toFixed(2);
	       		}
	       		
	       	},
	       	err => {
	       		this._globalService.showToast('Something went wrong. Please try again.');
	       	},
	       	function(){
	       		//completed callback
	       	}
	    );
	}

	saveTax(form:any) {
		let data:any = {};
		data['website_id'] = this.formModel.settingsId;
		data['basic_setup_id'] = this.formModel.settingsId;
		data['international_tax'] = this.formModel.international_tax;
		data['domestic_tax'] = this.formModel.domestic_tax;
		data['ip_address'] = this.ipaddress;
		data.createdby = this._globalService.getUserId();
        data.updatedby = this._globalService.getUserId();
		this._basicSetupService.saveTax(data,this.formModel.id).subscribe(
           	data => {
               	this.response = data;
              
               	if(this.response.status==1){
                   this._globalService.deleteTab(this.tabIndex,this.parentId);
                   this._router.navigate(['/basicsetup']);
               	}else{
                   
                   this.errorMsg = this.response.message;
               	}
            },
           	err => {
           		this._globalService.showToast('Something went wrong. Please try again.');
           	},
           	function(){
                //completed callback
           	}
        );		
	}

}


@Component({
  templateUrl: './templates/add_ship.html',
	providers: [BasicSetupService, Global],
	/*animations: [AddEditTransition],
	host: {
		'[@AddEditTransition]': ''
	},*/
})
export class FlatShipAddEditComponent implements OnInit, AfterViewInit { 

	public response: any;
	public errorMsg: string;
	public successMsg: string;
	public formModel: any = {};
	public ipaddress: any;

	public country_list:any = [];
	public state_list:any = [];
	
	public tdStates = [];
	public selectedStateList = [];
	public zone_list:any = [];

	@ViewChild(MatAutocompleteTrigger) trigger;	
	constructor(
		private _basicSetupService:BasicSetupService,
		public _globalService:GlobalService,
		private _global:Global,
		private _router: Router,
		private dialogRef: MatDialogRef<FlatShipAddEditComponent>,
		public dialog: MatDialog,
		@Optional() @Inject(MAT_DIALOG_DATA) public data: any
	) {
		dialog.afterOpen.subscribe(() => {
           let containerElem:HTMLElement = <HTMLElement>document.getElementsByClassName('mat-dialog-container')[0];
           containerElem.classList.remove('pop-box-up');
        });
        this.ipaddress = _globalService.getCookie('ipaddress'); 
	}
	
	ngOnInit(){
		this.formModel.shipping_id = this.data.id;

		this.formModel.picking_type = 'HomeDelivery'
		this.formModel.shipping_master_type_id  =this.data.shipping_master_type_id
		this.formModel.state_id = null;
		let selected_states:any = [];
		this.loadCountry();
		this.loadZoneMaster();

		if (this.formModel.shipping_id>0) {
			this._basicSetupService.shippingLoad(this.formModel.shipping_id,this.formModel.shipping_master_type_id).subscribe(
		       	data => {
		       		this.response = data;
		       		//this.formModel = Object.assign({},this.response.shipping_info[0]);
		       		this.formModel.title = this.response.shipping_info[0].title;
		       		this.formModel.flat_price = this.response.shipping_info[0].flat_price;
		       		this.formModel.description = this.response.shipping_info[0].description;
		       		this.formModel.handling_price = this.response.shipping_info[0].handling_price;
		       		this.formModel.dispatch_time_max = this.response.shipping_info[0].dispatch_time_max;
		       		this.formModel.self_pickup_price = this.response.shipping_info[0].self_pickup_price

		       		let zone_ids =  this.response.shipping_info[0].zone_id.split(',');
					let selected_zones = zone_ids.map(Number);
		       		this.formModel.zone_id = selected_zones

		       		
		       		this.formModel.shipping_id = this.response.shipping_info[0].id;
		       		if(this.response.shipping_info[0].mthod_type!=null){
		       			this.formModel.mthod_type = this.response.shipping_info[0].mthod_type.toString();
		       		} else {
		       			this.formModel.mthod_type = "2";
							 }
							 
							if(this.response.shipping_info[0].handling_fees_type!=null){
								this.formModel.handling_fees_type = this.response.shipping_info[0].handling_fees_type.toString();
							} else {
								this.formModel.handling_fees_type = "0";
							}

		       		this.formModel.is_ebay = (this.response.shipping_info[0].is_ebay=='y')? true : false;
							this.formModel.country_ids = parseInt(this.response.shipping_info[0].country_ids);
							selected_states = this.response.shipping_info[0].state_id.split(',');
							selected_states = selected_states.map(Number);

		       		this.formModel.state_id = selected_states;
		       		// let zone_ids = this.response.shipping_info[0].zone_id.split(",");
		       		// this.formModel.zone_id = zone_ids.map(Number);
		       		//this.formModel.self_pickup_price = this.response.shipping_info[0].self_pickup_price;
		       		
		       		if(this.response.shipping_info[0].handling_fees_type != null) {
		       			this.formModel.handling_fees_type = this.response.shipping_info[0].handling_fees_type.toString();
		       		} else {
		       			this.formModel.handling_fees_type = "0";
		       		}
					   //this.get_states(this.response.shipping_info[0].country_ids);
						  this._basicSetupService.loadStateEdit(this.formModel.country_ids, this.formModel.shipping_master_type_id, this.formModel.shipping_id).subscribe(
						data => {
							this.state_list = data.states;
						},
						err => console.log(err),
						function () {
						}
					);
		       	},
		       	err => console.log(err),
		       	function(){
		       		//completed callback
		       	}
		    );
		} else {
			this.formModel.shipping_id = 0;
			this.formModel.country_ids = 99;
			this.get_states(this.formModel.country_ids);
			this.formModel.handling_fees_type = '0';
			this.formModel.mthod_type = '2';
		}
		
	}

	 loadZoneMaster() {
        this._global.getWebServiceData('zone_list','GET','','').subscribe(result => {
            if(result["status"] == 1) {
                this.zone_list = result.data;
            }
        }, err => {
        });
    }


	loadCountry() {
		this._basicSetupService.loadCountry().subscribe(
			data => {
				this.country_list = data.countrylist;
			},
			err => console.log(err),
			function () {
				//completed callback
			}
		);
	}

	get_states(country_id:number) {
		this._basicSetupService.loadStates(country_id, this.formModel.shipping_master_type_id).subscribe(
			data => {
				this.state_list = data.states;
			},
			err => console.log(err),
			function () {
			}
		);
	}

	ngAfterViewInit() {
    
    }
	
   addEditShip(form: any) {
   		this.errorMsg = '';
	    let data: any = {};
		//data = Object.assign({},this.formModel);
		data.website_id = this.formModel.settingsId;
		data.country_ids = this.formModel.country_ids;
		if (this.formModel.shipping_id<1) {
        	data.isblocked = 'n';
					//data.createdby = this._globalService.getUserId();
        }
        /*if(this.data.ship_type==1) {
						data.shipping_method_id = 4;
					} else if (this.data.ship_type==2) {
						data.shipping_method_id=5;
				}*/

		data.shipping_method_id = 4;
		data.mthod_type = this.formModel.mthod_type;
		data.handling_fees_type = this.formModel.handling_fees_type;
		data.shipping_id = this.formModel.shipping_id; 
		data.title = this.formModel.title;
		data.flat_price = this.formModel.flat_price;
		data.handling_price = this.formModel.handling_price;

		data.self_pickup_price = this.formModel.self_pickup_price;
		data.zone_id = this.formModel.zone_id.join(",");
		
		data.description = this.formModel.description;
		data.country_ids = this.formModel.country_ids;
		data.dispatch_time_max = this.formModel.dispatch_time_max;
		data['is_ebay'] = (this.formModel.is_ebay)?'y':'n';
	    data.website_id = this._globalService.getWebsiteId();
		data['status'] = 'yes';
 
	    if (this.formModel.state_id.length>0) {
			data['state_id'] = this.formModel.state_id.join(',');
		} else {
    		data['state_id'] = '';
    	}		
	    if ((this.formModel.state_id.length > 0) || this.formModel.state_id==0){
    		this._basicSetupService.shipAddEdit(data,this.formModel.shipId).subscribe(
	           	data => {
	               	this.response = data;
	               	if(this.response.status==1){
	                   this.closeDialog();
	               	}else{
		               this.errorMsg = this.response.Message;
	               	}
	            },
	           	err => console.log(err),
	           	function(){
	                //completed callback
	           	}
	        );
    	}
    }

    closeDialog(){
		this.dialogRef.close();
	}
}


@Component({
	templateUrl: './templates/channel_setup.html',
	providers: [BasicSetupService, Global],
	animations: [AddEditTransition],
	host: {
		'[@AddEditTransition]': ''
	},
})
export class ChannelSetupAddEditComponent implements OnInit { 
	public response: any;
	public errorMsg: string;
	public successMsg: string;
	public formModel: any = {};
	public ipaddress: any;
	public tabIndex: number;
	public parentId: number = 0;
	private sub: any;
	public channel_list:any = [];
	@ViewChild(MatAutocompleteTrigger) trigger;	

	constructor(
		private _basicSetupService:BasicSetupService,
		public _globalService:GlobalService,
		private _global:Global,
		public dialog: MatDialog,
		private _router: Router,
		private _route: ActivatedRoute ) {
		  	this.ipaddress = _globalService.getCookie('ipaddress'); 
	 	}
	  
	  	ngOnInit() {
				this.tabIndex = +this._globalService.getCookie('active_tabs');
				this.parentId = this._globalService.getParentTab(this.tabIndex);
				this.formModel.website_id = this.formModel.settingsId;
				this.sub = this._route.params.subscribe(params => {
					this.formModel.settingsId = +params['id']; // (+) converts string 'id' to a number
				});
				this.formModel.website_id = this.formModel.website_id > 0 ? this.formModel.website_id : 1;
				this._basicSetupService.channelSetupList(this.formModel.website_id).subscribe(
					data => {
						this.response = data;
						this.channel_list = this.response.channels;
					},
					err => {
						this._globalService.showToast('Something went wrong. Please try again.');
					},
					function () {
						//completed callback
					}
				);
			  }
			  
	loadBasicSetup(form:any) {
		this.tabIndex = +this._globalService.getCookie('active_tabs');
		this.parentId = this._globalService.getParentTab(this.tabIndex);
		this.ngOnInit();
		this._globalService.deleteTab(this.tabIndex, this.parentId);
	}
		

	dialogRefAmazonSettings: MatDialogRef<AmazonAuthenticationComponent> | null;
	dialogRefFlipkartSettings: MatDialogRef<FlipkartAuthenticationComponent> | null;
	dialogRefSnapdealSettings: MatDialogRef<SnapdealAuthenticationComponent> | null;
	dialogRefPaytmSettings: MatDialogRef<PaytmAuthenticationComponent> | null;
	dialogRefEbaySettings: MatDialogRef<EbayAuthenticationComponent> | null;
	
	authenticateMarketplaces(parent_id:any){
		let data:any = {};
		data['parent_id'] = parent_id;
		if (parent_id == 2) { // this is for Amazon
			this.dialogRefAmazonSettings = this.dialog.open(AmazonAuthenticationComponent, { data: data });
		} else if (parent_id == 20) { // this is for flipkart
			this.dialogRefFlipkartSettings = this.dialog.open(FlipkartAuthenticationComponent, { data: data });
		} else if (parent_id == 21) { // this is for Snapdeal
			this.dialogRefSnapdealSettings = this.dialog.open(SnapdealAuthenticationComponent, { data: data });
		} else if (parent_id == 23) { // this is for Paytm
			this.dialogRefPaytmSettings = this.dialog.open(PaytmAuthenticationComponent, { data: data });
		} else if (parent_id == 1) { // this is for Ebay
			this.dialogRefEbaySettings = this.dialog.open(EbayAuthenticationComponent, { data: data });
			// this.dialogRefEbaySettings.afterClosed().subscribe(result => {
			// });
		}
	}

	//amazon_channel_setup: MatDialogRef<AmazonAuthenticationComponent> | null;
	activate_channels(parent_id, event) {
		let website_id = this.formModel.settingsId; // getting website id from the cookies
		let mode = '';
		let is_active = 0;
		if (event.checked == true) {
			mode = 'Activate';
			is_active = 1;
		} else {
			mode = 'Deactivate';
			is_active = 0;
		}
		let data: any = {};
		if (parent_id > 0) {
			data['website_id'] = website_id;
			data['is_active'] = is_active;
			data['parent_id'] = parent_id;
			this._basicSetupService.activateChannel(data).subscribe(
				data => {
					if (event.checked == true) {
						this.authenticateMarketplaces(parent_id);
					} 
					this.ngOnInit();
					// this.response = data;
					// //this.channel_lists = this.response.credentials;
					// this.formModel.channel_lists = this.response.credentials;
				},
				err => console.log(err),
				function () {
					//completed callback
				}
			);
		}		
	}
}



@Component({
	templateUrl: './templates/amazon_settings.html',
	providers: [BasicSetupService, Global]
})
  export class AmazonAuthenticationComponent implements OnInit { 
  
	  public response: any;
	  public errorMsg: string;
	  public successMsg: string;
	  public formModel: any = {};
	  public ipaddress: any;
	  public channel_lists: any = [];
	  @ViewChild(MatAutocompleteTrigger) trigger;	
	  constructor(
		  private _basicSetupService:BasicSetupService,
		  public _globalService:GlobalService,
		  private _global:Global,
		  private _router: Router,
		  private dialogRef: MatDialogRef<AmazonAuthenticationComponent>,
		  public dialog: MatDialog,
		  @Optional() @Inject(MAT_DIALOG_DATA) public data: any
	  ) {
		  dialog.afterOpen.subscribe(() => {
			 let containerElem:HTMLElement = <HTMLElement>document.getElementsByClassName('mat-dialog-container')[0];
			 containerElem.classList.remove('pop-box-up');
		  });
		  this.ipaddress = _globalService.getCookie('ipaddress'); 
	  }
	  
	  ngOnInit() {
		  this.formModel.parent_id = this.data.parent_id;
		  this.formModel.website_id = this.formModel.settingsId; // getting website id from the cookies
		  if (this.formModel.parent_id>0) {
			  this._basicSetupService.loadChannelSettings(this.formModel.parent_id, this.formModel.website_id).subscribe(
				data => {
					this.response = data;
					this.formModel.channel_lists = this.response.credentials;
					this.formModel.channel_lists.forEach(function (channel_list: any) {
						channel_list['title' + channel_list.id] = channel_list.id;
						channel_list['amz_access_key' + channel_list.id] = channel_list.id;
						channel_list['amz_access_secret' + channel_list.id] = channel_list.id;
					});	
				},
				err => console.log(err),
					function(){
						//completed callback
					}
				);
		    }
		}
	 
		closeDialog(){
			this.dialogRef.close();
		}

		saveAmazonCredential(form: any) {
			let that = this;
			let data: any = {};
			data = Object.assign({}, this.formModel);
			data.channel_lists.forEach(function(channel_list:any){
				channel_list['channel_id'] = channel_list.id;
				channel_list['company_website_id'] = that._globalService.getWebsiteId();
				channel_list['channel_parrent_id'] = data.parent_id;
				channel_list['company_id'] = that._globalService.getCompanyId();
				that._basicSetupService.saveMarketplaceSettings(channel_list, channel_list.id).subscribe(
				data => {
					if (data.status == 1) {
						that._globalService.showToast('Successfully Saved!');
						this.closeDialog();
					} else {
						this.errorMsg = data.Message;
					}
				},
					err => console.log(err),
					function () {
						//completed callback
					}
				);

			});	
		}
    }



@Component({
	templateUrl: './templates/flipkart_settings.html',
	providers: [BasicSetupService, Global]
})
export class FlipkartAuthenticationComponent implements OnInit {

	public response: any;
	public errorMsg: string;
	public successMsg: string;
	public formModel: any = {};
	public ipaddress: any;
	public parent_id: number = 0;
	@ViewChild(MatAutocompleteTrigger) trigger;
	constructor(
		private _basicSetupService: BasicSetupService,
		public _globalService: GlobalService,
		private _global: Global,
		private _router: Router,
		private dialogRef: MatDialogRef<FlipkartAuthenticationComponent>,
		public dialog: MatDialog,
		@Optional() @Inject(MAT_DIALOG_DATA) public data: any
	) {
		dialog.afterOpen.subscribe(() => {
			let containerElem: HTMLElement = <HTMLElement>document.getElementsByClassName('mat-dialog-container')[0];
			containerElem.classList.remove('pop-box-up');
		});
		this.ipaddress = _globalService.getCookie('ipaddress');
	}

	ngOnInit() {
		this.formModel.parent_id = +this.data.parent_id;
		
		this.formModel.channel_id = this.formModel.parent_id;
		this.formModel.website_id = this.formModel.settingsId; // getting website id from the cookies
		if (this.formModel.parent_id > 0) {
			this._basicSetupService.loadChannelSettings(this.formModel.channel_id, this.formModel.website_id).subscribe(
				data => {
					this.response = data;
					if (data.status == 1) {
						this.formModel.fullfilment_by = this.response.credentials[0].fullfilment_by;
						this.formModel.username = this.response.credentials[0].username;
						this.formModel.password = this.response.credentials[0].password;
					} else {
						this.formModel.fullfilment_by = 'standard';
					}
				},
				err => console.log(err),
				function () {
					//completed callback
				}
			);
		}
	}

	closeDialog() {
		this.dialogRef.close();
	}

	saveFlipkartCredential(form: any) {
		let that = this;
		this.errorMsg = '';
		let channel_id :  number;
		let data: any = {};
		data = Object.assign({}, this.formModel);
		
		channel_id = data.parent_id;
		data['company_website_id'] = that._globalService.getWebsiteId();
		data['company_id'] = that._globalService.getCompanyId();
		this._basicSetupService.saveMarketplaceSettings(data, channel_id).subscribe(
			data => {
				if (data.status == 1) {
					that._globalService.showToast('Successfully Saved!');
					this.closeDialog();
				} else {
					this.errorMsg = data.Message;
				}
			},
			err => console.log(err),
			function () {
				//completed callback
			}
		);
	}
}



@Component({
	templateUrl: './templates/snapdeal_settings.html',
	providers: [BasicSetupService, Global]
})
export class SnapdealAuthenticationComponent implements OnInit {

	public response: any;
	public errorMsg: string;
	public successMsg: string;
	public formModel: any = {};
	public ipaddress: any;

	@ViewChild(MatAutocompleteTrigger) trigger;
	constructor(
		private _basicSetupService: BasicSetupService,
		public _globalService: GlobalService,
		private _global: Global,
		private _router: Router,
		private dialogRef: MatDialogRef<SnapdealAuthenticationComponent>,
		public dialog: MatDialog,
		@Optional() @Inject(MAT_DIALOG_DATA) public data: any
	) {
		dialog.afterOpen.subscribe(() => {
			let containerElem: HTMLElement = <HTMLElement>document.getElementsByClassName('mat-dialog-container')[0];
			containerElem.classList.remove('pop-box-up');
		});
		this.ipaddress = _globalService.getCookie('ipaddress');
	}

	ngOnInit() {
		this.formModel.parent_id = +this.data.parent_id;
		this.formModel.channel_id = +this.formModel.parent_id;
		this.formModel.website_id = this.formModel.settingsId; // getting website id from the cookies
		if (this.formModel.parent_id > 0) {
			this._basicSetupService.loadChannelSettings(this.formModel.parent_id, this.formModel.website_id).subscribe(
				data => {
					this.formModel = Object.assign(this.formModel, data.credentials[0]);
				},
				err => console.log(err),
				function () {
					//completed callback
				}
			);
		}
	}

	saveSnapdealSettings(form: any) {
		let that = this;
		this.errorMsg = '';
		let channel_id: number;
		let data: any = {};
		data = Object.assign({}, this.formModel);

		channel_id = data.parent_id;
		data['company_website_id'] = that._globalService.getWebsiteId();
		data['company_id'] = that._globalService.getCompanyId();
		//{ "name": "xddf", "username": "asdadasdasd", "refreshtoken": "676655ba-269b-337b-975b-9b5eeb0e2575", "channel_id": 21, "parent_id": 21, "company_website_id": 1, "company_id": 1 }
		this._basicSetupService.saveMarketplaceSettings(data, channel_id).subscribe(
			data => {
				if (data.status == 1) {
					that._globalService.showToast('Successfully Saved!');
					this.closeDialog();
				} else {
					this.errorMsg = data.Message;
				}
			},
			err => console.log(err),
			function () {
				//completed callback
			}
		);
	}

	closeDialog() {
		this.dialogRef.close();
	}
}


@Component({
	templateUrl: './templates/paytm_settings.html',
	providers: [BasicSetupService, Global]
})
export class PaytmAuthenticationComponent implements OnInit {

	public response: any;
	public errorMsg: string;
	public successMsg: string;
	public formModel: any = {};
	public ipaddress: any;

	@ViewChild(MatAutocompleteTrigger) trigger;
	constructor(
		private _basicSetupService: BasicSetupService,
		public _globalService: GlobalService,
		private _global: Global,
		private _router: Router,
		private dialogRef: MatDialogRef<PaytmAuthenticationComponent>,
		public dialog: MatDialog,
		@Optional() @Inject(MAT_DIALOG_DATA) public data: any
	) {
		dialog.afterOpen.subscribe(() => {
			let containerElem: HTMLElement = <HTMLElement>document.getElementsByClassName('mat-dialog-container')[0];
			containerElem.classList.remove('pop-box-up');
		});
		this.ipaddress = _globalService.getCookie('ipaddress');
	}

	ngOnInit() {
		this.formModel.parent_id = +this.data.parent_id;
		this.formModel.channel_id = +this.formModel.parent_id;
		this.formModel.website_id = this.formModel.settingsId; // getting website id from the cookies
		if (this.formModel.parent_id > 0) {
			this._basicSetupService.loadChannelSettings(this.formModel.parent_id, this.formModel.website_id).subscribe(
				data => {
					this.response = data;
					this.formModel.username = this.response.credentials[0].username;
					this.formModel.password = this.response.credentials[0].password;
					this.formModel.client_id = this.response.credentials[0].client_id;
					this.formModel.secret_code = this.response.credentials[0].secret_code;
					this.formModel.paytm_merchant_id = this.response.credentials[0].paytm_merchant_id;
					this.formModel.fullfilment_by = this.response.credentials[0].fullfilment_by;
				},
				err => console.log(err),
				function () {
					//completed callback
				}
			);
		}
	}

	savePaytmSettings(form: any) {
		let that = this;
		this.errorMsg = '';
		let channel_id: number;
		let data: any = {};
		data = Object.assign({}, this.formModel);
		channel_id = data.parent_id;
		data['company_website_id'] = that._globalService.getWebsiteId();
		data['company_id'] = that._globalService.getCompanyId();
		//{ "name": "xddf", "username": "asdadasdasd", "refreshtoken": "676655ba-269b-337b-975b-9b5eeb0e2575", "channel_id": 21, "parent_id": 21, "company_website_id": 1, "company_id": 1 }
		this._basicSetupService.saveMarketplaceSettings(data, channel_id).subscribe(
			data => {
				//console.log(data);
				if (data.status == 1) {
					that._globalService.showToast('Successfully Saved!');
					this.closeDialog();
				} else {
					this.errorMsg = data.Message;
				}
			},
			err => console.log(err),
			function () {
				//completed callback
			}
		);
	}

	closeDialog() {
		this.dialogRef.close();
	}
}

@Component({
	templateUrl: './templates/ebay_settings.html',
	providers: [BasicSetupService, Global],
	animations: [AddEditTransition]
})
export class EbayAuthenticationComponent implements OnInit {
	public response: any;
	public errorMsg: string;
	public successMsg: string;
	public formModel: any = {};
	public ipaddress: any;
	@ViewChild(MatAutocompleteTrigger) trigger;
	constructor(
		private _basicSetupService: BasicSetupService,
		public _globalService: GlobalService,
		private _global: Global,
		private _router: Router,
		private dialogRef: MatDialogRef<EbayAuthenticationComponent>,
		public dialog: MatDialog,
		@Optional() @Inject(MAT_DIALOG_DATA) public data: any
	) {
		dialog.afterOpen.subscribe(() => {
			let containerElem: HTMLElement = <HTMLElement>document.getElementsByClassName('mat-dialog-container')[0];
			containerElem.classList.remove('pop-box-up');
		});
		this.ipaddress = _globalService.getCookie('ipaddress');
	}

	ngOnInit() {
		this.formModel.parent_id = this.data.parent_id
		this.formModel.website_id = this.formModel.settingsId;
		if (this.formModel.parent_id > 0) {
			this._basicSetupService.loadChannelSettings(this.formModel.parent_id, this.formModel.website_id).subscribe(
				data => {
					this.response = data;
					this.formModel.channel_lists = this.response.credentials;
					this.formModel.channel_lists.forEach(function (channel_list: any) {
						channel_list['username' + channel_list.id] = channel_list.id;
					});	
				},
				err => console.log(err),
				function () {
					//completed callback
				}
			);
		}
	}

	saveEbayCredentials(form: any) {
		let that = this;
		let data: any = {};
		//console.log(this.formModel)
		data = Object.assign({}, this.formModel);
		data.channel_lists.forEach(function(channel_list:any){
			channel_list['channel_id'] = channel_list.id;
			channel_list['company_website_id'] = that._globalService.getWebsiteId();
			channel_list['channel_parrent_id'] = data.parent_id;
			channel_list['company_id'] = that._globalService.getCompanyId();
			if (data.username == 'undefined') {
				channel_list['username'] = '';
			}
			that._basicSetupService.saveMarketplaceSettings(channel_list, channel_list.id).subscribe(
			data => {
				if (data.status == 1) {
					that._globalService.showToast('Successfully Saved!');
					
				} else {
					this.errorMsg = data.Message;
				}
			},
				err => console.log(err),
				function () {
					//completed callback
				}
			);

		});	
	}
	
	closeDialog() {
		this.dialogRef.close();
	}
}



@Component({
	templateUrl: './templates/table_rate.html',
	providers: [BasicSetupService, Global],	
})
export class TableRateAddEditComponent implements OnInit {
	public response: any;
	public errorMsg: string;
	public successMsg: string;
	public formModel: any = {};
	public ipaddress: any;
	public country_list: any = [];
	public state_list: any = [];
	public tdStates = [];
	public selectedStateList = [];
	public sample_xls: any;
	public import_files:any;
	public website_id_new :any;
	@ViewChild(MatAutocompleteTrigger) trigger;
	constructor(
		private _basicSetupService: BasicSetupService,
		public _globalService: GlobalService,
		private _global: Global,
		private _router: Router,
		private dialogRef: MatDialogRef<TableRateAddEditComponent>,
		public dialog: MatDialog,
		@Optional() @Inject(MAT_DIALOG_DATA) public data: any
	) {
		dialog.afterOpen.subscribe(() => {
			let containerElem: HTMLElement = <HTMLElement>document.getElementsByClassName('mat-dialog-container')[0];
			containerElem.classList.remove('pop-box-up');
		});
		this.ipaddress = _globalService.getCookie('ipaddress');
	}

	ngOnInit() {
		this.sample_xls = window.location.protocol + '//' + window.location.hostname + ':8085' + '/media/importfile/sample/tablerates_weight_xls.xls';
		this.formModel.handling_fees_type = '0';
		this.formModel.matrix_type = '0';
		this.formModel.shipping_method_id = this.data.shipping_master_type_id;
		this.formModel.shipping_id = this.data.id;
		this.formModel.shipping_master_type_id  =this.data.shipping_master_type_id
		if (this.formModel.shipping_id>0) {
			this._basicSetupService.shippingLoad(this.formModel.shipping_id,this.formModel.shipping_master_type_id).subscribe(
		       	data => {
		       		this.response = data;
		       		this.formModel.title =  this.response.title;
		       	},
		       	err => console.log(err),
		       	function(){
		       		//completed callback
		       	}
		    );
		} 
	}

	closeDialog() {
		this.dialogRef.close();
	}

	browseFileXLSTableRate(e: Event) {
		let files: any = {};
		let target: HTMLInputElement = e.target as HTMLInputElement;
		for (let i = 0; i < target.files.length; i++) {
			let file_arr: any = [];

			let reader = new FileReader();
			reader.readAsDataURL(target.files[i]);
			reader.onload = (event) => {
				file_arr['url'] = event.srcElement['result']
			}

			file_arr['_file'] = target.files[i];
			files['import_file'] = file_arr;
		}
		this.import_files = files.import_file._file;
		let filename = files.import_file._file.name;
		let extn = filename.split(".").pop();
		if (extn == 'xls' || extn == 'xlsx') {
			//this.dialogRef.close(files);
		}
		else {
			this._globalService.showToast('Please choose XLS/XLSX file');
		}
	}

	saveTableRate(form:any) {
			let data: any = {};
			this.website_id_new = 1;
			data  =  this.formModel;
			data.website_id = 1;
			let form_data = new FormData();
      		form_data.append('data', JSON.stringify(data));
      		form_data.append("import_file", this.import_files);
			form_data.append('website_id', this.website_id_new);
			
			this._basicSetupService.saveFlatRateData(form_data).subscribe(
			data => {
				this.dialogRef.close();
			},
			err => {
				this._globalService.showToast('Something went wrong. Please try again.');
			},
			function () {
				//completed callback
			}
		);
	}

	applicable_shippings(event,title,shipping_method_id) {
		 console.log(event);
	}
}


@Component({
	templateUrl: './templates/free-shipping.html',
	providers: [BasicSetupService, Global],	
})
export class FreeShippingComponent implements OnInit {

	public response: any;
	public errorMsg: string;
	public successMsg: string;
	public formModel: any = {};
	public ipaddress: any;
	public country_list: any = [];
	public state_list: any = [];

	public tdStates = [];
	public selectedStateList = [];
	public sample_xls: any;
	public import_files:any;
	public website_id_new :any;
	@ViewChild(MatAutocompleteTrigger) trigger;
	constructor(
		private _basicSetupService: BasicSetupService,
		public _globalService: GlobalService,
		private _global: Global,
		private _router: Router,
		private dialogRef: MatDialogRef<FreeShippingComponent>,
		public dialog: MatDialog,
		@Optional() @Inject(MAT_DIALOG_DATA) public data: any
	) {
		dialog.afterOpen.subscribe(() => {
			let containerElem: HTMLElement = <HTMLElement>document.getElementsByClassName('mat-dialog-container')[0];
			containerElem.classList.remove('pop-box-up');
		});
		this.ipaddress = _globalService.getCookie('ipaddress');
	}

	ngOnInit() {
		this.formModel.shipping_method_id = this.data.shipping_master_type_id;
		this.loadCountry();
		this.formModel.shipping_id = this.data.id;
		this.formModel.shipping_master_type_id  =this.data.shipping_master_type_id
		if (this.formModel.shipping_id>0) {
			this._basicSetupService.shippingLoad(this.formModel.shipping_id,this.formModel.shipping_master_type_id).subscribe(
		       	data => {
		       		this.response = data;
		       		this.formModel.title = this.response.shipping_info[0].title;
		       		this.formModel.description = this.response.shipping_info[0].description;
		       		this.formModel.shipping_id = this.response.shipping_info[0].id;
		       		this.formModel.is_ebay = (this.response.shipping_info[0].is_ebay=='y')? true : false;
							this.formModel.country_ids = parseInt(this.response.shipping_info[0].country_ids);
							this.formModel.minimum_order_amount = parseInt(this.response.shipping_info[0].minimum_order_amount);
							let selected_states = this.response.shipping_info[0].state_id.split(',');
							selected_states = selected_states.map(Number);
							this.formModel.state_id = selected_states;
		       		this.get_states(this.response.shipping_info[0].country_ids);		       		
		       	},
		       	err => console.log(err),
		       	function(){
		       		//completed callback
		       	}
		    );
		} else {
			this.formModel.shipping_id = 0;
			this.formModel.country_ids = 99;
			this.get_states(this.formModel.country_ids);
		} 
	}

	closeDialog() {
		this.dialogRef.close();
	}

	loadCountry() {
		this._basicSetupService.loadCountry().subscribe(
			data => {
				this.country_list = data.countrylist;				
			},
			err => console.log(err),
			function () {
				//completed callback
			}
		);
	}

	get_states(country_id: number) {
		this._basicSetupService.loadStates(country_id, this.formModel.shipping_method_id).subscribe(
			data => {
				this.state_list = data.states;
			},
			err => console.log(err),
			function () {
			}
		);
	}

	addEditFreeShip (form:any){
		this.errorMsg = '';
	    let data: any = {};
		data.website_id = this.formModel.settingsId;
		data.title =  this.formModel.title;
		data.minimum_order_amount =  this.formModel.minimum_order_amount;
		data.shipping_method_id =  6;
		data.description =  this.formModel.description;
		data.country_ids = this.formModel.country_ids;
		data.shipping_id = this.formModel.shipping_id; 
		data.website_id = this._globalService.getWebsiteId();
		
	    if (this.formModel.state_id.length>0) {
			data['state_id'] = this.formModel.state_id.join(',');
		} else {
    		data['state_id'] = '';
    	}		
	    if ((this.formModel.state_id.length > 0) || this.formModel.state_id==0){
    		this._basicSetupService.shipAddEdit(data,this.formModel.shipId).subscribe(
	           	data => {
	               	this.response = data;
	               	if(this.response.status==1){
	                   this.closeDialog();
	               	}else{
		               this.errorMsg = this.response.Message;
	               	}
	            },
	           	err => console.log(err),
	           	function(){
	                //completed callback
	           	}
	        );
    	}
	}	
}


@Component({
	templateUrl: './templates/cod-zipcode.html',
	providers: [BasicSetupService, Global],	
})
export class CODZipcodeComponent implements OnInit {

	public response: any;
	public errorMsg: string;
	public successMsg: string;
	public formModel: any = {};
	public ipaddress: any;
	public country_list: any = [];
	public state_list: any = [];

	public tdStates = [];
	public selectedStateList = [];
	public sample_xls: any;
	public import_files:any;
	public website_id_new :any;
	public file_selection_tool: any;
	@ViewChild(MatAutocompleteTrigger) trigger;
	constructor(
		private _basicSetupService: BasicSetupService,
		public _globalService: GlobalService,
		private _global: Global,
		private _router: Router,
		private dialogRef: MatDialogRef<CODZipcodeComponent>,
		public dialog: MatDialog,
		@Optional() @Inject(MAT_DIALOG_DATA) public data: any
	) {
		dialog.afterOpen.subscribe(() => {
			let containerElem: HTMLElement = <HTMLElement>document.getElementsByClassName('mat-dialog-container')[0];
			containerElem.classList.remove('pop-box-up');
		});
		this.ipaddress = _globalService.getCookie('ipaddress');
	}

	ngOnInit() {
		this.sample_xls = window.location.protocol + '//' + window.location.hostname + ':8085' + '/media/importfile/sample/COD_rate_sheet_boostmysale.xls';
		this.formModel.shipping_master_type_id  =this.data.shipping_master_type_id;
		this.file_selection_tool = 'No file choosen';
	}

	closeDialog() {
		this.dialogRef.close();
	}

	browseFileXLSFedexZicopcode(e: Event) {
		let files: any = {};
		let target: HTMLInputElement = e.target as HTMLInputElement;
		for (let i = 0; i < target.files.length; i++) {
			let file_arr: any = [];

			let reader = new FileReader();
			reader.readAsDataURL(target.files[i]);
			reader.onload = (event) => {
				file_arr['url'] = event.srcElement['result']
			}

			file_arr['_file'] = target.files[i];
			files['import_file'] = file_arr;
		}
		this.import_files = files.import_file._file;
		let filename = files.import_file._file.name;
		this.file_selection_tool = filename;
		let extn = filename.split(".").pop();
		if (extn == 'xls' || extn == 'xlsx') {
			//this.dialogRef.close(files);
		}
		else {
			this._globalService.showToast('Please choose XLS/XLSX file');
		}
	}

	saveFedexZicopcode(form:any) {
		let data: any = {};
		this.website_id_new = this.formModel.settingsId;
		data  =  this.formModel;
		data.website_id = this.formModel.settingsId;
		let form_data = new FormData();
			form_data.append('data', JSON.stringify(data));
			form_data.append("import_file", this.import_files);
			form_data.append('website_id', this.website_id_new);
			form_data.append('title', this.formModel.title);
			form_data.append('description', this.formModel.description);
		if(this.import_files != undefined) {
			this._basicSetupService.saveCODZipcodes(form_data).subscribe(
			data => {
				this.dialogRef.close();
			},
			err => {
				this._globalService.showToast('Something went wrong. Please try again.');
			},
			function () {
				//completed callback
			});
		} else {
			this._globalService.showToast('Please choose XLS/XLSX file');
		}
	}

	applicable_shippings(event) {
		console.log(event);
	}
}




