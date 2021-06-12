import { Component, OnInit, Inject, ViewChild } from '@angular/core';
import { Router,ActivatedRoute } from '@angular/router';
import { StoreCategoryService } from './settings.store-category.service';
import { GlobalService } from '../../global/service/app.global.service';
import {Global} from '../../global/service/global';
import { AddEditTransition } from '../.././addedit.animation';
import { GooglePlaceDirective } from 'ngx-google-places-autocomplete';
import { Address } from 'ngx-google-places-autocomplete/objects/address';
import { GlobalVariable } from '../../global/service/global';
@Component({
  templateUrl: './templates/add_store_category.html',
  providers: [StoreCategoryService]
})
export class storeCategoryAddEditComponent implements OnInit {
		
	public tabIndex: number;
	public parentId: number = 0;
	private sub: any;
	public formModel: any = {};
	public saveButton:boolean = false;
	public file_selection_tool: any;
	public xls_file: any;
	public popupLoder:boolean = false;
	public parent_category_list:any = [];

	constructor(
		private _storeCategoryService:StoreCategoryService,
		public _globalService:GlobalService,
		private _router: Router,
		private _route: ActivatedRoute ,
		private _global:Global,
	) {}

	ngOnInit(){
		this.file_selection_tool = 'No file choosen';
		this.sub = this._route.params.subscribe(params => {
			this.formModel.storeCategoryId = +params['id']; // (+) converts string 'id' to a number
		 });
		 this.tabIndex = +this._globalService.getCookie('active_tabs'); // current active tab index
		 this.parentId = this._globalService.getParentTab(this.tabIndex); // parent id of the current active tab
		 this.loadParentcategory();
		 if(this.formModel.storeCategoryId>0){
			this._storeCategoryService.storeCategoryLoad(this.formModel.storeCategoryId).subscribe(
				response => {
					console.log(response)
					console.log(response.data)
					console.log(response.data.image)
						if(response.data.image != '' && response.data.image!= null) {
							this.formModel.fileUrl = GlobalVariable.S3_URL+"storecategorylogo/200x200/"+response.data.image;
							this.formModel.storecategory_logo = response.data.image;
						} else {
							this.formModel.fileUrl = '';
						} 
						this.formModel.store_name = response.data.name;
						this.formModel.sequence_number = response.data.order;
						if(response.data.store_type_categories_selected != null &&  response.data.store_type_categories_selected !='') {
							this.formModel.store_type_categories_selected = response.data.store_type_categories_selected.split(",").map(Number);
						} else {
							this.formModel.store_type_categories_selected = response.data.store_type_categories_selected;
						}
						
				},
				err => console.log(err),
				function(){
					//completed callback
				}
			);
		}else{
			this.formModel.storeCategoryId = 0;
		}
	}

	loadParentcategory() {
		this._global.getWebServiceData('category_load','GET','','').subscribe(
			data => {
				if(data.status == 1) {
					this.parent_category_list = data.category
				} else {
					this.parent_category_list = []
				}
				
			}, err => {

			}, function() {

			}
		)
	}

	addEditStoreCategory(form: any){
		console.log(this.formModel.fileUrl)
		if(this.formModel.fileUrl!=undefined){
			var data: any = {};
			data = Object.assign({}, this.formModel);
			data.website_id = this._globalService.getWebsiteId();			
			console.log(data)
			this._storeCategoryService.storeCategoryAddEdit(data,this.formModel.warehouseId).subscribe(data => {
					if(data.status == 1){
						this._globalService.deleteTab(this.tabIndex,this.parentId);
					}
				},
				err => console.log(err),
				function(){
				}
			);
		}else{
			this._globalService.showToast('Pleas select a logo');
		}
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
			form_data.append("module_name",'storecategorylogo');
			this.popupLoder = true;	
			this._global.uploadFile('upload-image', 'POST', form_data).subscribe(
				results => { // Assign the Uploaded data into formModel
					if (results["status"] == '1') {
						this.formModel.fileUrl = results["AMAZON_IMAGE_URL"] + results["data"][0].link800 ;
						this.formModel.storecategory_logo = results["data"][0].file_name;
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
	
}
