import { Component, ElementRef, OnInit, Input, Inject, AfterViewInit, Optional } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA, MatDialog } from '@angular/material';
import { Router, ActivatedRoute, NavigationEnd } from '@angular/router';
import { Global } from '../../global/service/global';
import { DOCUMENT } from '@angular/platform-browser';
import { DialogsService } from '../../global/dialog/confirm-dialog.service';
import { ShipmentService } from './order.shipment.service';
import { GlobalService } from '../../global/service/app.global.service';
import { GlobalVariable } from '../../global/service/global';
/*import { MatColorPickerModule } from 'mat-color-picker'; */
import { CookieService } from 'ngx-cookie'; 
import { OrderService }  from '../../order/order/order.order.service';
import { AddEditTransition, AddEditStepFlipTransition } from '../.././addedit.animation';
// Picklist start here by cds on 17nth May 2019 - Picklist
@Component({
	templateUrl: './templates/picklist.html',
	providers: [ShipmentService],
	animations: [AddEditTransition],
	host: {
		'[@AddEditTransition]': ''
	},
})
export class ShipmentAddEditComponent implements OnInit {
	public response: any;
	public errorMsg: string;
	public successMsg: string;
	public formModel: any = {};
	private sub: any;
	public tabIndex: number;
	public parentId: number = 0;
	public picklistDetails: any = {};
	public picklist_img: boolean = false;
	public img_base: string;
	constructor(
		private _shipmentService: ShipmentService,
		public _globalService: GlobalService,
		private _router: Router,
		private _route: ActivatedRoute,
		private _cookieService: CookieService,
		public dialog: MatDialog,
		private dialogsService: DialogsService,
	) {}
	ngOnInit() {
		this.sub = this._route.params.subscribe(params => {
			this.formModel.picklist_id = +params['id']; // (+) converts string 'id' to a number
		});
		this.tabIndex = +this._globalService.getCookie('active_tabs');
		this.parentId = this._globalService.getParentTab(this.tabIndex);
		let website_id = this._globalService.getWebsiteId();
		let data: any = {};
		data.website_id = this._globalService.getWebsiteId();
		data.company_id = this._globalService.getCompanyId();
		data.picklist_id = this.formModel.picklist_id;
		data.shipmentType = "OrderWise"; // this is not used in web service
		data.selectedIds = "1"; //// this is not used in web service
		data.userId = this._globalService.getUserId();
		this.img_base = GlobalVariable.S3_URL + 'product/100x100/';
		this._shipmentService.loadPickList(data).subscribe(
			data => {
				this.picklistDetails = data.picklist_details;
				this.picklistDetails.pickListItems = data.api_status;
				this.formModel.is_picklist_created = this.picklistDetails.is_picklist_created;
				this.formModel.picklist_id = this.picklistDetails.picklist_id;
				this.formModel.warehouse_id = this.picklistDetails.warehouse_id;
				this.formModel.picklist_product_id = this.picklistDetails.picklist_product_id;
			},
			err => {
				this._globalService.showToast(data.message);
			},
			function() {}
		);
		this.formModel.created_date = new Date();
		this.formModel.payment_date = new Date();
	}

	addPicklist(form: any) {
		let data = {};
		data['is_picklist_created'] = this.formModel.is_picklist_created;
		data['picklist_id'] = this.formModel.picklist_id;
		data['website_id'] = this._globalService.getWebsiteId();
		data['company_id'] = this._globalService.getCompanyId();
		data['userId'] = this._globalService.getUserId();
		data['warehouse_id'] = this.formModel.warehouse_id;
		data['picklist_product_id'] = this.formModel.picklist_product_id;
		//console.log(data)
		//console.log('Yes coming...');
		this._shipmentService.generatePicklist(data).subscribe(
			data => {
				this._router.navigate(['/picklist/grn/' + this.formModel.picklist_id]);
			},
			err => {},
			function() {}
		);
		//this._router.navigate(['/shipment/invoice/' + this.formModel.shipment_id]);
	}
	
	showImage(event) {
		if (event.checked) {
			this.picklist_img = true;
		} else {
			this.picklist_img = false;
		}
	}

	delete_picklist_product(product_id) {
		let msg= "Do you really want to delete this product from pick list?";
		if(this.picklistDetails.length > 1){
			this.dialogsService.confirm('Warning', msg).subscribe(res => {
				if (res) {
				}
			});
		} else {
			this._globalService.showToast("You can't delete this product from picklist ! ");
		}
	}
}

// GRN start here by cds on 17nth May 2019 - Picklist
@Component({
	templateUrl: './templates/grn.html',
	providers: [ShipmentService],
	animations: [AddEditTransition],
	host: {
		'[@AddEditTransition]': ''
	},
})
export class ShipmentLabelComponent implements OnInit {
	public response: any;
	public errorMsg: string;
	public successMsg: string;
	public formModel: any = {};
	private sub: any;
	public tabIndex: number;
	public parentId: number = 0;
	public add_edit: any = '';
	public bulk_ids: any = [];
	public selectedAll: any = false;
	public individualRow: any = {};
	public shipmentOrder: any = [];
	public shipmentOrderProduct: any = [];
	public orderData: any = [];
	public isPickingDone: any = true;
	public img_base: string;
	constructor(
		private _shipmentService: ShipmentService,
		public _globalService: GlobalService,
		private _router: Router,
		private _route: ActivatedRoute,
		private _cookieService: CookieService,
		public dialog: MatDialog,
	) {
		this.img_base = GlobalVariable.S3_URL + 'product/100x100/';
	}
	ngOnInit() {
		this.tabIndex = +this._globalService.getCookie('active_tabs');
		this.parentId = this._globalService.getParentTab(this.tabIndex);
		let website_id = this._globalService.getWebsiteId();
		this.add_edit = 'add';
		this.sub = this._route.params.subscribe(params => {
			this.formModel.shipment_id = +params['id']; // (+) converts string 'id' to a number
		});
		let data: any = {};
		let userData = this._cookieService.getObject('userData');
		let dateFormat = userData["gl_date_format"].replace(/%/g, "");
		this._shipmentService.loadGrn(this.formModel.shipment_id, website_id).subscribe(
			data => {
				if (data.status == 1) {
					this.formModel.picklist_id = data.picklist_id;
					this.formModel.shipmentOrder = data.api_status;
					this.formModel.time_slot = data.time_slot;
					this.formModel.orderData = data.time_slot;
					if(data.total_grn_completed_order > 0) {
						this.isPickingDone = false;
					}
					let that = this;
					this.formModel.orderData.forEach(function(item:any, index:number) {
						let selected_order_arr: any = [];
						that.formModel.shipmentOrder.forEach(function(inner_item:any, inner_index:number) {
							if(item.time_slot_id == inner_item.order_data.time_slot_id) {
								//console.log('Yes coming');
								if(item.ids_arr[0] == inner_item.order_data.order_id) {
									//inner_item.order_data.display_time_slot_date = that._globalService.convertDate(inner_item.order_data.display_time_slot_date, dateFormat);
									item['selected_order'] = inner_item;
									item['right_order_list'] = false;
									if(item['selected_order'].shipment_status == 'Created' || item['selected_order'].shipment_status == 'Picking') {
										item['selected_order']['grn_finish'] = 'n';
										that.checking_grn_done(item['selected_order'].order, item.time_slot_id);
									} else {
										item['selected_order']['grn_finish'] = 'y';
									}
								}
								let selected_order_list: any = {};
								selected_order_list['order_id'] = inner_item.order_data.order_id;
								selected_order_list['custom_order_id'] = inner_item.order_data.custom_order_id;
								selected_order_list['shipment_status'] = inner_item.shipment_status;
								selected_order_arr.push(selected_order_list);
							}
						});
						item['selected_order_list'] = selected_order_arr;
					});
				} else {
					this._globalService.showToast(data.message);
				}
			},
			err => {
				this._globalService.showToast(data.message);
			},
			function() {

			}
		);
	}

	// new grn moduel from chakradhar...
	changeQuantity(order_id:any, shipemnt_order_product_id:any, scan_quantity:any, time_slot_id:any, field_type:any ) {
		//console.log(order_id);
		//console.log(shipemnt_order_product_id);
		//console.log(scan_quantity);
		let that = this;
		this.formModel.orderData.forEach(function(item:any, index:number) {
			if(item.selected_order.order_data.order_id == order_id && item.time_slot_id == time_slot_id) {
				if(item.selected_order.shipment_status != 'Created' && item.selected_order.shipment_status != 'Picking') {
					that.errorMsg = '';
					that.successMsg = 'Picking fully completed for this order.';
					return false;
				}
				let error_count = 0;
				item.selected_order.order_data.shipment_order_product.forEach(function(inner_item:any, inner_index:number) {
					let quantity = inner_item.quantity;
					if(inner_item.order_product == shipemnt_order_product_id) {
						//console.log(shipemnt_order_product_id);
						let remaining_quantity = quantity;
						let grn_quantity = inner_item.grn_quantity;
						let shortage = inner_item.shortage;
						
						if(field_type == 'GRN') {
							grn_quantity = scan_quantity;
							remaining_quantity = remaining_quantity-shortage;
						} else {
							shortage = scan_quantity;
							remaining_quantity = remaining_quantity-grn_quantity;
						}

						let total_quantity = grn_quantity + shortage;
						if(total_quantity > quantity) {
							that._globalService.showToast('Entered value could not be greater Item Order.'); //Picked Qty
							if(field_type == 'GRN') {
								inner_item.grn_quantity = remaining_quantity;
							} else {
								inner_item.shortage = remaining_quantity;
							}
							return false;
						} else {
							if(field_type == 'GRN') {
								inner_item.grn_quantity = scan_quantity;
							} else {
								inner_item.shortage = scan_quantity;
							}
							return false;   
						}
					}
				});
				that.checking_grn_done(order_id, time_slot_id);
			}
		});
	}

	// grn code started...
	checking_grn_done(order_id:any,time_slot_id:any) {
		let that = this;
		this.formModel.orderData.forEach(function(item:any, index:number) {
			if(item.time_slot_id == time_slot_id) {
				if(item.selected_order.order_data.order_id == order_id && item.time_slot_id == time_slot_id) {
					let error_count = 0;
					item.selected_order.order_data.shipment_order_product.forEach(function(inner_item:any, inner_index:number) {
						let quantity = inner_item.quantity;
						let other_quantity = inner_item.grn_quantity + inner_item.shortage; //returns + third_party_qty + instock_qty
						if(quantity != other_quantity) {
							error_count++;
							inner_item.picked_item_class = ''
						} else {
							inner_item.picked_item_class = 'picked_item'
						}
					});
					if(error_count == 0) {
						item.selected_order['grn_finish'] = 'y';
					} else {
						item.selected_order['grn_finish'] = 'n';
					}
					if(error_count == 0) {
						item.selected_order['grn_finish'] = 'y';
					} else {
						item.selected_order['grn_finish'] = 'n';
					}
				}
			}
		});
	}

	getGrnOrderDetails(order_id: any, time_slot_id:any) {
		let data: any = {};
		data.trent_picklist_id = this.formModel.picklist_id;
		data.order_id = order_id;
		data.website_id = this._globalService.getWebsiteId();
		let userData = this._cookieService.getObject('userData');
		let dateFormat = userData["gl_date_format"].replace(/%/g, "");
		let that = this;
		this._shipmentService.getGrnOrderDetails(data).subscribe(
			data => {
				if (data.status == 1) {
					this.formModel.orderData.forEach(function(item:any, index:number) {
						// console.log(that.formModel.orderData);
						if(item.time_slot_id == time_slot_id) {
							item['selected_order'] = data.api_status[0];
							if(item['selected_order'].shipment_status == 'Created' || item['selected_order'].shipment_status == 'Picking') {
								item['selected_order']['grn_finish'] = 'n';
							} else {
								item['selected_order']['grn_finish'] = 'y';
							}
							//item['selected_order'].order_data.display_time_slot_date = that._globalService.convertDate(data.api_status[0].order_data.display_time_slot_date, dateFormat);
							item['selected_order'].no_of_crates = data.api_status[0].no_of_crates
						}
					});
					this.toggleMenu(order_id, time_slot_id);
				} else {
					this._globalService.showToast(data.message);
				}
				// console.log(this.formModel.orderData[0].selected_order.order_data.billing_phone)
			},
			err => {
				this._globalService.showToast(data.message);
			},
			function() {

			}
		);
	}

	toggleMenu(order_id:any, time_slot_id:any) {
		this.formModel.orderData.forEach(function(item:any, index:number) {
			if(item.time_slot_id == time_slot_id) {
				item.right_order_list = !item.right_order_list
			}
		});
	}

	get_grn_substitute_products() {

	}

	// List of order prodduct for search and scan...
	search_picked_products(picklist_id: any, order_id: any) {
		let data: any = {};
		data.trent_picklist_id = this.formModel.picklist_id;
		data.order_id = order_id;
		this._shipmentService.searchPickedProducts(data).subscribe(
			data => {
				if (data.status == 1) {
					this.formModel.InvoiceDetails = data.InvoiceDetails;
				} else {
					this._globalService.showToast(data.message);
				}
			},
			err => {
				this._globalService.showToast(data.message);
			},
			function() {

			}
		);
	}

	// get_order_products_info(barcode, 1, 'EAN', order_id);
	get_order_products_info(order_id: any,barcode:any='',shipment_status:any) {
		let data: any = {};
		data.trent_picklist_id = this.formModel.picklist_id;
		data.order_id = order_id;
		data.ean = barcode;
		data.scan_qty = 1;
		data.num_type = 'EAN';
		if(shipment_status != 'Created' && shipment_status != 'Picking') {
			this.errorMsg = '';
			this.successMsg = 'Picking fully completed.';
		} else if(barcode == '') {
			this.successMsg = '';
			this.errorMsg = "Please enter product ean number.";
		} else {
			this._shipmentService.getOrderProductsInfo(data).subscribe(
				data => {
					if (data.status == 1) {
						let shipment_order_product_id = data.api_status.id;
						this.formModel.orderData.forEach(function(item:any, index:number) {
							if(item.selected_order.order == order_id) {
								let error_count = 0;
								item.selected_order.order_data.shipment_order_product.forEach(function(inner_item:any, inner_index:number) {
									let quantity = inner_item.quantity;
									if(shipment_order_product_id == inner_item.id) {
										inner_item.grn_quantity = inner_item.quantity-inner_item.shortage;
									}
									let other_quantity = inner_item.grn_quantity + inner_item.shortage; //returns + third_party_qty + instock_qty
									if(quantity != other_quantity) {
										error_count++;
									}
								});
								if(error_count == 0) {
									item.selected_order['grn_finish'] = 'y';
								} else {
									item.selected_order['grn_finish'] = 'n';
								}
								if(error_count == 0) {
									item.selected_order['grn_finish'] = 'y';
								} else {
									item.selected_order['grn_finish'] = 'n';
								}
							}
						});
					} else {
						this._globalService.showToast(data.message);
					}
				},
				err => {
					this._globalService.showToast(data.message);
				},
				function() {

				}
			);
		}
	}

	// Get all crates....
	get_all_crates(picklist_id: any, order_id: any) {
		let data: any = {};
		data.trent_picklist_id = this.formModel.picklist_id;
		data.order_id = order_id;
		data.userId = this._globalService.getUserId();
		this._shipmentService.getAllCrates(data).subscribe(
			data => {
				if (data.status == 1) {
					this.formModel.InvoiceDetails = data.InvoiceDetails;
				} else {
					this._globalService.showToast(data.message);
				}
			},
			err => {
				this._globalService.showToast(data.message);
			},
			function() {

			}
		);
	}

	handleSpacebar(ev:any) {
		//console.log(ev.keyCode);
		if (ev.keyCode === 13 || ev.keyCode === 32) {
			ev.stopPropagation();
		}
	}

	// Get add all crates....
	add_crates(order_id: any, crate_barcode:any = '', shipment_status:any) {
		//console.log(order_id);console.log(crate_barcode);
		let data: any = {};
		//data.crate_barcode = '12123';
		data.trent_picklist_id = this.formModel.picklist_id;
		data.order_id = order_id;
		data.crate_barcode = crate_barcode;
		data.userId = this._globalService.getUserId();
		//console.log(data);
		if(crate_barcode) {
			crate_barcode = crate_barcode.trim();
		}
		if(shipment_status != 'Created' && shipment_status != 'Picking') {
			this.successMsg = '';
			this.errorMsg = 'Picking fully completed.';
		} else if(crate_barcode == '') {
			this.successMsg = '';
			this.errorMsg = "Please enter crate name."
		} else {
			this._shipmentService.addCrates(data).subscribe(
				data => {
					if (data.crate_count > 0) { //data.status == 1 && 
						this.formModel.orderData.forEach(function(item:any, index:number) {
							if(item.selected_order.order == order_id) {
								item.selected_order.no_of_crates = data.crate_count
								item.scan_crate = '';
							}
						});
						this._globalService.showToast("Crate added successfully");
					} else {
						this._globalService.showToast(data.message);
					}
				},
				err => {
					this._globalService.showToast(data.message);
				},
				function() {
				}
			);
		}
	}

	grn_save_as_draft(order_id: any) {
		let that = this;
		let error_count = 0;
		let success_message = '';
		let shipment_status = 'Picking';
		let save_order_data_arr: any = [];
		this.formModel.orderData.forEach(function(item:any, index:number) {
			if(item.selected_order.order_data.order_id == order_id) {
				shipment_status = item.selected_order.shipment_status;
				item.selected_order.order_data.shipment_order_product.forEach(function(inner_item:any, inner_index:number) {
					//console.log('Yes coming');
					let selected_order_list: any = {};
					selected_order_list['id'] = inner_item.id;
					selected_order_list['shipment'] = inner_item.shipment;
					selected_order_list['trent_picklist_id'] = inner_item.trent_picklist_id;
					selected_order_list['quantity'] = inner_item.quantity;
					selected_order_list['shortage'] = inner_item.shortage;
					selected_order_list['returns'] = inner_item.returns;
					selected_order_list['grn_quantity'] = inner_item.grn_quantity;
					selected_order_list['shipment_status'] = inner_item.shipment_status;
					selected_order_list['shipment_order_id'] = inner_item.shipment_order;
					selected_order_list['order_id'] = inner_item.order;
					selected_order_list['product_id'] = inner_item.product;
					selected_order_list['order_product_id'] = inner_item.order_product;
					save_order_data_arr.push(selected_order_list);
				});
				that.shipmentOrderProduct = save_order_data_arr;
			}
		});
		let data: any = {};
		data.shipment_id = this.formModel.shipment_id;
		data.order_id = order_id;
		data.shipmentOrderProduct = this.shipmentOrderProduct;
		data.userId = this._globalService.getUserId();
		//console.log(shipment_status);
		if(shipment_status != 'Created' && shipment_status != 'Picking') {
			success_message = 'Picking fully completed for this order.';
			++error_count
		} 

		if(error_count > 0) {
			this.successMsg = success_message;
			this.errorMsg = '';
			return false;
		}

		this._shipmentService.grnSaveAsDraft(data).subscribe(
			data => {
				if (data.status == 1) {
					//this.formModel.InvoiceDetails = data.InvoiceDetails;
					this.errorMsg = '';
					this.successMsg = "GRN product data save successfully.";
					//this._globalService.showToast("GRN product data save successfully");
				} else {
					this._globalService.showToast(data.message);
				}
			},
			err => {
				this._globalService.showToast(data.message);
			},
			function() {
			}
		);
	}

	grn_save_as_draft_sustitute(order_id: any,time_slot_id:any) {
		let that = this;
		let error_count = 0;
		let success_message = '';
		let shipment_status = 'Picking';
		let save_order_data_arr: any = [];
		this.formModel.orderData.forEach(function(item:any, index:number) {
			if(item.selected_order.order_data.order_id == order_id) {
				shipment_status = item.selected_order.shipment_status;
				item.selected_order.order_data.shipment_order_product.forEach(function(inner_item:any, inner_index:number) {
					//console.log('Yes coming');
					let selected_order_list: any = {};
					selected_order_list['id'] = inner_item.id;
					selected_order_list['shipment'] = inner_item.shipment;
					selected_order_list['trent_picklist_id'] = inner_item.trent_picklist_id;
					selected_order_list['quantity'] = inner_item.quantity;
					selected_order_list['shortage'] = inner_item.shortage;
					selected_order_list['returns'] = inner_item.returns;
					selected_order_list['grn_quantity'] = inner_item.grn_quantity;
					selected_order_list['shipment_status'] = inner_item.shipment_status;
					selected_order_list['shipment_order_id'] = inner_item.shipment_order;
					selected_order_list['order_id'] = inner_item.order;
					selected_order_list['product_id'] = inner_item.product;
					selected_order_list['order_product_id'] = inner_item.order_product;
					save_order_data_arr.push(selected_order_list);
				});
				that.shipmentOrderProduct = save_order_data_arr;
			}
		});
		let data: any = {};
		data.shipment_id = this.formModel.shipment_id;
		data.order_id = order_id;
		data.shipmentOrderProduct = this.shipmentOrderProduct;
		data.userId = this._globalService.getUserId();
		//console.log(shipment_status);
		if(shipment_status != 'Created' && shipment_status != 'Picking') {
			success_message = 'Picking fully completed for this order.';
			++error_count
		} 

		if(error_count > 0) {
			this.successMsg = success_message;
			this.errorMsg = '';
			return false;
		}

		this._shipmentService.grnSaveAsDraft(data).subscribe(
			data => {
				if (data.status == 1) {
					//this.formModel.InvoiceDetails = data.InvoiceDetails;
					this.errorMsg = '';
					this.successMsg = "GRN product data save successfully.";
					//this._globalService.showToast("GRN product data save successfully");
					this.getGrnOrderDetails(order_id, time_slot_id);
				} else {
					this._globalService.showToast(data.message);
				}
			},
			err => {
				this._globalService.showToast(data.message);
			},
			function() {
			}
		);
	}

	grn_complete (order_id: any) {
		let that = this;
		let save_order_data_arr: any = [];
		let error_count = 0;
		let error_message = '';
		let success_message = '';
		let no_of_crates = 0
		let shipment_order_id = 0
		let shipment_status = 'Picking';
		let custom_order_id = '';
		let grn_finish = 'n';
		this.formModel.orderData.forEach(function(item:any, index:number) {
			if(item.selected_order.order_data.order_id == order_id) {
				no_of_crates = item.selected_order.no_of_crates;
				shipment_status = item.selected_order.shipment_status;
				shipment_order_id = item.selected_order.id;
				custom_order_id  = item.selected_order.custom_order_id;
				grn_finish  = item.selected_order.grn_finish;
				item.selected_order.order_data.shipment_order_product.forEach(function(inner_item:any, inner_index:number) {
					//console.log('Yes coming');
					let selected_order_list: any = {};
					selected_order_list['id'] = inner_item.id;
					selected_order_list['shipment'] = inner_item.shipment;
					selected_order_list['trent_picklist_id'] = inner_item.trent_picklist_id;
					selected_order_list['quantity'] = inner_item.quantity;
					selected_order_list['shortage'] = inner_item.shortage;
					selected_order_list['returns'] = inner_item.returns;
					selected_order_list['grn_quantity'] = inner_item.grn_quantity;
					selected_order_list['shipment_status'] = inner_item.shipment_status;
					selected_order_list['shipment_order_id'] = inner_item.shipment_order;
					selected_order_list['order_id'] = inner_item.order;
					selected_order_list['product_id'] = inner_item.product;
					selected_order_list['order_product_id'] = inner_item.order_product;
					save_order_data_arr.push(selected_order_list);
				});
				that.shipmentOrderProduct = save_order_data_arr;
			}
		});
		//console.log(this.formModel.orderData[0].selected_order);
		let data: any = {};
		//data = this.formModel.orderData[0].selected_order;
		data.order_id = order_id;
		data.trent_picklist_id = this.formModel.picklist_id;
		data.shipment_id = this.formModel.shipment_id;
		data.no_of_crates = no_of_crates;
		data.shipmentOrderProduct = this.shipmentOrderProduct;
		data.userId = this._globalService.getUserId();
		data.id = shipment_order_id;
		//console.log(data);
		if(shipment_status != 'Created' && shipment_status != 'Picking') {
			success_message = 'Picking fully completed for this order.';
			error_message = ''
			++error_count
		} else if(no_of_crates <= 0 && error_count == 0) {
			success_message = ''
			error_message = "Crates is not selected for " + custom_order_id + ' order.';
			++error_count;
		} else if(grn_finish == 'n') {
			success_message = ''
			error_message = "Picking not completed for " + custom_order_id + ' order.';
			++error_count;
		}
		// console.log(this.successMsg);
		if(error_count > 0) {
			this.successMsg = success_message;
			this.errorMsg = error_message;
			return false;
		}
		this._shipmentService.grnComplete(data).subscribe(
			data => {
				if (data.status == 1) {
					this.errorMsg = '';
					this.successMsg = "You have successfully created Picking.";
					this.isPickingDone = false;
					//this._globalService.showToast("You have successfully created Picking.");
					this.formModel.orderData.forEach(function(item:any, index:number) {
						if(item.selected_order.order_data.order_id == order_id) {
							let total_grn_completed_order = item.total_grn_completed_order
							item.selected_order_list.forEach(function(inner_item:any, inner_index:number) {
								if(inner_item.order_id == order_id) {
									inner_item.shipment_status = 'Invoicing';
									total_grn_completed_order = total_grn_completed_order+1;
									item.selected_order.shipment_status = 'Invoicing';
								}
							});
							item.total_grn_completed_order = total_grn_completed_order;
						}
					});
				} else {
					this._globalService.showToast(data.message);
				}
			},
			err => {
				this._globalService.showToast(data.message);
			},
			function() {
			}
		);
	}

	grnContinue(form: any) {
		this._router.navigate(['/picklist/invoice/' + this.formModel.shipment_id]);
	}

	dialogRefCrates: MatDialogRef < ManageCrateComponent > | null;
	openPopCrates(order_id: any) {
		this.dialogRefCrates = this.dialog.open(ManageCrateComponent, {
			data: {"trent_picklist_id":this.formModel.picklist_id, "order_id":order_id },
			disableClose: false
		});
		this.dialogRefCrates.afterClosed().subscribe(result => {
			let data: any = {};
			data.trent_picklist_id = this.formModel.picklist_id;
			data.order_id = order_id;
			data.search = '';
			//console.log(data);
			this._shipmentService.getAllCrates(data).subscribe(data => {
				this.response = data;
				let crate_count = this.response.crate_list.length;
				this.formModel.orderData.forEach(function(item:any, index:number) {
					if(item.selected_order.order_data.order_id == order_id) {
						item.selected_order.no_of_crates = crate_count
					}
				});
				//console.log(this.response);
			}, err => {
				this._globalService.showToast('Something went wrong. Please try again.');
			}, function() {

			});
		});
	}

	dialogRefOrderProduct: MatDialogRef <GrnOrderProductComponent> | null;
	searchPickedProducts(order_id: any, time_slot_id) {
		this.dialogRefOrderProduct = this.dialog.open(GrnOrderProductComponent, {
			data: {"trent_picklist_id":this.formModel.picklist_id, "order_id":order_id, "time_slot_id":time_slot_id}
		});
		let that = this;
		this.dialogRefOrderProduct.afterClosed().subscribe(result => {
			if(result && result.status==1) {
				let action_id = result.action_id
				let error_message = '';
				that.formModel.orderData.forEach(function(item:any, index:number) {
					if(item.time_slot_id == time_slot_id) {
						if(item['selected_order'].shipment_status != 'Created' && item['selected_order'].shipment_status != 'Picking') {
							error_message = 'Picking fully completed for this order.';
							that.successMsg = '';
							that.errorMsg = error_message;
							return false;
						} else {
							if(item.selected_order.order_data.order_id == order_id) {
								let error_count = 0;
								item.selected_order.order_data.shipment_order_product.forEach(function(inner_item:any, inner_index:number) {
									let quantity = inner_item.quantity;
									if(action_id.indexOf(inner_item.id) !== -1) {
										inner_item.grn_quantity = inner_item.quantity-inner_item.shortage;
									}
									let other_quantity = inner_item.grn_quantity + inner_item.shortage; //returns + third_party_qty + instock_qty
									if(quantity != other_quantity) {
										error_count++;
									}
								});
								if(error_count == 0) {
									item.selected_order['grn_finish'] = 'y';
								} else {
									item.selected_order['grn_finish'] = 'n';
								}
								if(error_count == 0) {
									item.selected_order['grn_finish'] = 'y';
								} else {
									item.selected_order['grn_finish'] = 'n';
								}
							}
						}
					}
				});
			}
		});
	}
	
	printPicklist() {
		let data: any = {};
		let selected_ids = this.bulk_ids.join(",");
		data.website_id = this._globalService.getWebsiteId();
		data.company_id = this._globalService.getCompanyId();
		data.trent_picklist_id = this.formModel.picklist_id;
		data.selectedIds = selected_ids; // this is not used in web service
		this._shipmentService.printPicklist(data).subscribe(
			data => {
				this.formModel.printsection = data.picklist_content;
			},
			err => {
				this._globalService.showToast("Someting went wrong");
			}, () => {
				setTimeout(this.printPicklistContent, 1000)
			}
		);
	}

	printPicklistContent() {
		let popupWinindow
		let innerContents = document.getElementById("printsection").innerHTML;
		popupWinindow = window.open('', '_blank', 'menubar=no,toolbar=no,location=no,status=no,titlebar=no');
		popupWinindow.document.open();
		popupWinindow.document.write('<html><head>');
		popupWinindow.document.write('<link rel="stylesheet" href="' + window.location.protocol + '//' + window.location.hostname + ':3000/' + 'assets/css/print.css">');
		popupWinindow.document.write('</head><body onload="window.print()">' + innerContents + '</html>');
		popupWinindow.document.close();
	}
	// edit GRN  edit_grn_pop added here 
	dialogRefEditGRN: MatDialogRef <EditGRNComponent > | null;
	edit_grn_pop(order_id: any, product_id: any, time_slot_id:any ) {
		this.dialogRefEditGRN = this.dialog.open(EditGRNComponent, {
			data: {"trent_picklist_id":this.formModel.picklist_id, "order_id":order_id, "product_id":product_id},
			disableClose: false
		});
		let that = this;
		this.dialogRefEditGRN.afterClosed().subscribe(result => {
			if(result && result.status==1) {
				that.getGrnOrderDetails(order_id, time_slot_id);
			}
		});
	}
	// Price Change edit_price_pop added here 
	dialogRefEditPrice: MatDialogRef <EditPriceComponent > | null;
	edit_price_pop(order_id: any, product_id: any, time_slot_id:any) {
		this.dialogRefEditPrice = this.dialog.open(EditPriceComponent, {
			data: {"trent_picklist_id":this.formModel.picklist_id, "order_id":order_id, "product_id":product_id},
			disableClose: false
		});
		let that = this;
		this.dialogRefEditPrice.afterClosed().subscribe(result => {
			if(result && result.status==1) {
				let selling_price = result.api_status.product_price;
				let uom_name = result.api_status.uom_name;
				that.formModel.orderData.forEach(function(item:any, index:number) {
					if(item.selected_order.order_data.order_id == order_id && item.time_slot_id == time_slot_id) {
						item.selected_order.order_data.shipment_order_product.forEach(function(inner_item:any, inner_index:number) {
							let quantity = inner_item.quantity;
							if(inner_item.product == product_id) {
								inner_item.order_product_details.selling_price = selling_price;
								inner_item.order_product_details.uom_name = uom_name;
							}
						});
					}
				});
				// console.log(selling_price)
				// that.getGrnOrderDetails(order_id, time_slot_id);
			}
		});
	}
	// substitude product add_grn_substitude_product added here 
	dialogRefAddSubstituteProduct: MatDialogRef <AddSubstituteProductComponent > | null;
	add_grn_substitude_product(order_id: any, product_id: any, time_slot_id:any, shortage:any) {
		this.dialogRefAddSubstituteProduct = this.dialog.open(AddSubstituteProductComponent, {
			data: {"trent_picklist_id":this.formModel.picklist_id, "order_id":order_id, "product_id":product_id,"shortage":shortage},
			disableClose: false
		});
		let that = this;
		this.dialogRefAddSubstituteProduct.afterClosed().subscribe(result => {
			if(result && result.status==1) {
				this.grn_save_as_draft_sustitute(order_id,time_slot_id);
			}
		});
	}
}

@Component({
	templateUrl: './templates/edit_grn.html',
	providers: [ShipmentService, Global],
})
export class EditGRNComponent implements OnInit {
	public response: any;
	public errorMsg: string;
	public successMsg: string;
	public formModel: any = {};
	private sub: any;
	public tabIndex: number;
	public parentId: number = 0;
	public userId: any;
	public trent_picklist_id:any;
	public order_id: number;
	public product_id: number;
	constructor( 
		private _shipmentService: ShipmentService,
		public _globalService: GlobalService,
		private _router: Router,
		private _route: ActivatedRoute,
		private _cookieService: CookieService,
		public dialogRef: MatDialogRef<EditGRNComponent>,
		public dialog: MatDialog,
		public dialogsService: DialogsService,
		@Inject(DOCUMENT) private document: any,
		@Optional()@ Inject(MAT_DIALOG_DATA) public data: any
	) {
		
	}

	ngOnInit() {
		alert();
		this.tabIndex = +this._globalService.getCookie('active_tabs');
		this.parentId = this._globalService.getParentTab(this.tabIndex);
		this.trent_picklist_id = this.data.trent_picklist_id;
		this.order_id  = this.data.order_id;
		this.product_id  = this.data.product_id;
		this.getEditGRN(this.order_id,this.product_id);
	}

	getEditGRN(order_id, product_id) {
		let data: any = {};
		data.trent_picklist_id = this.trent_picklist_id;
		data.order_id = order_id;
		data.product_id = product_id;
		data.website_id = this._globalService.getWebsiteId();
		this._shipmentService.getGrnProductInfo(data).subscribe(data => {
			this.response = data;
			// console.log(this.response);
			if (this.response.status > 0) {
				this.formModel = this.response.api_status;
				this.formModel.sku = this.formModel.order_product_details.product.sku;
				this.formModel.name = this.formModel.order_product_details.product.name;
				this.formModel.quantity = this.formModel.quantity;
				this.formModel.old_grn_quantity = this.formModel.grn_quantity;
				if(!this.formModel.shortage) {
					this.formModel.shortage = 0;
				}
				if(!this.formModel.grn_quantity) {
					this.formModel.grn_quantity = 0;
				}
				// console.log(this.formModel);
			} else {
				this.formModel = [];
			}
		}, err => {
			this._globalService.showToast('Something went wrong. Please try again.');
		}, function() {
			
		});
	}

	saveEditGRN() {
		let data: any = {};
		data.website_id = this._globalService.getWebsiteId();
		data.userId = this._globalService.getUserId();
		data.trent_picklist_id = this.trent_picklist_id;
		data.order_id = this.order_id;
		data.product_id = this.product_id;
		if(!this.formModel.shortage) {
			this.formModel.shortage = 0;
		}
		if(!this.formModel.grn_quantity) {
			this.formModel.grn_quantity = 0;
		}
		if(!this.formModel.old_grn_quantity) {
			this.formModel.old_grn_quantity = 0;
		}
		data.old_grn_quantity = this.formModel.old_grn_quantity;
		data.grn_quantity = this.formModel.grn_quantity;
		data.shortage = this.formModel.shortage;

		if(this.formModel.quantity != (data.grn_quantity+data.shortage)) {
			this._globalService.showToast('Grn is not completed for this product.'); //Picked Qty
			return false;
		}
		this._shipmentService.saveEditGRN(data).subscribe(
			data => {
				if (data.status == 1) {
					this._globalService.showToast(data.message);
					this.dialogRef.close(data);
				} else {
					this._globalService.showToast(data.message);
				}
			},
			err => {
				this._globalService.showToast(data.message);
			},
			function() {}
		);
	}

	// new grn moduel from chakradhar...
	validateQuantity(field_type) {
		//console.log(order_id);
		//console.log(shipemnt_order_product_id);
		let quantity = this.formModel.quantity;
		let remaining_quantity = this.formModel.quantity;
		if(!this.formModel.shortage) {
			this.formModel.shortage = 0;
		}
		if(!this.formModel.grn_quantity) {
			this.formModel.grn_quantity = 0;
		}
		let grn_quantity = this.formModel.grn_quantity;
		let shortage = this.formModel.shortage;
		
		if(field_type == 'GRN') {
			remaining_quantity = remaining_quantity-shortage;
		} else {
			remaining_quantity = remaining_quantity-grn_quantity;
		}

		let total_quantity = grn_quantity + shortage;
		if(total_quantity > quantity) {
			this._globalService.showToast('Entered value could not be greater Item Order.'); //Picked Qty
			if(field_type == 'GRN') {
				this.formModel.grn_quantity = remaining_quantity;
			} else {
				this.formModel.shortage = remaining_quantity;
			}
			return false;
		} else {
			if(field_type == 'GRN') {
				this.formModel.grn_quantity = grn_quantity;
			} else {
				this.formModel.shortage = shortage;
			}
			return false;
		}
	}
}

@Component({
	templateUrl: './templates/edit_price.html',
	providers: [ShipmentService, Global],
})
export class EditPriceComponent implements OnInit {
	public response: any;
	public errorMsg: string;
	public successMsg: string;
	public formModel: any = {};
	private sub: any;
	public tabIndex: number;
	public parentId: number = 0;
	public userId: any;
	public trent_picklist_id:any
	public order_id: number;
	public product_id: number;
	constructor( 
		private _shipmentService: ShipmentService,
		public _globalService: GlobalService,
		private _router: Router,
		private _route: ActivatedRoute,
		private _cookieService: CookieService,
		public dialogRef: MatDialogRef<EditPriceComponent>,
		public dialog: MatDialog,
		public dialogsService: DialogsService,
		@Inject(DOCUMENT) private document: any,
		@Optional()@ Inject(MAT_DIALOG_DATA) public data: any
	) {
	}
	ngOnInit() {
		this.tabIndex = +this._globalService.getCookie('active_tabs');
		this.parentId = this._globalService.getParentTab(this.tabIndex);
		this.trent_picklist_id = this.data.trent_picklist_id;
		this.order_id  = this.data.order_id;
		this.product_id  = this.data.product_id;
		this.getEditPrice(this.order_id, this.product_id);
	}

	getEditPrice(order_id, product_id) {
		let data: any = {};
		data.trent_picklist_id = this.trent_picklist_id;
		data.order_id = order_id;
		data.product_id = product_id;
		data.website_id = this._globalService.getWebsiteId();
		//console.log(data);
		this._shipmentService.getGrnProductInfo(data).subscribe(data => {
			this.response = data;
			// console.log(this.response);
			if (this.response.status > 0) {
				this.formModel = this.response.api_status;
				this.formModel.sku = this.formModel.order_product_details.product.sku;
				this.formModel.name = this.formModel.order_product_details.product.name;
				this.formModel.old_product_price = this.formModel.order_product_details.product_price+this.formModel.order_product_details.product_tax_price+this.formModel.order_product_details.product_discount_price;
				this.formModel.product_price = this.formModel.old_product_price
				this.formModel.product_weight = this.formModel.order_product_details.product.weight;
				if(this.formModel.order_product_details.weight && this.formModel.order_product_details.weight > 0) {
					this.formModel.weight = this.formModel.order_product_details.weight;
				} else if(this.formModel.order_product_details.product.weight) {
					this.formModel.weight = this.formModel.order_product_details.product.weight;
				}
				this.formModel.old_weight = this.formModel.weight;
				// console.log(this.formModel);
			} else {
				this.formModel = [];
			}
		}, err => {
			this._globalService.showToast('Something went wrong. Please try again.');
		}, function() {});
	}

	updatePrice() {
		if(this.formModel.product_weight > 0 && this.formModel.weight > 0 && this.formModel.old_product_price > 0) {
			let product_price = (this.formModel.old_product_price/this.formModel.old_weight)*this.formModel.weight;
			this.formModel.product_price = product_price.toFixed(2);
		}
	}

	saveEditPrice() {
		let data: any = {};
		data.website_id = this._globalService.getWebsiteId();
		data.userId = this._globalService.getUserId();
		var userData = this._cookieService.getObject('userData');
		data.employee_name = userData['first_name']+ ' '+ userData['last_name']
		data.trent_picklist_id = this.trent_picklist_id;
		data.order_id = this.order_id;
		data.product_id = this.product_id;
		data.sku = this.formModel.sku;
		data.weight = this.formModel.weight;
		if(!this.formModel.old_product_price) {
			this.formModel.old_product_price = 0;
		}
		if(!this.formModel.product_price) {
			this.formModel.product_price = 0;
		}
		if(this.formModel.old_product_price == this.formModel.product_price) {
			this._globalService.showToast('Please change price.');
			return false;
		}
		data.old_product_price = this.formModel.old_product_price;
		data.product_price = this.formModel.product_price;
		data.notes = this.formModel.notes!=undefined ? this.formModel.notes : '';
		// console.log(data);
		this._shipmentService.saveEditPrice(data).subscribe(
			resdata => {
				if (resdata.status == 1) {
					this._globalService.showToast(resdata.message);
					this.dialogRef.close(resdata);
				} else {
					this._globalService.showToast(resdata.message);
				}
			},
			err => {
				this._globalService.showToast(data.message);
			},
			function() {}
		);
	}
}

@Component({
	templateUrl: './templates/add_grn_substitude_product.html',
	providers: [ShipmentService, Global,OrderService],
})
export class AddSubstituteProductComponent implements OnInit {
	public response: any;
	public errorMsg: string;
	public successMsg: string;
	public formModel: any = {};
	private sub: any;
	public tabIndex: number;
	public parentId: number = 0;
	public userId: any;
	public trent_picklist_id:any
	public order_id: number;
	public product_id: number;
	public shortage: number;
	public product_list:any = [];
	orderProduct:any = []
	constructor( 
		private _shipmentService: ShipmentService,
		public _globalService: GlobalService,
		private _orderService: OrderService,
		private _router: Router,
		private _route: ActivatedRoute,
		private _cookieService: CookieService,
		public dialogRef: MatDialogRef<AddSubstituteProductComponent>,
		public dialog: MatDialog,
		public dialogsService: DialogsService,
		@Inject(DOCUMENT) private document: any,
		@Optional()@ Inject(MAT_DIALOG_DATA) public data: any
	) {
	}
	ngOnInit() {
		console.log(this.data)
		this.tabIndex = +this._globalService.getCookie('active_tabs');
		this.parentId = this._globalService.getParentTab(this.tabIndex);
		this.trent_picklist_id = this.data.trent_picklist_id;
		this.order_id  = this.data.order_id;
		this.product_id  = this.data.product_id;
		this.shortage  = this.data.shortage;
		this.getEditSubstituteProduct(this.order_id, this.product_id);
	}

	getEditSubstituteProduct(order_id, product_id) {
		let data: any = {};
		data.trent_picklist_id = this.trent_picklist_id;
		data.order_id = order_id;
		data.product_id = product_id;
		data.website_id = this._globalService.getWebsiteId();
		//console.log(data);
		this._shipmentService.getGrnProductInfo(data).subscribe(data => {
			this.response = data;
			// console.log(this.response);
			if (this.response.status > 0) {
				this.formModel = this.response.api_status;
				this.formModel.sku = this.formModel.order_product_details.product.sku;
				this.formModel.name = this.formModel.order_product_details.product.name;
				this.formModel.warehouse_id = this.formModel.order_product_details.warehouse_id;
				this.formModel.old_product_price = this.formModel.order_product_details.product_price+this.formModel.order_product_details.product_tax_price+this.formModel.order_product_details.product_discount_price;
				this.formModel.shortage = this.shortage;
				this.formModel.sub_product_list = this.response.substitute_product;
				this.orderProduct = this.response.order_products;
				this.loadsubstituteProduct(this.formModel.warehouse_id);
			} else {
				this.formModel = [];
			}
		}, err => {
			this._globalService.showToast('Something went wrong. Please try again.');
		}, function() {});
	}


	loadsubstituteProduct(warehouse_id) {
		let filterValue = '';
		let elasticData = '{"query":{"bool":{"must":[{"query_string":{"query":"'+filterValue+'"}},{"match":{"visibility_id":{"query":"Catalog Search","operator":"and"}}}],"filter":[{"nested":{"path":"inventory","query":{"bool":{"must":[{"term":{"inventory.id":'+warehouse_id+'}},{"range":{"inventory.stock":{"gt":0}}}]}},"score_mode":"avg"}},{"nested":{"path":"channel_currency_product_price","query":{"bool":{"must":[{"range":{"channel_currency_product_price.new_default_price":{"gt":0}}},{"term":{"channel_currency_product_price.warehouse_id":'+this.formModel.warehouse_id+'}}]}}}},{"nested":{"path":"product_images","query":{"bool":{"must":[{"term":{"product_images.is_cover":1}}]}}}}]}},"from":0,"size":10000}';
		this.product_list = [];
		this._orderService.getProductsES(elasticData, this._globalService.getWebsiteId()).subscribe(
			listData => {
				let tmpResult = [];
				listData.hits.hits.forEach(function (rows: any) {
					tmpResult.push(rows._source);
				});
				let that = this;
				//console.log(this.orderProduct);
				if (tmpResult.length > 0) {					
					tmpResult.forEach(tmpElement => {
						tmpElement.search_name = tmpElement.sku + ' | ' + tmpElement.name;						
					});
					this.product_list = tmpResult;
				} 
				this.product_list.forEach(element => {
					if(that.orderProduct.indexOf(element.id) > 0)  {
					   let index = that.orderProduct.indexOf(element.id);
					   this.product_list.splice(index, 1);
					}
				});
			},
			err => {
				this._globalService.showToast('Something went wrong. Please try again.');
			},
			function () {
				//completed callback
			}
		);
	}

	searchPRoduct(event) {
		console.log(event);
		let filterValue = event.term;
		let warehouse_id = this.formModel.warehouse_id;
		let that = this;
		let elasticData = '{"query":{"bool":{"must":[{"query_string":{"query":"'+filterValue+'"}},{"match":{"visibility_id":{"query":"Catalog Search","operator":"and"}}}],"filter":[{"nested":{"path":"inventory","query":{"bool":{"must":[{"term":{"inventory.id":'+warehouse_id+'}},{"range":{"inventory.stock":{"gt":0}}}]}},"score_mode":"avg"}},{"nested":{"path":"channel_currency_product_price","query":{"bool":{"must":[{"range":{"channel_currency_product_price.new_default_price":{"gt":0}}},{"term":{"channel_currency_product_price.warehouse_id":'+this.formModel.warehouse_id+'}}]}}}},{"nested":{"path":"product_images","query":{"bool":{"must":[{"term":{"product_images.is_cover":1}}]}}}}]}},"from":0,"size":1000}';
		this._orderService.getProductsES(elasticData, this._globalService.getWebsiteId()).subscribe(
			listData => {
				let tmpResult = [];
				listData.hits.hits.forEach(function (rows: any) {
					tmpResult.push(rows._source);
				});
				if (tmpResult.length > 0) {		
					tmpResult.forEach(tmpElement => {
						tmpElement.search_name = tmpElement.sku + ' | ' + tmpElement.name;
					});
					this.product_list = tmpResult;
					//console.log(this.product_list);
				} 

				this.product_list.forEach(element => {
					if(that.orderProduct.indexOf(element.id) > 0)  {
					   let index = that.orderProduct.indexOf(element.id);
					   this.product_list.splice(index, 1);
					}
				});
			},
			err => {
				this._globalService.showToast('Something went wrong. Please try again.');
			},
			function () {
				//completed callback
			}
		);
	}


	updateSubstitue(event) {
		console.log(event);
		if(event!=undefined) {
			this.formModel.sub_product_id = event.id
		} else {
			this.formModel.sub_product_id = null;
		}
		
	}
	saveSubstituteProduct() {
		if(this.formModel.sub_product_id > 0) {
			this.dialogsService.confirm('Warning', 'Are you sure to sustitute this product?').subscribe(res => {
			if (res) {
				let data: any = {};
				data.website_id = this._globalService.getWebsiteId();
				data.userId = this._globalService.getUserId();
				var userData = this._cookieService.getObject('userData');
				data.employee_name = userData['first_name']+ ' '+ userData['last_name']
				data.trent_picklist_id = this.trent_picklist_id;
				data.shipment_id = this.formModel.shipment;
				data.order_id = this.order_id;
				data.shipment_order_id = this.formModel.shipment_order
				data.product_id = this.product_id;
				data.sku = this.formModel.sku;
				data.sub_product_id = this.formModel.sub_product_id;
				data.shortage = this.formModel.shortage;
				// console.log(data);
				this._shipmentService.saveSubstituteProduct(data).subscribe(
					data => {
						if (data.status == 1) {
							this._globalService.showToast(data.message);
							this.dialogRef.close(data);
						} else {
							this._globalService.showToast(data.message);
						}
					},
					err => {
						// this._globalService.showToast(data.message);
					},
					function() {}
				);
			}});			
		} else {
			this._globalService.showToast('Select substitute product ');
		}
		
	}
}

@Component({
	templateUrl: './templates/manage_crates.html',
	providers: [ShipmentService, Global],
})
export class ManageCrateComponent implements OnInit {
	public response: any;
	public errorMsg: string;
	public successMsg: string;
	public formModel: any = {};
	private sub: any;
	public tabIndex: number;
	public parentId: number = 0;
	public bulk_crates_ids: any = [];
	public rel_data: any = [];
	public pagination: any = {};
	public pageIndex: number = 0;
	public pageList: number = 0;
	public sortBy: any = '';
	public sortOrder: any = '';
	public sortClass: any = '';
	public sortRev: boolean = false;
	public selectedAll: any = false;
	public result_list_crates: any = [];
	
	public userId: any;
	public search_text: string='';
	
	public individualRow: any = {};
	public selected_ids: any = [];
	constructor( 
		private _shipmentService: ShipmentService,
		public _globalService: GlobalService,
		private _router: Router,
		private _route: ActivatedRoute,
		private _cookieService: CookieService,
		public dialog: MatDialog,
		public dialogRef: MatDialogRef<ManageCrateComponent>,
		public dialogsService: DialogsService,
		@Inject(DOCUMENT) private document: any,
		@Optional()@ Inject(MAT_DIALOG_DATA) public data: any
	) {
	}
	ngOnInit() {
		this.tabIndex = +this._globalService.getCookie('active_tabs');
		this.parentId = this._globalService.getParentTab(this.tabIndex);
		let trent_picklist_id = this.data.trent_picklist_id;
		let search = '';
		let order_id = this.data.order_id;
		this.getallCrates(trent_picklist_id, order_id, this.search_text);
	}

	getallCrates(trent_picklist_id: any, order_id: any, search: any) {
		// search = search.trimLeft();
		if(search == '') {
			this.search_text = '';
		} else {
			this.search_text = search;
		}

		let elements: NodeListOf < Element > = this.document.getElementsByClassName('manage-crates');
		elements[0].classList.remove('show-pop');
		this.selectedAll = false;
		this.bulk_crates_ids = [];
		this.individualRow = {};
		
		let data: any = {};
		data.trent_picklist_id = trent_picklist_id;
		data.order_id = order_id;
		data.search = this.search_text.trim();
		//console.log(data);

		this._shipmentService.getAllCrates(data).subscribe(data => {
			this.response = data;
			//console.log(this.response);
			if (this.response.status > 0) {
				this.result_list_crates = this.response.crate_list;
			} else {
				this.result_list_crates = [];
			}
		}, err => {
			this._globalService.showToast('Something went wrong. Please try again.');
		}, function() {});
	}

	////////////////////////////Check/Uncheck//////////////
	toggleCheckAll(event: any) {
		let elements: NodeListOf < Element > = this.document.getElementsByClassName('manage-crates');
		let that = this;
		that.bulk_crates_ids = [];
		this.selectedAll = event.checked;
		this.result_list_crates.forEach(function(item: any) {
			item.selected = event.checked;
			if (item.selected) {
				that.bulk_crates_ids.push(item.id);
				elements[0].classList.add('show-pop');
			} else {
				elements[0].classList.remove('show-pop');
			}
		});
	}
	toggleCheckCrates(id: any, event: any) {
		let elements: NodeListOf < Element > = this.document.getElementsByClassName('manage-crates');
		let that = this;
		this.result_list_crates.forEach(function(item: any) {
			if (item.id == id) {
				item.selected = event.checked;
				if (item.selected) {
					that.bulk_crates_ids.push(item.id);
					elements[0].classList.add('show-pop');
				} else {
					var index = that.bulk_crates_ids.indexOf(item.id);
					that.bulk_crates_ids.splice(index, 1);
					elements[0].classList.remove('show-pop');
				}
			}
			if (that.bulk_crates_ids.length == 1) {
				that.bulk_crates_ids.forEach(function(item_id: any) {
					if (item_id == item.id) {
						that.individualRow = item;
					}
				});
			}
			that.selectedAll = false;
		});
	}

	delete_crates(trent_picklist_id: any, order_id: any, action_id: number) {
		if (action_id) {
			let that = this;
			that.bulk_crates_ids = [];
			that.bulk_crates_ids.push(action_id);
		}
		let data: any = {};
		data.action_id = this.bulk_crates_ids;
		data.trent_picklist_id = trent_picklist_id;
		data.order_id = order_id;
		data.userId = this._globalService.getUserId();
		var msg = 'Do you really want to delete selected crates?';
		if (this.bulk_crates_ids.length > 0) {
			this.dialogsService.confirm('Warning', msg).subscribe(res => {
				if (res) {
					this._shipmentService.deleteCrates(data).subscribe(
						data => {
							if (data.status == 1) {
								this._globalService.showToast("Crate deleted successfully");
								this.getallCrates(trent_picklist_id, order_id, this.search_text);
							} else {
								this._globalService.showToast(data.message);
							}
						},
						err => {
							this._globalService.showToast(data.message);
						},
						function() {

						}
					);
				}
			});
		} else {
			this.dialogsService.alert('Error', 'Select Atleast One Record!').subscribe(res => {});
		}
	}
}

@Component({
	templateUrl: './templates/grn_order_products.html',
	providers: [ShipmentService, Global],
})
export class GrnOrderProductComponent implements OnInit {
	public response: any;
	public errorMsg: string;
	public successMsg: string;
	public formModel: any = {};
	private sub: any;
	public tabIndex: number;
	public parentId: number = 0;
	public bulk_crates_ids: any = [];
	public rel_data: any = [];
	public pagination: any = {};
	public pageIndex: number = 0;
	public pageList: number = 0;
	public sortBy: any = '';
	public sortOrder: any = '';
	public sortClass: any = '';
	public sortRev: boolean = false;
	public selectedAll: any = false;
	public result_list: any = [];
	
	public userId: any;
	public search_text: string='';
	
	public individualRow: any = {};
	public selected_ids: any = [];
	constructor( 
		private _shipmentService: ShipmentService,
		public _globalService: GlobalService,
		private _router: Router,
		private _route: ActivatedRoute,
		private _cookieService: CookieService,
		public dialog: MatDialog,
		public dialogRef: MatDialogRef<GrnOrderProductComponent>,
		public dialogsService: DialogsService,
		@Inject(DOCUMENT) private document: any,
		@Optional()@ Inject(MAT_DIALOG_DATA) public data: any
	) {
	}
	ngOnInit() {
		this.tabIndex = +this._globalService.getCookie('active_tabs');
		this.parentId = this._globalService.getParentTab(this.tabIndex);
		this.formModel.trent_picklist_id = this.data.trent_picklist_id;
		let search = '';
		this.formModel.order_id = this.data.order_id;
		this.formModel.time_slot_id = this.data.time_slot_id;
		this.getallOrderProducts(this.formModel.trent_picklist_id, this.formModel.order_id, this.search_text);
	}

	getallOrderProducts(trent_picklist_id: any, order_id: any, search: any) {
		// search = search.trimLeft();
		if(search == '') {
			this.search_text = '';
		} else {
			this.search_text = search;
		}
		this.selectedAll = false;
		this.bulk_crates_ids = [];
		this.individualRow = {};
		let data: any = {};
		data.trent_picklist_id = trent_picklist_id;
		data.order_id = order_id;
		data.search = this.search_text.trim();
		//console.log(data);
		this._shipmentService.searchPickedProducts(data).subscribe(data => {
			this.response = data;
			//console.log(this.response);
			if (this.response.status > 0) {
				this.result_list = this.response.api_status;
			} else {
				this.result_list = [];
			}
		}, err => {
			this._globalService.showToast('Something went wrong. Please try again.');
		}, function() {});
	}

	////////////////////////////Check/Uncheck//////////////
	toggleCheckAll(event: any) {
		let that = this;
		that.bulk_crates_ids = [];
		this.selectedAll = event.checked;
		this.result_list.forEach(function(item: any) {
			item.selected = event.checked;
			if (item.selected) {
				that.bulk_crates_ids.push(item.id);
			} else {
			}
		   // console.log(item);
		});
	}
	toggleCheckCrates(id: any, event: any) {
		let that = this;
		this.result_list.forEach(function(item: any) {
			if (item.id == id) {
				item.selected = event.checked;
				if (item.selected) {
					that.bulk_crates_ids.push(item.id);
				} else {
					var index = that.bulk_crates_ids.indexOf(item.id);
					that.bulk_crates_ids.splice(index, 1);
				}
			}
			if (that.bulk_crates_ids.length == 1) {
				that.bulk_crates_ids.forEach(function(item_id: any) {
					if (item_id == item.id) {
						that.individualRow = item;
					}
				});
			}
			that.selectedAll = false;
		});
	}

	selectOrderProducts() {
		let data: any = {};
		data.trent_picklist_id = this.formModel.trent_picklist_id;
		data.order_id = this.formModel.order_id;
		data.time_slot_id = this.formModel.time_slot_id;
		if (this.bulk_crates_ids.length > 0) {
			data.action_id = this.bulk_crates_ids;
			data.status = 1;
			this.dialogRef.close(data);
		} else {
			this.dialogsService.alert('Error', 'Select Atleast One Record!').subscribe(res => {});
		}
		// console.log(data);
	}

	closeDialog() {
		this.dialogRef.close();
	}
}

// Invoice start here by cds on 17nth May 2019 - Picklist
@Component({
	templateUrl: './templates/invoice.html',
	providers: [ShipmentService],
	animations: [AddEditTransition],
	host: {
		'[@AddEditTransition]': ''
	},
})
export class ShipmentInvoiceComponent implements OnInit {
	public response: any;
	public errorMsg: string='';
	public successMsg: string='';
	public formModel: any = {};
	public bulk_ids: any = [];
	private sub: any;
	public tabIndex: number;
	public parentId: number = 0;
	public add_edit: any = '';
	public selectedAll: any = false;
	public individualRow: any = {};
	constructor(
		private _shipmentService: ShipmentService,
		public _globalService: GlobalService,
		private _router: Router,
		private _route: ActivatedRoute,
		private _cookieService: CookieService,
		public dialog: MatDialog,
	) {}
	ngOnInit() {
		this.tabIndex = +this._globalService.getCookie('active_tabs');
		this.parentId = this._globalService.getParentTab(this.tabIndex);
		let website_id = this._globalService.getWebsiteId();
		this.add_edit = 'add';
		this.sub = this._route.params.subscribe(params => {
			this.formModel.shipment_id = +params['id']; // (+) converts string 'id' to a number
		});
		this.formModel.printsection = '';
		this.formModel.invoice_email = 'n';
		let data: any = {};
		data.picked_by_id = this._globalService.getUserId();
		data.website_id = this._globalService.getWebsiteId();
		data.company_id = this._globalService.getCompanyId();
		data.shipment_id = this.formModel.shipment_id;
		data.shipmentType = "OrderWise"; // this is not used in web service
		data.selectedIds = "1"; //// this is not used in web service
		data.invoice_create_request = 'n';
		data.userId = this._globalService.getUserId();
		//console.log(data)
		this._shipmentService.loadInvoices(data).subscribe(
			data => {
				if (data.status == 1) {
					this.formModel.InvoiceDetails = data.InvoiceDetails;
					this.formModel.picklist_id = data.picklist_id;
					this.formModel.is_invoice_created = data.is_invoice_created;
				}
			},
			err => {
				this._globalService.showToast(data.message);
			},
			function() {
				
			});
	}
	toggleCheckAll(event: any) {
		//let elements: NodeListOf < Element > = this.document.getElementsByClassName('action-box');
		let that = this;
		that.bulk_ids = [];
		this.selectedAll = event.checked;
		this.formModel.InvoiceDetails.forEach(function(item: any) {
			item.selected = event.checked;
			if (item.selected) {
				that.bulk_ids.push(item.order.id);
				//elements[0].classList.add('show');
			} else {
				//elements[0].classList.remove('show');
			}
		});
	}
	toggleCheck(id: any, event: any) {
		//let elements: NodeListOf < Element > = this.document.getElementsByClassName('action-box');
		let that = this;
		this.formModel.InvoiceDetails.forEach(function(item: any) {
			if (item.order.id == id) {
				item.selected = event.checked;
				if (item.selected) {
					that.bulk_ids.push(item.order.id);
					//that.action_order_status_ids.push(item.order_status);
					//elements[0].classList.add('show');
				} else {
					let index = that.bulk_ids.indexOf(item.order.id);
					that.bulk_ids.splice(index, 1);
					if (that.bulk_ids.length == 0) {
						//elements[0].classList.remove('show');
					}
				}
			}
			if (that.bulk_ids.length == 1) {
				that.bulk_ids.forEach(function(item_id: any) {
					if (item_id == item.order.id) {
						that.individualRow = item;
					}
				});
			}
			that.selectedAll = false;
		});
	}

	createInvoice() {
		if (this.bulk_ids.length > 0) {
			let selected_ids = this.bulk_ids.join(",");
			let data: any = {};
			data.picked_by_id = this._globalService.getUserId();
			data.website_id = this._globalService.getWebsiteId();
			data.company_id = this._globalService.getCompanyId();
			data.trent_picklist_id = this.formModel.picklist_id;
			data.shipment_id = this.formModel.shipment_id;
			data.shipmentType = "OrderWise"; // this is not used in web service
			data.selectedIds = selected_ids; // this is not used in web service
			data.selectedProdIds = '';
			data.is_invoice_created = this.formModel.is_invoice_created;
			data.userId = this._globalService.getUserId();
			data.invoice_email = this.formModel.invoice_email;
			data.invoice_create_request = 'y';
			//console.log(data)
			this._globalService.showLoaderSpinner(true);
			this._shipmentService.loadInvoices(data).subscribe(
				data => {
					if (data.status == 1) {
						this.formModel.InvoiceDetails = data.InvoiceDetails;
						if(data.payment_response.status == 'success'){
							this._globalService.showToast("Invoice created successfully");
						}else{
							this._globalService.showToast(data.payment_response.msg);
						}
						this.selectedAll = false;
						this.bulk_ids = []; // removed all order ids
					} else {
						this._globalService.showToast(data.message);
					}
					this._globalService.showLoaderSpinner(false);
				},
				err => {
					// this._globalService.showToast(data.message);
				},
				function() {
					// this._globalService.showLoaderSpinner(false);
				}
			);
		} else {
			this.errorMsg = "Please select at least one order.";
		}
	}

	printInvoice() {
		if (this.bulk_ids.length > 0) {
			let data: any = {};
			let selected_ids = this.bulk_ids.join(",");
			data.website_id = this._globalService.getWebsiteId();
			data.company_id = this._globalService.getCompanyId();
			data.trent_picklist_id = this.formModel.picklist_id;
			data.selectedIds = selected_ids; // this is not used in web service
			this._shipmentService.printInvoice(data).subscribe(
				data => {
					if (data.status == 1) {
						this.formModel.printsection = data.invoice_content;
						setTimeout(this.printInvoiceContent, 1000)
					} else {
						this._globalService.showToast(data.message);
					}
				},
				err => {
					this._globalService.showToast("Someting went wrong");
				}, () => {
				}
			);
		} else {
			this._globalService.showToast("Please select at least one order.");
		}
	}

	printInvoiceContent() {
		let popupWinindow
		let innerContents = document.getElementById("printsection").innerHTML;
		popupWinindow = window.open('', '_blank', 'menubar=no,toolbar=no,location=no,status=no,titlebar=no');
		popupWinindow.document.open();
		popupWinindow.document.write('<html><head>');
		popupWinindow.document.write('<link rel="stylesheet" href="' + window.location.protocol + '//' + window.location.hostname + ':3000/' + 'assets/css/print.css">');
		popupWinindow.document.write('</head><body onload="window.print()">' + innerContents + '</html>');
		popupWinindow.document.close();
	}

	invoiceContinue(form: any) {
		this._router.navigate(['/shipment/delivery_planner/' + this.formModel.shipment_id]);
	}

	sendInvoiceEmail(event) {
		if (event.checked) {
			this.formModel.invoice_email = 'y';
		} else {
			this.formModel.invoice_email = 'n';
		}
	}
}

// Invoice start here by cds on 17nth May 2019 - Picklist
@Component({
	templateUrl: './templates/delivery_planner.html',
	providers: [ShipmentService],
	animations: [AddEditTransition],
	host: {
		'[@AddEditTransition]': ''
	},
})
export class DeliveryPlannerComponent implements OnInit {
	public response: any;
	public formModel: any = {};
	public bulk_ids: any = [];
	private sub: any;
	public tabIndex: number;
	public parentId: number = 0;
	public add_edit: any = '';
	public selectedAll: any = false;
	public individualRow: any = {};
	constructor(
		private _shipmentService: ShipmentService,
		public _globalService: GlobalService,
		private _router: Router,
		private _route: ActivatedRoute,
		private _cookieService: CookieService,
		public dialogsService: DialogsService,
		public dialog: MatDialog,
	) {}
	ngOnInit() {
		this.tabIndex = +this._globalService.getCookie('active_tabs');
		this.parentId = this._globalService.getParentTab(this.tabIndex);
		let website_id = this._globalService.getWebsiteId();
		this.add_edit = 'add';
		this.sub = this._route.params.subscribe(params => {
			this.formModel.shipment_id = +params['id']; // (+) converts string 'id' to a number
		});
		let data: any = {};
		data.website_id = this._globalService.getWebsiteId();
		data.shipment_id = this.formModel.shipment_id;
		//console.log(data)
		this._shipmentService.loadDeliveryPlanner(data).subscribe(
			data => {
				if (data.status == 1) {
					this.formModel.orderData = data.api_status;
					if(this.formModel.orderData[0].shipping_status != 'Shipment Processing') {
						this.add_edit = 'edit';
					}
				} else {
					this._globalService.showToast(data.message);
				}
			},
			err => {
				this._globalService.showToast(data.message);
			},
			function() {}
	   );
	}
	toggleCheckAll(event: any) {
		//let elements: NodeListOf < Element > = this.document.getElementsByClassName('action-box');
		let that = this;
		that.bulk_ids = [];
		this.selectedAll = event.checked;
		this.formModel.orderData.forEach(function(item: any) {
			item.selected = event.checked;
			if (item.selected) {
				that.bulk_ids.push(item.order.id);
				//elements[0].classList.add('show');
			} else {
				//elements[0].classList.remove('show');
			}
		});
	}
	toggleCheck(id: any, event: any) {
		//let elements: NodeListOf < Element > = this.document.getElementsByClassName('action-box');
		let that = this;
		this.formModel.orderData.forEach(function(item: any) {
			if (item.order.id == id) {
				item.selected = event.checked;
				if (item.selected) {
					that.bulk_ids.push(item.order.id);
					//that.action_order_status_ids.push(item.order_status);
					//elements[0].classList.add('show');
				} else {
					let index = that.bulk_ids.indexOf(item.order.id);
					that.bulk_ids.splice(index, 1);
					if (that.bulk_ids.length == 0) {
						//elements[0].classList.remove('show');
					}
				}
			}
			if (that.bulk_ids.length == 1) {
				that.bulk_ids.forEach(function(item_id: any) {
					if (item_id == item.order.id) {
						that.individualRow = item;
					}
				});
			}
			that.selectedAll = false;
		});
	}

	
	deliveryPlannerContinue(form: any) {
		let data:any = {};
		let that = this;
		let dataArr= [];
		this.formModel.orderData.forEach(function(item: any) {
			let selected_order_list: any = {};
			selected_order_list['user_id'] = that._globalService.getUserId();
			selected_order_list['website_id'] = that._globalService.getWebsiteId();
			selected_order_list['shipment_id'] = that.formModel.shipment_id;
			selected_order_list['order_id'] = item.order.id;
			selected_order_list['sort_by_distance'] = item.sort_by_distance;
			dataArr.push(selected_order_list);
		});
		data.order_data = dataArr;
		if(data) {
			this._shipmentService.saveSortBydistance(data).subscribe(
				data => {
					if (data.status == 1) {
						that._globalService.addTab('shipment','shipment/manifest/'+this.formModel.shipment_id,'Delivery Note',this.parentId)
						that._router.navigate(['/shipment/manifest/'+this.formModel.shipment_id]);
					} else {
						this._globalService.showToast(data.message);
					}
				},
				err => {
					this._globalService.showToast(data.message);
				},
				function() {}
			);
		} else {
			this._globalService.addTab('shipment','shipment/manifest/'+this.formModel.shipment_id,'Delivery Note',this.parentId)
			this._router.navigate(['/shipment/manifest/'+this.formModel.shipment_id]);
		}
		// console.log(data);
	}

	remove_from_shipment(shipment_id:any) {
		let that = this;
		if(that.bulk_ids.length > 0) {
			let selectedIds = that.bulk_ids;
			let data:any = {};
			data.shipment_id = shipment_id;
			data.website_id = this._globalService.getWebsiteId();
			data.userId = this._globalService.getUserId();
			data.selectedIds  = selectedIds.join(",");
			//console.log(data)
			this.dialogsService.confirm('Remove From Shipment', 'Do you want to remove from shipment for selected order(s).').subscribe(res => {
				if (res) {
					this._shipmentService.removeFromShipment(data).subscribe(
						data => {
							if(data.status == 1) {
								this.ngOnInit()
							} else {
								this._globalService.showToast(data.message);
							}
						} ,
						err => {
						} , // callback function
						function () {
					});
				}
			});
		} else {
			that._globalService.showToast("Please select atleast one order");
		}
	}

	dialogRefAssignVehicle: MatDialogRef <AssignVehicleComponent > | null;
	pop_assign_vehicle(order_id: any) {
		this.dialogRefAssignVehicle = this.dialog.open(AssignVehicleComponent, {
			data: {"shipment_id":this.formModel.shipment_id},
			disableClose: false
		});
		let that = this;
		this.dialogRefAssignVehicle.afterClosed().subscribe(result => {
			if(result && result.status==1) {
				// console.log(result);
				that.ngOnInit();
			}
		});
	}
}

@Component({
	templateUrl: './templates/assign_vehicle.html',
	providers: [ShipmentService, Global],
})
export class AssignVehicleComponent implements OnInit {
	public response: any;
	public errorMsg: string;
	public successMsg: string;
	public formModel: any = {};
	private sub: any;
	public tabIndex: number;
	public parentId: number = 0;
	public userId: any;
	public warehouse_id: any;
	constructor( 
		private _shipmentService: ShipmentService,
		public _globalService: GlobalService,
		private _router: Router,
		private _route: ActivatedRoute,
		private _cookieService: CookieService,
		public dialogRef: MatDialogRef<AssignVehicleComponent>,
		public dialog: MatDialog,
		public dialogsService: DialogsService,
		@Inject(DOCUMENT) private document: any,
		@Optional()@ Inject(MAT_DIALOG_DATA) public data: any
	) {
	}

	ngOnInit() {
		let userData = this._cookieService.getObject('userData');
		this.warehouse_id = userData['warehouse_id'];

		this.tabIndex = +this._globalService.getCookie('active_tabs');
		this.parentId = this._globalService.getParentTab(this.tabIndex);
		let shipment_id = this.data.shipment_id;
		this.getAssignVehicle(shipment_id);
	}

	getAssignVehicle(shipment_id: any) {
		let data: any = {};
		data.website_id = this._globalService.getWebsiteId();
		data.shipment_id = shipment_id;
		data.warehouse_id = this.warehouse_id;
		//console.log(data);
		this._shipmentService.getAssignVehicle(data).subscribe(data => {
			this.response = data;
			// console.log(this.response);
			if (this.response.status > 0) {
				this.formModel = this.response.api_status;
				this.formModel.user_id = this.formModel.driverVehicleArr.user_id;
				this.formModel.vehicle_id = this.formModel.driverVehicleArr.vehicle_id;
				this.formModel.shipment_id = shipment_id;
			} else {
				this.formModel = [];
				this.formModel.shipment_id = shipment_id;
				this.formModel.totalVechicle = 0;
			}
		}, err => {
			this._globalService.showToast('Something went wrong. Please try again.');
		}, function() {});
	}

	saveAssignVehicle() {
		//console.log(this.formModel)
		let selected_ids = '';
		let data: any = {};
		data.website_id = this._globalService.getWebsiteId();
		data.shipment_id = this.formModel.shipment_id;
		// data.driver_id = this.formModel.user_id;
		// data.vehicle_id = this.formModel.vehicle_id;
		data.totalVechicle = this.formModel.totalVechicle;
		data.delivery_date = this.formModel.delivery_date;
		data.driverVehicleArr = this.formModel.driverVehicleArr
		data.userId = this._globalService.getUserId();
		this._shipmentService.createAssignVehicle(data).subscribe(
			data => {
				if (data.status == 1) {
					this.formModel.orderDetails = data.api_status;
					this._globalService.showToast("Assign Vehicle Successfully Completed.");
					this.dialogRef.close(data);
				} else {
					this._globalService.showToast(data.message);
				}
			},
			err => {
				// this._globalService.showToast(data.message);
			},
			function() {}
		);
	}
}

@Component({
	templateUrl: './templates/manifest.html',
	providers: [ShipmentService],
	animations: [AddEditTransition],
	host: {
		'[@AddEditTransition]': ''
	},
})
export class ShipmentManifestComponent implements OnInit {
	public response: any;
	public formModel: any = {};
	public sub: any;
	public tabIndex: number;
	public parentId: number = 0;
	public add_edit: any = '';
	public bulk_ids: any = [];
	public selectedAll: any = false;
	public individualRow: any = {};
	constructor(
		private _shipmentService: ShipmentService,
		public _globalService: GlobalService,
		private _router: Router,
		private _route: ActivatedRoute,
		private _cookieService: CookieService,
		public dialog: MatDialog,
	) {

	}
	ngOnInit() {
		this.tabIndex = +this._globalService.getCookie('active_tabs');
		this.parentId = this._globalService.getParentTab(this.tabIndex);
		let website_id = this._globalService.getWebsiteId();
		this.add_edit = 'edit';
		this.sub = this._route.params.subscribe(params => {
			this.formModel.shipment_id = +params['id']; // (+) converts string 'id' to a number
		});
		let data: any = {};
		data.website_id = this._globalService.getWebsiteId();
		data.shipment_id = this.formModel.shipment_id;
		//console.log(data)
		this.formModel.manifest_details = {};
		this.formModel.orderData = [];
		this._shipmentService.loadManifest(data).subscribe(
			data => {
				if (data.status == 1) {
					this.formModel.orderData = data.api_status;
					this.formModel.manifest_details = data.manifest_details;
					this.formModel.manifest_details.zone_name = data.api_status[0].order.zone_name
				} else {
					this.formModel.orderData = [];
					this._globalService.showToast(data.message);
				}
			},
			err => {
				this._globalService.showToast(data.message);
			},
			function() {

			}
	   );
	}

	createManifest() {
		//console.log(this.bulk_ids)
		if (this.bulk_ids.length > 0) {
			let selected_ids = this.bulk_ids.join(",");
			let data: any = {};
			data.shipment_id = this.formModel.shipment_id;
			data.website_id = this._globalService.getWebsiteId();
			data.order_ids = selected_ids; // this is not used in web service
			data.comment = this.formModel.manifest_details.comment;
			data.user_id = this._globalService.getUserId();
			// console.log(data)
			this._shipmentService.createManifest(data).subscribe(
				data => {
					if (data.status == 1) {
						this.formModel.manifest_id = data.api_status;
						this._globalService.showToast("You have successfully created delivery note.");
						this.ngOnInit()
						this.selectedAll = false;
						this.bulk_ids = []; // removed all order ids
					} else {
						this._globalService.showToast(data.message);
					}
				},
				err => {
					this._globalService.showToast(data.message);
				},
				function() {

				}
			);
		} else {
			this._globalService.showToast("Please select at least one order.");
		}
	}

	toggleCheckAll(event: any) {
		let that = this;
		that.bulk_ids = [];
		this.selectedAll = event.checked;
		this.formModel.orderData.forEach(function(item: any) {
			item.selected = event.checked;
			if (item.selected) {
				that.bulk_ids.push(item.order.id);
				//elements[0].classList.add('show');
			} else {
				//elements[0].classList.remove('show');
			}
		});
	}
	toggleCheck(id: any, event: any) {
		let that = this;
		this.formModel.orderData.forEach(function(item: any) {
			if (item.order.id == id) {
				item.selected = event.checked;
				if (item.selected) {
					that.bulk_ids.push(item.order.id);
					//that.action_order_status_ids.push(item.order_status);
					//elements[0].classList.add('show');
				} else {
					let index = that.bulk_ids.indexOf(item.order.id);
					that.bulk_ids.splice(index, 1);
					if (that.bulk_ids.length == 0) {
						//elements[0].classList.remove('show');
					}
				}
			}
			if (that.bulk_ids.length == 1) {
				that.bulk_ids.forEach(function(item_id: any) {
					if (item_id == item.order.id) {
						that.individualRow = item;
					}
				});
			}
			that.selectedAll = false;
		});
	}

	printManifest() {
		if (this.bulk_ids.length > 0) {
			let data: any = {};
			let selected_ids = this.bulk_ids.join(",");
			data.shipment_id = this.formModel.shipment_id;
			data.website_id = this._globalService.getWebsiteId();
			data.order_ids = selected_ids; // this is not used in web service
			data.manifest_id = this.formModel.manifest_details.id;
			this._shipmentService.printManifest(data).subscribe(
				data => {
					if (data.status == 1) {
						this.formModel.printsection = data.email_content;
						setTimeout(this.printManifestContent, 1000)
					} else {
						this._globalService.showToast("Please create manifest for printing.");
					}
				},
				err => {
					this._globalService.showToast("Someting went wrong");
				}, () => {
				}
			);
		} else {
			this._globalService.showToast("Please select at least one order.");
		}
	}

	printManifestContent() {
		//this._globalService.printPicklist('printsection')
		let popupWinindow
		let innerContents = document.getElementById("printsection").innerHTML;
		popupWinindow = window.open('', '_blank', 'menubar=no,toolbar=no,location=no,status=no,titlebar=no');
		popupWinindow.document.open();
		popupWinindow.document.write('<html><head>');
		popupWinindow.document.write('<link rel="stylesheet" href="' + window.location.protocol + '//' + window.location.hostname + ':3000/' + 'assets/css/print.css">');
		popupWinindow.document.write('</head><body onload="window.print()">' + innerContents + '</html>');
		popupWinindow.document.close();
	}

	manifestContinue(form: any) {
		this._globalService.deleteTab(this.tabIndex, this.parentId);
		this._router.navigate(['/shipment/shipment']);
		this._globalService.addTab(193, '/shipment/shipment', 'Shipment', this.parentId); // 193 id for shipment menu
	}
}