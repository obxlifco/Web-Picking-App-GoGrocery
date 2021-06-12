import { mergeMap, map, filter } from 'rxjs/operators';
import { Component, OnInit, Inject } from '@angular/core';
import { Router, ActivatedRoute, NavigationEnd } from '@angular/router';
import { PromotionService } from './products.promotion.service';
import { GlobalService } from '../../global/service/app.global.service';
import { CookieService } from 'ngx-cookie';
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material';
import { Global } from '../../global/service/global';
import { OrderService } from '../../order/order/order.order.service';
// import { TabsComponent } from '../../partial-component/app.tabs.component';

@Component({
	templateUrl: './templates/coupon_conditions.html',
	providers: [PromotionService]
})
export class PromotionConditionsComponent implements OnInit {
	public response: any;
	public errorMsg: string;
	public successMsg: string;

	public discount_fields: any;
	public discount_conditions: any = [];
	public formModel: any = {};

	public tabIndex: number;
	public parentId: number = 0;
	public ipaddress: any;
	public add_edit: any;
	public discount_master_type: number;
	public product_id_qty: any;
	constructor(
		private _promotionService: PromotionService,
		public _globalService: GlobalService,
		private _router: Router,
		private _route: ActivatedRoute,
		private _cookieService: CookieService,
		public dialog: MatDialog,
		// public _tabsComponent: TabsComponent

	) {
		this.ipaddress = _globalService.getCookie('ipaddress');
		this._router.events.pipe(
			filter((event) => event instanceof NavigationEnd),
			map(() => this._route),
			map((route) => {
				while (route.firstChild) route = route.firstChild;
				return route;
			}),
			filter((route) => route.outlet === 'primary'),
			mergeMap((route) => route.data))
			.subscribe((event) => {
				this.discount_master_type = event['discountType'];
			});
	}

	// Initialization method
	ngOnInit() {
		this.tabIndex = +this._globalService.getCookie('active_tabs');
		this.parentId = this._globalService.getParentTab(this.tabIndex);
		this.add_edit = this._cookieService.getObject('action');
		if (this.add_edit == 'add') {
			this.formModel.discountId = this._cookieService.getObject('coupon_add');
		} else {
			this.formModel.discountId = this._cookieService.getObject('coupon_edit');
		}
		if(this.discount_master_type == 0) {
			this.discount_fields = [
				{
					field: { name: 'Category', value: 0 },
					condition: [
						{ name: 'Not Equals To', value: '!=' },
						{ name: 'Equals To', value: '==' },
					],
					is_pop: 1
				},
				{
					field: { name: 'SKU', value: 13633 },
					condition: [
						{ name: 'Not Equals To', value: '!=' },
						{ name: 'Equals To', value: '==' },
					],
					is_pop: 1
				},
				// {
				// 	field: { name: 'Customer', value: -2 },
				// 	condition: [
				// 		{ name: 'Not Equals To', value: '!=' },
				// 		{ name: 'Equals To', value: '==' },
				// 	],
				// 	is_pop: 1
				// },
				// {
				// 	field: { name: 'Customer Group', value: -3 },
				// 	condition: [
				// 		{ name: 'Not Equals To', value: '!=' },
				// 		{ name: 'Equals To', value: '==' },
				// 	],
				// 	is_pop: 1
				// }
			];
		} else {
			this.discount_fields = [
				{
					field: { name: 'Category', value: 0 },
					condition: [
						{ name: 'Not Equals To', value: '!=' },
						{ name: 'Equals To', value: '==' },
					],
					is_pop: 1
				},
				{
					field: { name: 'SKU', value: 13633 },
					condition: [
						{ name: 'Not Equals To', value: '!=' },
						{ name: 'Equals To', value: '==' },
					],
					is_pop: 1
				},
				{
					field: { name: 'Order Amount', value: -1 },
					condition: [
						{ name: 'Equals To', value: '==' },
						{ name: 'Equals or less than', value: '<=' },
						{ name: 'Equals or Greater than', value: '>=' },
					],
					is_pop: 0
				},
				// {
				// 	field: { name: 'Customer', value: -2 },
				// 	condition: [
				// 		{ name: 'Not Equals To', value: '!=' },
				// 		{ name: 'Equals To', value: '==' },
				// 	],
				// 	is_pop: 1
				// },
				// {
				// 	field: { name: 'Customer Group', value: -3 },
				// 	condition: [
				// 		{ name: 'Not Equals To', value: '!=' },
				// 		{ name: 'Equals To', value: '==' },
				// 	],
				// 	is_pop: 1
				// },
				// {
				// 	field: { name: 'Weekly', value: -7 },
				// 	condition: [
				// 		{ name: 'Not Equals To', value: '!=' },
				// 		{ name: 'Equals To', value: '==' },
				// 	],
				// 	is_pop: 1
				// },
				// {
				// 	field: { name: 'Free shiping', value: -8 },
				// 	condition: [
				// 		{ name: 'Equals To', value: '==' },
				// 		{ name: 'Equals or less than', value: '<=' },
				// 		{ name: 'Equals or Greater than', value: '>=' },
				// 	],
				// 	is_pop: 0
				// },
			];
		}
		// console.log(this.discount_master_type);
		this.formModel.discount_filters = [];
		this.formModel.discount_filters.push({});
		if (this.formModel.discountId > 0) {
			this._promotionService.conditionLoad(this.formModel.discountId).subscribe(
				data => {
					this.response = data;
					if (this.response.Rows.length) {
						this.formModel.discount_filters = [];
						let that = this;
						this.response.Rows.forEach(function (item: any, index: number) {
							that.formModel.discount_filters.push({
									id: item.id,
									field: item.fields,
									condition: item.condition,
									conditionValues: item.value,
									temp_conditionValues: item.value,
									all_product_id: item.all_product_id,
									all_customer_id: item.all_customer_id,
									all_category_id: item.all_category_id,
									all_product_qty: item.all_product_qty,
								});
							that.get_conditions(item.fields, index);
						});
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

	// Get conditions depending on a field
	get_conditions(value: any, index: number) {
		let that = this;
		this.discount_fields.forEach(function (item: any) {
			if (item.field.value == value) {
				that.discount_conditions[index] = item.condition;
				if (item.is_pop) {
					that.formModel.discount_filters[index]['is_pop'] = true;
				} else {
					that.formModel.discount_filters[index]['is_pop'] = false;
					//that.formModel.discount_filters[index]['conditionValues'] = item.value;
				}
			}
		});

	}
	change_value(value: any, index: number) {
		this.discount_fields.forEach(element => {
			if (element.field.value == value) {
				//this.formModel.discount_filters[index]['conditionValues'] = temp_value;
			} else {
				this.formModel.discount_filters[index]['conditionValues'] = null;
			}
		});

	}
	// Add more row
	addRow() {
		this.formModel.discount_filters.push({});
	}

	// Remove a row by index
	removeRow(index: number) {
		this.formModel.discount_filters.splice(index, 1);
	}

	// Add/Edit coupon conditions
	addEditCouponCondition(form: any) {
		this.errorMsg = '';
		var data: any = {};
		data.value = [];
		data['discount_master_id'] = this.formModel.discountId;
		let that = this;
		this.formModel.discount_filters.forEach(function (item: any) {

			if (Object.keys(item).length) {
				let row = {};
				row['fields'] = item.field;
				row['discount_master_id'] = that.formModel.discountId;
				row['condition'] = item.condition;
				row['value'] = item.conditionValues;
				row['all_product_qty'] = item.all_product_qty;

				if (item.field == 13633) {
					row['all_product_id'] = (item.all_product_id) ? item.all_product_id : null;
					row['all_customer_id'] = null;
					row['all_category_id'] = null;
				} else if (item.field == 0) {
					row['all_product_id'] = null;
					row['all_customer_id'] = null;
					row['all_category_id'] = (item.all_category_id) ? item.all_category_id : null;
				} else if (item.field == -2 || item.field == -3) {
					row['all_product_id'] = null;
					row['all_customer_id'] = (item.all_customer_id) ? item.all_customer_id : null;
					row['all_category_id'] = null;
				}

				row['condition_type'] = 'AND';
				row['ip_address'] = (that.ipaddress) ? that.ipaddress : '';
				row['updatedby'] = that._globalService.getUserId();
				if (that.add_edit == 'add') {
					row['createdby'] = that._globalService.getUserId();
				}

				data.value.push(row);
			}
		});
		
		if (data.value.length > 0) {
			this._promotionService.conditionAddEdit(data, this.formModel.discountId).subscribe(
				data => {
					this.response = data;
					if (this.response.status == 1) {
						if (this.add_edit == 'add') {
							this._cookieService.remove('action');
							this._cookieService.remove('coupon_add');
							if (this.discount_master_type == 0) {
								this._router.navigate(['/discount_product']);
							} else {
								this._router.navigate(['/discount_coupon']);
							}
						} else {
							this._cookieService.remove('action');
							this._cookieService.remove('coupon_edit');
							if (this.discount_master_type == 0) {
								this._router.navigate(['/discount_product']);
							} else {
								this._router.navigate(['/discount_coupon']);
							}
						}
						this._globalService.deleteTab(this.tabIndex, this.parentId);
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
		} else {
			this._cookieService.remove('action');
			this._cookieService.remove('coupon_edit');
			if (this.discount_master_type == 1) {
				this._router.navigate(['/discount_coupon']);
			} else {
				this._router.navigate(['/discount_product']);
			}
		}
	}
	// condition popup references
	dialogCategoryRef: MatDialogRef<CategoryListComponent> | null;
	dialogProductRef: MatDialogRef<ProductListComponent> | null;
	dialogCustomerGroupRef: MatDialogRef<CustomerGroupListComponent> | null;
	dialogCustomerRef: MatDialogRef<CustomerListComponent> | null;
	dialogWeekRef: MatDialogRef<WeekListComponent> | null;
	openPop(type: number, index: number) {
		let data: any = {};
		data['index'] = index;
		data['all_product_qty'] = this.product_id_qty;
		// console.log(data);
		if (type == 0) { // Category
			data['condition_id'] = this.formModel.discount_filters[index]['id'];
			this.dialogCategoryRef = this.dialog.open(CategoryListComponent, {
				data: data,
				height: '700px',
				width: '800px'
			});
			this.dialogCategoryRef.afterClosed().subscribe(result => {
				if (result) {
					this.formModel.discount_filters[result['index']]['all_category_id'] = result['category_ids'];
					this.formModel.discount_filters[result['index']]['conditionValues'] = result['category_names'];
				}
			});
		} else if (type == 13633) { // Sku
			data['all_product_id'] = this.formModel.discount_filters[index]['all_product_id'];
			data['product_names'] = this.formModel.discount_filters[index]['conditionValues'];
			data['all_product_qty'] = this.formModel.discount_filters[index]['all_product_qty'];
			this.dialogProductRef = this.dialog.open(ProductListComponent, {
				 data: data,
				 height: '800px',
                 width: '800px'
			});
			this.dialogProductRef.afterClosed().subscribe(result => {
				if (result) {
					// console.log(result);
					this.formModel.discount_filters[result['index']]['all_product_id'] = result['product_ids'];
					this.formModel.discount_filters[result['index']]['all_product_qty'] = result['all_product_qty'];
					this.formModel.discount_filters[result['index']]['conditionValues'] = result['product_names'];
					// this.product_id_qty = result['all_product_qty'];

				}
			});
		} else if (type == -2) { // Customer
			data['all_customer_id'] = this.formModel.discount_filters[index]['all_customer_id'];
			data['customer_names'] = this.formModel.discount_filters[index]['conditionValues'];
			this.dialogCustomerRef = this.dialog.open(CustomerListComponent, {
				data: data,
				height: '800px',
                width: '800px'
			});
			this.dialogCustomerRef.afterClosed().subscribe(result => {
				if (result) {
					this.formModel.discount_filters[result['index']]['all_customer_id'] = result['customer_ids'];
					this.formModel.discount_filters[result['index']]['conditionValues'] = result['customer_names'];
				}
			});
		} else if (type == -3) { // Customer type
			data['all_customer_id'] = this.formModel.discount_filters[index]['all_customer_id'];
			data['customer_names'] = this.formModel.discount_filters[index]['conditionValues'];
			this.dialogCustomerGroupRef = this.dialog.open(CustomerGroupListComponent, {
				data: data,
				height: '800px',
                width: '800px'
			 });
			this.dialogCustomerGroupRef.afterClosed().subscribe(result => {
				if (result) {
					this.formModel.discount_filters[result['index']]['all_customer_id'] = result['customer_grp_ids'];
					this.formModel.discount_filters[result['index']]['conditionValues'] = result['customer_grp_names'];
				}
			});
		} else if (type == -7) { // Weekly
			data['all_customer_id'] = this.formModel.discount_filters[index]['all_customer_id'];
			this.dialogWeekRef = this.dialog.open(WeekListComponent, {
				data: data,
				height: '800px',
				width: '800px' 
			});
			this.dialogWeekRef.afterClosed().subscribe(result => {
				if (result) {
					this.formModel.discount_filters[result['index']]['all_customer_id'] = result['customer_grp_ids'];
					this.formModel.discount_filters[result['index']]['conditionValues'] = result['customer_grp_names'];
				}
			});
		}
	}
}

@Component({
	templateUrl: './templates/coupon_conditions_category.html',
	providers: [PromotionService]
})
export class CategoryListComponent implements OnInit {
	public formModel: any = {};
	public response: any;
	public parent_category_list: any = [];
	public child_category_list: any = [];
	public sub_child_category_list: any = [];
	public sub_sub_child_category_list: any = [];
	constructor(
		public _globalService: GlobalService,
		private _promotionService: PromotionService,
		public dialog: MatDialog,
		private dialogRef: MatDialogRef<CategoryListComponent>,
		@Inject(MAT_DIALOG_DATA) public data: any
	) {
		this.formModel.select_category = 1;
	}
	ngOnInit() {
		this._promotionService.categoryLoad(this.data.condition_id).subscribe(
			data => {
				if (this.data.condition_id) {
					this.response = data;
					this.formModel.parent_categories = Object.assign([], this.response.parent_child);
					this.parent_category_list = this.response.category;
					let that = this;
					this.formModel.parent_categories.forEach(function (item: any, index: number) {
						if (item.category_4) {
							that.get_child_categories(item.category_1, index, 1, 0);
							that.get_child_categories(item.category_2, index, 2, 0);
							that.get_child_categories(item.category_3, index, 3, 0);
						}
						else if (item.category_3) {
							that.get_child_categories(item.category_1, index, 1, 0);
							that.get_child_categories(item.category_2, index, 2, 0);
							that.get_child_categories(item.category_3, index, 3, 0);

						} else if (item.category_2) {

							that.get_child_categories(item.category_1, index, 1, 0);
							that.get_child_categories(item.category_2, index, 2, 0);
						}
						else {
							if (item.category_1) {
								that.get_child_categories(item.category_1, index, 1, 0);
							}
						}
					});
				} else {
					this.response = data;
					this.formModel.parent_categories = [{}];
					this.parent_category_list = this.response.category;
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

	closeDialog() {
		this.dialogRef.close();
	}

	// Add more row
	addRow() {
		this.formModel.parent_categories.push({});
	}

	// Remove a row by index
	removeRow(index: number) {
		this.formModel.parent_categories.splice(index, 1);
		this.child_category_list.splice(index, 1);
		this.sub_child_category_list.splice(index, 1);
		this.sub_sub_child_category_list.splice(index, 1);
	}

	saveCategory() {
		let returnData: any = [];
		returnData['index'] = this.data.index;
		let category_ids: any = [];
		let categroy_names: any = [];
		let that = this;
		if (this.formModel.select_category == 1) {
			this.formModel.parent_categories.forEach(function (item: any, index: number) {
				if (item.category_4) {
					category_ids.push(item.category_4);
					if (that.sub_sub_child_category_list[index].length) {
						that.sub_sub_child_category_list[index].forEach(function (child: any, index: number) {
							if (child.id == item.category_4) {
								categroy_names.push(child.name);
							}
						});
					}
				} else if (item.category_3) {
					category_ids.push(item.category_3);
					if (that.sub_child_category_list[index].length) {
						that.sub_child_category_list[index].forEach(function (child: any, index: number) {
							if (child.id == item.category_3) {
								categroy_names.push(child.name);
							}
						});
					}
				} else if (item.category_2) {
					category_ids.push(item.category_2);
					if (that.child_category_list[index].length) {
						that.child_category_list[index].forEach(function (child: any, index: number) {
							if (child.id == item.category_2) {
								categroy_names.push(child.name);
							}
						});
					}
				} else {
					category_ids.push(item.category_1);
					if (that.parent_category_list.length) {
						that.parent_category_list.forEach(function (child: any, index: number) {
							if (child.id == item.category_1) {
								categroy_names.push(child.name);
							}
						});
					}
				}
			});
			returnData['category_ids'] = category_ids.join(',');
			returnData['category_names'] = categroy_names.join(',');
			this.dialogRef.close(returnData);
		} else {
			this._promotionService.allCategoryLoad().subscribe(
				data => {
					this.response = data;
					let that = this;
					this.response.category.forEach(function (item: any, index: number) {
						category_ids.push(item.id);
						categroy_names.push(item.name);
					});

					returnData['category_ids'] = category_ids.join(',');
					returnData['category_names'] = categroy_names.join(',');

					this.dialogRef.close(returnData);
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

	get_child_categories(parent_id: number, index: number, lvl: number, reset: number) {
		this._promotionService.getChildCategory(parent_id, 0, lvl + 1).subscribe(
			data => {
				this.response = data;
				if (this.response.status) {
					if (lvl == 1) { //level 1 category
						if (reset == 0) {
							this.child_category_list[index] = this.response.category;
						}
						else {
							this.child_category_list[index] = [];
							this.sub_child_category_list[index] = [];
							this.sub_sub_child_category_list[index] = [];
							this.child_category_list[index] = this.response.category;
							this.formModel.parent_categories[index].category_2 = 0;
							this.formModel.parent_categories[index].category_3 = 0;
							this.formModel.parent_categories[index].category_4 = 0;
						}
					}
					else if (lvl == 2) { //level 2 category
						if (reset == 0) {
							this.sub_child_category_list[index] = this.response.category;
						} else {
							this.sub_child_category_list[index] = [];
							this.sub_sub_child_category_list[index] = [];
							this.sub_child_category_list[index] = this.response.category;
							this.formModel.parent_categories[index].category_3 = 0;
							this.formModel.parent_categories[index].category_4 = 0;
						}
					} else { //level 3 category
						if (reset == 0) {
							this.sub_sub_child_category_list[index] = this.response.category;
						} else {
							this.sub_sub_child_category_list[index] = [];
							this.sub_sub_child_category_list[index] = this.response.category;
							this.formModel.parent_categories[index].category_4 = 0;
						}
					}
				} else {
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
	templateUrl: './templates/coupon_conditions_product.html',
	providers: [PromotionService,OrderService]
})
export class ProductListComponent implements OnInit {
	public product_list: any = [];
	public response: any;
	public selectedAll: boolean;
	public bulk_ids: any = [];
	public bulk_sku: any = [];
	public search_text: string;
	public sortBy: any = '';
	public sortOrder: any = '';
	public sortClass: any = '';
	public sortRev: boolean = false;
	public customer_list: any = [];
	public errorMsg: string;
	public successMsg: string;
	public bulk_ids_exist: any = [];
	public pagination: any = {};
	public pageIndex: number = 0;
	public pageList: number = 0;
	public website_id: number = 1;
	public stat: any = {};
	public result_list: any = [];
	public total_list: any = [];
	public cols: any = []
	public post_data = {};
	public page: number = 1;
	public filter: string = '';
	public maxSize: number = 10;
	public directionLinks: boolean = true;
	public autoHide: boolean = false;
	public config: any = {};
	public customers: any = [];
	public formModel: any = {};
	public userId: number;
	constructor(
		public _globalService: GlobalService,
		private _promotionService: PromotionService,
		public dialog: MatDialog,
		private dialogRef: MatDialogRef<ProductListComponent>,
		private _cookieService: CookieService,
		private _orderService: OrderService,
		@Inject(MAT_DIALOG_DATA) public data: any
	) {
	}
	ngOnInit() {
		console.log('this.data');
		console.log(this.data);
		if (this.data['all_product_id']) {
			this.bulk_ids = this.data['all_product_id'].split(",").map(Number);
		}
		if (this.data['product_names']) {
			this.bulk_sku = this.data['product_names'].split(",");
		}
		this.generateGrid(0, '', '', '', '');
	}

	closeDialog() {
		this.dialogRef.close();
	}
	//GRID FROM ELASTIC 
	generateGrid(reload: any, page: any, sortBy: any, filter: any, search: any) {
        let matchArr = [];
        /////////////// loading default conditions for grid /////////////////
        let conditions: any = {}
        conditions.isdeleted = 'n';
        let innerMatch: any = {};
        innerMatch.match = conditions;
        matchArr.push(innerMatch);
        let websiteId = this._globalService.getWebsiteId();
        if (websiteId != 1) {
            conditions = {}
            conditions.website_id = websiteId;
            innerMatch = {};
            innerMatch.match = conditions;
            matchArr.push(innerMatch);
        }

        if (search != '') { // pushing search conditions
            conditions = {}
            conditions.query = "*" + search + "*";
            innerMatch = {};
            innerMatch.query_string = conditions;
            matchArr.push(innerMatch);
        }

        // search = search.trimLeft();
        if (search == '') {
            this.search_text = '';
        } else {
            this.search_text = search;
        }
        this.sortBy = sortBy;
        if (sortBy != "" && sortBy != undefined) {
            if (this.sortRev) {
                this.sortOrder = "+";
                this.sortRev = !this.sortRev;
                this.sortClass = "icon-down";
            } else {
                this.sortOrder = "-";
                this.sortRev = !this.sortRev;
                this.sortClass = "icon-up";
            }
        }
        let userData = this._cookieService.getObject('userData');
        this.userId = userData['uid'];
        let data = {
            "userid": this.userId,
            "search": this.search_text.trim(),
            "order_by": sortBy,
            "order_type": this.sortOrder,
            "website_id": this._globalService.getWebsiteId(),
            // "channel_id": this.webshop_id,
            "show_all": 0
        }

        ///// startig query string filer ////////////////
        if (sortBy == '') {
            sortBy = 'id';
        }
        if (sortBy != 'id') {
            sortBy = sortBy + '.keyword';
        }
        let orderType = 'asc';
        if (this.sortOrder == '+') {
            orderType = 'asc'
        } else {
            orderType = 'desc'
        }
        let from = 0;
        if (page <= 0 || page == '') {
            page = 1;
            from = 0;
        } else {
            let start = page - 1;
            from = start * 25;
            //from = from - 1;
        }
        if (from < 0) {
            from = 0;
        }

        let extraFilter = JSON.stringify(matchArr);
        let elasticData = '{"query":{"bool":{"must":' + extraFilter + '}},"from": ' + from + ',"size": 25  ,"sort": [{"' + sortBy + '": "' + orderType + '"}]}';
        //this._orderService.productLoad(data, page).subscribe(
        this._orderService.getProductsES(elasticData, websiteId).subscribe(
            listData => {
                let tmpResult = [];
                listData.hits.hits.forEach(function (rows: any) {
                    tmpResult.push(rows._source);
                });
                
                if (tmpResult.length > 0) {
                    this.result_list = tmpResult;
                    let that = this;
                    this.result_list.forEach(function (item: any) {
                        if (that.bulk_ids.indexOf(item.id) > -1) {
                            item.Selected = true;
                        }
                        let stock = item.inventory[0].stock;
                        item.real_stock = stock;
                    });
                    
                    if (userData['elastic_host'] == '50.16.162.98') {  // this is for new elsatic server
                        listData.hits.total = listData.hits.total.value;
                    }
                    
                    for (var i = 0; i < listData.hits.total; i++) {
                        this.total_list.push(i);
                    }

                } else {
                    this.result_list = [];
				}
				//PAGINATION NOT WORKING PROPERLY
                // this.pagination.total_page = Math.ceil(listData.hits.total / 25);
                // this.config.currentPageCount = this.result_list.length
                // this.config.currentPage = page
				// this.config.itemsPerPage = 25;
				//PAGINATION NOT WORKING PROPERLY


				
				// this.pagination.total_page = Math.ceil(listData.hits.total / 10);
				// this.pageList = this.response.per_page_count;
				// this.config.currentPageCount = this.result_list.length
				// this.config.currentPage = page
				// this.config.itemsPerPage = 10;
                //console.log(this.config);
            },
            err => {
                this._globalService.showToast('Something went wrong. Please try again.');
            },
            function () {
                //completed callback
            }
        );
	}
	//NORMAL GRID
	generateGrid1(reload: any, page: any, sortBy: any, filter: any, search: any) {
		this.sortBy = sortBy;

		if (sortBy != "" && sortBy != undefined) {
			if (this.sortRev) {
				this.sortOrder = "-";
				this.sortRev = !this.sortRev;
				this.sortClass = "icon-down";
			} else {
				this.sortOrder = "+";
				this.sortRev = !this.sortRev;
				this.sortClass = "icon-up";
			}
		}
		let userData = this._cookieService.getObject('userData');
		this.userId = userData['uid'];
		let data = {
			"model": 'EngageboostProducts',
			"screen_name": 'list',
			"userid": this.userId,
			"search": this.search_text,
			"order_by": sortBy,
			"order_type": this.sortOrder,
			"status": 'n',
			"visibility_id": "Category,Search",
			"website_id": this._globalService.getWebsiteId()
		}

		this._promotionService.productLoad(data, page).subscribe(
			data => {
				let that = this;
				this.response = data;
				this.total_list = [];

				if (this.response.count > 0) {
					this.result_list = this.response.results[0].result;
					this.result_list.forEach(function (item: any) {
						item.quantity = 1;
						if (that.bulk_ids.indexOf(item.id) > -1) {
							item.Selected = true;
							//Checking for item quantity
							item.quantity = 1;
							let str = that.data.all_product_qty;
							let str_array = str.split(',');
							str_array.forEach(element => {
								let temp_id = element.split('@')[0];
								let temp_qty = element.split('@')[1];
								if (item.id == temp_id) {
									item.quantity = temp_qty;
								}
							});
						}
					});
					for (var i = 0; i < this.response.count; i++) {
						this.total_list.push(i);
					}
				} else {
					this.result_list = [];
				}
				this.pagination.total_page = this.response.per_page_count;
				this.pageList = this.response.per_page_count;
				this.config.currentPageCount = this.result_list.length
				this.config.currentPage = page
				this.config.itemsPerPage = this.response.page_size;

			},
			err => {
				this._globalService.showToast('Something went wrong. Please try again.');
			},
			function () {
				//completed callback
			}
		);
	}


	////////////////////////////Check/Uncheck//////////////

	toggleCheckAll(event: any) {

		let that = this;
		that.bulk_ids = [];
		that.bulk_sku = [];
		this.selectedAll = event.checked;
		this.result_list.forEach(function (item: any) {
			item.Selected = event.checked;
			if (item.Selected) {
				that.bulk_ids.push(item.id);
				that.bulk_sku.push(item.sku);
			}
		});

	}

	toggleCheck(id: any, event: any) {

		let that = this;
		this.result_list.forEach(function (item: any) {
			if (item.id == id) {
				item.Selected = event.checked;
				if (item.Selected) {
					that.bulk_ids.push(item.id);
					that.bulk_sku.push(item.sku);
				}
				else {
					var index = that.bulk_ids.indexOf(item.id);
					var index2 = that.bulk_sku.indexOf(item.id);
					that.bulk_ids.splice(index, 1);
					that.bulk_sku.splice(index2, 1);
				}
			}
		});
	}

	saveSku() {

		let returnData: any = [];
		returnData['index'] = this.data.index;

		let product_ids: string = '';
		let product_names: string = '';

		product_ids = this.bulk_ids.join(',');
		product_names = this.bulk_sku.join(',');

		// let that = this;
		// this.bulk_ids.forEach(function (item: any) {


		// 	//Updating result list check
		// 	that.result_list.forEach(function (inner_item: any) {

		// 		if (item == inner_item.id) {
		// 			products.push(inner_item.sku);
		// 			item_quantity.push(inner_item.id + '@' + inner_item.quantity);
		// 		}
		// 	});
		// });

		returnData['product_ids'] = product_ids;
		// returnData['product_names'] = product_names;
		returnData['product_names'] = product_names;
		// returnData['all_product_qty'] = item_quantity.join(",");

		this.dialogRef.close(returnData);
	}
}

@Component({
	templateUrl: './templates/coupon_conditions_customers.html',
	providers: [PromotionService,Global]
})
export class CustomerListComponent implements OnInit {
	public response: any;
	public errorMsg: string;
	public successMsg: string;
	public bulk_ids: any = [];
	public bulk_names: any = [];
	public bulk_ids_exist: any = [];
	public search_text: string;
	public pagination: any = {};
	public pageIndex: number = 0;
	public pageList: number = 0;
	public sortBy: any = '';
	public sortOrder: any = '';
	public sortClass: any = '';
	public sortRev: boolean = false;
	public selectedAll: any = false;
	public website_id: number = 1;
	public stat: any = {};
	public result_list: any = [];
	public total_list: any = [];
	public cols: any = []
	public post_data = {};
	public page: number = 1;
	public filter: string = '';
	public maxSize: number = 10;
	public directionLinks: boolean = true;
	public autoHide: boolean = false;
	public config: any = {};
	public customers: any = [];
	public formModel: any = {};
	public warehouse_list: any = [];
	public userId: number;

	constructor(
		public _globalService: GlobalService,
		private _promotionService: PromotionService,
		public dialog: MatDialog,
		private dialogRef: MatDialogRef<CustomerListComponent>,
		private _cookieService: CookieService,
		private global: Global,
		@Inject(MAT_DIALOG_DATA) public data: any
	) {
		global.reset_dialog();

	}


	ngOnInit() {
		if (this.data['all_customer_id']) {
			this.bulk_ids = this.data['all_customer_id'].split(",").map(Number);
		}
		if (this.data['customer_names']) {
			this.bulk_names = this.data['customer_names'].split(",");
		}
		this.generateGrid(0, '', '', '', '');
	}

	closeDialog() {
		this.dialogRef.close();
	}
	generateGrid(reload: any, page: any, sortBy: any, filter: any, search: any) {
		this.sortBy = sortBy;

		if (sortBy != "" && sortBy != undefined) {
			if (this.sortRev) {
				this.sortOrder = "-";
				this.sortRev = !this.sortRev;
				this.sortClass = "icon-down";
			} else {
				this.sortOrder = "+";
				this.sortRev = !this.sortRev;
				this.sortClass = "icon-up";
			}
		}

		let userData = this._cookieService.getObject('userData');
		this.userId = userData['uid'];

		let data = {
			"model": 'EngageboostCustomers',
			"screen_name": 'list',
			"userid": this.userId,
			"search": this.search_text,
			"order_by": sortBy,
			"order_type": this.sortOrder,
			"status": 'n',
			"website_id": this._globalService.getWebsiteId()
		}

		this._promotionService.customerLoad(data, page).subscribe(
			data => {
				console.log(data);
				
				let that = this;
				this.response = data;
				this.total_list = [];

				if (this.response.count > 0) {
					this.result_list = this.response.results[0].result;
					this.result_list.forEach(function (item: any) {
						if (that.bulk_ids.indexOf(item.id) > -1) {
							item.Selected = true;
						}
					});
					for (var i = 0; i < this.response.count; i++) {
						this.total_list.push(i);
					}
				} else {
					this.result_list = [];
				}
				console.log(this.total_list);

				this.pagination.total_page = this.response.per_page_count;
				this.pageList = this.response.per_page_count;
				this.config.currentPageCount = this.result_list.length
				this.config.currentPage = page
				this.config.itemsPerPage = this.response.page_size;
				console.log(this.config);

			},
			err => {
				this._globalService.showToast('Something went wrong. Please try again.');
			},
			function () {
				//completed callback
			}
		);
	}
	// Check/Uncheck
	toggleCheckAll(event: any) {

		let that = this;
		that.bulk_ids = [];
		this.selectedAll = event.checked;
		this.result_list.forEach(function (item: any) {
			item.Selected = event.checked;
			if (item.Selected) {
				that.bulk_ids.push(item.id);
				that.bulk_names.push(item.first_name);
			}
		});
	}

	toggleCheck(id: any, event: any) {
		let that = this;
		this.result_list.forEach(function (item: any) {
			if (item.id == id) {
				item.Selected = event.checked;
				if (item.Selected) {
					that.bulk_ids.push(item.id);
					that.bulk_names.push(item.first_name);
				}
				else {
					var index = that.bulk_ids.indexOf(item.id);
					that.bulk_ids.splice(index, 1);
					that.bulk_names.splice(index, 1);
				}
			}
		});
	}

	saveCustomers() {
		let returnData: any = [];
		returnData['index'] = this.data.index;
		let customer_ids: string = '';
		let customer_names: string = '';
		let customers: any = [];
		customer_ids = this.bulk_ids.join(',');
		customer_names = this.bulk_names.join(',');
		// let that = this;
		// this.bulk_ids.forEach(function (item: any) {

		// 	that.result_list.forEach(function (inner_item: any) {

		// 		if (item == inner_item.id) {
		// 			customers.push(inner_item.first_name);
		// 		}
		// 	});
		// });

		// customer_names = customers.join(',');
		returnData['customer_ids'] = customer_ids;
		returnData['customer_names'] = customer_names;
		// console.log(returnData);		
		this.dialogRef.close(returnData);
	}
}

@Component({
	templateUrl: './templates/coupon_conditions_customerGroups.html',
	providers: [PromotionService,Global]
})
export class CustomerGroupListComponent implements OnInit {
	public customerGrp_list: any = [];
	public response: any;
	public selectedAll: boolean;
	public bulk_ids: any = [];
	public bulk_names: any = [];
	public search_text: string;
	public sortBy: any = '';
	public sortOrder: any = '';
	public sortClass: any = '';
	public sortRev: boolean = false;
	public errorMsg: string;
	public successMsg: string;
	public bulk_ids_exist: any = [];
	public pagination: any = {};
	public pageIndex: number = 0;
	public pageList: number = 0;
	public website_id: number = 1;
	public stat: any = {};
	public result_list: any = [];
	public total_list: any = [];
	public cols: any = []
	public post_data = {};
	public page: number = 1;
	public filter: string = '';
	public maxSize: number = 10;
	public directionLinks: boolean = true;
	public autoHide: boolean = false;
	public config: any = {};
	public customers: any = [];
	public formModel: any = {};
	public userId: number;
	constructor(
		public _globalService: GlobalService,
		private _promotionService: PromotionService,
		public dialog: MatDialog,
		private dialogRef: MatDialogRef<CustomerGroupListComponent>,
		private _cookieService: CookieService,
		private global: Global,
		@Inject(MAT_DIALOG_DATA) public data: any
	) {
		global.reset_dialog();
	}
	ngOnInit() {
		
		if (this.data['all_customer_id']) {
			this.bulk_ids = this.data['all_customer_id'].split(",").map(Number);
		}
		if (this.data['customer_names']) {
			this.bulk_names = this.data['customer_names'].split(",");
		}
		this.generateGrid(0, '', '', '', '');
	}

	closeDialog() {
		this.dialogRef.close();
	}

	generateGrid(reload: any, page: any, sortBy: any, filter: any, search: any) {
		this.sortBy = sortBy;

		if (sortBy != "" && sortBy != undefined) {
			if (this.sortRev) {
				this.sortOrder = "-";
				this.sortRev = !this.sortRev;
				this.sortClass = "icon-down";
			} else {
				this.sortOrder = "+";
				this.sortRev = !this.sortRev;
				this.sortClass = "icon-up";
			}
		}

		let userData = this._cookieService.getObject('userData');
		this.userId = userData['uid'];

		let data = {
			"model": 'EngageboostCustomerGroup',
			"screen_name": 'list',
			"userid": this.userId,
			"search": this.search_text,
			"order_by": sortBy,
			"order_type": this.sortOrder,
			"status": 'n',
			"website_id": this._globalService.getWebsiteId()
		}

		this._promotionService.customerGroupLoad(data, page).subscribe(
			data => {
				let that = this;
				this.response = data;
				this.total_list = [];
				if (this.response.count > 0) {
					this.result_list = this.response.results[0].result;
					this.result_list.forEach(function (item: any) {
						if (that.bulk_ids.indexOf(item.id) > -1) {
							item.Selected = true;
						}
					});
					for (var i = 0; i < this.response.count; i++) {
						this.total_list.push(i);
					}
				} else {
					this.result_list = [];
				}
				this.pagination.total_page = this.response.per_page_count;
				this.pageList = this.response.per_page_count;
				this.config.currentPageCount = this.result_list.length
				this.config.currentPage = page
				this.config.itemsPerPage = this.response.page_size;
			},
			err => {
				this._globalService.showToast('Something went wrong. Please try again.');
			},
			function () {
				//completed callback
			}
		);
	}
	// Check/Uncheck
	toggleCheckAll(event: any) {
		let that = this;
		that.bulk_ids = [];
		this.selectedAll = event.checked;
		this.result_list.forEach(function (item: any) {
			item.Selected = event.checked;
			console.log(item);
			
			if (item.Selected) {
				that.bulk_ids.push(item.id);
				that.bulk_names.push(item.name);
			}
		});

	}

	toggleCheck(id: any, event: any) {
		let that = this;
		this.result_list.forEach(function (item: any) {
			if (item.id == id) {
				item.Selected = event.checked;
				if (item.Selected) {
					that.bulk_ids.push(item.id);
					that.bulk_names.push(item.name);
				}
				else {
					var index = that.bulk_ids.indexOf(item.id);
					that.bulk_ids.splice(index, 1);
					that.bulk_names.splice(index, 1);
				}
			}
		});
	}
	saveCustomerGroup() {
		let returnData: any = [];
		returnData['index'] = this.data.index;
		let customer_grp_ids: string = '';
		customer_grp_ids = this.bulk_ids.join(',');
		let customer_names = this.bulk_names.join(',');

		// let that = this;
		// this.bulk_ids.forEach(function (item: any) {
		// 	that.result_list.forEach(function (inner_item: any) {
		// 		if (item == inner_item.id) {
		// 			customer_grps.push(inner_item.name);
		// 		}
		// 	});
		// });
		returnData['customer_grp_ids'] = customer_grp_ids;
		returnData['customer_grp_names'] = customer_names;
		this.dialogRef.close(returnData);
	}
}

@Component({
	templateUrl: './templates/coupon_conditions_week.html',
	providers: [PromotionService]
})
export class WeekListComponent implements OnInit {
	public week_list: any = [];
	public response: any;
	public selectedAll: boolean;
	public bulk_ids: any = [];
	public search_text: string;
	public sortBy: any = '';
	public sortOrder: any = '';
	public sortClass: any = '';
	public sortRev: boolean = false;
	constructor(
		public _globalService: GlobalService,
		public dialog: MatDialog,
		private dialogRef: MatDialogRef<WeekListComponent>,
		private global: Global,
		@Inject(MAT_DIALOG_DATA) public data: any
	) {
		global.reset_dialog();
	}

	ngOnInit() {
		if (this.data['all_customer_id']) {
			this.bulk_ids = this.data['all_customer_id'].split(",").map(Number);
		}

		this.reload('', 'id');
	}

	closeDialog() {
		this.dialogRef.close();
	}

	reload(search_key: string, sortBy: string) {
		this.sortBy = sortBy;
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
		}

		let data = {};
		if (search_key.trim() != '') {
			data['search'] = search_key;
			this.search_text = search_key;
		} else {
			data['search'] = '';
			this.search_text = '';
		}

		data['order_by'] = this.sortBy;
		data['order_type'] = this.sortOrder;
		this.week_list = [
			{ 'id': '1', 'name': 'Monday' },
			{ 'id': '2', 'name': 'Tuesday' },
			{ 'id': '3', 'name': 'Wednesday' },
			{ 'id': '4', 'name': 'Thursday' },
			{ 'id': '5', 'name': 'Friday' },
			{ 'id': '6', 'name': 'Saturday' },
			{ 'id': '7', 'name': 'Sunday' },
		]
		let that = this;
		this.week_list.forEach(function (item: any) {

			if (that.bulk_ids.indexOf(item.id) > -1) {
				item.Selected = true;
			}

		});
		// this._promotionService.weekLoad(data).subscribe(
		//      	data => {

		//      		this.response = data;
		//      		this.week_list = this.response.customergrp;
		//      		let that=this;  
		//        		this.week_list.forEach(function(item:any){

		//                 if(that.bulk_ids.indexOf(item.id)>-1){
		//                 	item.Selected = true;
		//                 }

		//             });
		//      	},
		//      	err => {
		//      		this._globalService.showToast('Something went wrong. Please try again.');
		//      	},
		//      	function(){
		//      		//completed callback
		//      	}
		//   );
	}
	////////////////////////////Check/Uncheck//////////////
	toggleCheckAll(event: any) {
		let that = this;
		that.bulk_ids = [];
		this.selectedAll = event.checked;
		this.week_list.forEach(function (item: any) {
			item.Selected = event.checked;
			if (item.Selected) {
				that.bulk_ids.push(item.id);
			}
		});
	}

	toggleCheck(id: any, event: any) {
		let that = this;
		this.week_list.forEach(function (item: any) {
			if (item.id == id) {
				item.Selected = event.checked;
				if (item.Selected) {
					that.bulk_ids.push(item.id);
				} else {
					var index = that.bulk_ids.indexOf(item.id);
					that.bulk_ids.splice(index, 1);
				}
			}
		});
	}

	saveWeek() {
		let returnData: any = [];
		returnData['index'] = this.data.index;
		let customer_grp_ids: string = '';
		let customer_grp_names: string = '';
		let customer_grps: any = [];
		customer_grp_ids = this.bulk_ids.join(',');
		let that = this;
		this.bulk_ids.forEach(function (item: any) {
			that.week_list.forEach(function (inner_item: any) {

				if (item == inner_item.id) {
					customer_grps.push(inner_item.name);
				}
			});
		});
		customer_grp_names = customer_grps.join(',');
		returnData['customer_grp_ids'] = customer_grp_ids;
		returnData['customer_grp_names'] = customer_grp_names;
		this.dialogRef.close(returnData);
	}
}