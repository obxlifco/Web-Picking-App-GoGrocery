import { Component, OnInit, OnDestroy, Inject, Optional,ElementRef,ViewChild} from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { CategoryService } from './products.category.service';
import { GlobalService } from '../../global/service/app.global.service';
import { CookieService } from 'ngx-cookie';
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material';
import { PopupImgDirective, ImageUploadUrlDialog } from '../.././global/directive/popup-image.directive';
import { DialogsService } from '../.././global/dialog/confirm-dialog.service';
import { AddEditTransition, AddEditStepFlipTransition } from '../.././addedit.animation';
import { Global,GlobalVariable } from '../../global/service/global';
// Warehouse selection auto 
import {COMMA, ENTER} from '@angular/cdk/keycodes';
import {MatChipInputEvent} from '@angular/material/chips';
import {MatAutocompleteSelectedEvent, MatAutocomplete} from '@angular/material/autocomplete';
import {FormControl} from '@angular/forms';
import {Observable} from 'rxjs';
import {map,startWith} from 'rxjs/operators';
// Warehouse selection auto 
@Component({
	templateUrl: './templates/add_category.html',
	providers: [CategoryService],
	animations: [AddEditTransition],
	host: {
		'[@AddEditTransition]': ''
	},
})
export class CategoryAddEditComponent implements OnInit, OnDestroy {
	public response: any;
	public errorMsg: string;
	public successMsg: string;
	public customergrp_list: any;
	public formModel: any = {};
	public channel_list: any;
	public category_list: any;
	public child_category_list: any = [];
	public child_child_category_list: any = [];
	public marketplace_categories: any = [];
	public marketplace_category_list: any = [];
	public parent_child: any;
	private sub: any;
	public tabIndex: number;
	public parentId: number = 0;
	public add_edit: any;
	public imgsubscriber: any;
	public category_base: string = '';
	public all_languages: any = [];
	public warehouse_id: any;
	// Set chip property for warehouse matchip
	public visible:boolean = true;
	public selectable:boolean = true;
	public removable:boolean = true;
	public addOnBlur = true;
	readonly separatorKeysCodes: number[] = [ENTER, COMMA];
	// public wareHouseCtrl = new FormControl();
	public filteredWareHouse: Observable<any>;
	public selectedWareHouseList = [];
	public allWareHouseList = [];
	public all_WareHouse_List = [];
	public wareHouseList = [];
	public ware_House_List = [];
	public default_warehouse;
	@ViewChild('fruitInput') fruitInput: ElementRef<HTMLInputElement>;
    @ViewChild('auto') matAutocomplete: MatAutocomplete;

	constructor(
		private _categoryService: CategoryService,
		public _globalService: GlobalService,
		private _router: Router,
		private _route: ActivatedRoute,
		private _cookieService: CookieService,
		public dialog: MatDialog,
	) {
		// this.filteredWareHouse = this.wareHouseCtrl.valueChanges.pipe(
        // startWith(''),
        // map((searchKeyWord) => {
        // 	if(searchKeyWord && searchKeyWord.length > 0) {
        // 		return this._filter(searchKeyWord);
        // 	}
        // 	return this.allWareHouseList;
        // }));

        // Get all warehouse list
		
		this.sub = this._route.params.subscribe(params => { // pick id from the route url
			this.formModel.categoryId = +params['id']; // (+) converts string 'id' to a number
		});

		this.allWareHouseList=[{'id':0,'name':'All'}]
		this.getAllWareHouseList();
		this.get_All_WareHouseList();
		let userData = this._cookieService.getObject('userData');
		this.warehouse_id = userData['warehouse_id'];
	 }

	// Initialization method
	ngOnInit() {
		this.category_base = window.location.protocol + '//' + window.location.hostname + ':'+window.location.port + '/category/';
		this.tabIndex = +this._globalService.getCookie('active_tabs'); // current active tab index
		this.parentId = this._globalService.getParentTab(this.tabIndex); // parent id of the current active tab

		// this.selectedWareHouseList=[{'id':0,'name':'All'}]
		if (this.formModel.categoryId) {
			this._cookieService.putObject('cid_edit', this.formModel.categoryId);
			this._cookieService.putObject('action', 'edit');
			this.add_edit = 'edit';
		} else {
			this._cookieService.putObject('action', 'add');
			this.formModel.categoryId = this._cookieService.getObject('cid_add');
			this.add_edit = 'add';
		}

		this.formModel.applicable_imei = 'N';
		// set default show in navigation
		this.formModel.show_navigation = 'Y';
		
		// call http service at the time of basic info load
		console.log(this.formModel.categoryId)
		this._categoryService.basicInfoLoad(this.formModel.categoryId).subscribe(
			data => {
				this.all_languages = data.all_languages;
				// console.log(this.all_languages)
				this.response = data;
				if (this.formModel.categoryId > 0) {
					if (this.response.marketplace.length > 0) {
						let that = this;
						this.response.marketplace.forEach(function (item: any, index: number) {
							that.marketplace_categories.push({ "channel": item.channel_id, "category_channel": item.channel_category_id });
							that.marketplace_category_list[index] = item.category;
						});
					}
					else {
						this.marketplace_categories = [{}];
					}
					console.log(this.formModel)
					this.formModel = Object.assign({}, this.response.api_status);
					console.log(this.formModel)
					this.formModel.categoryId = this.response.api_status.id;
					if (this.response.api_status.parent_id > 0) {
						this.formModel.is_parent = 'N';
					} else {
						this.formModel.is_parent = 'Y';
					}
					// this.ware_House_List = this.formModel.warehouse;
					// console.log(this.ware_House_List)
					// let ware_house:any = [];
					// this.ware_House_List.forEach(e => {
					// 	ware_house.push(e['id']);
					// });
					// console.log(ware_house)
					// let warehouse_ids = ware_house.join(',');
                    // var array = warehouse_ids.split(",").map(Number);
                    // this.default_warehouse = array;
					// Set default show in navigation 

					this.formModel.show_navigation = this.response.api_status.show_navigation ? this.response.api_status.show_navigation : 'N';
					// Set selected warehouse list
					// this.selectedWareHouseList = this.response.api_status.warehouse ? this.response.api_status.warehouse : [];
					// let newlist = []
					// newlist = this.allWareHouseList.filter(
					// 	item => !this.selectedWareHouseList.some(other => item['id'] == other['id'])
					// );
					// if(newlist) {
					// 	this.allWareHouseList = [];
					// 	this.allWareHouseList = newlist;
					// }

					this.channel_list = this.response.channel;
					this.category_list = this.response.category;
					if (this.response.api_status.parent_id != 0) {
						this.formModel.category_3 = this.response.parent_child.category_3;
						this.formModel.category_2 = this.response.parent_child.category_2;
						this.formModel.category_1 = this.response.parent_child.category_1;
						// var parent_id=this.response.api_status.parent_id
						// this.get_child_categories(parent_id,1,0);

						if (this.formModel.category_3 != 0) {
							this.get_child_categories(this.formModel.category_1, 1, 0);
							this.get_child_categories(this.formModel.category_2, 2, 0);

						} else if (this.formModel.category_2 != 0) {
							this.get_child_categories(this.formModel.category_1, 1, 0);
							this.get_child_categories(this.formModel.category_2, 2, 0);

						} else {
							this.get_child_categories(this.formModel.category_1, 1, 0);
						}
					}

					let img_base = GlobalVariable.S3_URL + 'category/200x200/';
					if (this.formModel.banner_image) {
						this.formModel.banner_image = {};
						this.formModel.banner_image['name'] = this.response.api_status.banner_image;
						this.formModel.banner_image['url'] = img_base + this.response.api_status.banner_image;
					}

					if (this.formModel.image) {
						this.formModel.image = {};
						this.formModel.image['name'] = this.response.api_status.image;
						this.formModel.image['url'] = img_base + this.response.api_status.image;
					}

					img_base = GlobalVariable.S3_URL + 'category/100x100/';
					if (this.formModel.thumb_image) {
						this.formModel.thumb_image = {};
						this.formModel.thumb_image['name'] = this.response.api_status.thumb_image;
						this.formModel.thumb_image['url'] = img_base + this.response.api_status.thumb_image;
					}
					this.formModel.category_url = this.response.api_status.category_url;//this.formModel.category_url.split("/").pop();
				} else {
					this.formModel.categoryId = 0;
					this.channel_list = this.response.channel;
					this.category_list = this.response.category;
					this.marketplace_categories = [{}];
					this.formModel.is_parent = 'Y';
					this.formModel.display_mobile_app = 'Y';
					this.formModel.applicable_imei = 'N';
					this.formModel.isblocked = 'n';
					this.formModel.page_title = this.formModel.name;
					// this.default_warehouse = 0;
				}
			},
			err => {
				this._globalService.showToast('Something went wrong. Please try again.');
			},
			function () {
				//completed callback
			}
		);
	}

	createSlug(value) {
		value = value.trim();
		var slug = '';
		slug = value.toLowerCase().replace(/[^\w ]+/g, '').replace(/ /g, '-');
		 this.formModel.category_url = this.category_base +  slug;
		//this.formModel.category_url = slug;
		this.formModel.page_title = value;
	}

	chopSlug(value) {
		value = value.split('/category/')[1];
		this.formModel.category_url = value;
	}

	addEditBasicInfo(form: any) {
		this.errorMsg = '';
		var data: any = {};
		console.log(this.formModel)
		data = Object.assign({}, this.formModel);
		console.log(data)
		data.name = data.name.trim();
		// Check if Show in Navifation exists
		data.warehouse = [];
		// console.log(this.warehouse_id)
		// if(this.warehouse_id && this.warehouse_id > 0 && this.formModel.categoryId < 1) {
		// 	data.warehouse.push(this.warehouse_id);
		// 	// console.log('WM add new');
		// } else {
		// 	data.warehouse = this.default_warehouse;
		// 	if(data.warehouse.includes(0)){
		// 		data.warehouse = [];
		// 		this.wareHouseList.forEach(e => {
		// 			if(e['id'] != 0){
		// 				data.warehouse.push(e['id']);
		// 			}
		// 		});
		// 	}
		// }
		
		if (this.formModel.category_url) {
			//data.url_suffix = this.formModel.category_url;
			data.url_suffix = '';
			//data.category_url = this.category_base + this.formModel.category_url;
			data.category_url = this.formModel.category_url.split("/").pop();
		} else {
			data.url_suffix = '';
			var slug = '';
			slug = this.formModel.name.toLowerCase().replace(/[^\w ]+/g, '').replace(/ +/g, '-');
			data.category_url = this.category_base + slug;
		}

		data.website_id = this._globalService.getWebsiteId();
		if (this.formModel.is_parent == 'Y') {
			data.parent_id = 0;
		} else {
			if (this.formModel.category_3 != '') {
				data.parent_id = this.formModel.category_3;
			} else if (this.formModel.category_2 != '') {
				data.parent_id = this.formModel.category_2;
			} else {
				data.parent_id = this.formModel.category_1;
			}
		}
		if (this.formModel.categoryId < 1) {
			data.createdby = this._globalService.getUserId();
		}
		data.updatedby = this._globalService.getUserId();

		if (this.formModel.banner_image && this.formModel.banner_image.hasOwnProperty("name")) {
			data.banner_image = this.formModel.banner_image.name;
		} else {
			data.banner_image = '';
		}
		if (this.formModel.image && this.formModel.image.hasOwnProperty("name")) {
			data.image = this.formModel.image.name;
		} else {
			data.image = '';
		}
		if (this.formModel.thumb_image && this.formModel.thumb_image.hasOwnProperty("name")) {
			data.thumb_image = this.formModel.thumb_image.name;
		} else {
			data.thumb_image = '';
		}

		if (this.marketplace_categories.length > 0) {
			var marketplace_categories: any = [];
			let that = this;
			this.marketplace_categories.forEach(function (item: any, index: number) {
				if (item.channel) {
					marketplace_categories.push({ "channel": item.channel, "category_channel": item.category_channel });
				}
			});
			data.marketplace_categories = marketplace_categories;
		}
		var form_data = new FormData();
		form_data.append('data', JSON.stringify(data));
		if (this.formModel.image) {
			if (this.formModel.image.type == 1) {
				form_data.append('image_url', this.formModel.image.url);
			} else {
				if (this.formModel.image._file) {
					form_data.append('image', this.formModel.image._file);
				} else {
					form_data.append('image_url', '');
				}
			}
		} else {
			form_data.append('image_url', '');
		}
		if (this.formModel.banner_image) {
			if (this.formModel.banner_image.type == 1) {
				form_data.append('banner_image_url', this.formModel.banner_image.url);
			} else {
				if (this.formModel.banner_image._file) {
					form_data.append('banner_image', this.formModel.banner_image._file);
				} else {
					form_data.append('banner_image_url', '');
				}

			}
		} else {
			form_data.append('banner_image_url', '');
		}

		if (this.formModel.thumb_image) {
			if (this.formModel.thumb_image.type == 1) {
				form_data.append('thumb_image_url', this.formModel.thumb_image.url);
			} else {
				if (this.formModel.thumb_image._file) {
					form_data.append('thumb_image', this.formModel.thumb_image._file);
				} else {
					form_data.append('thumb_image_url', '');
				}
			}
		} else {
			form_data.append('thumb_image_url', '');
		}
		
		let that = this;
		this._categoryService.basicInfoAddEdit(form_data, this.formModel.categoryId).subscribe(
			data => {
				this.response = data;
				if (this.response.status == 1) {
					if (this.add_edit == 'add') {
						this._cookieService.putObject('cid_add', this.response.api_status.id);
						this._router.navigate(['/category/add/step2']);
					}
					else {
						this._router.navigate(['/category/edit/' + this.formModel.categoryId + '/step2']);
					}
					this._globalService.showToast(this.response.message);
				} else {
					this.errorMsg = this.response.message;
				}
			},
			err => {
				this._globalService.showToast('Something went wrong. Please try again.');
				this._globalService.showLoaderSpinner(false);
			},
			function () {
				//completed callback
				that._globalService.showLoaderSpinner(false);
			}
		);

	}


	get_child_categories(parent_id: number, lvl: number, reset: number) {
		this._categoryService.getChildCategory(parent_id, this.formModel.categoryId, lvl + 1).subscribe(
			data => {
				this.response = data;
				if (this.response.status) {
					if (lvl == 1) { //level 1 category
						if (reset == 0) {
							this.child_category_list = this.response.category;
						} else {
							this.child_category_list = [];
							this.child_child_category_list = [];
							this.child_category_list = this.response.category;
							this.formModel.category_2 = 0;
							this.formModel.category_3 = 0;

						}
					} else { //level 2 category
						if (reset == 0) {
							this.child_child_category_list = this.response.category;
						}
						else {
							this.child_child_category_list = [];
							this.child_child_category_list = this.response.category;
							this.formModel.category_3 = 0;
						}
					}
				} else {
					if (lvl == 1) { //level 1 category
						this.child_category_list = [];
						this.child_child_category_list = [];
					} else { //level 2 category
						this.child_child_category_list = [];
					}
				}
			},
			err => {
				this._globalService.showToast('Something went wrong. Please try again.');
			},
			function () {
				//completed callback
			}
		);
	}
	ma(channel: any) {
		// this.channel_list.splice(channel, 1);
	}
	addRow() {
		this.marketplace_categories.push({});
	}

	removeRow(index: number) {
		this.marketplace_categories.splice(index, 1);
		this.child_category_list.splice(index, 1);
	}

	dialogRef: MatDialogRef<PopupImgDirective> | null;
	openImagePop(imgFor: string, multiple: boolean = false) {
		let data = { imgFor: imgFor, is_multiple: multiple, type: 'category' };
		this.dialogRef = this.dialog.open(PopupImgDirective, { data: data });
		this.dialogRef.afterClosed().subscribe(result => {
			for (let key in result) {
				let value = result[key][0];
				value['type'] = 2; // image upload type - 2 i.e upload from browse file
				this.formModel[key] = value;
			}
		});

		this._globalService.imageArrayChange$.subscribe(result => {
			for (let key in result) {
				let value = result[key];
				value['type'] = 1;  // image upload type - 1 i.e upload from inserted link,google picker, dropbox picker
				this.formModel[key] = value;
			}
		});
	}
	dialogRefChannel: MatDialogRef<MarketplaceCategoryChooseComponent> | null;
	ChooseMarketplaceCat(channel: any, item: any, index: number) {
		this.dialogRefChannel = this.dialog.open(MarketplaceCategoryChooseComponent, { data: channel });
		this.dialogRefChannel.afterClosed().subscribe(result => {
			if (result != undefined) {
				this.marketplace_category_list[index] = result;
				item.category_channel = result[0]['id'];
			}
		});
	}

	ngAfterViewInit() {
		this.imgsubscriber = this._globalService.libArrayChange$.subscribe(result => {
			for (let key in result) {
				let value = result[key][0];
				value['name'] = value['url'];
				if (key == 'thumb_image') {
					value['url'] = GlobalVariable.S3_URL + 'category/100x100/' + value['url'];
				} else {
					value['url'] = GlobalVariable.S3_URL + 'category/200x200/' + value['url'];
				}
				value['type'] = 3;  // image upload type - 3 i.e upload from s3 library
				this.formModel[key] = value;
			}
		});
	}
	delImg = function (is_remove: number, scope_var: string, file_var: string, is_arr: number, index: number) {
		if (is_remove > 0) {
			var form_data: any = {};
			form_data.id = is_remove;
			form_data.field = file_var;
			form_data.file_name = this[scope_var][file_var]['name'];
			if (form_data.file_name) {
				this._categoryService.categoryImageDelete(form_data).subscribe(
					data => {
						this.response = data;
						if (this.response.status == 1) {
						} else {
							this.errorMsg = this.response.message;
						}
					},
					err => {
						this._globalService.showToast('Something went wrong. Please try again.');
					},
					function () {
						//completed callback
					}
				);
			}
			else {
				this._globalService.showToast('Successfully Deleted!');
			}
		}

		if (is_arr) {
			if (scope_var != '') {
				this[scope_var][file_var].splice(index, 1);
			} else {
				this[file_var].splice(index, 1);
			}
		} else {
			if (scope_var != '') {
				this[scope_var][file_var] = '';
			} else {
				this[file_var] = '';
			}
		}
	};
	ngOnDestroy() {
		this.sub.unsubscribe();
		this.imgsubscriber.unsubscribe();
	}
	/**
	 * Method for getting all warehouse list
	 * @access public
	*/
	getAllWareHouseList() {
		let that = this;
		this._categoryService.getAllWareHouseList().subscribe(response => {
			if(response && response['status'] == 1 && response['api_status'].length > 0) {
				response['api_status'].forEach(function (item: any) {
					that.allWareHouseList.push({
						'id' : item.id,
						'name' : item.name
					});
				});
				this.wareHouseList = that.allWareHouseList;
				// console.log(this.wareHouseList);
				if(+this.formModel.categoryId == 0 || this.formModel.categoryId == null) {
					const index = this.allWareHouseList.findIndex(wareHouse => {
						return wareHouse.id == 0;
					});
				    if (index == 0) {
				      this.allWareHouseList.splice(index, 1);
				    }
				}
			}
		});
	}

	get_All_WareHouseList(){
		this._categoryService.getAllWareHouseList().subscribe(response => {
			this.all_WareHouse_List = response.api_status;
			let obj = {};
			obj["id"]= 0 ;
			obj["name"]='All';
			this.all_WareHouse_List.splice(0, 0, obj);
			console.log(this.all_WareHouse_List);
			// if(response && response['status'] == 1 && response['api_status'].length > 0) {
			// 	response['api_status'].forEach(function (item: any) {
			// 		this.all_WareHouse_List.push({
			// 			'id' : item.id,
			// 			'name' : item.name
			// 		});
			// 	});
			// }
		});
	}
	/**
	 * Method for adding a chip of warehouse
     * @param matChipEvent
	*/
	//   add(event: MatChipInputEvent): void {
    // // Add fruit only when MatAutocomplete is not open
    // // To make sure this does not conflict with OptionSelected Event
	//     if (!this.matAutocomplete.isOpen) {
	//       const input = event.input;
	//       const value = event.value;
	//       // Add our fruit
	//       if ((value || '').trim()) {
	//         this.selectedWareHouseList.push({name:value.trim()});
	//       }
	//       // Reset the input value
	//       if (input) {
	//         input.value = '';
	//       }
	//       this.wareHouseCtrl.setValue(null);
	//     }
	//   }
	/**
	 * Method for removing a chip event
	 * @param wareHousw
	*/
	// remove(wareHouseList): void {
	// 	let all_ware  = {};
	// 	const index = this.selectedWareHouseList.findIndex(wareHouse => {
	// 		return wareHouse.id == wareHouseList;
	// 	});
	//     if (index >= 0) {
	//       	this.allWareHouseList.push(this.selectedWareHouseList[index]);
	//       	this.selectedWareHouseList.splice(index, 1);
	//     }
  	// }
  	/**
  	 * Method on selected warehouse value
  	 * @access public
  	*/
  	// selected(event: MatAutocompleteSelectedEvent): void {
	//     this.selectedWareHouseList.push({id:event.option.value,name : event.option.viewValue});
	//     const index = this.allWareHouseList.findIndex(wareHouse => {
	// 		return wareHouse.id == event.option.value;
	// 	});
	//     if (index >= 0) {
	//       	this.allWareHouseList.splice(index, 1);
	//     }

	//     this.fruitInput.nativeElement.value = '';
	//     this.wareHouseCtrl.setValue(null);
    //  }
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
  	// private _formatWareHouseforEdit() {
  	// 	let tempList = [];
  	// 	if(this.selectedWareHouseList.length > 0) {
  	// 		this.selectedWareHouseList.forEach(wareHouse => {
	// 				// if(wareHouse.id==0){}
  	// 			tempList.push(wareHouse['id']);
  	// 		});
  	// 	}
  	// 	return tempList;
  	// }
  	
}

@Component({
	templateUrl: './templates/choose_channel_category.html',
	providers: [CategoryService],
})
export class MarketplaceCategoryChooseComponent implements OnInit {
	public response: any;
	public errorMsg: string;
	public successMsg: string;
	public formModel: any = {};
	private sub: any;
	public tabIndex: number;
	public parentId: number = 0;
	public add_edit: any = '';
	public default_list: any = [];
	public show_desc: boolean = false;
	public channel_list: any = [];
	public category: any = [];
	constructor(
		private _categoryService: CategoryService,
		public _globalService: GlobalService,
		private _cookieService: CookieService,
		private dialogRef: MatDialogRef<MarketplaceCategoryChooseComponent>,
		private _route: ActivatedRoute,
		private _router: Router,
		public dialog: MatDialog,
		private _global: Global,
		@Optional() @Inject(MAT_DIALOG_DATA) public data: any
	) {

		_global.reset_dialog();
	}

	ngOnInit() {
		this.formModel.channel = this.data;
		this.formModel.category = '';
		this.add_edit = this._cookieService.getObject('action');
		if (this.add_edit == 'add') {
			this.formModel.categoryId = this._cookieService.getObject('cid_add');
		} else {
			this.formModel.categoryId = this._cookieService.getObject('cid_edit');
		}
		if (this.formModel.categoryId > 0) {
			this._categoryService.getMarketplaceCategory(0, this.formModel.channel).subscribe(
				data => {
					this.response = data;
					this.formModel.categories = this.response.parents;
				},
				err => {
					this._globalService.showToast('Something went wrong. Please try again.');
				},
				function () {
					//completed callback
				}
			);
		}
		else {
			this._categoryService.getMarketplaceCategory(0, this.formModel.channel).subscribe(
				data => {
					this.response = data;
					this.formModel.categories = this.response.parents;
				},
				err => {
					this._globalService.showToast('Something went wrong. Please try again.');
				},
				function () {
					//completed callback
				}
			);
		}
	}

	get_marketplace_categories(cat_id: number, category: string, channel: number, lvl: number) {
		this.category = [];
		if (lvl == 0) {
			this.category.push(category);
		} else {
			this._categoryService.getMarketplaceCategory(cat_id, channel).subscribe(
				data => {
					this.response = data;
					console.log(this.response);
					if (this.response.status == 1) {
						if (lvl == 2) {
							this.formModel.sub_categories = this.response.child;
						}
						if (lvl == 3) {
							this.formModel.sub_sub_categories = this.response.child;
						}
					} else {
						this.category.push(category);
					}
				},
				err => {
					this._globalService.showToast('Something went wrong. Please try again.');
				},
				function () {
					//completed callback
				}
			);
		}
	}
	chooseCategory() {
		this.dialogRef.close(this.category);
	}
	closeDialog() {
		this.dialogRef.close();
	}
}

@Component({
	templateUrl: './templates/add_category2.html',
	providers: [CategoryService],
	//   animations: [ AddEditStepFlipTransition ],
	//   host: {
	//     '[@AddEditStepFlipTransition]': ''
	//   },
})

export class CategoryCustomFieldComponent implements OnInit {
	public response: any;
	public errorMsg: string;
	public successMsg: string;
	public formModel: any = {};
	private sub: any;
	public tabIndex: number;
	public parentId: number = 0;
	public add_edit: any = '';
	public default_list: any = [];
	public default_active_list: any = [];
	public compulsory_list: any = [];
	public optional_list: any = [];
	public show: boolean = false;
	public channel_list: any = [];
	public all_languages: any = [];
	constructor(
		private _categoryService: CategoryService,
		public _globalService: GlobalService,
		private _router: Router,
		private _route: ActivatedRoute,
		private _cookieService: CookieService,
		public dialog: MatDialog,
		private dialogsService: DialogsService,
	) { }


	ngOnInit() {
		this.loadData(false, 6);
	}

	loadData(show, channel) {
		this.show = show;
		this.tabIndex = +this._globalService.getCookie('active_tabs');
		this.parentId = this._globalService.getParentTab(this.tabIndex);
		this.add_edit = this._cookieService.getObject('action');
		if (this.add_edit == 'add') {
			this.formModel.categoryId = this._cookieService.getObject('cid_add');
		} else {
			this.formModel.categoryId = this._cookieService.getObject('cid_edit');
		}
		this.compulsory_list = [];
		this.optional_list = [];
		this.default_active_list = [];
		this._categoryService.categoryCustomField(this.formModel.categoryId, channel).subscribe(
			data => {
				this.response = data;
				this.all_languages = data.all_languages;
				this.channel_list = this.response.channel;
				this.default_list = this.response.value;
				let that = this;
				this.default_list.forEach(function (item: any) {
					that.formModel[item.field_id] = item.default_values;
					////////////Custom values///
					if (item.custom_values == '') {
						item.custom_values = '';
					}
					else {
						var array = [];
						var array_lang = [];
						array = item.custom_values.split('##');
						// console.log(item.lang_data)
						///////Checkobox////////
						if ((item.input_type == 'Checkbox')) {
							var array_default = [];
							array_default = item.default_values.split('##');
							array.forEach(function (item_default: any) {
								if (array_default.includes(item_default)) {
									that.formModel[item_default] = true;
								}
							});
						}
						item.custom_values = array;
						
						item.lang_data.forEach(function (item_lang: any) {
							var lang_array_default = [];
							array_lang = item_lang.field_lable_value.split('##');
							// console.log(lang_array_default)
							array_lang.forEach(function (item_default: any) {
								if (array_lang.includes(item_default)) {
									that.formModel[item_default] = true;
								}
							});
							var custom_val = "custom_values_"+item_lang.language_code;
							item[custom_val] = array_lang;
						})
					}
					
					///////Generate List/////
					if (item.is_system == 'y') {
						that.default_active_list.push(item);
						if (item.is_optional == 1) {
							that.compulsory_list.push(item);
						} else {
							that.optional_list.push(item);
						}
					}
				})
			},
			err => {
				this._globalService.showToast('Something went wrong. Please try again.');
			},
			function () {
				//completed callback
			}
		);
	}

	show_custom() {
		this.show = !this.show;
	}

	save_custom() {
		var data: any = [];
		let that = this;
		this.default_list.forEach(function (item: any) {
			data.push({ "field_id": item.field_id, "is_system": 'y' })
		});
		this._categoryService.categoryCustomFieldSystem(data).subscribe(
			data => {
				this.response = data;
				if (this.response.status == 1) {
					this.loadData(false, 6);
				} else {

					this.errorMsg = this.response.message;
				}
			},
			err => console.log(err),
			function () {
				//completed callback
			}
		);
	}
	dialogRef: MatDialogRef<CategoryAddEditCustomFieldComponent> | null;
	show_pop(id: any) {
		this.dialogRef = this.dialog.open(CategoryAddEditCustomFieldComponent, { data: id, width: '500px' });
		this.dialogRef.afterClosed().subscribe(result => { this.loadData(true, 6); });
	}

	dialogRefImport: MatDialogRef<CategoryImportCustomFieldComponent> | null;
	show_import() {
		this.dialogRefImport = this.dialog.open(CategoryImportCustomFieldComponent, { data: 'import_file' });
		this.dialogRefImport.afterClosed().subscribe(result => {
			if (result) {
				var form_data = new FormData();
				var category_id = this.formModel.categoryId;
				form_data.append('category_id', JSON.stringify(category_id));
				form_data.append('import_file', result.import_file._file);
				this._categoryService.categoryCustomFieldImport(form_data).subscribe(
					data => {
						this.response = data;
						if (this.response) {
							this.show_preview(this.response.msg);

						} else {

							this.errorMsg = this.response.message;
						}
					},
					err => {
						this._globalService.showToast('Something went wrong. Please try again.');
					},
					function () {
						//completed callback
					}
				);
			}
		});
	}

	dialogRefPreview: MatDialogRef<CategoryImportPreviewComponent> | null;
	show_preview(data: any) {
		this.dialogRefPreview = this.dialog.open(CategoryImportPreviewComponent, { data: data });
		this.dialogRefPreview.afterClosed().subscribe(result => { this.loadData(true, 6); });
	}

	deleteCustom(id: any) {
		this.dialogsService.confirm('Warning', 'Do you really want to delete selected records?').subscribe(res => {
			if (res) {
				this._categoryService.categoryCustomFieldDelete(id, this.formModel.categoryId).subscribe(
					data => {
						this.response = data;
						this.loadData(true, 6);
					},
					err => {
						this._globalService.showToast('Something went wrong. Please try again.');
					},
					function () {
						//completed callback
					}
				);
			}
		});
	}
	addEditAdditional() {
		var data: any = [];
		let that = this;
		// this.save_custom();
		this.default_list.forEach(function (item: any) {
			///////Checkobox////////
			if (item.input_type == 'Checkbox') {
				var checked_values: any = '';
				item.custom_values.forEach(function (item_default: any) {
					if (that.formModel[item_default]) {
						item_default = item_default + "##";
						checked_values += item_default
					}
				});
				default_value = checked_values;
			} else if (that.formModel[item.field_id]) { ///////Others////////  
				var default_value: any = that.formModel[item.field_id];
			} else { 
				var default_value: any = ''; 
			}
			data.push({ "field_id": item.field_id, "default_value": default_value })
		});
		this._categoryService.categoryDefaultFieldAddEdit(data).subscribe(
			data => {
				this.response = data;
				if (this.response.status == 1) {
					this.ngOnInit();
					this._globalService.deleteTab(this.tabIndex, this.parentId);
					if (this.add_edit == 'add') {
						this._cookieService.remove('cid_add');
					} else {
						this._cookieService.remove('cid_edit');
					}
					this._cookieService.remove('action');
				} else {
					this.errorMsg = this.response.message;
				}
			},
			err => {
				this._globalService.showToast('Something went wrong. Please try again.');
			},
			function () {
				//completed callback
			}
		);
	}
}

@Component({
	templateUrl: './templates/add_customefields.html',
	providers: [CategoryService],
})
export class CategoryAddEditCustomFieldComponent implements OnInit {
	public response: any;
	public errorMsg: string;
	public successMsg: string;
	public formModel: any = {};
	private sub: any;
	public tabIndex: number;
	public parentId: number = 0;
	public add_edit: any = '';
	public default_list: any = [];
	public show_desc: boolean = false;
	public channel_list: any = [];
	public all_languages :any = [];
	constructor(
		private _categoryService: CategoryService,
		public _globalService: GlobalService,
		private _cookieService: CookieService,
		private dialogRef: MatDialogRef<CategoryAddEditCustomFieldComponent>,
		private _route: ActivatedRoute,
		private _router: Router,
		public dialog: MatDialog,
		@Inject(MAT_DIALOG_DATA) public data: any
	) {
		dialog.afterOpen.subscribe(() => {
			let containerElem: HTMLElement = <HTMLElement>document.getElementsByClassName('mat-dialog-container')[0];
			containerElem.classList.remove('pop-box-up');
		});
	}

	ngOnInit() {
		this.formModel.customId = this.data;
		this.add_edit = this._cookieService.getObject('action');
		if (this.add_edit == 'add') {
			this.formModel.categoryId = this._cookieService.getObject('cid_add');
			this.show_desc = true;
		} else {
			this.formModel.categoryId = this._cookieService.getObject('cid_edit');
		}
		if (this.formModel.customId > 0) {
			this._categoryService.categoryCustomFieldEdit(this.formModel.customId, this.formModel.categoryId).subscribe(
				data => {
					this.response = data;
					this.all_languages = data.all_languages
					this.formModel = this.response.api_status;
					this.channel_list = this.response.channel;
					this.formModel.channel_id = this.response.show_market_places_id.split(",").map(Number);
					this.formModel.show_market_places_name = this.response.show_market_places_name;
					this.formModel.customId = this.response.api_status.id
					this.formModel.default_values = this.response.default_values
					this.formModel.categoryId = this.response.category_id
					var fieldVal = this.response.api_status.input_type;
					if ((fieldVal == 'Checkbox') || (fieldVal == 'Radio') || (fieldVal == 'Dropdown')) {
						this.show_desc = true;
					}
					else {
						this.formModel.custom_values = "";
					}

					var array = [];
					array = this.response.api_status.custom_values.split('##');
					var custom_values_count = array.length;
					if (custom_values_count > 0) {
						var custom_values = '';
						array.forEach(function (item: any, index: number = 1) {
							if (custom_values_count != index) { item = item + "\n"; }
							else { item = item; }
							custom_values += item;
						});
						this.formModel.custom_values = custom_values;
					}
					else {
						this.formModel.custom_values = '';
					}
					// custom field edit
					var array_lang = [];
					array_lang = this.response.api_status.custom_values.split('##');
					var lang_custom_values_count = array_lang.length;
					if (lang_custom_values_count > 0) {
						var custom_values = '';
						array_lang.forEach(function (item: any, index: number = 1) {
							if (lang_custom_values_count != index) { item = item + "\n"; }
							else { item = item; }
							custom_values += item;
						});
						this.formModel.custom_values = custom_values;
					} else {
						this.formModel.custom_values = '';
					}
				},
				err => {
					this._globalService.showToast('Something went wrong. Please try again.');
				},
				function () {
					//completed callback
				}
			);
		} else {
			this._categoryService.categoryCustomFieldAddLoad().subscribe(
				data => {
					this.response = data;
					this.all_languages = data.all_languages;
					this.channel_list = this.response.channel;
					this.formModel.is_variant = 'No';
					this.formModel.channel_id = [6];
				},
				err => {
					this._globalService.showToast('Something went wrong. Please try again.');
				},
				function () {
					//completed callback
				}
			);
		}
	}

	OnchangeField(fieldVal) {
		if ((fieldVal == 'Checkbox') || (fieldVal == 'Radio') || (fieldVal == 'Dropdown')) { this.show_desc = true; }
		else { this.show_desc = false; }
	}

	addEditCustomfield(form: any){
	    this.errorMsg = '';
		var data: any = {};
    	if(this.formModel.customId==0){
          	data.createdby = this._globalService.getUserId();
        } else {
         	data.dId=this.formModel.customId;
        }
	    data.updatedby = this._globalService.getUserId();
	    data.category_id=this.formModel.categoryId;
	    if(this.formModel.custom_values && this.formModel.custom_values.trim()!=""){
		    var array=[];
		    array=this.formModel.custom_values.split('\n');
		    array = array.filter(function(x){
			  return (x !== (undefined || null || ''));
			});
		    var custom_values_count=array.length;
	        if(custom_values_count>0)
	        {
	          var custom_values='';
	          	var i=0;
	            array.forEach(function (item: any) {
	            		i++;
	            		  if(item!=""){
		            		if(custom_values_count!=i){item=item+"##";}
				            else{item=item;}
				            custom_values+=item;
				            }
				            else{
				            }
	          		});
	          data.custom_values=custom_values;
	        }
	    }
        else
        {
          data.custom_values='';
		}
		if(this.formModel.default_values){
	     	data.default_values=this.formModel.default_values;
	    } else {
	     	data.default_values=''
		}
	    data.input_type=this.formModel.input_type;
	    data.is_variant=this.formModel.is_variant;
	    data.name=this.formModel.name;
	    data.field_name= this.formModel.name.toLowerCase().replace(/[^\w ]+/g,'').replace(/ +/g,'_');
	    data.channel_id=this.formModel.channel_id.join();
	    data.show_market_places_name="";
	    data.show_type = 0;
	    data.is_system = "y";
	    if(this.formModel.is_optional){
        	data.is_optional = 1;
      	} else {
        	data.is_optional = 0;
		}
		// lang
		let that = this;
		this.all_languages.forEach(function (lang: any,index: number=1) {
			data['name_'+lang.lang_code] = that.formModel['name_'+lang.lang_code];
			
			if(that.formModel['custom_values_'+lang.lang_code] && that.formModel['custom_values_'+lang.lang_code].trim()!=""){
				var lang_array=[];
				lang_array=that.formModel['custom_values_'+lang.lang_code].split('\n');
				lang_array = lang_array.filter(function(x){
				  return (x !== (undefined || null || ''));
				});
				var lang_custom_values_count=lang_array.length;
				if(lang_custom_values_count>0)
				{
				  var custom_values='';
					  var i=0;
					  lang_array.forEach(function (item: any) {
							i++;
							  if(item!=""){
								if(lang_custom_values_count!=i){item=item+"##";}
								else{item=item;}
								custom_values+=item;
								}
								else{
								}
						  });
				  data['custom_values_'+lang.lang_code]=custom_values;
				}
			} else {
			  data['custom_values_'+lang.lang_code]='';
			}
		});
	    this._categoryService.categoryCustomFieldAddEdit(data,this.formModel.customId,this.formModel.categoryId).subscribe(
           	data => {
               	this.response = data;
               	if(this.response.status==1){
                   this.closeDialog();
                   this.ngOnInit();
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
    }
	closeDialog() {
		this.dialogRef.close();
	}
}

@Component({
	templateUrl: './templates/import_customefields.html',
	providers: [CategoryService]
})
export class CategoryImportCustomFieldComponent implements OnInit {
	public response: any;
	public errorMsg: string;
	public successMsg: string;
	public formModel: any = {};
	private sub: any;
	public tabIndex: number;
	public parentId: number = 0;
	public add_edit: any = '';
	public default_list: any = [];
	public sample_csv: any;
	public sample_xls: any;
	public importOpt: string = 'csv';
	constructor(
		private _categoryService: CategoryService,
		public _globalService: GlobalService,
		private _cookieService: CookieService,
		private dialogRef: MatDialogRef<CategoryImportCustomFieldComponent>,
		private _route: ActivatedRoute,
		public dialog: MatDialog,
		@Inject(MAT_DIALOG_DATA) public data: any
	) {
		dialog.afterOpen.subscribe(() => {
			let containerElem: HTMLElement = <HTMLElement>document.getElementsByClassName('mat-dialog-container')[0];
			containerElem.classList.remove('pop-box-up');
		});
	}

	ngOnInit() {
		this.formModel.customId = this.data;
		this.sample_csv = window.location.protocol + '//' + window.location.hostname + ':8062' + '/media/importfile/sample/custom_fields_import.csv';
		this.sample_xls = window.location.protocol + '//' + window.location.hostname + ':8062' + '/media/importfile/sample/custom_fields_import.xls';
		this.add_edit = this._cookieService.getObject('action');
		if (this.add_edit == 'add') {
			this.formModel.categoryId = this._cookieService.getObject('cid_add');
		} else {
			this.formModel.categoryId = this._cookieService.getObject('cid_edit');
		}
		if (this.formModel.customId > 0) {
			this._categoryService.categoryCustomFieldEdit(this.formModel.customId, this.formModel.categoryId).subscribe(
				data => {
					this.response = data;
					this.formModel = this.response.api_status;
					this.formModel.show_market_places_name = this.response.show_market_places_name;
					this.formModel.customId = this.response.api_status.id
				},
				err => {
					this._globalService.showToast('Something went wrong. Please try again.');
				},
				function () {
					//completed callback
				}
			);
		}
	}
	fileChooseXLS(e: Event) {
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
			files[this.data] = file_arr;
		}
		var filename = files.import_file._file.name;
		var extn = filename.split(".").pop();
		if (extn == 'xls' || extn == 'xlsx') {
			this.dialogRef.close(files);
		} else {
			this._globalService.showToast('Please choose XLS/XLSX file');
		}
	}
	fileChooseCSV(e: Event) {
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
			files[this.data] = file_arr;
		}
		var filename = files.import_file._file.name;
		var extn = filename.split(".").pop();
		if (extn == 'csv') {
			this.dialogRef.close(files);
		} else {
			this._globalService.showToast('Please choose CSV file');
		}
	}
	closeDialog() {
		this.dialogRef.close();
	}
}

@Component({
	templateUrl: './templates/preview_customefields.html',
	providers: [CategoryService]
})
export class CategoryImportPreviewComponent implements OnInit {
	public response: any;
	public errorMsg: string;
	public successMsg: string;
	public formModel: any = {};
	private sub: any;
	public tabIndex: number;
	public parentId: number = 0;
	public add_edit: any = '';
	public preview_list: any;
	constructor(
		private _categoryService: CategoryService,
		public _globalService: GlobalService,
		private _cookieService: CookieService,
		private dialogRef: MatDialogRef<CategoryImportPreviewComponent>,
		private _route: ActivatedRoute,
		public dialog: MatDialog,
		@Inject(MAT_DIALOG_DATA) public data: any
	) {
		dialog.afterOpen.subscribe(() => {
			let containerElem: HTMLElement = <HTMLElement>document.getElementsByClassName('mat-dialog-container')[0];
			containerElem.classList.remove('pop-box-up');
		});
	}

	ngOnInit() {
		this.add_edit = this._cookieService.getObject('action');
		if (this.add_edit == 'add') {
			this.formModel.categoryId = this._cookieService.getObject('cid_add');
		} else {
			this.formModel.categoryId = this._cookieService.getObject('cid_edit');
		}
		this.preview_list = this.data;
	}
	saveImport() {
		var data: any = {}
		data.category_id = this.formModel.categoryId;
		data.rows = this.preview_list;
		this._categoryService.categoryImportInsert(data).subscribe(
			data => {
				this.response = data;

				this.closeDialog();
			},
			err => {
				this._globalService.showToast('Something went wrong. Please try again.');
			},
			function () {
				//completed callback
			}
		);
	}

	closeDialog() {
		this.dialogRef.close();
	}
}
