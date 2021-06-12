import {Component,OnInit,Inject} from '@angular/core';
import { Router,ActivatedRoute } from '@angular/router';
import { GlobalService } from '../../global/service/app.global.service';
import {CookieService} from 'ngx-cookie';
import {PaginationInstance} from 'ngx-pagination';
import {DOCUMENT} from '@angular/platform-browser';
import { MatDialog,MatDialogRef,MAT_DIALOG_DATA } from '@angular/material';
import {DialogsService} from '../../global/dialog/confirm-dialog.service';
import {PurchaseOrderService} from './inventory.purchase-order.service';
import { OrderService } from '../../order/order/order.order.service';
@Component({
  templateUrl: 'templates/add_purchase_order.html',
  providers: [PurchaseOrderService, OrderService]
})
export class PurchaseOrderAddEditComponent implements OnInit {
    public tabIndex: number;
    public parentId: number = 0;
    public formModel: any = {};
    public errorMsg: string = '';
    public supplier_list: any = [];
    public currency_list: any = [];
    public supplier_currency: any = {};
    public minDate: any;
    private sub: any;
    public product_list: any = [];

    public warehouse_list: any = [];
    public payment_list: any = [];
    public shipping_list: any = [];
    public selected_warehouse: any = {};
    public temp_total_amt: any = 0;

    public old_supplier_id: number = 0;
    public productsList: any = [];
    public selected_products_ids: any = '' ;
    public cart_list: any = [];
    public productPriceArr: any = {};
    public quantitiesArr: any = {};
    public selected_coupon_code :string = '';
    public orderData:any = {};
    public orderDetails: any = {};
    public itemDetailsArr:any=[];
    constructor(public _globalService: GlobalService,
        private _cookieService: CookieService,
        private _purchaseOrderService: PurchaseOrderService,
        private _router: Router,
        private _route: ActivatedRoute,
        public dialog: MatDialog,
        private _orderService: OrderService,
        public dialogsService: DialogsService,
        @Inject(DOCUMENT) private document: any) {
        this.tabIndex = +_globalService.getCookie('active_tabs');
        this.parentId = _globalService.getParentTab(this.tabIndex);
    }

    ngOnInit() {
        this.sub = this._route.params.subscribe(params => { // pick id from the route url
            this.formModel.id = +params['id']; // (+) converts string 'id' to a number
        });
        this.formModel.shipping_cost = (0).toFixed(2)
        this.formModel['products'] = [];
        this._purchaseOrderService.purchaseOrderLoad(this.formModel.id).subscribe(
            data => {
                this.supplier_list = data.Suppliers;
                this.currency_list = data.currency;

                this.formModel.supplier_id = data.Suppliers[0].id; // Assign default supplier 
                this.formModel.warehouse_id = data.warehouse[0].id; // Assign default warehouse
                this.formModel.currency_id = data.currency[0].id; // Assign default currency
                this.formModel.purchase_order_shipping_id = data.PurchaseOrders_shipping_method[0].id; // Assign default po shipping method
                this.formModel.purchase_order_payment_id = data.PurchaseOrders_payment_method[0].id; // Assign default payment method
                this.formModel.shipping_cost_stats = "i";

                this.minDate = new Date();
                this.warehouse_list = data.warehouse;
                this.payment_list = data.PurchaseOrders_payment_method;
                this.shipping_list = data.PurchaseOrders_shipping_method;
                if (this.formModel.id > 0) {
                    this.formModel = data.purchase_order_list[0];
                    this.formModel['products'] = data.purchase_order_products;
                    this.currencyDetails();
                    this.getWarehouseDetails(this.formModel.warehouse_id);
                    let request_data: any = {};
                    request_data['order_by'] = 'id';
                    request_data['order_type'] = '+';
                    request_data['search'] = '';
                    this._purchaseOrderService.getProducts(this.formModel.supplier_id, request_data, 'all').subscribe(
                        data => {
                            this.product_list = data.product;
                            let that = this;
                            this.formModel.products.forEach(function(item: any, index: number) {
                                that.product_list.forEach(function(inner_item: any) {
                                    if (item.product_id == inner_item.id) {
                                        item['sku'] = inner_item.sku;
                                        item['name'] = inner_item.name;
                                    }
                                });
                                that.calcAmt(index);
                            });
                        },
                        err => {
                            this._globalService.showToast('Something went wrong. Please try again.');
                        },
                        function() {
                            //completed callback
                        }
                    );
                } else {
                    this.formModel['order_date'] = new Date();
                    this.formModel['purchase_order_id'] = data.purchase_order_id;
                    this.getSupplierProducts(this.formModel.supplier_id)
                }
            },
            err => console.log(err),
            function() {
                //completed callback
            }
        );
    }

    getSupplierProducts(supplier_id: any) {
        // check default supplier currency
        let that = this;
        that.formModel.currency_id = 0;

        if (this.formModel['products'].length > 0 && this.formModel['products'][0]['product_id'] > 0) {
            this.dialogsService.confirm('Warning', 'Do you really want to change supplier ? All the selected products in your bucket will be removed.').subscribe(res => {
                if (res) {
                    this.formModel['products'] = [{
                        'quantity': 1,
                        'price': 0.00,
                        'discount': 0.00,
                        'net_amt': 0.00,
                        'gross_amt': 0.00
                    }];
                } else {
                    this.formModel.supplier_id = this.old_supplier_id;
                }
                this.supplier_list.forEach(function(item: any) {
                    if (item.id == that.formModel.supplier_id) {
                        that.formModel.currency_id = item.currency_id;
                        that.currencyDetails();
                    }
                });

                this.old_supplier_id = this.formModel.supplier_id;
            });
        } else {
            this.supplier_list.forEach(function(item: any) {
                if (item.id == supplier_id) {
                    that.formModel.currency_id = item.currency_id;
                    that.currencyDetails();
                }
            });

            this.old_supplier_id = this.formModel.supplier_id;
        }

    }

    // get currency details
    currencyDetails() {
        let that = this;
        this.currency_list.forEach(function(item: any) {
            if (item.id == that.formModel.currency_id) {
                that.supplier_currency = item;
            }
        });

    }

    // get warehouse details
    getWarehouseDetails(warehouse_id: number) {

        let that = this;
        this.warehouse_list.forEach(function(item: any) {
            if (item.id == warehouse_id) {
                that.selected_warehouse = item;
            }
        });

    }


    // Remove a row by index
    removeRow(index: number) {
        this.formModel.products.splice(index, 1);
        this.calcAmt(0);
    }

    // calculate amount on quantity, cpu and discount change
    calcAmt(index: number) {

        //calculate gross amount
        this.formModel.products[index]['quantity'] = (isNaN(this.formModel.products[index]['quantity']) ? 0 : this.formModel.products[index]['quantity']);
        this.formModel.products[index]['price'] = (isNaN(this.formModel.products[index]['price']) ? 0 : this.formModel.products[index]['price']);
        this.formModel.products[index]['gross_amt'] = (this.formModel.products[index]['quantity'] * this.formModel.products[index]['price']).toFixed(2);

        // calculate discount amount
        this.formModel.products[index]['discount'] = (isNaN(this.formModel.products[index]['discount']) ? 0 : this.formModel.products[index]['discount']);
        this.formModel.products[index]['discount_amount'] = (this.formModel.products[index]['gross_amt'] * (this.formModel.products[index]['discount'] / 100)).toFixed(2);

        //calculate net amount
        this.formModel.products[index]['net_amt'] = (this.formModel.products[index]['gross_amt'] - this.formModel.products[index]['discount_amount']).toFixed(2);

        let that = this;
        //calculate total gross amount

        this.formModel['gross_amount'] = 0.00;
        this.formModel.products.forEach(function(item: any) {
            that.formModel.gross_amount = (parseFloat(that.formModel.gross_amount) + parseFloat(item.gross_amt)).toFixed(2);
        });

        //calculate total discount amount

        this.formModel['discount_amount'] = 0.00;
        this.formModel.products.forEach(function(item: any) {
            that.formModel.discount_amount = (parseFloat(that.formModel.discount_amount) + parseFloat(item.discount_amount)).toFixed(2);
        });

        //calculate total net amount

        this.formModel['net_amount'] = 0.00;
        this.formModel.products.forEach(function(item: any) {
            that.formModel.net_amount = (parseFloat(that.formModel.net_amount) + parseFloat(item.net_amt)).toFixed(2);
        });



        this.temp_total_amt = 0;
        this.temp_total_amt += this.formModel.net_amount;

        // calculate total net amount based on shiping option status
        this.formModel.shipping_cost = (this.formModel.shipping_cost == '' || isNaN(this.formModel.shipping_cost)) ? (0).toFixed(2) : parseFloat(this.formModel.shipping_cost).toFixed(2);
        if (this.formModel.shipping_cost_stats == 'e') {
            this.temp_total_amt = parseFloat(this.temp_total_amt) + parseFloat(this.formModel.shipping_cost);
        }

        //calculate total net amount based on tax amount
        this.formModel.purchase_order_tax = (this.formModel.purchase_order_tax == '' || isNaN(this.formModel.purchase_order_tax)) ? (0).toFixed(2) : parseFloat(this.formModel.purchase_order_tax).toFixed(2);
        this.temp_total_amt = parseFloat(this.temp_total_amt) + parseFloat(this.formModel.purchase_order_tax);

        //calculate total net amount based on discount amount
        // this.formModel.discount_amount = (this.formModel.discount_amount=='' || isNaN(this.formModel.discount_amount))?(0).toFixed(2):parseFloat(this.formModel.discount_amount).toFixed(2);
        // this.temp_total_amt = parseFloat(this.temp_total_amt) - parseFloat(this.formModel.discount_amount);

        this.temp_total_amt = (this.temp_total_amt).toFixed(2);

    }

    dialogProductRef: MatDialogRef < SupplierProductsComponent > | null;
    openProductPop(index: number) {

        if (this.formModel.supplier_id > 0) {
            let data: any = {};
            data['index'] = index;
            data['supplier_id'] = this.formModel.supplier_id;

            this.dialogProductRef = this.dialog.open(SupplierProductsComponent, {
                data: data
            });
            this.dialogProductRef.afterClosed().subscribe(result => {
                if (result) {

                    let that = this;
                    result.selected_product.forEach(function(item: any, index: number) {

                        if (index == 0) {

                            that.formModel.products[result['index']]['product_id'] = item.id;
                            that.formModel.products[result['index']]['sku'] = item.sku;
                            that.formModel.products[result['index']]['name'] = item.name;
                            that.formModel.products[result['index']]['price'] = (item.cost_per_unit) ? parseFloat(item.cost_per_unit).toFixed(2) : 0;
                            that.formModel.products[result['index']]['quantity'] = 1;
                            that.formModel.products[result['index']]['net_amt'] = that.formModel.products[result['index']]['price'] * that.formModel.products[result['index']]['quantity'];
                            that.formModel.products[result['index']]['discount'] = (0).toFixed(2);
                            that.formModel.products[result['index']]['discount_amount'] = (0).toFixed(2);
                            that.formModel.products[result['index']]['gross_amt'] = that.formModel.products[result['index']]['net_amt'] - that.formModel.products[result['index']]['discount'];


                        } else {
                            let prod: any = {};
                            prod['product_id'] = item.id;
                            prod['sku'] = item.sku;
                            prod['name'] = item.name;
                            prod['price'] = (item.cost_per_unit) ? parseFloat(item.cost_per_unit).toFixed(2) : 0;
                            prod['quantity'] = 1;
                            prod['net_amt'] = prod['price'] * prod['quantity'];
                            prod['discount'] = (0).toFixed(2);
                            prod['discount_amount'] = (0).toFixed(2);
                            prod['gross_amt'] = prod['net_amt'] - prod['discount'];


                            that.formModel.products.push(prod);
                        }

                        that.calcAmt(index);
                    });

                }
            });
        } else {
            this.dialogsService.alert('Error', 'Select supplier to choose products').subscribe(res => {});
        }

    }


    poCheckout(form: any) {

        if (this.formModel.products.length > 0 && this.formModel.products[0]['product_id'] > 0) {
            this.formModel.net_amount = this.temp_total_amt;

            let data: any = {};

            data['order'] = Object.assign({}, this.formModel);
            if (!data.order.payment_due_date) {
                data.order.payment_due_date = null;
            }
            data['products'] = Object.assign([], this.formModel.products);
            data.order.website_id = 1;
            data.order['ip_address'] = (this._globalService.getCookie('ipaddress')) ? this._globalService.getCookie('ipaddress') : '';
            if (!this.formModel.id) {
                data.order.createdby = this._globalService.getUserId();
            }
            data.order.updatedby = this._globalService.getUserId();

            data.order.shipping_cost_base = this.formModel.shipping_cost;
            data.order.purchase_order_tax_base = this.formModel.purchase_order_tax;
            data.order.gross_amount_base = this.formModel.gross_amount;
            data.order.net_amount_base = this.formModel.net_amount;
            data.order.discount_amount_base = this.formModel.discount_amount;
            data.order.paid_amount = 0;
            data.order.paid_amount_base = 0;

            let that = this;
            that._globalService.showLoaderSpinner(true);

            this._purchaseOrderService.poAddEdit(data, this.formModel.id).subscribe(
                data => {

                    if (data.status == 1) {
                        this._router.navigate(['/purchase_order']);
                        this._globalService.deleteTab(this.tabIndex, this.parentId);
                    } else {
                        this.errorMsg = data.message;
                    }
                },
                err => {
                    this._globalService.showToast('Something went wrong. Please try again.');
                    that._globalService.showLoaderSpinner(false);
                },
                function() {
                    //completed callback
                    that._globalService.showLoaderSpinner(false);
                }
            );
        } else {
            this.dialogsService.alert('Error', 'Select atleast one product').subscribe(res => {});
        }


    }

    //SEARC/SCAN ITEM
    getProductDetails(sku:string,event) {
        if (event.keyCode != 13 && event.keyCode != 38 && event.keyCode != 40) {
            let filterValue: string = '';
            filterValue = sku;
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
                conditions = {}
                conditions.query = "*" + filterValue + "*";
                innerMatch = {};
                innerMatch.query_string = conditions;
                matchArr.push(innerMatch);
            }

            let userData = this._cookieService.getObject('userData');
            let extraFilter = JSON.stringify(matchArr);
            let elasticData = '{"query":{"bool":{"must":' + extraFilter + '}}}';
            this._orderService.getProductsES(elasticData, websiteId).subscribe(
                listData => {
                    let tmpResult = [];
                    listData.hits.hits.forEach(function (rows: any) {
                        tmpResult.push(rows._source);
                    });

                    if (tmpResult.length > 0) {
                        this.productsList = tmpResult;
                        if (userData['elastic_host'] == '50.16.162.98') {  // this is for new elsatic server
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
    }

    displayFnCustomer(obj: any) {
        return obj ? obj.first_name : obj;
    }
    displayFnSKU(obj: any) {
        //return obj ? obj.sku : obj;
    }

    UpdateItems(itemDetails :any) {
        this.formModel.sku=null;
        if (this.formModel.warehouse_id == undefined || this.formModel.warehouse_id <= 0) {
            this._globalService.showToast("Please select a warehousr.");
            window.scrollTo(0, 0);
            return false;
        }else{
            let details={
                'product_id': itemDetails.id,
                'sku': itemDetails.sku,
                'name': itemDetails.name,
                'cost_per_unit': itemDetails.cost_per_unit,
                'quantity': 1,
                'discount': (0).toFixed(2),
                'price': (itemDetails.cost_per_unit) ? parseFloat(itemDetails.cost_per_unit).toFixed(2) : 0,
                'net_amt': 0,
                'discount_amount':(0).toFixed(2),
                'gross_amt': 0
            }
            this.formModel.products.splice(this.formModel.products.length,0,details);
            this.formModel.sku=null;
        }   
    }
}

@Component({
    templateUrl: './templates/supplier_product.html',
    providers: [PurchaseOrderService]
})
export class SupplierProductsComponent implements OnInit {
    public products_list: any = [];
    public search_text: string;
    public sortBy: any = '';
    public sortOrder: any = '';
    public sortClass: any = '';
    public sortRev: boolean = false;
    public product_spec: string = 'exclusive';
    constructor(
        public _globalService: GlobalService,
        private _purchaseOrderService: PurchaseOrderService,
        public dialog: MatDialog,
        private dialogRef: MatDialogRef < SupplierProductsComponent > , @Inject(MAT_DIALOG_DATA) public data: any
    ) {

    }
    ngOnInit() {
        this.reload('', 'id');
    }
    
    reload(search_key: string, sortBy: string) {
        this.sortBy = sortBy;
        if (sortBy != '' && sortBy != undefined) {
            if (this.sortRev) {
                this.sortOrder = '-';
                this.sortRev = !this.sortRev;
                this.sortClass = 'icon-down';
            } else {
                this.sortOrder = '+';
                this.sortRev = !this.sortRev;
                this.sortClass = 'icon-up';
            }
        } else {
            this.sortBy = 'id';
            this.sortOrder = '+';
            this.sortRev = !this.sortRev;
            this.sortClass = 'icon-up';
        }

        let request_data: any = {};
        request_data['order_by'] = this.sortBy;
        request_data['order_type'] = this.sortOrder;
        if (search_key.trim() != '') {
            request_data['search'] = search_key;
        } else {
            request_data['search'] = '';
            this.search_text = '';
        }

        if (this.data.supplier_id > 0) {
            this._purchaseOrderService.getProducts(this.data.supplier_id, request_data, this.product_spec).subscribe(
                data => {
                    if (this.product_spec == 'exclusive') {
                        this.products_list = data.Suppliers_products;
                    } else {
                        this.products_list = data.product;
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

    closeDialog() {
        this.dialogRef.close();
    }

    ////////////////////////////Check/Uncheck//////////////

    toggleCheck(id: any, event: any) {

        let that = this;
        this.products_list.forEach(function(item: any) {
            if (item.id == id) {
                item.selected = event.checked;
            }
        });
    }

    selectProduct() {

        let returnData: any = [];
        returnData['index'] = this.data.index;
        returnData['selected_product'] = [];

        let product_ids: string = '';
        let product_names: string = '';
        let products: any = [];

        let that = this;
        this.products_list.forEach(function(item: any) {
            if (item.selected) {
                returnData['selected_product'].push({
                    'id': item.id,
                    'sku': item.sku,
                    'name': item.name,
                    'cost_per_unit': item.cost_per_unit
                });
                item.selected = false;
            }
        });

        this.dialogRef.close(returnData);
    }

    changeProductSpec() {

        this.reload('', '');
    }
}

@Component({
    templateUrl: './templates/purchase_order_view.html',
    providers: [PurchaseOrderService]
})
export class PurchaseOrderViewComponent implements OnInit {
    public tabIndex: number;
    public parentId: number = 0;
    public purchase_order: any = {};
    public warehouse_list: any = [];
    public supplier_list: any = [];
    public payment_list: any = [];
    public shipping_list: any = [];
    public currency_list: any = [];
    public supplier_currency: any = {};
    public selected_warehouse: any = {};
    public selected_supplier: any = {};
    public selected_ship: any = {};
    public selected_payment: any = {};
    public sub: any;
    public purchase_order_id: number = 0;
    constructor(
        public _globalService: GlobalService,
        private _purchaseOrderService: PurchaseOrderService,
        private _cookieService: CookieService,
        private _router: Router,
        private _route: ActivatedRoute,
    ) {
        this.tabIndex = +_globalService.getCookie('active_tabs');
        this.parentId = _globalService.getParentId(this.tabIndex);
    }

    ngOnInit() {
        this.sub = this._route.params.subscribe(params => { // pick id from the route url
            this.purchase_order_id = +params['id']; // (+) converts string 'id' to a number
        });
        this._purchaseOrderService.purchaseOrderView(this.purchase_order_id).subscribe(
            data => {
                if (this.purchase_order_id) {
                    this.purchase_order = data.purchase_order_list[0];
                    this.purchase_order['products'] = [];
                    this.purchase_order['products'] = data.purchase_order_products;
                    let that = this;
                    this.purchase_order['products'].forEach(function(item: any) {
                        item['sku'] = item.product.sku;
                        item['name'] = item.product.name;
                        if (item['total_qty'] >= 0) {
                            item['received_quantity'] = (item['quantity']) ? item['quantity'] : 0;
                            item['quantity'] = item['total_qty'];
                        } else {
                            item['received_quantity'] = 0;
                        }
                        //calculate gross amount
                        item['gross_amt'] = (item['quantity'] * item['price']).toFixed(2);
                        //calculate net amount
                        item['net_amt'] = (item['gross_amt'] - item['discount_amount']).toFixed(2);
                        item['damaged_quantity'] = (item['damage']) ? item['damage'] : 0;
                        item['shortage_quantity'] = (item['shortage']) ? item['shortage'] : 0;
                        item['remaining_quantity'] = item['quantity'] - (item['received_quantity'] + item['damaged_quantity'] + item['shortage_quantity']);
                    });
                } else {
                    this.purchase_order = this._cookieService.getObject('purchaseOrder');
                }
                this.warehouse_list = data.warehouse;
                this.supplier_list = data.Suppliers;
                this.payment_list = data.PurchaseOrders_payment_method;
                this.shipping_list = data.PurchaseOrders_shipping_method;
                this.currency_list = data.currency;
                let that = this;
                this.currency_list.forEach(function(item: any) {
                    if (item.id == that.purchase_order.currency_id) {
                        that.supplier_currency = item;
                    }
                });
                this.warehouse_list.forEach(function(item: any) {
                    if (item.id == that.purchase_order.warehouse_id) {
                        that.selected_warehouse = item;
                    }
                });
                this.supplier_list.forEach(function(item: any) {
                    if (item.id == that.purchase_order.supplier_id) {
                        that.selected_supplier = item;
                    }
                });
                this.shipping_list.forEach(function(item: any) {
                    if (item.id == that.purchase_order.purchase_order_shipping_id) {
                        that.selected_ship = item;
                    }
                });

                this.payment_list.forEach(function(item: any) {
                    if (item.id == that.purchase_order.purchase_order_payment_id) {
                        that.selected_payment = item;
                    }
                });

                this.purchase_order['received_date'] = data.received_date;
                this.purchase_order['received_id'] = data.received_purchaseorder_id;
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
    templateUrl: './templates/po_grn.html',
    providers: [PurchaseOrderService]
})
export class PurchaseOrderGrnComponent implements OnInit {
    public tabIndex: number;
    public parentId: number = 0;
    public errorMsg: string;
    public purchase_order: any = {};
    public warehouse_list: any = [];
    public supplier_list: any = [];
    public payment_list: any = [];
    public shipping_list: any = [];
    public currency_list: any = [];
    public supplier_currency: any = {};
    public selected_warehouse: any = {};
    public selected_supplier: any = {};
    public selected_ship: any = {};
    public selected_payment: any = {};
    public sub: any;
    public purchase_order_id: number = 0;
    public received_purchaseorder_master_id: number = 0;
    public custom_po_id :any = {};
    public formModel:any={};
    public poItemsIds:any=[];
    constructor(
        public _globalService: GlobalService,
        private _purchaseOrderService: PurchaseOrderService,
        private _cookieService: CookieService,
        private _router: Router,
        private _route: ActivatedRoute,
        public dialog: MatDialog,
    ) {
        this.tabIndex = +_globalService.getCookie('active_tabs');
        this.parentId = _globalService.getParentId(this.tabIndex);
    }

    ngOnInit() {
        this.sub = this._route.params.subscribe(params => { // pick id from the route url
            this.purchase_order_id = +params['id']; // (+) converts string 'id' to a number
        });

        this._purchaseOrderService.purchaseOrderLoad(this.purchase_order_id).subscribe(
            data => {

                if (this.purchase_order_id) {
                    this.purchase_order = data.purchase_order_list[0];
                    this.received_purchaseorder_master_id = data.received_purchaseorder_master_id;
                    this.custom_po_id = this.purchase_order_id;
                    this.purchase_order['products'] = [];
                    this.purchase_order['products'] = data.purchase_order_products;
                    let that = this;
                    this.purchase_order['products'].forEach(function(item: any) {
                        that.poItemsIds.push(item.product.id);
                        item['product_id'] = item.product.id;
                        item['sku'] = item.product.sku;
                        item['name'] = item.product.name;

                        if (item['total_qty'] >= 0) {
                            item['received_quantity'] = (item['quantity']) ? item['quantity'] : 0;
                            item['quantity'] = item['total_qty'];
                        } else {
                            item['received_quantity'] = 0;
                        }

                        //calculate gross amount
                        item['gross_amt'] = (item['quantity'] * item['price']).toFixed(2);

                        //calculate net amount
                        item['net_amt'] = (item['gross_amt'] - item['discount_amount']).toFixed(2);

                        item['damaged_quantity'] = (item['damage']) ? item['damage'] : 0;
                        item['shortage_quantity'] = (item['shortage']) ? item['shortage'] : 0;
                        item['remaining_quantity'] = item['quantity'] - (item['received_quantity'] + item['damaged_quantity'] + item['shortage_quantity']);

                        if(item['PO_receive_pro_details'].length > 0) {
                            item['expiry_date'] = item['PO_receive_pro_details'][0]['expiry_date'];
                        }
                        if(item['PO_receive_pro_details'].length > 0) {
                            item['batchNo'] = item['PO_receive_pro_details'][0]['lot_no'];
                        }
                        let quantityDetails:any  = [];
                        let childItem:any = {};
                        childItem.receivedQuanity = item["received_quantity"];
                        childItem.expiry_date = item['expiry_date']
                        childItem.batchNo = item['batchNo']
                        childItem.checked = true;
                        quantityDetails.push(childItem);
                        item["quantityDetails"] = quantityDetails;
                    });
                } else {
                    this.purchase_order = this._cookieService.getObject('purchaseOrder');
                }
                this.warehouse_list = data.warehouse;
                this.supplier_list = data.Suppliers;
                this.payment_list = data.PurchaseOrders_payment_method;
                this.shipping_list = data.PurchaseOrders_shipping_method;
                this.currency_list = data.currency;
                let that = this;
                this.currency_list.forEach(function(item: any) {
                    if (item.id == that.purchase_order.currency_id) {
                        that.supplier_currency = item;
                    }
                });
                this.warehouse_list.forEach(function(item: any) {
                    if (item.id == that.purchase_order.warehouse_id) {
                        that.selected_warehouse = item;
                    }
                });
                this.supplier_list.forEach(function(item: any) {
                    if (item.id == that.purchase_order.supplier_id) {
                        that.selected_supplier = item;
                    }
                });
                this.shipping_list.forEach(function(item: any) {
                    if (item.id == that.purchase_order.purchase_order_shipping_id) {
                        that.selected_ship = item;
                    }
                });

                this.payment_list.forEach(function(item: any) {
                    if (item.id == that.purchase_order.purchase_order_payment_id) {
                        that.selected_payment = item;
                    }
                });

                this.purchase_order['received_date'] = data.received_date;
                this.purchase_order['received_id'] = data.received_purchaseorder_id;
            },
            err => {
                this._globalService.showToast('Something went wrong. Please try again.');
            },
            function() {
                //completed callback
            }
        );
    }

    calcQty_old(index: number, type: number) {
        this.purchase_order.products[index].remaining_quantity = this.purchase_order.products[index].quantity - (this.purchase_order.products[index].received_quantity + this.purchase_order.products[index].damaged_quantity + this.purchase_order.products[index].shortage_quantity);        
        if (type == 1) { // Received Quantity

            if (this.purchase_order.products[index].remaining_quantity < 0) {
                this._globalService.showToast('Received Quantity must be smaller than Remaining quantity of product - ' + this.purchase_order.products[index]['name']);
                this.purchase_order.products[index].received_quantity = this.purchase_order.products[index].quantity - (this.purchase_order.products[index].damaged_quantity + this.purchase_order.products[index].shortage_quantity);
            }
        } else if (type == 2) { // Damaged Quantity
            if (this.purchase_order.products[index].remaining_quantity < 0) {
                this._globalService.showToast('Damaged Quantity must be smaller than Remaining quantity of product - ' + this.purchase_order.products[index]['name']);
                this.purchase_order.products[index].damaged_quantity = this.purchase_order.products[index].quantity - (this.purchase_order.products[index].received_quantity + this.purchase_order.products[index].shortage_quantity);
            }
        } else if (type == 3) { // Shotage Quantity
            if (this.purchase_order.products[index].remaining_quantity < 0) {
                this._globalService.showToast('Shortage Quantity must be smaller than Remaining quantity of product - ' + this.purchase_order.products[index]['name']);
                this.purchase_order.products[index].shortage_quantity = this.purchase_order.products[index].quantity - (this.purchase_order.products[index].received_quantity + this.purchase_order.products[index].damaged_quantity);
            }
        }

        this.purchase_order.products[index].remaining_quantity = this.purchase_order.products[index].quantity - (this.purchase_order.products[index].received_quantity + this.purchase_order.products[index].damaged_quantity + this.purchase_order.products[index].shortage_quantity);

    }

    addMoreBatches(index,itemIndex) {
        let remainsqty = this.purchase_order.products[index].remaining_quantity;
        if(remainsqty > 0) {
            let that = this;
            this.purchase_order['products'].forEach(function(item: any,key:any) {
                if(index ==  key) {
                    let childItems:any = {};
                    childItems.receivedQuanity = remainsqty;
                    childItems.expiry_date = "";//item['expiry_date'];
                    childItems.batchNo = "";//item['batchNo'];
                    childItems.checked = false;
                    // item["quantityDetails"].push(childItems);
                    const temp = Object.assign([], item["quantityDetails"]);
                    item['quantityDetails'] = [];
                    temp.forEach((element) => {
                        item['quantityDetails'].push(Object.assign({}, element));
                    })
                    item['quantityDetails'].push(Object.assign({}, childItems));
                    item["quantityDetails"].forEach(function(itemInfor:any,arrKey:any) {
                        if((arrKey+1) == item["quantityDetails"].length) {
                            itemInfor.checked = true;
                        } else {
                            itemInfor.checked = false;
                        }
                    })
                }
            });

            that.calcQty(index,1); // 1 for recevied Quantity  
        } else {
            this._globalService.showToast('All Quantity for this Item is received.');
        }
    }

    removeBatch(index,itemIndex) {
        if(this.purchase_order.products[index].quantityDetails.length > 0) {
            let that = this;
            this.purchase_order.products[index].quantityDetails.forEach(function(childItems:any,key:any) {
                if(itemIndex == key) {
                   that.purchase_order.products[index].quantityDetails.splice(itemIndex, 1);
                }
            })
            this.calcQty(index,1); // 1 for recevied Quantity
        }
    }

    ActivateRowItems(index,itemIndex,entities: any) {
        entities.forEach(function(childItems:any,key:any) {
        if (itemIndex != key) 
          childItems.checked = false;
        });
    }


    calcQty(index: number, type: number) {
        this.purchase_order.products[index].received_quantity = this.getReceivecQuantity(index); 
        this.purchase_order.products[index].remaining_quantity = this.purchase_order.products[index].quantity - (this.purchase_order.products[index].received_quantity + this.purchase_order.products[index].damaged_quantity + this.purchase_order.products[index].shortage_quantity);        
        if (type == 1) { // Received Quantity
            if (this.purchase_order.products[index].remaining_quantity < 0) {
                this._globalService.showToast('Received Quantity must be smaller than Remaining quantity of product - ' + this.purchase_order.products[index]['name']);
                this.purchase_order.products[index].received_quantity = this.purchase_order.products[index].quantity - (this.purchase_order.products[index].damaged_quantity + this.purchase_order.products[index].shortage_quantity);
            }
        } else if (type == 2) { // Damaged Quantity
            if (this.purchase_order.products[index].remaining_quantity < 0) {
                this._globalService.showToast('Damaged Quantity must be smaller than Remaining quantity of product - ' + this.purchase_order.products[index]['name']);
                this.purchase_order.products[index].damaged_quantity = this.purchase_order.products[index].quantity - (this.purchase_order.products[index].received_quantity + this.purchase_order.products[index].shortage_quantity);
            }
        } else if (type == 3) { // Shotage Quantity
            if (this.purchase_order.products[index].remaining_quantity < 0) {
                this._globalService.showToast('Shortage Quantity must be smaller than Remaining quantity of product - ' + this.purchase_order.products[index]['name']);
                this.purchase_order.products[index].shortage_quantity = this.purchase_order.products[index].quantity - (this.purchase_order.products[index].received_quantity + this.purchase_order.products[index].damaged_quantity);
            }
        }
        this.purchase_order.products[index].remaining_quantity = this.purchase_order.products[index].quantity - (this.purchase_order.products[index].received_quantity + this.purchase_order.products[index].damaged_quantity + this.purchase_order.products[index].shortage_quantity);
        if(this.purchase_order.products[index].remaining_quantity == 0) {
            this.purchase_order.products[index].selected = true;
        } else {
            this.purchase_order.products[index].selected = false;
        }

    }

    getReceivecQuantity(index) {
        let quantity:number  = 0;
        if(this.purchase_order.products[index].quantityDetails.length > 0) {
            this.purchase_order.products[index].quantityDetails.forEach(function(ItemDetails:any,key:any) {
                quantity = quantity+ItemDetails["receivedQuanity"];
            })
        }
        return quantity;
    }

    addEditGrn(form: any) {
        let data:any = {};
        const now = Date.now();
        data['purchase_order_id'] = this.purchase_order.id;
        if(this.purchase_order.received_date ! = '') {
            data['received_date'] = this._globalService.convertDate(this.purchase_order.received_date, 'yyyy-MM-dd');
        } else {
            data['received_date'] = this._globalService.convertDate( now , 'yyyy-MM-dd');
        }
        data['warehouse_id'] = this.purchase_order.warehouse_id;
        
        data['product'] = [];
        let remain_flag = 0;
        let that  = this;
        this.purchase_order.products.forEach(function(item:any) {
            
            let prod:any = {};
            prod['product_id'] = item.product_id;
            prod['quantity'] = item.received_quantity;
            prod['price'] = item.price;
            prod['discount'] = item.discount;
            prod['discount_amount'] = item.discount_amount;
            prod['damage'] = item.damaged_quantity;
            if(item.damageReason == undefined) {
                prod['damageReason'] = "";    
            } else {
                prod['damageReason'] = item.damageReason;
            }
            if(item.expiry_date != '') {
                prod['expiry_date'] = that._globalService.convertDate(item.expiry_date, 'yyyy-MM-dd');
            } else {
                prod['expiry_date'] = this._globalService.convertDate( now , 'yyyy-MM-dd');    
            }            
            prod['lot_no'] = item.lot_no;
            prod['shortage'] = item.shortage_quantity;
            prod['total_qty'] = item.quantity;
            if(item['quantityDetails'].length > 0) {
                item['quantityDetails'].forEach(function(item:any){
                    item.expiry_date = that._globalService.convertDate(item.expiry_date, 'yyyy-MM-dd');
                })
            }
            prod['quantityDetails'] = item['quantityDetails'];
            data['product'].push(prod);
            if(item.remaining_quantity > 0 ) {
                remain_flag ++;
            }
        });
        
        if(remain_flag>0) {
          data['status'] = 'Received Partial';
        }else{
          data['status'] = 'Received Full';
        }
        if(remain_flag > 0) {
            //this._globalService.showToast("Scan quantity and PO quantity mismatched.");
            let that = this;
            that._globalService.showLoaderSpinner(true);
            this._purchaseOrderService.poGrnEdit(data).subscribe(
                data => {                     
                    if(data.status==1){
                        this._globalService.deleteTab(this.tabIndex,this.parentId);
                        this._router.navigate(['/purchase_order']);
                    } else {
                        this.errorMsg = data.message;
                    }
                },
                err => {
                    this._globalService.showToast('Something went wrong. Please try again.');
                    that._globalService.showLoaderSpinner(false);
                },
                function(){
                    //completed callback
                    that._globalService.showLoaderSpinner(false);
                }
            );
        } else {
           let that = this;
            that._globalService.showLoaderSpinner(true);
            this._purchaseOrderService.poGrnEdit(data).subscribe(
                data => {                     
                    if(data.status==1){
                        this._globalService.deleteTab(this.tabIndex,this.parentId);
                        this._router.navigate(['/purchase_order']);
                    } else {
                        this.errorMsg = data.message;
                    }
                },
                err => {
                    this._globalService.showToast('Something went wrong. Please try again.');
                    that._globalService.showLoaderSpinner(false);
                },
                function(){
                    //completed callback
                    that._globalService.showLoaderSpinner(false);
                }
            ); 
        }        
    }    

    /*addEditGrn(form: any) {
        let data: any = {};
        data['purchase_order_id'] = this.purchase_order.id;
        data['received_date'] = this.purchase_order.received_date;
        data['warehouse_id'] = this.purchase_order.warehouse_id;

        data['product'] = [];
        let remain_flag = 0;
        this.purchase_order.products.forEach(function(item: any) {
            let prod: any = {};
            prod['product_id'] = item.product_id;
            prod['quantity'] = item.received_quantity;
            prod['price'] = item.price;
            prod['discount'] = item.discount;
            prod['discount_amount'] = item.discount_amount;
            prod['damage'] = item.damaged_quantity;
            prod['shortage'] = item.shortage_quantity;
            prod['total_qty'] = item.quantity;
            data['product'].push(prod);
            if (item.remaining_quantity > 0) {
                remain_flag++;
            }
        });

        if (remain_flag > 0) {
            data['status'] = 'Received Partial';
        } else {
            data['status'] = 'Received Full';
        }

        let that = this;
        that._globalService.showLoaderSpinner(true);
        this._purchaseOrderService.poGrnEdit(data).subscribe(
            data => {

                if (data.status == 1) {
                    this._globalService.deleteTab(this.tabIndex, this.parentId);
                    this._router.navigate(['/purchase_order']);

                } else {

                    this.errorMsg = data.message;
                }
            },
            err => {
                this._globalService.showToast('Something went wrong. Please try again.');
                that._globalService.showLoaderSpinner(false);
            },
            function() {
                //completed callback
                that._globalService.showLoaderSpinner(false);
            }
        );
    }
    */

    scanEAN() {
        let eanNo = this.formModel.scanItems;
        if(eanNo!='') {
            let data:any = {};
            data["website_id"] = this._globalService.getWebsiteId();
            data["ean"] = eanNo;
            const poItemsIdsArr = this.poItemsIds;
            data["itemId"] = poItemsIdsArr.join(',');
            let that = this;
            this._purchaseOrderService.getProductFromEan(data).subscribe(res => {
                if(res.status == 1) {
                    that.purchase_order.products.forEach(function(lineItems,index) {
                        if(res.data.id  == lineItems.product.id) {
                            let remainsqty = that.purchase_order.products[index].remaining_quantity;
                            if(lineItems["quantityDetails"].length > 0 && remainsqty > 0) {
                                lineItems["quantityDetails"].forEach( (element) => {
                                    if(element.checked == true) {
                                        element.receivedQuanity = parseInt(element.receivedQuanity)+1;            
                                    } else {
                                        that._globalService.showToast("Please select a batch or rack no");        
                                    }
                                }) 
                            } else {
                                //that._globalService.showToast("You have received all items");
                            }
                            
                            that.calcQty(index,1);
                        }
                    })
                } else { // if EAN is not found
                    this._globalService.showToast(res.Message);
                }
            }, err => {

            });
        }
    }

    dialogPoProductRef: MatDialogRef < ScanItemComponent > | null;
    scanItemDetails(index,typeIndexNumber,activityType,purchageOrderId,productId) {
        let data: any = {};
        data['index'] = index;
        data['typeIndexNumber'] = typeIndexNumber;
        data['activityType'] = activityType;
        data['purchageOrderId'] = purchageOrderId;
        data['productId'] = productId;
        this.dialogPoProductRef = this.dialog.open(ScanItemComponent, {
            data: data
        });
        this.dialogPoProductRef.afterClosed().subscribe(result => {
            if(result != undefined) {
                if(result["products_list"].length > 0) {
                    if(result['activityType'] == 'Received') { // putting the data for received item details
                        let quantity:any = 0;
                        let received:any = [];
                        result["products_list"].forEach(function(val:any,key:any) {
                            if(val.product.id == productId) {
                                let scanedData:any = {};
                                scanedData['quantity'] = parseInt(val['quantity_'+key])
                                scanedData['received_date'] = '2019-03-27';//this._globalService.convertDate(val.created_date, 'yyyy-MM-dd');
                                scanedData['expiry_date'] = null;
                                scanedData['expiry_issue_comment'] = "";
                                scanedData['expiry_issue'] = "";
                                scanedData['lot_no'] = val["batchNo"];
                                scanedData['rack_no'] = val["rackNo"];
                                scanedData['manufactured_date'] = null;
                                scanedData['remarks'] = "";
                                scanedData['price'] = "0.00";
                                scanedData['discount'] = "0.00";
                                scanedData['goods_condition'] = "OK";
                                received.push(scanedData);
                                quantity = parseInt(quantity)+parseInt(val['quantity']);
                            }                            
                        });
                        this.purchase_order.products[index].received = received;
                        this.purchase_order.products[index].received_quantity = quantity;
                        this.calcQty(index,typeIndexNumber);
                    } else {
                        this.purchase_order.products[index].received = [];
                    }

                    if(result['activityType'] == 'Damaged') { // this is for damaged quantity
                        let quantity:any = 0;
                        let damagedArr:any = [];
                        result["products_list"].forEach(function(val:any,key:any) {
                            if(val.product.id == productId) {
                                let scanedData:any = {};
                                scanedData['quantity'] = parseInt(val['quantity'])
                                scanedData['received_date'] = '2019-03-27';//this._globalService.convertDate(val.created_date, 'yyyy-MM-dd');
                                scanedData['expiry_date'] = null;
                                scanedData['expiry_issue_comment'] = "";
                                scanedData['expiry_issue'] = "";
                                scanedData['lot_no'] = val["batchNo"];
                                scanedData['rack_no'] = val["rackNo"];
                                scanedData['manufactured_date'] = null;
                                scanedData['remarks'] = "";
                                scanedData['price'] = "0.00";
                                scanedData['discount'] = "0.00";
                                scanedData['goods_condition'] = "OK";
                                damagedArr.push(scanedData);
                                quantity = parseInt(quantity)+parseInt(val['quantity']);
                            }
                        });
                        this.purchase_order.products[index].damaged = damagedArr;
                        this.purchase_order.products[index].damaged_quantity = quantity;
                        this.calcQty(index,typeIndexNumber);
                    } else {
                        this.purchase_order.products[index].damaged = [];
                    }

                     if(result['activityType'] == 'Shortage') {  // this is for shortage quantity
                        let quantity:any = 0;
                        let shortagedArr:any = [];
                        result["products_list"].forEach(function(val:any,key:any) {
                            if(val.product.id == productId) {
                                let scanedData:any = {};
                                scanedData['quantity'] = parseInt(val['quantity'])
                                scanedData['received_date'] = '2019-03-27';//this._globalService.convertDate(val.created_date, 'yyyy-MM-dd');
                                scanedData['expiry_date'] = null;
                                scanedData['expiry_issue_comment'] = "";
                                scanedData['expiry_issue'] = "";
                                scanedData['lot_no'] = val["batchNo"];
                                scanedData['rack_no'] = val["rackNo"];
                                scanedData['manufactured_date'] = null;
                                scanedData['remarks'] = "";
                                scanedData['price'] = "0.00";
                                scanedData['discount'] = "0.00";
                                scanedData['goods_condition'] = "OK";
                                shortagedArr.push(scanedData);
                                quantity = parseInt(quantity)+parseInt(val['quantity']);
                            }
                        });
                        this.purchase_order.products[index].shortage = shortagedArr;
                        this.purchase_order.products[index].shortage_quantity = quantity;
                        this.calcQty(index,typeIndexNumber);
                    } else {
                        this.purchase_order.products[index].shortage = [];
                    }
                }
            }
        });
    }
}

@Component({
    templateUrl: './templates/scan_items.html',
    providers: [PurchaseOrderService]
})
export class ScanItemComponent implements OnInit {
    public products_list: any = [];
    public search_text: string;
    public sortBy: any = '';
    public sortOrder: any = '';
    public sortClass: any = '';
    public sortRev: boolean = false;
    public scanItemId:any;
    public activityType:any;
    public poProductList = [];
    public formModel:any={};
    public parentData:any={};
    public scanItemDetailsArr:any = [];
    constructor(
        public _globalService: GlobalService,
        private _purchaseOrderService: PurchaseOrderService,
        public dialog: MatDialog,
        private dialogRef: MatDialogRef < ScanItemComponent > , @Inject(MAT_DIALOG_DATA) public data: any
    ) {}

    ngOnInit() {
        this.scanItemId = this.data.productId;
        let purchageOrderId = this.data.purchageOrderId; // assigned the purchage order ID
        this.activityType = this.data.activityType;
        this.parentData = this.data;
        this.getPoItemDetails(purchageOrderId);
    }

    getPoItemDetails(purchageOrderId ) {
        let request_data: any = {};
        this._purchaseOrderService.scanItemDetails(purchageOrderId).subscribe(
            data => {
                if(data["status"] == 1) {
                    this.products_list = data.purchase_order_products;
                    let that = this;
                    this.products_list.forEach(function(itemsList: any,key:any) {
                        if(that.scanItemId == itemsList['product']['id']) { // Assign the Master Item details
                            that.poProductList = itemsList;
                        }
                    });
                }
                this.scanItemDetailsArr.push(this.poProductList)
                this.scanItemDetailsArr.forEach(function(listArr: any,key:any) {
                    listArr['quantity_'+key] = listArr.quantity;
                    listArr['expiry_date_'+key] = '2019-02-02';
                    listArr['batchNo_'+key] = '';
                    listArr['lotNo_'+key] = '';
                })
            },
            err => {
                this._globalService.showToast('Something went wrong. Please try again.');
            },
            function() {
                //completed callback
            }
        );
    }

    closeDialog() {
        this.dialogRef.close();
    }

    addMoreBatch() {
        this.scanItemDetailsArr.push(this.poProductList);
        this.scanItemDetailsArr.forEach(function(listArr: any,key:any) {
            listArr['quantity_'+key] = listArr.quantity;
            listArr['expiry_date_'+key] = '2019-02-02';
            listArr['batchNo_'+key] = '';
            listArr['lotNo_'+key] = '';
        })
    }  

    deleteBatchNo(productId,indexNo) {
        let that = this;
        this.scanItemDetailsArr.forEach(function(itemsList: any,key:any) {
            if (key == indexNo) {
                that.scanItemDetailsArr.splice(indexNo, 1);
            }
        });
    }

    applyChanges() {
        let data:any = {};
        data['products_list'] = this.products_list;
        data['activityType'] = this.parentData['activityType'];
        data['index'] = this.parentData['index'];
        data['purchageOrderId'] = this.parentData['purchageOrderId'];
        data['productId'] = this.parentData['productId'];
        this.dialogRef.close(data);
    }
}