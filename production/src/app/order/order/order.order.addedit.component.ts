import { Component, OnInit, Inject, Optional, Input, OnChanges, SimpleChanges, DoCheck } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA, MatDialog, MatAutocompleteModule } from '@angular/material';
import { Router, ActivatedRoute, NavigationEnd } from '@angular/router';
import { Global } from '../../global/service/global';
import { DOCUMENT } from '@angular/platform-browser';
import { DialogsService } from '../../global/dialog/confirm-dialog.service';
import { OrderService }  from './order.order.service';
import { GlobalService } from '../../global/service/app.global.service';
import { PaginationInstance } from 'ngx-pagination';
//import { MatColorPickerModule } from 'mat-color-picker';
import { CookieService } from 'ngx-cookie';
import { AddEditTransition, AddEditStepFlipTransition } from '../.././addedit.animation';
import { COMMA, ENTER } from '@angular/cdk/keycodes';
import { MatChipInputEvent } from '@angular/material';
import { TimeFormatPipe } from '../../global/pipes/convertFrom24To12Format.pipe';
import { AlertDialog } from '../../global/dialog/confirm-dialog.component';
export interface CouponCode {
    name: string;
}

@Component({
    selector: 'app-order-addedit',
    templateUrl: './templates/add_order.html',
    providers: [Global,OrderService],
    animations: [AddEditTransition],
    host: {
        '[@AddEditTransition]': ''
    },
})
export class OrderAddEditComponent implements OnInit, DoCheck {
    public response: any;
    public errorMsg: string;
    public successMsg: string;
    public formModel: any = {};
    private sub: any;
    public tabIndex: number;
    public parentId: number = 0;
    public add_edit: any = '';
    public product_list:any = [];
    public channel_list: any = [];
    public payment_list: any = [];
    public warehouse_list:any  = [];

    public locationType:any = 'Z';
    
    public country_list: any = [];

    public billing_state_list: any = [];
    public shipping_state_list: any = [];
    public subAreaList:any = [];
    public selected_products_ids: any = '' ;
    public cart_list: any = [];
    public orderDetails: any = {};
    public quantitiesArr: any = {};
    public productPriceArr: any = {};
    public orderData:any = {};
    public zone_list:any = [];
    public deliverySlotList:any = [];
    public selected_coupon_code :string = '';
    public currency_list: any = [];
    public selectedSlot:any= [];
    public activitySettings: boolean = false;
    visible = true;
    selectable = true;
    removable = true;
    addOnBlur = true;
    public orderInfo: any = {};
    public orderId:number=0;
    readonly separatorKeysCodes: number[] = [ENTER];
    applied_code: CouponCode[] = [];
    public productsList: any = [];
    public is_coupon_applied:boolean = false;
    public customer_list:any  = [];
    customerInfo = null;

    search_customer_list = [];
    selectedCustomers:any = [];
    isLoaderCustomer:boolean = false;

    scan_sku:any= [];
    
    CARRIER_CODE:any = [50,52,54,55,56,58];
    country_carrier_code :any=971;
    country_carrier_code_list:any = [971]
    public applicable_coupon_type:string = 'loaddata';
    public is_apply_wallet:number = 0;  
    public is_wallet_applicable :boolean = false;
    

    constructor(
        private _orderService: OrderService,
        public _globalService: GlobalService,
        private global: Global,
        private _router: Router,
        private _route: ActivatedRoute,
        private _cookieService: CookieService,
        public dialog: MatDialog,
        public dialogsService: DialogsService,
        @Inject(DOCUMENT) private document: any) {
            this.tabIndex = +this._globalService.getCookie('active_tabs');
            this.parentId = this._globalService.getParentTab(this.tabIndex);
            this.filterCustomerFirst(' ');
        }
        
    changeLog: string[] = [];

    ngDoCheck() {
       // console.log("Logged is coming");
    }


    ngOnInit() {
        let website_id = this._globalService.getWebsiteId();
        this.loadWarehouseList();
        this.formModel.created = new Date();
        this.formModel.pay_txndate = new Date();
        let userData = this._cookieService.getObject('userData');
        this.formModel.currency_id = userData['currencyId'];
        this.formModel.currencyCode = userData['currencysymbol'];
        this.formModel.send_email = 'n';
        this.formModel.delivery_country = 221;
        this.get_shipping_state(this.formModel.delivery_country);
        this.add_edit = 'Add';
        this.formModel.webshop_id = 6;
        this.formModel.payment_method_id = 16;
        this.sub = this._route.params.subscribe(params => {
            this.formModel.orderId = +params['id']; // (+) converts string 'id' to a number
            this.orderId = params['id'];
            if (this.orderId) {
                this.add_edit = 'Edit';
            } else {
                this.orderId = 0
            }
            let that = this;
            this._orderService.orderLoad(this.formModel.orderId).subscribe(
                data => {
                    this.country_list = data.country_list;
                    this.channel_list = data.channel;
                    this.payment_list = data.payment_method;
                    this.zone_list = data.zone_list;
                     
                    ////////////////// start customer selection  ////////////////
                    this.customer_list = data.customers;
                    if (this.orderId > 0) {
                        this.selectedCustomers = data.api_status.customer;
                        this.search_customer_list.push(this.selectedCustomers);
                        this.search_customer_list.map((i) => { i.fullName = i.first_name + ' ' + (i.last_name != null ? i.last_name : ''); return i; });     
                    }
                    ////////////////// End customer selection  ////////////////
                    if (this.formModel.orderId > 0 && data.api_status) {
                        this.formModel = data.api_status;
                        this.formModel.products = data.products;
                    }
                    
                    if (this.formModel.id > 0) {
                        if (this.formModel.applied_coupon != "") {
                            this.is_coupon_applied = true;
                        }
                        this.formModel.customer_id = data.api_status.customer.id;
                        let phone = this.formModel.billing_phone;
                        phone  = phone.replace("+","");
                        let billing_phone = phone;
                        phone  = phone.substr(0,5);
                        let carrier_code = +phone.replace("971","");
                        console.log(carrier_code);
                        this.formModel.carrier_code = carrier_code;
                        this.formModel.billing_phone = billing_phone.replace(phone,"");

                        this.formModel.orderId = this.formModel.id;

                        this.formModel.warehouse_id = this.formModel.assign_wh; // assigned the selected warehouse.
                        if(this.formModel.warehouse_id) {
                        //this.formModel.time_slot_date_id = this.formModel.time_slot_date + ' ' + this.formModel.time_slot_id
                        this.formModel.time_slot_date_id = this.formModel.time_slot_date;
                        this.getTimeSLot(this.formModel.warehouse_id, this.formModel.time_slot_date_id);
                        }
                                                
                        let productIdsArr = []
                        let that = this;
                        this.formModel.products.forEach(function (item: any) {
                            productIdsArr.push(item.product_id)
                            that.quantitiesArr[item.product_id] = item.quantity; 
                        });
                        this.selected_products_ids = productIdsArr.join(',');
                        this.updateCartDetails(this.selected_products_ids);

                        /*this.cart_list = data.api_status.order_products;
                        this.cart_list.forEach( function (orderItems:any)  {
                            orderItems.id = orderItems.product.id;
                            orderItems.search_name = orderItems.product.sku + ' | ' + orderItems.product.name;
                            orderItems.new_default_price_unit = orderItems.product_price;
                            orderItems.qty = orderItems.quantity;
                            orderItems.discount_price = orderItems.product_discount_price;
                            orderItems.new_default_price = orderItems.product_price*orderItems.quantity;
                            orderItems.is_igst = 'No';
                            orderItems.tax_price_unit = orderItems.product_tax_price;
                            orderItems.discount_price_unit = orderItems.product_discount_price;
                        });

                        let applied_coupon_obj:any = {}
                        applied_coupon_obj.name  = data.api_status.applied_coupon;
                        applied_coupon_obj.coupon_code  = data.api_status.applied_coupon;
                        applied_coupon_obj.status  = 1
                        this.orderData["applied_coupon"]= [];
                        this.orderData["applied_coupon"].push(applied_coupon_obj);
                        console.log(this.orderData);

                        
                        this.orderDetails.net_total = data.api_status.net_amount;
                        this.orderDetails.sub_total = data.api_status.net_amount;
                        this.orderDetails.tax_amount = data.api_status.tax_amount;
                        this.orderDetails.handling_charge = data.api_status.handling_charge;
                        this.orderDetails.shipping_charge = data.api_status.shipping_cost;

                        this.orderDetails.cod_charge = data.api_status.cod_charge;

                        this.orderDetails.cart_discount = data.api_status.cart_discount;
                        this.orderDetails.grand_total = data.api_status.gross_amount;

                        // this.orderData.applied_coupon = data.api_status.applied_coupon;
                        // this.orderData.shipping_flat = 0;

                        let tmpOData:any = {};
                        tmpOData.balance_due = data.api_status.balance_due;
                        tmpOData.cart_discount = data.api_status.cart_discount;
                        tmpOData.cod_charge = data.api_status.cod_charge
                        tmpOData.grand_total= data.api_status.gross_amount
                        tmpOData.gross_discount = data.api_status.gross_discount_amount;
                        tmpOData.handling_charge = data.api_status.handling_charge;
                        tmpOData.max_amount = data.api_status.max_amount;
                        tmpOData.min_amount = data.api_status.min_amount;
                        tmpOData.paid_amount = data.api_status.paid_amount;
                        tmpOData.net_total = data.api_status.net_amount;
                        tmpOData.shipping_charge = data.api_status.shipping_cost;
                        tmpOData.sub_total = data.api_status.net_amount;
                        tmpOData.tax_amount = data.api_status.tax_amount;
                        this.orderData["postdata"]= [];
                        this.orderData["postdata"].push(tmpOData); */

                        if (this.formModel.currency_code != "") {
                            this.getCurrencyDetails(this.formModel.currency_code);
                        }

                    } else {
                        this.formModel.orderId = 0;
                        this.formModel.customer_id = 0;
                        this.formModel['created_date'] = new Date();
                        this.formModel['custom_order_id'] = data.Order_id;
                        this.formModel['promocode'] = [];
                        this.formModel.payment_type_id = 4;
                        this.formModel.set_primary = 1;
                    }
                },
                err => {
                    that._globalService.showToast('Something went wrong. Please try again.');
                },
                function () {
                    //completed callback
                }
            );
        });
        this.orderInfo = { orderId: this.formModel.orderId, activityType: 1 } // Asign the order data into activity variables                    
    }

    apply_loyality_point(event) {
        this.is_wallet_applicable = event.checked;
        this.applicable_coupon_type = 'applycode';    
        this.is_apply_wallet = event.checked == true ? 1 : 0;
        this.updateCartDetails(this.selected_products_ids);
    }

    loadWarehouseList() {
		this._orderService.loadWarehouseList().subscribe(data => {
			if (data.status == 1) {
				this.warehouse_list = data.api_status;
			}
			//console.log(this.tag_list);
		}, err => console.log(err), function () { });
	}

    generateCartInfo(cartInfo:any) {
        let cart:any = [];
        //console.log(cartInfo);
    }

    loadZoneMaster() {
        this.global.getWebServiceData('zone_list','GET','','').subscribe(result => {
            if(result["status"] == 1) {
                this.zone_list = result.data;
            }
        }, err => {
        });
    }

    getCurrencyDetails(currencyCode) {
        if(currencyCode == '' || currencyCode == null) {
            currencyCode = 'INR';
        }
        let data:any = {};
        data.currency_code = currencyCode;
        this.global.getWebServiceData('currency-by-code','POST',data,'').subscribe(result => {
            if(result["status"] == 1) {
                this.formModel.currency = result["data"]["id"]+'SSS'+result["data"]["currencysymbol"];
                this.currencySettings(this.formModel.currency);
            } else { // show error message
                this._globalService.showToast(result["message"]);
            }
        }, err => {
        });
    }

    getTimeSLot(warehouseId,time_slot_date_id:any='') {
        this.selectedSlot= [];
        if(time_slot_date_id != '') {
            this.selectedSlot.push({
                groupLabelSlot: time_slot_date_id,
                groupOptionValue: time_slot_date_id,
            });
        }

        this._orderService.getAvailableSlot(warehouseId).subscribe(result => {
            if(result["status"] == 1) {
                this.deliverySlotList = result.delivery_slot; 
                const tmp = this.deliverySlotList;
                tmp.forEach((element) => {
                    element.groupLabel = this._globalService.convertDate(element.delivery_date , 'EEEE') + '('+element.delivery_date+')';
                    const slotData = element.available_slot;
                    if(slotData.length > 0) {
                        slotData.forEach((val) => {
                            //val.groupLabelSlot = element.delivery_date+' '+this._globalService.convertDate(element.delivery_date+' '+val.start_time , 'h:mm a')+'-'+this._globalService.convertDate(element.delivery_date+' '+val.end_time , 'h:mm a');
                            val.groupLabelSlot = element.delivery_date;
                            val.groupOptionValue = element.delivery_date+'##'+this._globalService.convertDate(element.delivery_date+' '+val.start_time , 'h:mm a')+'-'+this._globalService.convertDate(element.delivery_date+' '+val.end_time , 'h:mm a')+'##'+val.start_time+'##'+val.end_time;
                        })
                    }
                });
                // console.log("==============================")
                // console.log(tmp);
                if(time_slot_date_id != '') {
                    this.formModel.time_slot_date_id = time_slot_date_id;
                }
            }
        }, err => {
        });
    }

    
    remove() {
        this.applicable_coupon_type = 'applycode';
        this.selected_coupon_code = "";
        this.updateCartDetails(this.selected_products_ids);
        this.formModel.applied_coupon = "";
        this.is_coupon_applied = false;
    }

    applyCouponCode() {
        this.applicable_coupon_type = 'applycode';
        this.applied_code = this.formModel.applied_coupon;
        if (this.applied_code.length > 0) {
            this.selected_coupon_code = this.formModel.applied_coupon;
            this.updateCartDetails(this.selected_products_ids);
        }
    }

    loadChannels(website_id: number) {
        this._orderService.loadChanneslMasters(website_id).subscribe(data => {
            if (data.status == 1) {
                this.channel_list = data.api_status; // list of marketplace
            }
        }, err => {}, function() { // call back function when exection is done
        })
    }
    // loadWebsitePaymentMethods(website_id) {
    //     let data: any = {};
    //     data.website_id = website_id;
    //     this._orderService.getWebsitePaymentMethods(data).subscribe(data => {
    //         if (data.status == 1) {
    //             this.payment_method_list = data.api_status; // list of payment method
    //         }
    //     }, err => {}, function() { // call back function when exection is done
    //     })
    // }
    // generate custom order id
    generateCustomOrderId(webshop_id) {
        if( this.formModel.orderId == 0) {
            this._orderService.getCustomOrderId(webshop_id).subscribe(data => {
                if (data.status == 1) {
                    this.formModel.custom_order_id = data.api_status; // list of marketplace
                }
            }, 
            err => {}, function() { // call back function when exection is done
            })
        }
    }
    

    showActivityPanel(show:boolean) {
        this.activitySettings = !show;
    }

    get_billing_state(country_id: number) {
        this._orderService.loadStates(country_id).subscribe(data => {
            this.billing_state_list = data.states;
        }, err => console.log(err), function() {});
    }
    get_shipping_state(country_id: number) {
        this._orderService.loadStates(country_id).subscribe(data => {
            this.shipping_state_list = data.states;
        }, err => console.log(err), function() {});
    }

    filterCustomer(val: any,event) {
        if (event.keyCode != 13 && event.keyCode != 38 && event.keyCode != 40) {
            let data: any = {};
            data.search = val;
            this._orderService.filterCustomerList(data).subscribe(data => {
                if (data.status == 1) {
                    this.customer_list = data.api_status;
                } else {
                    this.customer_list = [];
                }
            }, err => { }, function () { });
        }
    }

    onSearchCustomer(event) {
        this.isLoaderCustomer = true;
        let val = event.term;
        if (val != null && val != "") {
            let data: any = {};
            data.search = val;
            this._orderService.filterCustomerList(data).subscribe(data => {
                if (data.status == 1) {
                    this.customer_list = data.api_status;
                    this.search_customer_list = this.customer_list;
                    this.search_customer_list.map((i) => { i.fullName = i.first_name + ' ' + (i.last_name != null ? i.last_name : ''); return i; });
                    this.isLoaderCustomer = false;
                } else {
                    this.isLoaderCustomer = false;
                    this.search_customer_list = this.customer_list;
                    this.customer_list = [];
                }
            }, err => { }, function () { });
        } else {
            this.isLoaderCustomer = false;
            this.filterCustomerFirst(' ');
        }
    }

    filterCustomerFirst(val) {
          let data: any = {};
            data.search = val;
            this._orderService.filterCustomerList(data).subscribe(data => {
                if (data.status == 1) {
                    this.customer_list = data.api_status;
                    this.search_customer_list = this.customer_list;
                    this.search_customer_list.map((i) => { i.fullName = i.first_name + ' ' + (i.last_name != null ? i.last_name : ''); return i; });
                    this.isLoaderCustomer = false;
                } else {
                    this.isLoaderCustomer = false;
                    this.customer_list = [];
                }
            }, err => { }, function () { });
    }

    getValues() {
        if (this.selectedCustomers != null) {
            if (this.selectedCustomers.id > 0 ) {
                this.setBillingAddress(this.selectedCustomers);
            } else {
                this.formModel.billing_name = this.selectedCustomers.fullName;
            }
            this.isLoaderCustomer = false;    
        }       
    }


    getSubAreaList(keyword) {
        this._orderService.getAreaSubarea(keyword).subscribe(res => {
            if (res.status == 1) {
                this.subAreaList = res.data;
            } else {
                this.subAreaList = [];
            }
        }, err => {}, function() {});   
    }

    loadCurrencyMasters() {
        this.global.getWebServiceData('currencylist','GET','','').subscribe(res => {
            if(res["status"] == 1) {
                this.currency_list = res["data"];
            }
        }, err => {

        })
    }

    currencySettings(currencyData:any) {
        const currencyArr = currencyData.split("SSS"); // string contains 'SSS'
        this.formModel.currency_id = currencyArr[0];
        this.formModel.currencyCode = currencyArr[1];
    }
    
    
    setBillingAddress(customers: any) {
        setTimeout(() => { // showing automatic activity
            this._globalService.showLoaderSpinner(true);
        }, 500);
        let billing_name = '';
        let data: any = {};
        data.id = customers.id;
        this.formModel.customer_id = customers.id;
        this._orderService.getCustomerAddressInfo(data).subscribe(data => {
            let response = data.api_status[0];
            this.formModel.user_group_id = response.group_id;
            if(response.last_name != null) {
                billing_name  = response.first_name + ' ' + response.last_name;
            } else {
                billing_name  = response.first_name;
            }
            this.formModel.billing_name = billing_name
            this.formModel.billing_email_address = response.email;
            
            //this.formModel.billing_phone = response.phone;
            let phone = response.phone;
            phone  = phone.replace("+","");
            let billing_phone = phone;
            phone  = phone.substr(0,5);
            let carrier_code = +phone.replace("971","");
            console.log(carrier_code);
            this.formModel.carrier_code = carrier_code;
            this.formModel.billing_phone = billing_phone.replace(phone,"");
            
            /////////// setting the billing address ///////////////////
            let addressInfo = data.api_status[0].customer_address_book;
            //if (addressInfo.length > 0) { // if address information is found.
                this.formModel.billing_street_address = addressInfo.billing_street_address;
                this.formModel.billing_street_address1 = addressInfo.billing_street_address1;
                this.formModel.billing_country = addressInfo.billing_country;
                if (addressInfo.billing_country > 0) {
                    this.get_billing_state(addressInfo.billing_country);
                }
                this.formModel.billing_state = +addressInfo.billing_state; // only integrer is allowed
                this.formModel.billing_city = addressInfo.billing_city;
                this.formModel.billing_postcode = addressInfo.billing_postcode;
                /////////// setting the shipping address ///////////////////
                this.formModel.delivery_street_address = addressInfo.delivery_street_address;
                this.formModel.delivery_street_address1 = addressInfo.delivery_street_address1;
                this.formModel.delivery_country = 221
                if (addressInfo.delivery_country > 0) {
                    this.get_shipping_state(addressInfo.delivery_country);
                }
                this.formModel.delivery_state = +addressInfo.delivery_state; // only integrer is allowed
                this.formModel.address_book_id = +addressInfo.id
                this.formModel.delivery_city = addressInfo.delivery_city;
                this.formModel.delivery_postcode = addressInfo.delivery_postcode;
                this.formModel.set_primary = addressInfo.set_primary;
                setTimeout(() => { // showing automatic activity
                    this._globalService.showLoaderSpinner(false);
            }, 500);
            //}
        }, err => {}, function() {});
    }
    copyAddress(event) {
        if (event.checked) { // copy billing address to shipping address
            this.formModel.delivery_street_address = this.formModel.billing_street_address;
            this.formModel.delivery_street_address1 = this.formModel.billing_street_address1;
            this.formModel.delivery_country = this.formModel.billing_country;
            if (this.formModel.delivery_country > 0) {
                this.get_shipping_state(this.formModel.delivery_country);
            }
            this.formModel.delivery_state = this.formModel.billing_state; // only integrer is allowed
            this.formModel.delivery_city = this.formModel.billing_city;
            this.formModel.delivery_postcode = this.formModel.billing_postcode;
        } else { // else shipping address might be different
            this.formModel.delivery_street_address = '';
            this.formModel.delivery_street_address1 = '';
            this.formModel.delivery_state = ''; // only integrer is allowed
            this.formModel.delivery_city = '';
            this.formModel.delivery_postcode = '';
        }
    }

    sendOrderEmailSetings(event) {
        if (event.checked) { 
            this.formModel.send_email = 'y';
        } else {
            this.formModel.send_email = 'n';
        }
    }
    dialogRefTags: MatDialogRef <SelectProductComponent>|null;
    openProductPop(index: number) {
        if(index <= 0) {
            index = -1;
        }
        if (this.formModel.webshop_id == undefined || this.formModel.webshop_id <= 0) {
            this._globalService.showToast("Please select a store.");
            window.scrollTo(0, 0);
            return false;
        }  else { 
            let data: any = {};
            data['index'] = index;
            data['webshop_id'] = this.formModel.webshop_id;
            if (this.formModel.orderId > 0) {
                data['order_id'] = this.formModel.orderId;
            }
            data['selected_products_ids'] = this.selected_products_ids;
            this.dialogRefTags = this.dialog.open(SelectProductComponent, {
                data: data,
                height: '800px',
                width: '800px'
            });
            this.dialogRefTags.afterClosed().subscribe(result => {
                if (result !== undefined) {
                    this.selected_products_ids = result['product_ids'];
                    //console.log(this.selected_products_ids);
                    this.updateCartDetails(this.selected_products_ids);
                }
            });
        }
    }

    onlyUnique(value, index, self) {
        return self.indexOf(value) === index;
    }

    updateCartDetails(product_ids) {
        //console.log(product_ids);
        setTimeout(() => { // showing automatic activity
            this._globalService.showLoaderSpinner(true);
        }, 500);
        if(product_ids != '') {
            let data: any = {};
            data.website_id = this._globalService.getWebsiteId();
            data.company_id = this._globalService.getCompanyId();
            
            let productIdsArr = [];
            let productIdsObj: any = {};
            let defaultPriceObj = {};
            productIdsArr = product_ids.split(',');
            var uniqueAArr = productIdsArr.filter(this.onlyUnique); 
            data.product_ids = uniqueAArr.join(",");
            let defaultPrice = [];
            let newQtyArr: any = [];
            let priceStr:any;
            let qtyStr:any;
            for (let i = 0; i < productIdsArr.length; i++) {
                if (!defaultPriceObj[productIdsArr[i]]) {
                    defaultPriceObj[productIdsArr[i]] = 0;
                }
                defaultPriceObj[productIdsArr[i]] = this.productPriceArr[productIdsArr[i]] != undefined ? this.productPriceArr[productIdsArr[i]] : 0; // this is not using for now.                
                if (priceStr!= undefined) {
                    //alert(priceStr);
                    priceStr = priceStr+','+defaultPriceObj[productIdsArr[i]];
                } else {
                    priceStr = '' + defaultPriceObj[productIdsArr[i]]+'';
                }
            }
            for (let i = 0; i < productIdsArr.length; i++) {
                if (!productIdsObj[productIdsArr[i]]) {
                    productIdsObj[productIdsArr[i]] = '';
                }
                let itemQuantity = this.quantitiesArr[productIdsArr[i]] != undefined ? this.quantitiesArr[productIdsArr[i]] : 1; // putting default quantiy as 1 for new added products
                //newQtyArr.push(itemQuantity);
                productIdsObj[productIdsArr[i]] = itemQuantity;

                if (qtyStr != undefined) {
                    qtyStr = qtyStr + ',' + productIdsObj[productIdsArr[i]];
                } else {
                    qtyStr = '' + productIdsObj[productIdsArr[i]]+'';
                }
            }
           
            this.quantitiesArr = productIdsObj; // assigned quantity to global variable
            this.productPriceArr = defaultPriceObj;
           
            data.qtys = qtyStr
            data.prod_price = priceStr;
            data.country_id = this.formModel.delivery_country;
            data.state_id = this.formModel.delivery_state;
            data.post_code = this.formModel.delivery_postcode;
            data.payment_method_id = this.formModel.payment_method_id;
            data.customer_id = this.formModel.customer_id;
            data.user_group_id = this.formModel.user_group_id;
            data.coupon_code = this.selected_coupon_code;
            data.applicable_coupon_type = this.applicable_coupon_type;
            data.warehouse_id = this.formModel.warehouse_id;
            data.is_apply_wallet = this.is_apply_wallet;
            data.customer_id = this.formModel.customer_id;
            if(this.formModel.orderId > 0) {
                data.order_id = this.formModel.orderId;
            }
            
            this._orderService.loadCartInfo(data).subscribe(data => {
                this.orderData = data;
                this.cart_list = data.cartdetails;
                this.cart_list.forEach(tmp => {
                    tmp.search_name = tmp.sku + ' | ' + tmp.name;
                });
                // this.orderDetails = data.orderamountdetails[0];  
                this.orderDetails = data.postdata[0];
                this.is_wallet_applicable =  this.orderDetails.applied_loyalty_amount > 0 ? true : false;
                if(data["applied_coupon"].length > 0) {
                    this.orderDetails.cart_discount = data["applied_coupon"][0]['amount'] > 0 ? data["applied_coupon"][0]['amount'] : 0 ;
                    if(data["applied_coupon"][0]["status"] == 1) { // coupon code is applied successfully
                        //this._globalService.showToast('Discount Amount ' +data["applied_coupon"][0]["amount"]);
                        this._globalService.showToast("Coupon code applied successfully.");
                        this.is_coupon_applied = true;
                    } else { // invalid coupon code 
                        this._globalService.showToast(data["applied_coupon"][0]["message"]);
                        this.is_coupon_applied = false;
                        this.formModel.applied_coupon = "";
                    }
                    this.productsList = [];
                }
                setTimeout(() => { // showing automatic activity
                    this._globalService.showLoaderSpinner(false);
                }, 500);
            }, err => {
                setTimeout(() => { // showing automatic activity
                    this._globalService.showLoaderSpinner(false);
                }, 500);
            }, function() {});
        } else {
            setTimeout(() => { // showing automatic activity
                this._globalService.showLoaderSpinner(false);
            }, 500);
            this._globalService.showToast("Your cart can not be empty.");
        }
    }

    deleteFromCart(deletedItemId: number) {
        let productIdsArr:any = [];
        productIdsArr = this.selected_products_ids.split(',').map(function (item) {
            return parseInt(item, 10);
        });
        var index = productIdsArr.indexOf(deletedItemId);
        if(index > -1) {
            productIdsArr.splice(index, 1);    
            if (productIdsArr.length > 0) {
                this.selected_products_ids = productIdsArr.join(',');
                this.updateCartDetails(this.selected_products_ids);
            } else {
                this.selected_products_ids = "";
                this.updateCartDetails(this.selected_products_ids);
                this.cart_list= [];
                this.orderDetails.sub_total = 0;
                this.orderDetails.tax_amount = 0;
                this.orderDetails.handling_charge = 0;
                this.orderDetails.cod_charge = 0;
                this.orderDetails.cart_discount = 0;
                this.orderDetails.grand_total = 0;

            }
        }
    }

    updateQuantity(product_id: number, qty: number) {
        if(qty > 0) {
            this.quantitiesArr[product_id] = +qty; // + converted quantity as number
            this.updateCartDetails(this.selected_products_ids);    
        } else {
            this.quantitiesArr[product_id] = 1;
        }
        
    }

    updateProductPrice(product_id: number, price: any) {
       this.productPriceArr[product_id] = price;
        this.updateCartDetails(this.selected_products_ids);
    }

    addEditOrderSave(form:any) {
        // console.log(this.formModel);
        if(this.cart_list.length==0) {
            this.dialogsService.alert('Error', 'Select at least one product').subscribe(res => {});
        } else {
            let that = this;
            let data:any = {};
            data['data'] = Object.assign({},this.formModel);
            data.data.website_id = this._globalService.getWebsiteId();
            data.data.company_id = this._globalService.getCompanyId();
            data.data['user_id'] = this._globalService.getUserId();
            data.data['ip_address'] = (this._globalService.getCookie('ipaddress'))?this._globalService.getCookie('ipaddress'):'';
            if(!this.formModel.orderId){
                data.data.createdby = this._globalService.getUserId();
            }
            data.data.updatedby = this._globalService.getUserId();
            if(this.orderId == 0) {
                data.data['buy_status'] = 1;
                data.data['order_status'] = 0;
            }
            data.data['pay_txntranid'] = this.formModel.pay_txntranid!=undefined ? this.formModel.pay_txntranid : "";
            data.data['custom_msg'] = this.formModel.custom_msg!=undefined ? this.formModel.custom_msg : "";
            data.data['sub_total'] = this.formModel.gross_amount;
            data.data['net_total'] = this.formModel.net_amount;
            data.data['shipping_charge'] = this.formModel.shipping_cost;
            
            let customerInfo:any= {};
            customerInfo.billing_name = this.formModel.billing_name;
            customerInfo.billing_email_address = this.formModel.billing_email_address;
            customerInfo.billing_phone = "971"+this.formModel.carrier_code+""+this.formModel.billing_phone;
            
            if(this.formModel.customer_id > 0) {
                customerInfo.user_id = this.formModel.customer_id;
            }
            customerInfo.delivery_street_address = this.formModel.delivery_street_address!=undefined ?  this.formModel.delivery_street_address : "";
            customerInfo.delivery_street_address1 = this.formModel.delivery_street_address1!=undefined ?  this.formModel.delivery_street_address1 : "";
            customerInfo.delivery_country = 221;
            customerInfo.delivery_state = this.formModel.delivery_state;
            customerInfo.delivery_city = this.formModel.delivery_city;
            customerInfo.delivery_postcode = this.formModel.delivery_postcode;
            
            customerInfo.billing_street_address = this.formModel.delivery_street_address!=undefined ?  this.formModel.delivery_street_address : "";
            customerInfo.billing_street_address1 = this.formModel.delivery_street_address1!=undefined ?  this.formModel.delivery_street_address1 : "";
            customerInfo.billing_country = this.formModel.delivery_country;
            customerInfo.billing_state = this.formModel.delivery_state;
            customerInfo.billing_city = this.formModel.delivery_city;
            customerInfo.billing_postcode = this.formModel.delivery_postcode;
            customerInfo.address_book_id = this.formModel.address_book_id;
            customerInfo.delivery_street_address1 = this.formModel.delivery_street_address1;
            customerInfo.area_id = 0;
            
            customerInfo.set_primary = this.formModel.set_primary;
            data.data['customerdetails'] = customerInfo;
            this.cart_list.forEach(element => {
                this.cart_list['qty']=element.quantity;
            });
            data.data['cartdetails'] = this.cart_list;
            data.data['applied_coupon'] = this.orderData["applied_coupon"];
            data.data['shipping_flat'] = this.orderData["shipping_flat"];

            data.data['balance_due'] = this.orderData["postdata"][0].balance_due;
            data.data['cart_discount'] = this.orderData["postdata"][0].cart_discount;
            data.data['cod_charge'] = this.orderData["postdata"][0].cod_charge;
            data.data['grand_total'] = this.orderData["postdata"][0].grand_total;
            data.data['gross_discount'] = this.orderData["postdata"][0].gross_discount;
            data.data['handling_charge'] = this.orderData["postdata"][0].handling_charge;
            data.data['max_amount'] = this.orderData["postdata"][0].max_amount;
            data.data['min_amount'] = this.orderData["postdata"][0].min_amount;
            data.data['paid_amount'] = this.orderData["postdata"][0].paid_amount;
            data.data['net_total'] = this.orderData["postdata"][0].net_total;
            data.data['shipping_charge'] = this.orderData["postdata"][0].shipping_charge;
            data.data['sub_total'] = this.orderData["postdata"][0].sub_total;
            data.data['tax_amount'] = this.orderData["postdata"][0].tax_amount;
            data.data['warehouse_id'] = this.formModel.warehouse_id;
            data.data["pay_wallet_amount"] = this.orderData["postdata"][0].applied_loyalty_amount;
            // console.log(this.orderData);
            that._globalService.showLoaderSpinner(true);
            // console.log('Yes data is coming...');
            // console.log(data);
            this._orderService.createOrders(data, this.orderId).subscribe(
                data => {
                    if(data.status === 1) {
                        this._globalService.showToast(data.message);
                        //if(this.orderId == 0) {
                            this._globalService.deleteTab(this.tabIndex,this.parentId);
                        //}
                    } else{
                        this._globalService.showToast(data.message);
                        that._globalService.showLoaderSpinner(false);
                    }
                } ,
                err => {
                } , function () {
                       that._globalService.showLoaderSpinner(false);
                }
            );
        }
    }

    getSlotDetails(slotDetails:any) {
        if (slotDetails.value != undefined) {
            const slotArr = slotDetails.value.split("##");
            this.formModel.time_slot_date = slotArr[0];
            this.formModel.time_slot_id = slotArr[1];
            this.formModel.slot_start_time = slotArr[2];
            this.formModel.slot_end_time = slotArr[3];
        }
    }

    getProductDetails(sku:string,event) {
        if(this.formModel.warehouse_id != undefined) {
            if (event.keyCode != 13 && event.keyCode != 38 && event.keyCode != 40) {
                let filterValue: any = '';
    
                filterValue = event.term;
                let matchArr = [];
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
                if (filterValue != '') { // pushing search conditions
                    let fieldsArr:any = ["name", "sku"];
                    if (filterValue != undefined ) {
                        filterValue = filterValue.replace("/", "\\", filterValue);
                    } else {
                        filterValue = "";
                    }
                    
                    conditions = {}
                    conditions.query = "*" + filterValue + "*";
                    conditions.fields = fieldsArr;
                    innerMatch = {};
                    innerMatch.query_string = conditions;
                    matchArr.push(innerMatch);
                } else {
                    filterValue = "a";
                }
    
    
                let userData = this._cookieService.getObject('userData');
                let extraFilter = JSON.stringify(matchArr);
                //"query_string": {"fields": ["name","sku"]}
    
                //let elasticData = '{"query":{"bool":{"must": ' + extraFilter + '}}}';
                let elasticData = '{"query":{"bool":{"must":[{"query_string":{"query":"'+filterValue+'"}},{"match":{"visibility_id":{"query":"Catalog Search","operator":"and"}}}],"filter":[{"nested":{"path":"inventory","query":{"bool":{"must":[{"term":{"inventory.id":'+this.formModel.warehouse_id+'}},{"range":{"inventory.stock":{"gt":0}}}]}},"score_mode":"avg"}},{"nested":{"path":"channel_currency_product_price","query":{"bool":{"must":[{"range":{"channel_currency_product_price.new_default_price":{"gt":0}}},{"term":{"channel_currency_product_price.warehouse_id":'+this.formModel.warehouse_id+'}}]}}}},{"nested":{"path":"product_images","query":{"bool":{"must":[{"term":{"product_images.is_cover":1}}]}}}}]}},"from":0,"size":100}';
                this._orderService.getProductsES(elasticData, websiteId).subscribe(
                    listData => {
                        let tmpResult = [];
                        listData.hits.hits.forEach(function (rows: any) {
                            tmpResult.push(rows._source);
                        });
    
                        if (tmpResult.length > 0) {
                            this.productsList = tmpResult;
                            this.productsList.forEach(tmpElement => {
                                tmpElement.search_name = tmpElement.sku + ' | ' + tmpElement.name;
                            });
                            if (userData['elastic_host'] == 'uat.grocersolution.com' || userData['elastic_host'] == 'mikarito.grocersolution.com' || userData['elastic_host'] == 'basracenter.grocersolution.com' ) {  // this is for new elsatic server
                                listData.hits.total = listData.hits.total.value;
                            }
                        } else {
                            this.productsList = [];
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
        } else {
            this._globalService.showToast('Please select a store.');
        }
        
    }

    displayFnCustomer(obj: any) {
        //console.log(obj);
        return obj ? obj.first_name : obj;
    }
    displayFnSKU(obj: any) {
        //return obj ? 'test' : obj;
    }

    scanItem1(itemIndex,event) {
        let newItemId = event.id;
        this.scanItem(itemIndex, newItemId)
    }

    scanItem(itemIndex,itemId) {
        console.log(itemId)
        if (this.formModel.webshop_id == undefined || this.formModel.webshop_id <= 0) {
            this._globalService.showToast("Please select a store.");
            window.scrollTo(0, 0);
            return false;
        } else if (this.formModel.payment_method_id == undefined || this.formModel.warehouse_id <= 0) {
            this._globalService.showToast("Please select a store.");
            window.scrollTo(0, 0);
            return false;
        } else {
            let productId = this.scan_sku.id;
            if (itemId > 0) {
                productId = itemId;
            }
                          
            let bulk_ids: any = [];
            if (this.selected_products_ids != '') {
                bulk_ids = this.selected_products_ids.split(",");
                if (itemIndex != '') { // checking the first item of the selection
                    bulk_ids[itemIndex] = productId;
                } else {
                    bulk_ids.push(productId);
                }
                let uniqueIds = bulk_ids.filter(function (item, pos) {
                    return bulk_ids.indexOf(item) == pos;
                })
                this.selected_products_ids = uniqueIds.join(",");
            } else {
                this.selected_products_ids = productId.toString();
            }
            this.updateCartDetails(this.selected_products_ids);
            this.formModel.sku = '';
            this.scan_sku = [];
        }
    }

    UpdateItems(itemDetails :any,itemIndex:any) {
        if (this.formModel.webshop_id == undefined || this.formModel.webshop_id <= 0) {
            this._globalService.showToast("Please select a store.");
            window.scrollTo(0, 0);
            return false;
        }  else if (this.formModel.delivery_street_address1 == undefined || this.formModel.delivery_street_address1 == '') {
            this._globalService.showToast("Please enter delivery area.");
            window.scrollTo(0, 0);
            return false;
        } else if (this.formModel.delivery_postcode == undefined || this.formModel.delivery_postcode == '') {
            this._globalService.showToast("Please enter delivery zipcode.");
            window.scrollTo(0, 0);
            return false;
        } else {
            let productId = itemDetails.id;
            let bulk_ids: any = [];
            if (this.selected_products_ids != '') {
                bulk_ids = this.selected_products_ids.split(",");
                // console.log("--------------");
                // console.log(bulk_ids);
                // console.log("--------------");
                if (itemIndex != '') { // checking the first item of the selection
                    bulk_ids[itemIndex] = productId;
                } else {
                    bulk_ids.push(productId);
                }                
                let uniqueIds = bulk_ids.filter(function (item, pos) {
                    return bulk_ids.indexOf(item) == pos;
                })
                this.selected_products_ids = uniqueIds.join(",");
            } else {
                this.selected_products_ids = productId.toString();
            }
            this.updateCartDetails(this.selected_products_ids);
            this.formModel.sku = '';
        }        
    }
}

@Component({
    templateUrl: './templates/manage_tags.html',
    providers: [OrderService, Global],
})
export class ManageTagsComponent implements OnInit {
    public add_edit: any = '';
    public response: any;
    public errorMsg: string;
    public successMsg: string;
    public formModel: any = {};
    private sub: any;
    public tabIndex: number;
    public parentId: number = 0;
    public bulk_tags_ids: any = [];
    public rel_data: any = [];
    public pagination: any = {};
    public pageIndex: number = 0;
    public pageList: number = 0;
    public sortBy: any = '';
    public sortOrder: any = '';
    public sortClass: any = '';
    public sortRev: boolean = false;
    public selectedAllTagList: any = false;
    public stat: any = {};
    public result_list_tags: any = [];
    public total_list: any = [];
    public cols: any = []
    public add_btn: string;
    public post_data = {};
    public page: number = 1;
    public filter: string = '';
    public maxSize: number = 10;
    public directionLinks: boolean = true;
    public autoHide: boolean = false;
    public config: any = {};
    public permission: any = [];
    public show_btn: any = {
        'add': true,
        'edit': true,
        'delete': true,
        'block': true
    };
    public userId: any;
    public search_text: string;
    public childData: any = {};
    public individualRow: any = {};
    public selected_ids: any = [];
    constructor(
        private _orderService: OrderService,
        public _globalService: GlobalService, 
        private global: Global,
        private dialogsService: DialogsService,
        public dialog: MatDialog,
        private _router: Router,
        @Inject(DOCUMENT) private document: any
    ) {}
    ngOnInit() {
        this.tabIndex = +this._globalService.getCookie('active_tabs');
        this.parentId = this._globalService.getParentTab(this.tabIndex);
        this.childData = {
            table: 'EngageboostTags',
            heading: 'Tags',
            ispopup: 'N',
            tablink: 'Tags',
            tabparrentid: this.parentId,
            screen: 'list',
        }
        this.generateGrid(0, '', '', '', '');
    }
    generateGrid(reload: any, page: any, sortBy: any, filter: any, search: any) {
        let elements: NodeListOf < Element > = this.document.getElementsByClassName('manage-tags');
        elements[0].classList.remove('show-pop');
        this.total_list = [];
        this.selectedAllTagList = false;
        this.filter = filter;
        this.bulk_tags_ids = [];
        this.individualRow = {};
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
        this.userId = this._globalService.getUserId();
        this.post_data = {
            "model": this.childData.table,
            "screen_name": this.childData.screen,
            "userid": this.userId,
            "search": search,
            "order_by": sortBy,
            "order_type": this.sortOrder,
            "status": filter,
            "website_id":this._globalService.getWebsiteId(),
        }
        this._orderService.doGrid(this.post_data, page).subscribe(data => {
            this.response = data;
            if (this.response.count > 0) {
                this.result_list_tags = this.response.results[0].result;
                this.result_list_tags.forEach(function(item: any) {
                    if (item.isblocked == 'n') {
                        item.isblocked = 'Active';
                    } else {
                        item.isblocked = 'Inactive';
                    }
                })
                for (var i = 0; i < this.response.count; i++) {
                    this.total_list.push(i);
                }
            } else {
                this.result_list_tags = [];
            }
            // this.cols = this.response.results[0].layout;
            this.cols = this.response.results[0].applied_layout;
            this.pagination.total_page = this.response.per_page_count;
            this.pageList = this.response.per_page_count;
            this.stat.active = this.response.results[0].active;
            this.stat.inactive = this.response.results[0].inactive;
            this.stat.all = this.response.results[0].all;
            this.config.currentPage = page
            this.config.itemsPerPage = this.response.page_size;
        }, err => {
            this._globalService.showToast('Something went wrong. Please try again.');
        }, function() {});
    }
    seach_tags(seach_keyword: string, short_by: string) {
            this.generateGrid(1, 1, short_by, '', seach_keyword);
        }
        ////////////////////////////Check/Uncheck//////////////
    toggleCheckAllTags(event: any) {
        let elements: NodeListOf < Element > = this.document.getElementsByClassName('manage-tags');
        let that = this;
        that.bulk_tags_ids = [];
        this.selectedAllTagList = event.checked;
        this.result_list_tags.forEach(function(item: any) {
            item.selected = event.checked;
            if (item.selected) {
                that.bulk_tags_ids.push(item.id);
                elements[0].classList.add('show-pop');
            } else {
                elements[0].classList.remove('show-pop');
            }
        });
    }
    toggleCheckTags(id: any, event: any) {
        let elements: NodeListOf < Element > = this.document.getElementsByClassName('manage-tags');
        let that = this;
        this.result_list_tags.forEach(function(item: any) {
            if (item.id == id) {
                item.selected = event.checked;
                if (item.selected) {
                    that.bulk_tags_ids.push(item.id);
                    elements[0].classList.add('show-pop');
                } else {
                    var index = that.bulk_tags_ids.indexOf(item.id);
                    that.bulk_tags_ids.splice(index, 1);
                    elements[0].classList.remove('show-pop');
                }
            }
            if (that.bulk_tags_ids.length == 1) {
                that.bulk_tags_ids.forEach(function(item_id: any) {
                    if (item_id == item.id) {
                        that.individualRow = item;
                    }
                });
            }
            that.selectedAllTagList = false;
        });
    }
    updateStatusAll(type: number, id: number) {
        if (id) {
            let that = this;
            that.bulk_tags_ids = [];
            that.bulk_tags_ids.push(id);
        }
        if (type == 2) {
            var msg = 'Do you really want to delete selected records?';
            var perm = 'Y';
            var msgp = 'You have no permission to delete!';
        } else if (type == 1) {
            var msg = 'Do you really want to block selected records?';
            var perm = 'Y';
            var msgp = 'You have no permission to block!';
        } else {
            var msg = 'Do you really want to unblock selected records?';
            var perm = 'Y';
            var msgp = 'You have no permission to unblock!';
        }
        if (perm == 'Y') {
            if (this.bulk_tags_ids.length > 0) {
                this.dialogsService.confirm('Warning', msg).subscribe(res => {
                    if (res) {
                        this.global.doStatusUpdate(this.childData.table, this.bulk_tags_ids, type).subscribe(data => {
                            this.response = data;
                            this._globalService.showToast(this.response.Message);
                            this.generateGrid(1, 1, '', '', '');
                        }, err => console.log(err), function() {});
                    }
                });
            } else {
                this.dialogsService.alert('Error', 'Select Atleast One Record!').subscribe(res => {});
            }
        } else {
            this.dialogsService.alert('Permission Error', msgp).subscribe(res => {});
        }
    }
    dialogRefAddEditTags: MatDialogRef < ManageTagsAddEditComponent > | null;
    openPop(id: number) {
        this.dialogRefAddEditTags = this.dialog.open(ManageTagsAddEditComponent, {
            data: id
        });
        this.dialogRefAddEditTags.afterClosed().subscribe(result => {
            this.generateGrid(0, '', '', '', '');
        });
    }
}

@Component({
    templateUrl: './templates/add_tags.html',
    providers: [OrderService, Global],
})
export class ManageTagsAddEditComponent implements OnInit {
    public response: any;
    public errorMsg: string;
    public successMsg: string;
    public formModel: any = {};
    public ipaddress: any;
    constructor(private _orderService: OrderService, public _globalService: GlobalService, private global: Global, private dialogsService: DialogsService, private dialogRef: MatDialogRef < ManageTagsComponent > , public dialog: MatDialog, private _router: Router, @Optional()@ Inject(MAT_DIALOG_DATA) public data: any) {}
    ngOnInit() {
        this.formModel.tag_id = this.data;
        if (this.formModel.tag_id > 0) {
            this._orderService.loadTagsDetails(this.formModel.tag_id).subscribe(data => {
                this.response = data;
                if (this.formModel.tag_id > 0) {
                    this.formModel.tag_id = this.response.api_status[0].id;
                    this.formModel.tag_name = this.response.api_status[0].tag_name;
                    this.formModel.color_code = this.response.api_status[0].color_code;
                } else {
                    this.formModel.tag_id = 0;
                }
            }, err => console.log(err), function() {
                //completed callback
            });
        }
    }
    addEditTags(form: any) {
        this.errorMsg = '';
        var data: any = {};
        data.website_id = this._globalService.getWebsiteId();
        if (this.formModel.tag_id > 0) {
            data.id = this.formModel.tag_id;
        }
        data.tag_name = this.formModel.tag_name;
        data.color_code = this.formModel.color_code;
        this._orderService.tagAddEdit(data, this.formModel.tag_id).subscribe(data => {
            this.response = data;
            if (this.response.status == 1) {
                this.closeDialog();
                //this._router.navigate(['/brand/reload']);
            } else {
                this.errorMsg = this.response.message;
            }
        }, err => console.log(err), function() {
            //completed callback
        });
    }
    closeDialog() {
        this.dialogRef.close();
    }
}

@Component({
    templateUrl: './templates/product_list.html',
    providers: [OrderService]
})
export class SelectProductComponent implements OnInit {
    public formModel: any = {};
    public product_list: any = [];
    public response: any;
    public selectedAll: boolean;
    public bulk_ids: any = [];
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
    public config: any = {};
    public customers: any = [];
    public userId: number;
    public orderId:number;
    public webshop_id:any;
    showSkeletonLoaded: boolean = false;
    public temp_result = [];
    public temp_col = [];
    constructor( 
        public _globalService: GlobalService,
        private _orderService: OrderService,
        public dialog: MatDialog,
        private _cookieService: CookieService,
        @Inject(DOCUMENT) private document: any,
        public dialogRef: MatDialogRef<SelectProductComponent>,
        @Optional() @Inject(MAT_DIALOG_DATA) public data: any
    ) {

    }
    ngOnInit() {
        if (this.data) {
            this.webshop_id  = this.data.webshop_id;
            // this.index = this.data.index;
            this.userId = this.data.userId;
            if (this.data.selected_products_ids.length > 0) {
                let selected_products_ids = this.data.selected_products_ids;
                this.bulk_ids = selected_products_ids.split(",").map(Number);
                this.orderId = this.data.orderId;
            }
        }
        this.generateGrid(0, 1, 'id', '', '');
        this._globalService.loadSkeletonChange$.subscribe(
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
    }

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
            "channel_id": this.webshop_id,
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
                this.pagination.total_page = Math.ceil(listData.hits.total / 25);
                this.config.currentPageCount = this.result_list.length
                this.config.currentPage = page
                this.config.itemsPerPage = 25;
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

    generateGrid1(reload: any, page: any, sortBy: any, filter: any, search: any) {
        // search = search.trimLeft();
        if (search == '') {
            this.search_text = '';
        } else {
            this.search_text = search;
        }
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
            "userid": this.userId,
            "search": this.search_text.trim(),
            "order_by": sortBy,
            "order_type": this.sortOrder,
            "website_id": this._globalService.getWebsiteId(),
            "channel_id" : this.webshop_id,
            "show_all": 0
        }
        //this._orderService.productLoad(data, page).subscribe(
        this._orderService.getProducts(data, page).subscribe(
            data => {
                let that = this;
                this.response = data;
                this.total_list = [];
                if (this.response.count > 0) {
                    this.result_list = this.response.results[0].result;
                    // this.result_list = this.response.results[0].products;
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

    closeDialog() {
        this.dialogRef.close(); // pass the selected prodct ids 
    }

    toggleCheckAll(event: any) {
        let that = this;
        that.bulk_ids = [];
        this.selectedAll = event.checked;
        this.result_list.forEach(function (item: any) {
            item.Selected = event.checked;
            if (item.Selected) {
                that.bulk_ids.push(item.id);
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
                } else {
                    var index = that.bulk_ids.indexOf(item.id);
                    that.bulk_ids.splice(index, 1);
                }
            }
        });
    }

    applyChanges() {
        let returnData: any = [];
        //returnData['index'] = this.data.index;
        let product_ids: string = '';
        let product_names: string = '';
        let products: any = [];
        product_ids = this.bulk_ids.join(',');
        let that = this;
        this.bulk_ids.forEach(function(item: any) {
            that.product_list.forEach(function(inner_item: any) {
                if (item == inner_item.id) {
                    products.push(inner_item.sku);
                }
            });
        });
        product_names = products.join(',');
        returnData['product_ids'] = product_ids;
        this.dialogRef.close(returnData);
    }
}

@Component({
    templateUrl: './templates/view_order.html',
    providers: [OrderService],
    animations: [AddEditTransition],
    host: {
        '[@AddEditTransition]': ''
    },
})
export class ViewOrderComponent implements OnInit {
    public response: any;
    public errorMsg: string='dsfdsfs';
    public successMsg: string;
    public formModel: any = {};
    private sub: any;
    public tabIndex: number;
    public parentId: number = 0;
    public add_edit: any = '';
    public channel_list: any = [];
    public payment_method_list: any = [];
    public billing_country_list: any = [];
    public billing_state_list: any = [];
    public shipping_country_list: any = [];
    public shipping_state_list: any = [];
    public customer_list: any = [];
    public selected_products_ids: any = [];
    public cart_list: any = [];
    public orderDetails: any = {};
    public quantitiesArr: any = {};
    public orderData:any = {};
    public selected_coupon_code :string = '';
    public taxSettings:any;
    public ipaddress: any;
    public orderInfo:any = {};
    public is_return: boolean = false;
    public activitySettings:boolean=false
    constructor(
        private _orderService: OrderService,
        public _globalService: GlobalService,
        private _router: Router,
        private _route: ActivatedRoute,
        private _cookieService: CookieService,
        public dialog: MatDialog,
        private global:Global
    ) {
        this.ipaddress = _globalService.getCookie('ipaddress')
        let website_id = this._globalService.getWebsiteId();
        this.loadTaxSettings(website_id);
    }

    ngOnInit() {
        this.tabIndex = +this._globalService.getCookie('active_tabs');
        this.parentId = this._globalService.getParentTab(this.tabIndex);
        let website_id = this._globalService.getWebsiteId();
        this.formModel.created_date = new Date();
        this.formModel.payment_date = new Date();
        this.formModel.currencyCode = '$';
        this.sub = this._route.params.subscribe(params => {
          this.formModel.id = +params['id']; // (+) converts string 'id' to a number
        });
        this.orderInfo = { orderId: this.formModel.id, activityType : 1}
        let userData = this._cookieService.getObject('userData');
        let dateFormat = userData["gl_date_format"].replace(/%/g,"");
        this.global.getWebServiceData('view-order','GET','',this.formModel.id).subscribe(order => {
            if(order["status"] == '1') {
                this.orderData = order["data"];
                if(this.orderData.order_status == 4) {
                   this.is_return = true;
                }
                this.getCurrencyDetails(this.orderData.currency_code);
            } else {
                this._globalService.showToast("Something went wrong. Please try later.");
            }
        }, err => {

        })
    }

    loadTaxSettings(website_id) {
     this.global.getTaxSettings(website_id).subscribe(result => {
          if(result["status"] == 1) {
              this.taxSettings = result["api_status"];
              // console.log(this.taxSettings);
            }
        } , err => {

        });
     }

    getCurrencyDetails(currencyCode) {
        if(currencyCode == '' || currencyCode == null) {
            currencyCode = 'INR';
        }
        let data:any = {};
        data.currency_code = currencyCode;
        this.global.getWebServiceData('currency-by-code','POST',data,'').subscribe(result => {
            if(result["status"] == 1) {
                this.formModel.currency = result["data"]["id"]+'SSS'+result["data"]["currencysymbol"];
                this.currencySettings(this.formModel.currency);
            } else { // show error message
                this._globalService.showToast(result["message"]);
            }
        }, err => {
        });
    }

    currencySettings(currencyData:any) {
        const currencyArr = currencyData.split("SSS"); // string contains 'SSS'
        this.formModel.currency_id = currencyArr[0];
        this.formModel.currencyCode = currencyArr[1];
    }

    // edit GRN  edit_grn_pop added here 
    dialogRefReturnOrder: MatDialogRef <ReturnOrderComponent > | null;
    order_return_pop(order_id: any, custom_order_id:any) {
        this.dialogRefReturnOrder = this.dialog.open(ReturnOrderComponent, {
            data: {"order_id":order_id, "custom_order_id":custom_order_id},
            disableClose: false
        });
        this.dialogRefReturnOrder.afterClosed().subscribe(result => {
            
        });
    }

    showActivityPanel(show: boolean) {
        this.activitySettings = !show;
    }
}

@Component({
    templateUrl: './templates/order_return_pop.html',
    providers: [OrderService, Global],
})
export class ReturnOrderComponent implements OnInit {
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
    public custom_order_id: string;
    constructor( 
        private _orderService: OrderService,
        public _globalService: GlobalService,
        private _router: Router,
        private _route: ActivatedRoute,
        private _cookieService: CookieService,
        public dialogRef: MatDialogRef<ReturnOrderComponent>,
        public dialog: MatDialog,
        public dialogsService: DialogsService,
        @Inject(DOCUMENT) private document: any,
        @Optional()@ Inject(MAT_DIALOG_DATA) public data: any
    ) {
        
    }

    ngOnInit() {
        this.tabIndex = +this._globalService.getCookie('active_tabs');
        this.parentId = this._globalService.getParentTab(this.tabIndex);
        this.custom_order_id = this.data.custom_order_id;
        this.order_id  = this.data.order_id;
        this.get_return_pop(this.order_id);
    }

    get_return_pop(order_id) {
        let data: any = {};
        data.order_id = order_id;
        data.website_id = this._globalService.getWebsiteId();
    }
    
    saveReturnType() {
        let return_order_type = this.formModel.return_order_type
        let data: any = {};
        this.dialogRef.close(data);
        this._globalService.addTab('Refund Orders','return/refund_orders/'+this.order_id+'/'+return_order_type,'Refund Orders',12145)
        this._router.navigate(['/return/refund_orders/'+this.order_id+'/'+return_order_type]);
    }
}

@Component({
    templateUrl: './templates/activity.html',
    selector : 'order-activity',
    providers: [OrderService],
})
export class OrderActivityComponent implements OnInit {
    @Input() orderInfo: { orderId:number, activityType:any };
    public formModel: any = {};
    private sub: any;
    public tabIndex: number;
    public parentId: number = 0;
    public order_activity:any = [];
    public orderId:any ;   
    constructor(
        private _orderService: OrderService,
        public _globalService: GlobalService,
        private _cookieService: CookieService,
        private global: Global,
        @Inject(DOCUMENT) private document: any
    ) {
    }
    ngOnInit() {
        let orderId = +this.orderInfo.orderId;
        if(orderId) {
            this._orderService.getOrderActivity(orderId).subscribe(
                response => {
                    if (response["status"] == '1') {
                        this.order_activity = response["api_status"];
                    }
                }, err => {

                }
            );
        }
    }

    postActivity() {
        let userData = this._cookieService.getObject('userData');
        let orderId = +this.orderInfo.orderId;
        let activity_msg = '';
        if(this.formModel.activity_msg) {
            activity_msg = this.formModel.activity_msg.trim();
        }
        if (orderId > 0 && activity_msg != '') {
            let data: any = {};
            data.user_id = userData['uid'];
            data.activity_comments = activity_msg;
            data.activity_type = this.orderInfo.activityType;
            data.username = userData['first_name'] + ' ' + userData['last_name'];
            data.order_id = orderId;
            data.status = 0;
            this.global.getWebServiceData('post_activity', 'POST', data, '').subscribe(res => {
                if (res["status"] == '1') {
                    this.ngOnInit();
                    this.formModel.activity_msg = ''; // reset the activity fields
                }
            }, err => {

            })
        }
    }

    postOrderActivities(event) {
        if (event.keyCode == 13) {
            this.postActivity();
        }
    }
}