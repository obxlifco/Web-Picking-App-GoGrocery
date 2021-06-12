import { Component, ElementRef, OnInit, Input, Inject, AfterViewInit,Optional } from '@angular/core';
import { Global, GlobalVariable } from '../service/global';
import { GlobalService } from '../service/app.global.service';
import { Router } from '@angular/router';
import { DomSanitizer } from '@angular/platform-browser';
import { DOCUMENT } from '@angular/platform-browser';
// import { PaginationInstance} from 'ngx-pagination';
import { DialogsService } from '../dialog/confirm-dialog.service';
import { CookieService } from 'ngx-cookie';
import { MatDialogRef, MAT_DIALOG_DATA, MatDialog } from '@angular/material';
import { AccountDetailsComponent, PasswordUpdateComponent } from '../../profile/app.profile.component';
import { BrandAddEditComponent } from '../../products/brand/products.brand.addedit.component';
import { ProducttaxAddeditComponent } from '../../products/producttax/producttax.addedit.component';
import { ImportFileComponent, ExportFileComponent } from '../../products/promotion/products.promotion.addedit.component';
import { CurrencyManageComponent } from '../../settings/currency/settings.currency.manage.component';
import { UnitAddEditComponent } from '../../settings/unit/settings.unit.addedit.component';
import { PaymentMethodAddEditComponent } from '../../inventory/po-payment-method/inventory.payment-method.addedit.component';
import { ShippingMethodAddEditComponent } from '../../inventory/po-shipping-method/inventory.shipping-method.addedit.component';
import { PresetAddEditComponent } from '../../order/preset/order.preset.addedit.component';
import { AwbMasterComponent, ViewAwbComponent } from '../../order/courier/order.courier.addedit.component';
import { CurrencyService } from '../../settings/currency/settings.currency.service';
import { HsnCodeAddEditComponent, HsnCodeImportComponent } from '../../products/hsncode/products.hsncode.addedit.component';
import { ExportCategoryFile } from '../../products/category/products.category.component';
import { LanguageAddEditComponent } from '../../settings/language/settings.language.manage.component';
import { CdkDragDrop, moveItemInArray, transferArrayItem } from '@angular/cdk/drag-drop';

import { ViewChild} from '@angular/core';
import {VERSION} from '@angular/material';
import { FormControl } from '@angular/forms';
import {MatSelect} from '@angular/material';

import { Subject } from 'rxjs';
import { take, takeUntil } from 'rxjs/operators';
import { ReplaySubject } from 'rxjs';
interface Bank {
	id: string;
	name: string;
   }
@Component({
	selector: '<global-grid></global-grid>',
	templateUrl: './grid.html',
	providers: [Global, CurrencyService]
})
export class GridComponent implements OnInit, AfterViewInit {
	//MAT SELECT TO STRAT
	public bankCtrl: FormControl = new FormControl();
	public bankFilterCtrl: FormControl = new FormControl();
	public bankMultiCtrl: FormControl = new FormControl();
	public bankMultiFilterCtrl: FormControl = new FormControl();
	banks: Bank[] = [];
	public filteredBanks: ReplaySubject<Bank[]> = new ReplaySubject<Bank[]>(1);
	public filteredBanksMulti: ReplaySubject<Bank[]> = new ReplaySubject<Bank[]>(1);
	@ViewChild('singleSelect') singleSelect: MatSelect; 
	private _onDestroy = new Subject<void>();
	//MAT SELECT TO END
	@Input() childData: { table: string, heading: string, tablink: string, tabparrentid: any, screen: any, ispopup: any, is_export:any, is_import:any };
	constructor(
		private globalService: GlobalService,
		private global: Global,
		private _router: Router,
		private sanitizer: DomSanitizer,
		private dialogsService: DialogsService,
		private elRef: ElementRef,
		private _cookieService: CookieService,
		public dialog: MatDialog,
		private _currencyService: CurrencyService,
		@Inject(DOCUMENT) private document: any
	) { }
	public response: any;
	public errorMsg: string;
	public successMsg: string;
	public bulk_ids: any = [];
	public pagination: any = {};
	public pageIndex: number = 0;
	public pageList: number = 0;
	public sortBy: any = '';
	public sortOrder: any = '';
	public sortClass: any = '';
	public sortRev: boolean = false;
	public selectedAll: any = false;
	public stat: any = {};
	public result_list: any = [];
	public total_list: any = [];
	public cols: any = []
	public layout: any = [];
	public add_btn: string;
	public post_data = {};
	public page: number = 1;
	public maxSize: number = 10;
	public directionLinks: boolean = true;
	public autoHide: boolean = false;
	public config: any = {};
	public permission: any = [];
	public show_btn: any = { 'add': true, 'edit': true, 'delete': true, 'block': true };
	public userId: any;
	public individualRow: any = {};
	public search_text: any;
	public colSpanCount = 4;
	public showSkeletonLoaded: boolean = false;
	public temp_result=[];
	public temp_col=[];
	public selectedTabIndex :number = 0;
	public formModel: any = {};
	field_arr=[];
	ConditionArr=[];
	filterArr=[];
	public search_type_option=false;
	advanced_search=[];
	input_type:any;
	selectArr:any=[];
	temp_key:any=[];
	advanced_search_temp=[];
	filter={};

	Advancefilter={};
	order_information:any=[];
	item_information:any=[];
	customer_information:any=[];
	delivery_information:any=[];
	other_information:any=[];
	order_summary_information:any=[];
	show_data:any=[];
	remove_field_index:number;
	exclude_arr:any=[];
	public warehouse_id: any;
	edit_index:number;

	//////////////////////////Initilise////////////////////////////
	ngOnInit() {
		let userData = this._cookieService.getObject('userData');
		this.userId = userData['uid'];
		this.warehouse_id = userData['warehouse_id'];
		this.generateGrid(0, '', '', '', '');
		this.globalService.loadSkeletonChange$.subscribe(
			(value) => {
				this.showSkeletonLoaded = value;
			}
		);
		for (let i = 0; i < 15; i++) {
			this.temp_result.push(i);
		}
		for (let i = 0; i < 5; i++) {
			this.temp_col.push(i);
		}
		this.formModel.search_type=1

	}
	//SELECT TO STRAT
	private filterBanks() {
		if (!this.banks) {
			return;
		}
		// get the search keyword
		let search = this.bankFilterCtrl.value;
		if (!search) {
			this.filteredBanks.next(this.banks.slice());
			return;
		} else {
			search = search.toLowerCase();
		}
		// filter the banks
		this.filteredBanks.next(
		this.banks.filter(bank => bank.name.toLowerCase().indexOf(search) > -1)
		);
	}

	private filterBanksMulti() {
		if (!this.banks) {
			return;
		}
		// get the search keyword
		let search = this.bankMultiFilterCtrl.value;
		if (!search) {
			this.filteredBanksMulti.next(this.banks.slice());
			return;
		} else {
			search = search.toLowerCase();
		}
		// filter the banks
		this.filteredBanksMulti.next(
			this.banks.filter(bank => bank.name.toLowerCase().indexOf(search) > -1)
		);
	}
	// SELECT TO END
	ngAfterViewInit() {
	}

	/////////////////////////Grid//////////////////////////////////////////////
	generateGrid(reload: any, page: any, sortBy: any, filter: any, search: any) {
		if(search == '' || search == null) {
			this.search_text = '';
		} else {
			this.search_text = search; 
		}
		let elements: NodeListOf<Element> = this.document.getElementsByClassName('action-box');
		elements[0].classList.remove('show');
		this.bulk_ids = [];
		this.individualRow = {};
		this.total_list = [];
		this.selectedAll = false;
		this.filter = filter;
		if (sortBy != '' && sortBy != undefined) {
			if (this.sortRev) {
				this.sortOrder = '-'
				this.sortRev = !this.sortRev;
				this.sortClass = 'icon-down';
			} else {
				this.sortOrder = '+'
				this.sortRev = !this.sortRev;
				this.sortClass = 'icon-up';
			}
			this.sortBy = sortBy;
		}

		if(this.childData.table == "EngageboostCategoryMasters" && this.childData.screen == 'list') {
			if(this.sortBy == "parent_category") {
				this.sortBy = 'name';
			}
		} else if(this.childData.table == "EngageboostUsers" && this.childData.screen == 'list') {
			if(this.sortBy == "name") {
				this.sortBy = 'username';
			}
		} else if(this.childData.table == "EngageboostGlobalSettings" && this.childData.screen == 'list') {
			if(this.sortBy == "timezone_location") {
				this.sortBy = 'name';
			}
		} else if(this.childData.table == "EngageboostVehicleMasters" && this.childData.screen == 'list') {
			if(this.sortBy == "zone_name") {
				this.sortBy = 'vehicle_number';
			}
		} else if(this.childData.table == "EngageboostDeliveryManagers" && this.childData.screen == 'list') {
			if(this.sortBy == "zone_names") {
				this.sortBy = 'name';
			}
		}
		this.post_data = { 
			"model": this.childData.table, 
			"screen_name": this.childData.screen, 
			"userid": this.userId, 
			"search": this.search_text.trim(),
			"order_by": this.sortBy, 
			"order_type": this.sortOrder, 
			"status": filter, 
			"warehouse_id": this.warehouse_id,
			"website_id": this.globalService.getWebsiteId(),
			"advanced_search": this.advanced_search
		}
		this.globalService.skeletonLoader(true);
		this.global.doGrid(this.post_data, page).subscribe(
			data => {
				this.response = data;
				this.total_list=[];
				if (this.response.count > 0) {
					this.result_list = this.response.results[0].result;
					let that = this;
					this.result_list.forEach(function (item: any) {
						if (item.isblocked == 'n') {
							item.isblocked = 'Active';
						} else {
							item.isblocked = 'Inactive';
						}
						if (item.loyal_start_date != '') {
							item.loyal_start_date = that.globalService.convertDate(item.loyal_start_date, 'dd-MM-yyyy h:mm a');
						} else {
							item.loyal_start_date = item.loyal_start_date;
						}
						if (item.loyal_end_date != '') {
							item.loyal_end_date = that.globalService.convertDate(item.loyal_end_date, 'dd-MM-yyyy h:mm a');
						} else {
							item.loyal_end_date = item.loyal_end_date;
						}
						if (item.start_date != '') {
							item.start_date = that.globalService.convertDate(item.start_date, 'dd-MM-yyyy h:mm a');
						} else {
							item.start_date = item.start_date;
						}
						if (item.end_date != '') {
							item.end_date = that.globalService.convertDate(item.end_date, 'dd-MM-yyyy h:mm a');
						} else {
							item.end_date = item.end_date;
						}
						if (item.apply == 's') {
							item.apply = 'Shipping Addres';
						} else {
							item.apply = 'Billing Address';
						}
						if (item.has_multiplecoupons == 'n') {
							item.has_multiplecoupons = 'No'
						} else {
							item.has_multiplecoupons = 'Yes'
						}
						if (item.tax_rate_id != '') {
							item.tax_rate_id = item.tax_rate_name;
						} else {
							item.tax_rate_id = item.tax_rate_id;
						}
						if (item.created != '') {
							//item.created=that.globalService.convertDate(item.created, 'dd-MM-yyyy h:mm a');
						} else {
							item.created = item.created;
						}
						if (item.view_type == '1') {
							item.view_type = 'With Login';
						} else {
							item.view_type = 'Without Login';
						}
						if (item.default_ean == 'y') {
							item.default_ean = 'Y';
						} else {
							item.default_ean = 'No';
						}
						if (item.customer_type) {
							let customer_type = item.customer_group[0].name;
							item.customer_type = customer_type;
						}

						if (that.childData.table == 'EngageboostCategoryBanners') {
							item.banner_type = item.banner_type == 'C' ? 'Category Page' : 'Home Page';
						}
					})
					for (let i = 0; i < this.response.count; i++) {
						this.total_list.push(i);
					}
				} else {
					this.result_list = [];
				}

				this.cols = this.response.results[0].applied_layout;
				this.layout = this.response.results[0].layout;

				this.colSpanCount = this.response.results[0].layout.length;
				this.pagination.total_page = this.response.per_page_count;
				this.pageList = this.response.per_page_count;
				this.stat.active = this.response.results[0].active;
				this.stat.inactive = this.response.results[0].inactive;
				this.stat.all = this.response.results[0].all;
				this.add_btn = this.response.results[0].add_btn;
				this.config.currentPageCount = this.result_list.length
				this.config.currentPage = page
				this.config.itemsPerPage = this.response.page_size;
				this.permission = this.response.results[0].role_permission;
				if (this.childData.table == 'EngageboostGlobalSettings') {
					this.show_btn.add = false;
					this.show_btn.block = false;
					this.show_btn.delete = false;
				}
				if (this.childData.table == 'EngageboostCurrencyMasters') {
					this.show_btn.add = false;
					this.show_btn.edit = false;
					this.show_btn.block = false;
					this.show_btn.delete = false;
				}
				this.globalService.skeletonLoader(false);
				// Fired click event as data not loading....
				let myelement: HTMLElement = this.document.getElementsByClassName('autoclick');
				myelement[0].click();
			},err=>{
				console.log(err)
				this.globalService.skeletonLoader(false);
			}
		);
	}
	////////////////////////////////Popups/////////////////////////////////////// 
	dialogRefBrand: MatDialogRef<BrandAddEditComponent> | null;
	dialogRefProducttax: MatDialogRef<ProducttaxAddeditComponent> | null;
	dialogRefCurrency: MatDialogRef<CurrencyManageComponent> | null;
	dialogRefUnit: MatDialogRef<UnitAddEditComponent> | null;
	dialogRefPayment: MatDialogRef<PaymentMethodAddEditComponent> | null;
	dialogRefShipping: MatDialogRef<ShippingMethodAddEditComponent> | null;
	dialogRefPreset: MatDialogRef<PresetAddEditComponent> | null;
	dialogRefHsncode: MatDialogRef<HsnCodeAddEditComponent> | null;
	dialogRefLanguage: MatDialogRef<LanguageAddEditComponent> | null;
	openPop(id: any) {
		if (this.childData.table == 'EngageboostBrandMasters') {
			this.dialogRefBrand = this.dialog.open(BrandAddEditComponent, { data: id });
			this.dialogRefBrand.afterClosed().subscribe(result => {
				this.generateGrid(0, '', '', '', '');
			});
		}
		if (this.childData.table == 'EngageboostProductTaxClasses') {
			this.dialogRefProducttax = this.dialog.open(ProducttaxAddeditComponent, { data: id });
			this.dialogRefProducttax.afterClosed().subscribe(result => {
				this.generateGrid(0, '', '', '', '');
			});
		}
		if (this.childData.table == 'EngageboostHsnCodeMaster') {
			this.dialogRefHsncode = this.dialog.open(HsnCodeAddEditComponent, { data: id });
			this.dialogRefHsncode.afterClosed().subscribe(result => {
				this.generateGrid(0, '', '', '', '');
			});
		}
		if (this.childData.table == 'EngageboostCurrencyMasters') {
			this.dialogRefCurrency = this.dialog.open(CurrencyManageComponent, { data: id });
			this.dialogRefCurrency.afterClosed().subscribe(result => {
				this.generateGrid(0, '', '', '', '');
			});
		}
		if (this.childData.table == 'EngageboostUnitMasters') {
			this.dialogRefUnit = this.dialog.open(UnitAddEditComponent, { data: id });
			this.dialogRefUnit.afterClosed().subscribe(result => {
				this.generateGrid(0, '', '', '', '');
			});
		}
		if (this.childData.table == 'EngageboostPurchaseOrdersPaymentMethods') {
			this.dialogRefPayment = this.dialog.open(PaymentMethodAddEditComponent, { data: id });
			this.dialogRefPayment.afterClosed().subscribe(result => {
				this.generateGrid(0, '', '', '', '');
			});
		}
		if (this.childData.table == 'EngageboostPurchaseOrdersShippingMethods') {
			this.dialogRefShipping = this.dialog.open(ShippingMethodAddEditComponent, { data: id });
			this.dialogRefShipping.afterClosed().subscribe(result => {
				this.generateGrid(0, '', '', '', '');
			});
		}
		if (this.childData.table == 'EngageboostPresets') {
			this.dialogRefPreset = this.dialog.open(PresetAddEditComponent, { data: id });
			this.dialogRefPreset.afterClosed().subscribe(result => {
				this.generateGrid(0, '', '', '', '');
			});
		}
		if (this.childData.table == 'EngageboostLanguages') {
			this.dialogRefLanguage = this.dialog.open(LanguageAddEditComponent, { data: id });
			this.dialogRefLanguage.afterClosed().subscribe(result => {
				this.generateGrid(0, '', '', '', '');
			});
		}
	}

	openPopExRate(id: number) {
		let that = this;
		this.dialogsService.confirm('Warning', 'Do you really want to make selected currency as base currency?').subscribe(res => {
			if (res) {
				this._currencyService.setBaseCurrency(id).subscribe(
					data => {
						this.response = data;
						let base_curr: string = '';
						let exchange_rates: any = [];
						this.response.curreny.forEach(function (item: any) {
							if (item.isbasecurrency == 'y') {
								base_curr = item.currency_code;
							}
						});

						this._currencyService.syncCurr(this.globalService.getUserId()).subscribe(
							data => {
								this.generateGrid(0, '', '', '', '');
							},
							err => console.log(err),
							function () {
								//completed callback
							}
						);
						this.globalService.showToast(this.response.message);
						this.generateGrid(0, '', '', '', '');
					},
					err => console.log(err),
					function () {
					}
				);
			}
		});
	}

	////////////////////////Delete/Block/Unblock///////////////////////////////
	updateStatusAll(type: number, id: number) {
		let msg = '';
		let perm = '';
		let msgp = '';
		let that = this;
		if (id) {
			that.bulk_ids = [];
			that.bulk_ids.push(id);
		}
		if (type == 2) { msg = 'Do you really want to delete selected records?'; perm = this.permission.delete; msgp = 'You have no permission to delete!'; }
		else if (type == 1) { msg = 'Do you really want to block selected records?'; perm = this.permission.block; msgp = 'You have no permission to block!'; }
		else { msg = 'Do you really want to unblock selected records?'; perm = this.permission.block; msgp = 'You have no permission to unblock!'; }
		if (perm == 'Y') {
			if (this.bulk_ids.length > 0) {
				this.dialogsService.confirm('Warning', msg).subscribe(res => {
					if (res) {
						this.global.doStatusUpdate(this.childData.table, this.bulk_ids, type).subscribe(
							data => {
								this.response = data;
								this.globalService.showToast(this.response.Message);
								that.generateGrid(0, '', '', '', '');
								this.globalService.websitelist.next(true);
							},
							err => console.log(err),
							function () {
							}
						);
					}
				});
			}
			else {
				this.dialogsService.alert('Error', 'Select Atleast One Record!').subscribe(res => { });
			}
		} else {
			this.dialogsService.alert('Permission Error', msgp).subscribe(res => { });
		}

	}
	////////////////////////////Check/Uncheck//////////////
	toggleCheckAll(event: any) {
		let elements: NodeListOf<Element> = this.document.getElementsByClassName('action-box');
		let that = this;
		//console.log(that.childData.table);
		that.bulk_ids = [];
		this.selectedAll = event.checked;
		this.result_list.forEach(function (item: any) {
			item.selected = event.checked;
			if ((that.childData.table == 'EngageboostUsers' || that.childData.table == 'EngageboostGroups' || that.childData.table == 'EngageboostRolemasters') && item.id == 1) { // removed the superadmin user from user,role and group
				// reomved ids
			} else {
				if (item.selected) {
					that.bulk_ids.push(item.id);
					elements[0].classList.add('show');
				}
				else {
					elements[0].classList.remove('show');
				}
			}

		});
		let myelement: NodeListOf < Element > = this.document.getElementsByClassName('action-box orderfilter');
		myelement[0].classList.remove('show');
	}

	toggleCheck(id: any, event: any) {
		let elements: NodeListOf<Element> = this.document.getElementsByClassName('action-box');
		let that = this;
		//that.bulk_ids=[];
		this.result_list.forEach(function (item: any) {
			if (item.id == id) {
				item.selected = event.checked;
				if (item.selected) {
					that.bulk_ids.push(item.id);
					elements[0].classList.add('show');
				} else {
					let index = that.bulk_ids.indexOf(item.id);
					that.bulk_ids.splice(index, 1);
					if (that.bulk_ids.length == 0) {
						elements[0].classList.remove('show');
					}
				}
			}
			if (that.bulk_ids.length == 1) {
				that.bulk_ids.forEach(function (item_id: any) {
					if (item_id == item.id) {
						that.individualRow = item;
					}
				});
			}
			that.selectedAll = false;

		});
		let myelement: NodeListOf < Element > = this.document.getElementsByClassName('action-box orderfilter');
		myelement[0].classList.remove('show');
	}
	/////////////////////////Filter Grid//////////////////////
	updateGrid(isdefault: any) {
		this.global.doGridFilter(this.childData.table, isdefault, this.cols, "list").subscribe(
			data => {
				this.response = data;
				this.generateGrid(0, '', '', '', '');
			},
			err => console.log(err),
			function () {
			}
		);
	}

	dialogRefHsnCodeImport: MatDialogRef<HsnCodeImportComponent> | null;
	dialogRefPromotionImport: MatDialogRef<ImportFileComponent> | null;
	openImportBox(id: any) {
		if (this.childData.table == 'EngageboostHsnCodeMaster') {
			this.dialogRefHsnCodeImport = this.dialog.open(HsnCodeImportComponent, { data: 'import_file' });
			this.dialogRefHsnCodeImport.afterClosed().subscribe(result => {
				this.generateGrid(0, '', '', '', '');
			});
		}

		if (this.childData.table == 'EngageboostDiscountMasters') {
			this.dialogRefPromotionImport = this.dialog.open(ImportFileComponent, { data: 'import_file' });
			this.dialogRefPromotionImport.afterClosed().subscribe(result => {
			});
		}
		
	}

	dialogRefExportCategory: MatDialogRef<ExportCategoryFile> | null;
	OpenExportPopUp() {
		this.globalService.showLoaderSpinner(true);
		if (this.childData.table == 'EngageboostCategoryMasters') {
			let link = 'categoriesexport/';
			this.global.generateSheet(link).subscribe(
				data => {
					if (data.status == 1) {
						let export_file_data: any;
						export_file_data = data.file_path;
						this.dialogRefExportCategory = this.dialog.open(ExportCategoryFile, {
							data: export_file_data
						});
						this.dialogRefExportCategory.afterClosed().subscribe(result => { });
					}
					this.globalService.showLoaderSpinner(false);
				},
				err => {
				},
				function () {
					// complete callback 
				});
		} else {
			// this.exportData();
		}
	}

	dialogRefViewAwb: MatDialogRef<ViewAwbComponent> | null;
	viewAWBNumbers(id: number) {
		if (this.childData.table == 'EngageboostShippingMasters') {
			this.dialogRefViewAwb = this.dialog.open(ViewAwbComponent, { data: id });
			this.dialogRefViewAwb.afterClosed().subscribe(result => {
				//this.generateGrid(0,'','','','');
			});
		}
	}

	dialogRefAwbMaster: MatDialogRef<AwbMasterComponent> | null;
	addAwbNumbers(id: number, method_name: any) {
		if (this.childData.table == 'EngageboostShippingMasters') {
			let data: any = {};
			data['id'] = id;
			data['method_name'] = method_name;
			this.dialogRefAwbMaster = this.dialog.open(AwbMasterComponent, { data: data });
			this.dialogRefAwbMaster.afterClosed().subscribe(result => {
				this.generateGrid(0, '', '', '', '');
			});
		}
	}
	// exportData() {
	// 	if(this.permission.export=='N') {			
	// 		this.dialogsService.alert('Permission Error', `You don't have permission to export`).subscribe(res => {});
	// 	} else {
	// 	  	let  req_post_data = {};
	// 	  	req_post_data = this.post_data;
	// 	  	//this.post_data = {"model":this.childData.table,"screen_name":this.childData.screen,"userid":this.userId,"search":this.search_text,"order_by":this.sortBy,"order_type":this.sortOrder,"status":this.filter,"website_id": this.websiteId,"company_id": this.companyId, "role_id": this.role_id, 'dist_company_id' : this.dist_company_id, 'parent_id' : this._business_type}
	//         this.global.exportData(req_post_data,this.config.currentPage).subscribe(
	//            	data => {
	//            		if(data.status){
	//            			window.open(GlobalVariable.BASE_Frontend_URL+'csvexport/export_data.xlsx');
	//            		}
	//            	},
	//            	err => console.log(err),
	//            	function(){}
	//         );	
	// 	}
	// }

	dialogRefColumnLayout: MatDialogRef<ColumnLayoutComponent> | null;
	loadColumnLayout() {
		let data: any = {}
		data["column"] = this.cols;
		data["layout"] = this.layout;
		this.dialogRefColumnLayout = this.dialog.open(ColumnLayoutComponent, { data: data });
		this.dialogRefColumnLayout.afterClosed().subscribe(result => {
			if(result != undefined) {
				this.cols = result;
				this.updateGrid(0);
			}
		});
	}

	loadGridData(event: any) {
		let selectedTab = event.index;
		this.selectedTabIndex = selectedTab;
		if (selectedTab == 0) { // All
			this.generateGrid(0, '', '', '', this.search_text)
		} else if (selectedTab == 1) { // Active
			this.generateGrid(1, '', '', 'n', this.search_text)
		} else { // Inactive
			this.generateGrid(1, '', '', 'y', this.search_text)
		}
	}

	// NEW fILTER STRAT
	load_fiter_column(){
		let data:any={};
		data.model= this.childData.table;
		data.website_id = this.globalService.getWebsiteId();
		data.search = this.formModel.field_name;
		data.screen_name = this.childData.screen;
		data.exclude = this.exclude_arr;
		this.global.getWebServiceData('advanced_filter', 'POST', data, '').subscribe(res => {
			if (res.status == 1) {
				this.field_arr=res.api_status[0];
			}
		}, err => {
			this.globalService.showToast('Something went wrong');
		})
	}

	FiltertoggleCheck( event: any) {
		this.load_fiter_column();
		let elements: NodeListOf < Element > = this.document.getElementsByClassName('action-box orderfilter');
		elements[0].classList.add('show');
		this.formModel.update_key='';
	}

	//  Filter close when click on cross icon in right side
	CloseFilter(event: any){
		let elements: NodeListOf < Element > = this.document.getElementsByClassName('action-box orderfilter');
		elements[0].classList.remove('show');
		var element = this.document.getElementById('meta_keywordbox');
		element.classList.remove("show");
		this.advanced_search = [];
		this.formModel.field_name = '';
		this.formModel.search_module = null;
		this.formModel.search_type = 1;
		this.formModel.search_data = null;
		this.generateGrid(0, '', '', '', '');
		this.load_fiter_column();
		this.exclude_arr=[];   
	}
	get_data(data :any,index:number){
		this.selectArr = [];
		var element = this.document.getElementById('meta_keywordbox');
		element.classList.add("show");
		this.formModel.field_name_show=data.columns;
		this.formModel.field_id=data.id;
		this.formModel.input_type=data.input_type;
		this.formModel.search_module = data.search_module;
		if(data.field_type == 'int'){
			this.ConditionArr=[
				{'type':1,'name':'Equals to'},
				{'type':2,'name':'Not Equals to'}
			]
		}
		if(data.field_type == 'float'){
			this.ConditionArr=[
				{'type':1,'name':'Equals to'},
				{'type':2,'name':'Not Equals to'},
				{'type':7,'name':'Geater than'},
				{'type':8,'name':'Less than'},
			]
		}
		if(data.field_type == 'date'){
			this.ConditionArr=[
				{'type':1,'name':'Equals to'},
				{'type':2,'name':'Not Equals to'},
				{'type':7,'name':'Geater than'},
				{'type':8,'name':'Less than'},
			]
		}
		if(data.field_type == 'string'){
			this.ConditionArr=[
				{'type':1,'name':'Equals to'},
				{'type':2,'name':'Not Equals to'},
				{'type':3,'name':'Starts with'},
				{'type':4,'name':'Ends with'},
				{'type':5,'name':'Contains'},
				{'type':6,'name':'Does not contains'}
			]
		}
		//this.field_arr.splice(index,1);
		this.get_select_data();
		this.load_fiter_column();
		this.remove_field_index = index;
	}

	sendSearchData(){
		var search_data:any=[];
		var search_data_show:any=[];
		if(this.formModel.input_type=='multi_select'){
			this.formModel.search_data.forEach(element => {
				search_data.push(element.id);
				search_data_show.push(element.name);
			});
		}
		if( this.formModel.input_type=='select'){
			search_data=this.formModel.search_data.id;
			search_data_show=this.formModel.search_data.name;
		}
		if(this.formModel.input_type=='date'){
			search_data=this.globalService.convertDate(this.formModel.search_data, 'yyyy-MM-dd');
			search_data_show=this.globalService.convertDate(this.formModel.search_data, 'yyyy-MM-dd');
		}
		if(this.formModel.input_type=='float' || this.formModel.input_type=='text' || this.formModel.input_type=='fix_select' ){
			search_data=this.formModel.search_data;
			search_data_show=this.formModel.search_data;
		}
		if(search_data != ''){
			this.Advancefilter={'field':this.formModel.field_name,'comparer':this.formModel.search_type,'key':search_data,'name':this.formModel.field_name, 'show_name':this.formModel.field_name_show,'key2':search_data_show,'input_type':this.formModel.input_type,'field_id':this.formModel.field_id}
			if(this.edit_index!=undefined){
				this.advanced_search.splice(this.edit_index,1);
			}
			this.advanced_search.push(this.Advancefilter);
			this.generateGrid(0, '', '', '', '');
			let elements: NodeListOf < Element > = this.document.getElementsByClassName('meta_keywordbox');
			elements[0].classList.remove('show');
			this.selectArr=[];
			this.formModel.search_module = null;
			this.formModel.update_key = search_data_show;
			this.formModel.field_name = '';
			this.formModel.search_type = 1;
			this.formModel.search_data = null;
			this.get_select_data();
			this.field_arr.splice(this.remove_field_index,1);
		} else {
			this.globalService.showToast('Please enter value');
		}
		this.edit_index=null;
	}
	
	remove_filter(index:number){
		let remove_val=this.advanced_search.splice(index,1);
		const items = this.exclude_arr;
		const valueToRemove = remove_val[0].field_id;
		this.exclude_arr = items.filter(item => item !== valueToRemove)
		this.generateGrid(0, '', '', '', '');
	}

	show_options(){
		this.search_type_option = true;
	}

	cancel_filter() {
		let elements: NodeListOf < Element > = this.document.getElementsByClassName('meta_keywordbox');
		elements[0].classList.remove('show');  
		this.generateGrid(0, '', '', '', '');
		this.formModel.field_name = '';
		this.formModel.temp_name = '';
		this.formModel.search_data = null;
		this.load_fiter_column();
	}
	get_select_data(field_id=this.formModel.field_id){
		this.global.getWebServiceData('global_list/'+field_id, 'GET', '', '').subscribe(res => {
			if(res){
				if(res.status!=0){
					this.banks=res.results[0].result[0];
					//SELECT TO START
					this.bankCtrl.setValue(this.banks[10]);
					this.filteredBanks.next(this.banks.slice());
					this.filteredBanksMulti.next(this.banks.slice());
					this.bankFilterCtrl.valueChanges
					.pipe(takeUntil(this._onDestroy))
					.subscribe(() => {
						this.filterBanks();
					});
					this.bankMultiFilterCtrl.valueChanges
					.pipe(takeUntil(this._onDestroy))
					.subscribe(() => {
						this.filterBanksMulti();
					});
					//SELECt END
					this.selectArr=res.results[0].result[0];
				}else{
					this.banks=this.selectArr;
					//SELECT TO START
					this.bankCtrl.setValue(this.banks[10]);
					this.filteredBanks.next(this.banks.slice());
					this.filteredBanksMulti.next(this.banks.slice());
					this.bankFilterCtrl.valueChanges
					.pipe(takeUntil(this._onDestroy))
					.subscribe(() => {
						this.filterBanks();
					});
					this.bankMultiFilterCtrl.valueChanges
					.pipe(takeUntil(this._onDestroy))
					.subscribe(() => {
						this.filterBanksMulti();
					});
					//SELECt END
				}
			}
		}, err => {
			this.selectArr=[];
		})
	}

	edit_filter(i:number, item:any){
		this.get_select_data(item.field_id);
		this.formModel.field_name_show=item.show_name;
		this.formModel.field_id=item.field_id;
		this.formModel.input_type=item.input_type;
		if(this.formModel.input_type=="multi_select"){
			this.formModel.search_data=item.key;
		}else{
			this.formModel.search_data=item.key;
		}
		this.formModel.field_name=item.name;
		this.formModel.search_type=item.comparer;
		this.edit_index=i;
		var element = this.document.getElementById('meta_keywordbox');
		element.classList.add("show");
	}
	// NEW fILTER END
}


@Component({
	templateUrl: './column.html',
})
export class ColumnLayoutComponent implements OnInit {
	public response: any;
	public errorMsg: string;
	public successMsg: string;
	public formModel: any = {};
	public ipaddress: any;
	public columnItems:any = [];
	public gridColumns: any = [];
	appliedColumns = [];
	constructor(
		private _router: Router,
		private dialogRef: MatDialogRef<ColumnLayoutComponent>,
		public dialog: MatDialog,
		@Optional() @Inject(MAT_DIALOG_DATA) public data: any
	) {
		dialog.afterOpen.subscribe(() => {
			let containerElem: HTMLElement = <HTMLElement>document.getElementsByClassName('mat-dialog-container')[0];
			containerElem.classList.remove('pop-box-up');
		});
	}

	ngOnInit() {
		let column:any = [];
		this.columnItems = this.data.column;
		this.gridColumns = this.data.layout;
		this.columnItems.forEach(element => {
			if(element.show == 1) {
				let obj: any = {};
				obj.title = element.title;
				obj.field = element.field;
				obj.child = element.child;
				obj.field_type = element.field_type;
				obj.show = element.show;
				column.push(obj);
			}			
		});
		this.appliedColumns = column;
	}

	drop(event: CdkDragDrop<{ title: string, field: string, field_type: string, show: string, child:string }>) {
		moveItemInArray(this.appliedColumns, event.previousIndex, event.currentIndex);
		//console.log(this.appliedColumns)
	}

	closeDialog() {
		this.dialogRef.close();
	}

	toggleCheck(id: any, event: any) {
		let column:any = [];
		let that = this;
		// console.log(event.source.name);
		// console.log("=============");
		// console.log(this.columnItems);
		this.gridColumns.forEach(function (item: any,key:any) {
			if(id == key) {
				if(event.checked) { // check and push new item to fields 
                    let isExist = that.appliedColumns.filter(item =>  {
						return item.field == event.source.name;
					});
					if(isExist.length == 0) {
						console.log("New Item is added");
						let obj: any = {};
						obj.title = item.title;
						obj.field = item.field;
						obj.child = item.child;
						obj.field_type = item.field_type;
						obj.show = 1;
						that.appliedColumns.push(obj);
					}
					
				} else { // check and remove the item from feids
					let index = that.appliedColumns.findIndex(item =>  {
						return (item.field == event.source.name);
					});
					let data=that.appliedColumns;
					that.appliedColumns.splice(index, 1);
					 console.log(that.appliedColumns);
					// if(Object.keys(isExist).length > 0) {
					// 	console.log("Remove a item");
					// }
				}
			}
		});
	}	

	applyChanges(){
		console.log(this.appliedColumns);
		this.dialogRef.close(this.appliedColumns);
	}
}



