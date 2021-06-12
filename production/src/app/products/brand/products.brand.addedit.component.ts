import { Component, OnInit, Inject, Optional,ElementRef,ViewChild } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA, MatDialog } from '@angular/material';
import { Router } from '@angular/router';
import { BrandService } from './products.brand.service';
import { GlobalService } from '../../global/service/app.global.service';
import { Global, GlobalVariable } from '../../global/service/global';
import { CookieService } from 'ngx-cookie';

// Warehouse selection auto 
import {COMMA, ENTER} from '@angular/cdk/keycodes';
import {MatChipInputEvent} from '@angular/material/chips';
import {MatAutocompleteSelectedEvent, MatAutocomplete} from '@angular/material/autocomplete';
import {FormControl} from '@angular/forms';
import {Observable} from 'rxjs';
import {map,startWith} from 'rxjs/operators';

// Warehouse selection auto 
@Component({
	templateUrl: './templates/add_brands.html',
	providers: [BrandService,Global]
})
export class BrandAddEditComponent implements OnInit {
	public response: any;
	public errorMsg: string;
	public successMsg: string;
	public formModel: any = {};
	public ipaddress: any;
	public all_languages: any = [];
	public xls_file: any;
	public file_selection_tool: any;
	public saveButton:boolean = false;
	public popupLoder:boolean = false;
	public userId: any;
	public warehouse_id: any;
	// Set chip property for warehouse matchip
	public visible:boolean = true;
	public selectable:boolean = true;
	public removable:boolean = true;
	public addOnBlur = true;
	readonly separatorKeysCodes: number[] = [ENTER, COMMA];
	public wareHouseCtrl = new FormControl();
	public filteredWareHouse: Observable<any>;
	public selectedWareHouseList = [];
	public allWareHouseList = [];
	public wareHouseList = [];
	public slug_base: any;
	@ViewChild('fruitInput') fruitInput: ElementRef<HTMLInputElement>;
    @ViewChild('auto') matAutocomplete: MatAutocomplete;

	constructor(
		private _brandService: BrandService,
		private _globalService: GlobalService,
		private _router: Router,
		private dialogRef: MatDialogRef<BrandAddEditComponent>,
		private _cookieService: CookieService,
		public dialog: MatDialog,
		private _global: Global,
		@Optional() @Inject(MAT_DIALOG_DATA) public data: any
	) {
		_global.reset_dialog();
		this.ipaddress = _globalService.getCookie('ipaddress');
		this.allWareHouseList=[{'id':0,'name':'All'}]
		this.getAllWareHouseList();

		let userData = this._cookieService.getObject('userData');
		this.userId = userData['uid'];
		this.warehouse_id = userData['warehouse_id'];
	}

	ngOnInit() {
		this.slug_base = window.location.protocol + '//' + window.location.hostname + ':'+window.location.port + '/brand/';
		this.file_selection_tool = 'No file choosen';
		this.formModel.brandId = this.data;
		this.formModel.status = "n";
		if (this.formModel.brandId > 0) {
			this._brandService.brandLoad(this.formModel.brandId).subscribe(
				data => {
					this.response = data;
					this.all_languages = data.all_languages;
					if (this.formModel.brandId > 0) {
						this.formModel = Object.assign({}, this.response.api_status);
						this.formModel.brandId = this.response.api_status.id;
						this.formModel.brandName = this.response.api_status.name;
						this.formModel.status = this.response.api_status.isblocked;
						this.formModel.slug_url = this.slug_base+this.response.api_status.slug;
						if(this.response.api_status.brand_logo != '' && this.response.api_status.brand_logo!= null															) {
							this.formModel.fileUrl = GlobalVariable.S3_URL+"brand/200x200/"+this.response.api_status.brand_logo;
						} else {
							this.formModel.fileUrl = '';
						}
						// Set selected warehouse list
						this.selectedWareHouseList = this.response.api_status.warehouse ? this.response.api_status.warehouse : [];
						let newlist = []
						newlist = this.allWareHouseList.filter(
							item => !this.selectedWareHouseList.some(other => item['id'] == other['id'])
						);
						if(newlist) {
							this.allWareHouseList = [];
							this.allWareHouseList = newlist;
						}
						this.formModel.show_navigation = 'Y';
					} else {
						this.formModel.brandId = 0;
						this.formModel.status = "n";
						this.formModel.show_navigation = 'Y';
					}
				},
				err => console.log(err),
				function () {
					//completed callback
				}
			);
		} else {
			this._brandService.brandLoad(0).subscribe(
				data => {
					this.response = data;
					if (this.response.status > 0) {
						this.all_languages = data.all_languages;
					}
				},
				err => console.log(err),
				function () {
					//completed callback
				}
			);
			this.formModel.show_navigation = 'Y';
		}
	}

	selectBrandLogo(e: Event) {
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
			form_data.append("module_name",'brand');
			this.popupLoder = true;	
			this._global.uploadFile('upload-image', 'POST', form_data).subscribe(
				results => { // Assign the Uploaded data into formModel
					if (results["status"] == '1') {
						this.formModel.fileUrl = results["AMAZON_IMAGE_URL"] + results["data"][0].link200 ;
						this.formModel.brand_logo = results["data"][0].file_name;
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

	createSlug(value) {
		value = value.trim();
		var slug = '';
		slug = value.toLowerCase().replace(/[^\w ]+/g, '').replace(/ /g, '-');
		 this.formModel.slug_url = this.slug_base +  slug;
	}

	chopSlug(value) {
		value = value.split('/brand/')[1];
		this.formModel.slug_url = value;
	}

	addEditBrand(form: any) {
		this.popupLoder = true;
		this.errorMsg = '';
		var data: any = {};
		data.website_id = this._globalService.getWebsiteId();
		//data.name = this.formModel.brandName;
		Object.keys(this.formModel).forEach(key => {
			let res = key;
			let value = this.formModel[key];
			if (res != this.formModel.brandName && res != this.formModel.status) {
				data[res] = value;
			}
			data.isblocked = this.formModel.status;
		});
		data.name = this.formModel.brandName;
		if (this.formModel.brandId < 1) {
			data.createdby = this.userId;
		}
		data.updatedby = this.userId;
		if (this.ipaddress) {
			data.ip_address = this.ipaddress;
		} else {
			data.ip_address = '';
		}
		// save warehouse data
		data.warehouse = [];
		if(this.warehouse_id && this.warehouse_id > 0 && this.formModel.brandId < 1) {
			data.warehouse.push(this.warehouse_id);
		} else {
			if(this.formModel.show_navigation && this.formModel.show_navigation == 'Y') {
				data.warehouse = this._formatWareHouseforEdit();
				if(data.warehouse.includes(0)){
					data.warehouse=[];
					this.wareHouseList.forEach(e => {
						if(e['id'] != 0){
							data.warehouse.push(e['id']);
						}
					});
				}
			}
		}
		
		data.brand_logo = this.formModel.brand_logo;
		this._brandService.brandAddEdit(data, this.formModel.brandId).subscribe(
			data => {
				this.response = data;
				if (this.response.status == 1) {
					this.popupLoder = false;
					this.closeDialog();
					//this._router.navigate(['/brand/reload']);
				} else {
					this.popupLoder = false;
					this.errorMsg = this.response.message;
				}
			},
			err => console.log(err),
			function () {
				this.popupLoder = false;
				//completed callback
			}
		);
	}

	/**
	 * Method for getting all warehouse list
	 * @access public
	*/
	getAllWareHouseList() {
		let that = this;
		this._brandService.getAllWareHouseList().subscribe(response => {
			if(response && response['status'] == 1 && response['api_status'].length > 0) {
				response['api_status'].forEach(function (item: any) {
					that.allWareHouseList.push({
						'id' : item.id,
						'name' : item.name
					});
				});
				this.wareHouseList = that.allWareHouseList;
			}
		});
	}

	/**
	 * Method for adding a chip of warehouse
     * @param matChipEvent
	*/
	add(event: MatChipInputEvent): void {
    // Add fruit only when MatAutocomplete is not open
    // To make sure this does not conflict with OptionSelected Event
	    if (!this.matAutocomplete.isOpen) {
	      const input = event.input;
	      const value = event.value;
	      // Add our fruit
	      if ((value || '').trim()) {
	        this.selectedWareHouseList.push({name:value.trim()});
	      }
	      // Reset the input value
	      if (input) {
	        input.value = '';
	      }
	      this.wareHouseCtrl.setValue(null);
	    }
	}
	/**
	 * Method for removing a chip event
	 * @param wareHousw
	*/
	remove(wareHouseList): void {
		let all_ware  = {};
		const index = this.selectedWareHouseList.findIndex(wareHouse => {
			return wareHouse.id == wareHouseList;
		});
	    if (index >= 0) {
	      	this.allWareHouseList.push(this.selectedWareHouseList[index]);
	      	this.selectedWareHouseList.splice(index, 1);
	    }
  	}
  	/**
  	 * Method on selected warehouse value
  	 * @access public
  	*/
  	selected(event: MatAutocompleteSelectedEvent): void {
	    this.selectedWareHouseList.push({id:event.option.value,name : event.option.viewValue});
	    const index = this.allWareHouseList.findIndex(wareHouse => {
			return wareHouse.id == event.option.value;
		});
	    if (index >= 0) {
	      	this.allWareHouseList.splice(index, 1);
	    }

	    this.fruitInput.nativeElement.value = '';
	    this.wareHouseCtrl.setValue(null);
     }
  	/**
  	 * Method for filtering a warehouse
  	 * @access private
  	*/
  	private _filter(searchKeyWord){
  		let clonedArray = [];
    	const filterValue = searchKeyWord.toLowerCase();
    	clonedArray  = [].concat(this.allWareHouseList);
    	return clonedArray.filter(wareHouse => wareHouse['name'].toLowerCase().indexOf(filterValue) === 0);
  	}
  	/**
  	 * Method for formattig warehouse list
  	 * @access private
  	 * @return ware house list id
  	*/
  	private _formatWareHouseforEdit() {
  		let tempList = [];
  		if(this.selectedWareHouseList.length > 0) {
  			this.selectedWareHouseList.forEach(wareHouse => {
					// if(wareHouse.id==0){}
  				tempList.push(wareHouse['id']);
  			});
  		}
  		return tempList;
  	}

	closeDialog() {
		this.dialogRef.close();
	}
}