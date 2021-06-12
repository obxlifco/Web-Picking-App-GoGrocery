import { Component, OnInit, Inject, ViewChild } from '@angular/core';
import { Router,ActivatedRoute } from '@angular/router';
import { WarehouseService } from './inventory.warehouse.service';
import { GlobalService } from '../../global/service/app.global.service';
import {Global} from '../../global/service/global';
import { AddEditTransition } from '../.././addedit.animation';
import { GooglePlaceDirective } from 'ngx-google-places-autocomplete';
import { Address } from 'ngx-google-places-autocomplete/objects/address';
import { GlobalVariable } from '../../global/service/global';
@Component({
  templateUrl: './templates/add_warehouse.html',
  providers: [WarehouseService],
  animations: [ AddEditTransition ],
  host: {
    '[@AddEditTransition]': ''
  },
})

export class WarehouseAddEditComponent implements OnInit {
	@ViewChild("placesRef") placesRef : GooglePlaceDirective;
	public response: any;
	public errorMsg: string;
	public successMsg: string;
	public formModel: any = {};
	public List:any={}
	private sub: any;
	public tabIndex: number;
	public parentId: number = 0;
	public saveButton:boolean = false;
	public file_selection_tool: any;
	public xls_file: any;
	public popupLoder:boolean = false;
	public category_list: any = [];
	public store_type_list: any = [];
	public payment_option_list: any = [];
	public selectedCategory;
	public selectedStoreType;
	public selectedPaymentOption;
	public warehouseCategoryList: any = [];
	public storeTypeList: any = [];
	public paymentOptionList: any = [];
	public existing_selected_categories: any = [];
	
	constructor(
		private _warehouseService:WarehouseService,
		public _globalService:GlobalService,
		private _router: Router,
		private _route: ActivatedRoute ,
		private _global:Global,
	) {}
	ngOnInit(){
		this.file_selection_tool = 'No file choosen';
		this.sub = this._route.params.subscribe(params => {
	       this.formModel.warehouseId = +params['id']; // (+) converts string 'id' to a number
		});
		this.tabIndex = +this._globalService.getCookie('active_tabs'); // current active tab index
		this.parentId = this._globalService.getParentTab(this.tabIndex); // parent id of the current active tab		
		this._warehouseService.warehouseLoad(this.formModel.warehouseId).subscribe(
	       	data => {
				this.response = data;
	       		if(this.formModel.warehouseId>0) {
		            this.formModel = this.response.warehouse;
		            this.formModel.warehouseId = this.response.warehouse.id;
					this.formModel.country_id = this.response.warehouse.country_id;
					// if(this.formModel.country_id == 99){
					// 	this.formModel.country_id = null;
					// }
		            this.List.country_list=this.response.countries;
	       			this.List.channel_list=this.response.channel;
					this.List.user_list=this.response.users;
					if(this.response.warehouse.warehouse_logo != '' && this.response.warehouse.warehouse_logo!= null) {
						this.formModel.fileUrl = GlobalVariable.S3_URL+"warehouselogo/200x200/"+this.response.warehouse.warehouse_logo;
					} else {
						this.formModel.fileUrl = '';
					}   
	       			let that = this;
	       			var values_country:any=[];
	       			var values_channel:any=[];
	       			var values_user:any=[];
	       			this.List.country_list.forEach(function(item:any){
	       				if(item.status==1){
	       					values_country.push(item.id);
		        	    }    
		              });
	       			this.List.channel_list.forEach(function(item:any){
	       				if(item.status==1){
	       					values_channel.push(item.id);
		        	    }    
		              });
	       			this.List.user_list.forEach(function(item:any){
	       				if(item.status==1){
	       					values_user.push(item.id);
		        	    }    
		              });
	       			this.formModel.applicable_country_id=values_country;	
	       			this.formModel.applicable_channel_id=values_channel;	
					this.formModel.manager_id=values_user;

					if(this.response.warehouse_category.length > 0){
						this.warehouseCategoryList = this.response.warehouse_category;
						let ware_house_category:any = [];
						this.warehouseCategoryList.forEach(element => {
							ware_house_category.push(element['category']);
						});
						let warehouseCategoryIds = ware_house_category.join(',');
						var warehouseCategoryIdArray = warehouseCategoryIds.split(",").map(Number);
						
						this.selectedCategory = warehouseCategoryIdArray;
						this.existing_selected_categories = warehouseCategoryIdArray;
					}

					if(this.response.store_type.length > 0){
						this.storeTypeList = this.response.store_type;
						let store_type: any = [];
						this.storeTypeList.forEach(element => {
							store_type.push(element['type']);
						});
						let storeTypeIds = store_type.join(',');
						var storeTypeIdArray = storeTypeIds.split(",").map(Number);
						this.selectedStoreType = storeTypeIdArray;
					}

					if(this.response.payment_option.length > 0){
						this.paymentOptionList = this.response.payment_option;
						let payment_option_type: any = [];
						this.paymentOptionList.forEach(element => {
							payment_option_type.push(element['payment_method_id']);
						});
						let paymentOptionIds = payment_option_type.join(',');
						var paymentOptionIdArray = paymentOptionIds.split(",").map(Number);
						this.selectedPaymentOption = paymentOptionIdArray;
					}

					if(this.response.warehouse.expected_delivery_time){
						this.formModel.expected_delivery_time = this.response.warehouse.expected_delivery_time;
					}else{
						this.formModel.expected_delivery_time = 2;
						
					}
					   
	       		} else {
					this.formModel.warehouseId = 0;
					this.formModel.expected_delivery_time = 0;
	       			this.List.country_list=this.loadCountry();
	       			//this.List.channel_list=this.response.channel;
	       			this.loadChannels();
	       			this.List.user_list=this.response.users;
	       			this.formModel.country_id = 99;
				}
				// if(this.formModel.country_id == null){  
				// 	this.get_states(99);
				// }else{
				// 	this.get_states(this.formModel.country_id);
				// }
				this.loadCategoryType();
				this.loadStoreType();
				this.getPaymentMethod();
				this.get_states(this.formModel.country_id);
	       	},
	       	err => console.log(err),
	       	function(){
	       		//completed callback
	       	}
	    );
	}

	getStoreTypeCategory(store_type_ids) {
		console.log(store_type_ids);
		let data :any = {}
		data.store_type_ids = store_type_ids;
		this._global.getWebServiceData('get_store_type_categories','POST',data,'').subscribe(
		result => {
			console.log(result.data);
			if(result.data.length > 0) {
				let ware_house_category:any = [];
				result.data.forEach(element => {
					ware_house_category.push(element['id']);
				});
				let warehouseCategoryIds = ware_house_category.join(',');
				var warehouseCategoryIdArray = warehouseCategoryIds.split(",").map(Number);

				//let selected_store_type_category = this.existing_selected_categories.concat(warehouseCategoryIdArray);
				let selected_store_type_category = warehouseCategoryIdArray;
				
				let unique_store_type_category = Array.from(new Set(selected_store_type_category)); 
				this.selectedCategory = unique_store_type_category;
			}					
		}, err => {

		})
	}

	getPaymentMethod(){
		this._warehouseService.getPaymentMethod().subscribe(response => {
		console.log(response)
		let data: any =[];
		let paymentOptionList: any = [];
		data = response.api_status;
		console.log(data)
		data.forEach(element => {
			paymentOptionList.push(element.engageboost_paymentgateway_method_id);
		});
		console.log(paymentOptionList)
		let obj = {};
		obj["id"]= 0 ;
		obj["name"]='All';
		paymentOptionList.splice(0, 0, obj);
		this.payment_option_list = paymentOptionList;
		},
		err => console.log(err),
		function(){
			//completed callback
		});
	}

	loadCategoryType(){
		this._warehouseService.getAllCategory().subscribe(
			Response => {
				console.log(Response)
				if(Response.data.length > 0){
					let obj = {};
					obj["id"]= 0 ;
					obj["name"]='All';
					this.category_list = Response.data;
					this.category_list.splice(0, 0, obj);
				}else{
					this.category_list = Response.data;
				}
			},
			err => console.log(err),
			function(){
				//completed callback
			}
	 	);
	}

	loadStoreType(){
		this._warehouseService.getAllStoreType().subscribe(
			Response => {
				console.log(Response)
				let obj = {};
				obj["id"]= 0 ;
				obj["name"]='All';
				this.store_type_list = Response.data;
				this.store_type_list.splice(0, 0, obj);
			},
			err => console.log(err),
			function(){
				//completed callback
			}
	 	);
	}

	selectWarehouseLogo(e: Event) {
		this.saveButton = true;
		var files: any = {};
		var target: HTMLInputElement = e.target as HTMLInputElement;
		for (var i = 0; i < target.files.length; i++) {
			var file_arr: any = [];

			var reader = new FileReader();
			reader.readAsDataURL(target.files[i]);
			reader.onload = (event) => {
				file_arr['url'] = event.srcElement['result']
			}

			file_arr['_file'] = target.files[i];
			files['import_file'] = file_arr;
		}
		var filename = files.import_file._file.name;
		this.file_selection_tool = filename;
		this.xls_file = files.import_file._file;
		var extn = filename.split(".").pop();
		extn = extn.toLowerCase();
		if (extn == 'png' || extn == 'jpg' || extn == 'jpeg') {
			let data:any = {};
			let website_id:any = this._globalService.getWebsiteId();
			
			var form_data = new FormData();
			form_data.append("import_file", this.xls_file);
			form_data.append("website_id", website_id);
			form_data.append("module_name",'warehouselogo');
			this.popupLoder = true;	
			this._global.uploadFile('upload-image', 'POST', form_data).subscribe(
				results => { // Assign the Uploaded data into formModel
					if (results["status"] == '1') {
						this.formModel.fileUrl = results["AMAZON_IMAGE_URL"] + results["data"][0].link200 ;
						this.formModel.warehouse_logo = results["data"][0].file_name;
						this.saveButton = false;
					}
					this.popupLoder = false;
				},
				err => {

					this.popupLoder = false;
				}
			) 
		} else {
			this._globalService.showToast('Only JPEG,JPG,PNG file is allowed.');
		}
	}

	loadChannels() {
        this._global.getWebServiceData('marketplace_list','GET','','').subscribe(data => {
            if (data.status == 1) {
                this.List.channel_list = data.api_status; // list of marketplace
            }
        }, err => {}, function() { // call back function when exection is done
       	})
    }

    loadCountry() {
        this._global.getWebServiceData('countrylist','GET','','').subscribe(data => {
            this.List.country_list = data.countrylist; // list of country list
        }, err => {}, function() { // call back function when exection is done
        })
    }

	get_states(id:any){
		var country_id = id;
	      if(country_id>0){
	       this._warehouseService.warehouseState(country_id).subscribe(
           	data => {
               	this.response = data;
               	if(this.response){
                  	this.List.state_list=this.response.state_arr;
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
	}

	getStates(id:any){
		this.formModel.state_id = null;
		var country_id = id;
	      if(country_id>0){
	       this._warehouseService.warehouseState(country_id).subscribe(
           	data => {
               	this.response = data;
               	if(this.response){
                  	this.List.state_list=this.response.state_arr;
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
	}

	colorChange(color:any){
		if(color!=''){
			this.formModel.text_color=color;
		}
	}
    addEditWarehouse(form: any){
		if(this.formModel.fileUrl!=''){
			this.errorMsg = '';
			
			var data: any = {};
			data = Object.assign({}, this.formModel);
			data.website_id = 1;
			data.store_category_type = [];
			data.store_category = [];
			data.payment_option = [];

			if(this.selectedStoreType){
				data.store_category_type = this.selectedStoreType;
				if(data.store_category_type.includes(0)){
					data.store_category_type = [];
					this.store_type_list.forEach(e => {
						if(e['id'] != 0){
							data.store_category_type.push(e['id']);
						}
					});
				}
			}
			if(this.selectedCategory){
				data.store_category = this.selectedCategory;
				if(data.store_category.includes(0)){
					data.store_category = [];
					this.category_list.forEach(e => {
						if(e['id'] != 0){
							data.store_category.push(e['id']);
						}
					});
				}
			}
			if(this.selectedPaymentOption){
				data.payment_option = this.selectedPaymentOption;
				if(data.payment_option.includes(0)){
					data.payment_option = [];
					this.payment_option_list.forEach(element => {
						if(element['id'] !=0){
							data.payment_option.push(element['id']);
						}
					});
				}
			}
			if(this.formModel.applicable_country_id){
				data.applicable_country_id = this.formModel.applicable_country_id.join();
			}
			else{data.applicable_country_id ='';}
			if(this.formModel.applicable_channel_id){
				data.applicable_channel_id = this.formModel.applicable_channel_id.join();
			}
			else{data.applicable_channel_id ='';}
			if(this.formModel.manager_id){
				data.manager_id = this.formModel.manager_id.join();
			}
			else{data.manager_id ='';}
			if(this.formModel.warehouseId<1){
			data.createdby = this._globalService.getUserId();
			}
			data.updatedby = this._globalService.getUserId();
			
			this._warehouseService.warehouseAddEdit(data,this.formModel.warehouseId).subscribe(
				data => {
					this.response = data;
				
					if(this.response.status==1){
					
						this._globalService.deleteTab(this.tabIndex,this.parentId);

					}else{
					
					this.errorMsg = this.response.message;
					}
				},
				err => console.log(err),
				function(){
					//completed callback
				}
			);
		}else{
			this._globalService.showToast('Pleas select a logo');
			
		}
	}
	public handleAddressChange(address: Address) {
		// Do some stuff
		this.formModel.address=address.formatted_address;
		this.formModel.longitude=address.geometry.location.lng();
		this.formModel.latitude=address.geometry.location.lat();
		// this.formModel.max_distance_sales="25";
	}
	isNumber(evt) {
		// evt = (evt) ? evt : window.event;
		// var charCode = (evt.which) ? evt.which : evt.keyCode;
		// if (charCode > 31 && (charCode < 48 || charCode > 57)) {
		// 	return false;
		// }
		// return true;
		try{
			var charCode = (evt.which) ? evt.which : evt.keyCode;
			if(charCode==46){
				var txt=this.formModel.max_distance_sales;
				if(!(txt.indexOf(".") > -1)){
					return true;
				}
			}
			if (charCode > 31 && (charCode < 48 || charCode > 57) )
				return false;
			return true;
		}catch(w){
			// alert(w);
		}
	}
	
}
