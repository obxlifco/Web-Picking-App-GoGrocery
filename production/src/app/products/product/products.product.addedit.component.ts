import { Component, OnInit, Inject, OnDestroy, AfterViewInit, AfterContentInit, Optional } from '@angular/core';
import { Router, ActivatedRoute, NavigationEnd } from '@angular/router';
import { COMMA, ENTER } from '@angular/cdk/keycodes';
import { MatChipInputEvent } from '@angular/material';
import { DomSanitizer } from '@angular/platform-browser';
// import { PaginationInstance } from 'ngx-pagination';
import { CookieService } from 'ngx-cookie';
import { GlobalService } from '../../global/service/app.global.service';
import { Global, GlobalVariable } from '../../global/service/global';
import { ProductService } from './products.product.service';
import { DialogsService } from '../../global/dialog/confirm-dialog.service'; 
import { AddEditTransition, AddEditStepFlipTransition } from '../.././addedit.animation';
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material';
import { PopupImgDirective, ImageUploadUrlDialog, ImageMetaDataDialog } from '../.././global/directive/popup-image.directive';
import { EditorDialog } from '../.././global/directive/editor.directive';
import { CurrencyService } from '../../settings/currency/settings.currency.service';
import { DOCUMENT} from '@angular/platform-browser';
import { isNgTemplate } from '@angular/compiler';
export interface barCodesArr { name: string; }
export interface warehouseArr { name: string; }
@Component({
    templateUrl: './templates/add_product.html',
    providers: [ProductService],
    animations: [AddEditTransition],
    host: {
        '[@AddEditTransition]': ''
    },
})
export class ProductBasicInfoComponent implements OnInit, OnDestroy, AfterViewInit {
    public response: any;
    public errorMsg: string;
    public successMsg: string;
    public menu_list: any;
    public formModel: any = {};
    public List: any = {}
    private sub: any;
    public tabIndex: number;
    public parentId: number = 0;
    public add_edit: any = '';
    public imgsubscriber: any;
    public parent_category_list: any = [];
    public child_category_list: any = [];
    public sub_child_category_list: any = [];
    public sub_sub_child_category_list: any = [];
    public parent_child: any;
    public product_base: any;
    public all_languages :any = [];
    public hsncode_list: any = [];
    public status: any;
    public applicableTax:any = 'VAT';
    constructor(
        private _productService: ProductService,
        public _globalService: GlobalService,
        public global: Global,
        private _router: Router,
        private _route: ActivatedRoute,
        private _cookieService: CookieService,
        public dialog: MatDialog,
    ) {
    }
    
    visible = true;
    selectable = true;
    removable = true;
    addOnBlur = true;
    readonly separatorKeysCodes: number[] = [ENTER, COMMA];
    barcodes: barCodesArr[] = [];
    addBarcodes(event: MatChipInputEvent): void {
        const input = event.input;
        const value = event.value;
        // Add our barcode
        let count = this.barcodes.filter(e => e.name === value).length;
        if (count == 0) { // Unique checking of barcodes
            if ((value || '').trim()) {
                this.barcodes.push({ name: value.trim() });
            }
        }
        // Reset the input value
        if (input) {
            input.value = '';
        }
    }

    removeBarcode(barcode: barCodesArr): void {
        const index = this.barcodes.indexOf(barcode);
        if (index >= 0) {
            this.barcodes.splice(index, 1);
        }
    }

    ngOnInit() {
        this.product_base = window.location.protocol + '//' + window.location.hostname + ':8062' + '/product/';
        this.tabIndex = +this._globalService.getCookie('active_tabs');
        this.parentId = this._globalService.getParentTab(this.tabIndex);
        let userData = this._cookieService.getObject('userData');
        this.applicableTax = userData['applicable_tax'];

        //console.log(this.tabIndex + "============= " + this.parentId);
        this.sub = this._route.params.subscribe(params => {
            this.formModel.productId = +params['id']; // (+) converts string 'id' to a number                        
        });
        if (this.formModel.productId) {
            this._cookieService.putObject('pid_edit', this.formModel.productId);
            this._cookieService.putObject('action', 'edit');
            this.add_edit = 'edit';
        } else {
            this._cookieService.putObject('action', 'add');
            this.formModel.productId = this._cookieService.getObject('pid_add');
            this.add_edit = 'add';
            this.formModel.productId = 0;
            this.formModel.status = 'n';
        }

        this._productService.loadHsnCodeMaster().subscribe(
            res => {
                if(res["status"] == 1) {
                    this.hsncode_list = res["api_status"];
                }
        } , err => {

        })
        this.formModel.parent_categories = [{}];
        this._productService.productBasicInfoLoad().subscribe(
            data => {
                this.response = data;
                this.List.category_list = this.response.category;
                this.parent_category_list = this.response.category;
                this.List.brand_list = this.response.brand;
                this.List.supplier_list = this.response.supplier;
                this.List.taxclass_list = this.response.taxclass;
                this.List.ptaxclass_list = this.response.ptaxclass;
                this.List.customergrp_list = this.response.customergrp;
                this.List.minprice_list = this.response.minprice;
                this.List.maxprice_list = this.response.maxprice;
                this.List.unit_list = this.response.unit;
                this.List.warehouse_list = this.response.warehouse;
                this.all_languages = this.response.all_languages;
                if(this.add_edit == 'add') {
                    this.formModel.warehouse_id = this.List.warehouse_list[0]['id'];
                }
            },
            err => {
                this._globalService.showToast('Something went wrong. Please try again.');
            },
            function () {
                //completed callback
            }
        );

        this._route.params.subscribe(params => {
            if (this.formModel.productId > 0) {
                this._productService.productBasicInfoEdit(this.formModel.productId).subscribe(
                    data => {
                        this.response = data;
                        this.formModel = this.response.api_status;
                        if (this.formModel.barcode_list != '' && this.formModel.barcode_list != null) {
                            let dbBarcodes = this.formModel.barcode_list.split(',');
                            for (let i = 0; i < dbBarcodes.length;i++) {
                                if ((dbBarcodes[i] || '').trim()) {
                                    this.barcodes.push({ name: dbBarcodes[i].trim() });
                                }
                            }
                        }
                        this.formModel.hsn_id = +this.formModel.hsn_id;
                        this.formModel.productId = this.response.api_status.id;
                        this.formModel.parent_categories = [];
                        this.parent_child = this.response.parent_child;
                        if (this.formModel.url != null) {
                            this.formModel.meta_url = this.formModel.url;//this.formModel.url.split("/").pop();
                        } else {
                            this.formModel.meta_url = '';
                        }
                        if (this.parent_child.length) {
                            let that = this;
                            this.parent_child.forEach(function (item: any, index: number) {
                                if (item.sub_sub_child_id > 0) {
                                    that.formModel.parent_categories.push({
                                        "category_1": item.parent_id,
                                        "category_2": item.child_id,
                                        "category_3": item.sub_child_id,
                                        "category_4": item.sub_sub_child_id,
                                    });
                                    that.get_child_categories(item.parent_id, index, 1, 0);
                                    that.get_child_categories(item.child_id, index, 2, 0);
                                    that.get_child_categories(item.sub_child_id, index, 3, 0);

                                } else if (item.sub_child_id > 0) {
                                    that.formModel.parent_categories.push({
                                        "category_1": item.parent_id,
                                        "category_2": item.child_id,
                                        "category_3": item.sub_child_id,
                                        "category_4": null
                                    });
                                    that.get_child_categories(item.parent_id, index, 1, 0);
                                    that.get_child_categories(item.child_id, index, 2, 0);
                                    that.get_child_categories(item.sub_child_id, index, 3, 0);
                                } else if (item.child_id > 0) {

                                    that.formModel.parent_categories.push({
                                        "category_1": item.parent_id,
                                        "category_2": item.child_id,
                                        "category_3": null,
                                        "category_4": null
                                    });
                                    that.get_child_categories(item.parent_id, index, 1, 0);
                                    that.get_child_categories(item.child_id, index, 2, 0);
                                } else {
                                    that.formModel.parent_categories.push({
                                        "category_1": item.parent_id,
                                        "category_2": null,
                                        "category_3": null,
                                        "category_4": null
                                    });
                                    if (item.parent_id) {
                                        that.get_child_categories(item.parent_id, index, 1, 0);
                                    }
                                }
                            });
                        } else {
                            this.formModel.parent_categories.push({});
                        }
                        var values_category: any = [];
                        var brand: any = [];
                        this.response.product_category.forEach(function (item: any) {
                            values_category.push(item.category.id);
                        });
                        if (this.response.api_status.brand != null) {
                            var values_brand = +this.response.api_status.brand;//this.response.api_status.brand.split(",").map(Number);
                        }
                        if (this.response.api_status.supplier_id != null) {
                            var values_supplier = this.response.api_status.supplier_id.split(",").map(Number);
                        }
                        if (this.response.api_status.taxclass != null) {
                            this.formModel.taxclass_id = this.response.api_status.taxclass.id;
                        }
                        if (this.response.api_status.po_taxclass != null) {
                            this.formModel.po_taxclass_id = this.response.api_status.po_taxclass.id;
                        }
                        if (this.response.api_status.customer_group != null) {
                            this.formModel.customer_group_id = this.response.api_status.customer_group.id;
                        }
                        if (this.response.api_status.min_price_rule != null) {
                            this.formModel.min_price_rule_id = this.response.api_status.min_price_rule.id;
                        }
                        if (this.response.api_status.max_price_rule != null) {
                            this.formModel.max_price_rule_id = this.response.api_status.max_price_rule.id;
                        }
                        if (this.response.api_status.warehouse != null) {
                            this.formModel.warehouse_id = this.response.api_status.warehouse;
                        }
                        this.formModel.uom = parseInt(this.response.api_status.uom);
                        this.formModel.category = values_category;
                        this.formModel.brand = values_brand;
                        this.formModel.supplier_id = values_supplier;
                        this.formModel.status = this.response.api_status.isblocked;
                        //image section
                        let img_base = GlobalVariable.S3_URL + 'product/200x200/';
                        this.formModel.other_image = [];
                        this.formModel['image_meta_data'] = [];
                        let that = this;
                        this.response.product_img.forEach(function (item: any) {
                            if (item.is_cover) {
                                that.formModel['cover_image'] = [];
                                let cover_img = {};
                                let meta_data = {};
                                cover_img['name'] = item.img;
                                cover_img['url'] = img_base + item.img;
                                cover_img['id'] = item.id;
                                meta_data['id'] = item.id;
                                meta_data['img_alt'] = item.img_alt;
                                meta_data['img_order'] = item.img_order;
                                meta_data['img_title'] = item.img_title;
                                meta_data['is_cover'] = 1;
                                that.formModel['cover_image'].push(cover_img);
                                that.formModel['image_meta_data'].unshift(meta_data);
                            } else {
                                let image = {};
                                let meta_data = {};
                                image['name'] = item.img;
                                image['url'] = img_base + item.img;
                                image['id'] = item.id;
                                meta_data['id'] = item.id;
                                meta_data['img_alt'] = item.img_alt;
                                meta_data['img_order'] = item.img_order;
                                meta_data['img_title'] = item.img_title;
                                meta_data['is_cover'] = 0;
                                that.formModel.other_image.push({
                                    image: image,
                                    image_meta_data: meta_data
                                });
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
        });
        this.global.reset_dialog();
    }

    get_child_categories(parent_id: number, index: number, lvl: number, reset: number) {
        this._productService.getChildCategory(parent_id, 0, lvl + 1).subscribe(
            data => {
                this.response = data;
                if (this.response.status) {
                    if (lvl == 1) { //level 1 category
                        if (reset == 0) {
                            this.child_category_list[index] = this.response.category;
                        } else {
                            this.child_category_list[index] = [];
                            this.sub_child_category_list[index] = [];
                            this.sub_sub_child_category_list[index] = [];
                            this.child_category_list[index] = this.response.category;
                            this.formModel.parent_categories[index].category_2 = null;
                            this.formModel.parent_categories[index].category_3 = null;
                            this.formModel.parent_categories[index].category_4 = null;
                        }
                    } else if (lvl == 2) { //level 2 category
                        if (reset == 0) {
                            this.sub_child_category_list[index] = this.response.category;
                        } else {
                            this.sub_child_category_list[index] = [];
                            this.sub_sub_child_category_list[index] = [];
                            this.sub_child_category_list[index] = this.response.category;
                            this.formModel.parent_categories[index].category_3 = null;
                            this.formModel.parent_categories[index].category_4 = null;
                        }
                        // console.log(this.sub_child_category_list);
                    } else { //level 3 category
                        if (reset == 0) {
                            // console.log(30);
                            this.sub_sub_child_category_list[index] = this.response.category;
                        } else {
                            this.sub_sub_child_category_list[index] = [];
                            this.sub_sub_child_category_list[index] = this.response.category;
                            this.formModel.parent_categories[index].category_4 = null;
                        }
                        // console.log(this.sub_sub_child_category_list);
                    }
                } else {
                    // if(lvl==1){ //level 1 category
                    //  if(index > -1 && this.child_category_list[index]){
                    //      this.child_category_list[index] = [];
                    //      this.sub_sub_child_category_list[index] = [];
                    //  }else{
                    //      this.child_category_list.push({});
                    //  }
                    // }else{ //level 2 category

                    //  if(index > -1 && this.List.child_child_category_list[index]){
                    //      this.List.child_child_category_list[index] = [];
                    //  }else{
                    //      this.List.child_child_category_list.push({});
                    //  }
                    // }
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
        slug = value.toLowerCase().replace(/[^\w ]+/g, '').replace(/ +/g, '-');
        this.formModel.meta_url = this.product_base + slug;
    }
    addRow() {
        this.formModel.parent_categories.push({});
    }

    removeRow(index: number) {
        this.formModel.parent_categories.splice(index, 1);
        this.child_category_list.splice(index, 1);
    }
    addEditBasicInfo(form: any) {
        this.errorMsg = '';
        var data: any = {};
        data = Object.assign({}, this.formModel);
        if (this.formModel.meta_url) {
            //data.url_suffix = this.formModel.meta_url;
            data.url_suffix = "";
            //data.meta_url = this.product_base + this.formModel.meta_url;
            data.meta_url = this.formModel.meta_url;
        } else {
            data.url_suffix = '';
            var slug = '';
            slug = this.formModel.name.toLowerCase().replace(/[^\w ]+/g, '').replace(/ +/g, '-');
            data.meta_url = this.product_base + slug;
        }
        if (this.formModel.supplier_id) {
            data.supplier_id = this.formModel.supplier_id.join();
        }
        // if (this.formModel.brand) {
        //     //data.brand = this.formModel.brand.join();
        //     data.brand = this.formModel.brand;
        // }
        if (!this.formModel.customer_group_id) {
            data.customer_group_id = '';
        }
        if (!this.formModel.min_price_rule_id) {
            data.min_price_rule_id = '';
        }
        if (!this.formModel.max_price_rule_id) {
            data.max_price_rule_id = '';
        }
        if (!this.formModel.warehouse_id) {
            data.warehouse_id = '';
        }
        if (!this.formModel.po_taxclass_id) {
            data.po_taxclass_id = '';
        }
        if (!this.formModel.taxclass_id) {
            data.taxclass_id = '';
        }
        if (this.formModel.productId < 1) {
            data.createdby = this._globalService.getUserId();
        }
        data.amazon_addstatus = 1;
        data.amazon_itemid = 1;
        data.amazon_itemid = 1;
        data.twitter_addstatus = 1;
        if (this.formModel.productId > 0) {
            data.createdby = this._globalService.getUserId();
        }
        let ean:any = [];
        this.barcodes.forEach(element => {
            ean.push(element.name);
        });

        data.barcode_list = ean.join(",");
        data.website_id = this._globalService.getWebsiteId();
        
        data.updatedby = this._globalService.getUserId();
        data.isblocked = this.formModel.status;
        data.order_id = 1;
        data.website_id = 1;
        data.numberof_sale = 1;
        data.numberof_view = 1;
        data.ebay = 1;
        data.amazon = 1;
        data.webshop = 1;
        data.order_price = 1;
        data.visibility_id = 1;
        data.url = 1;
        data.other_image = [];
        data.image_meta_data_edit = [];
        data.image_meta_data = [];
        data.image_library = [];

        if (this.formModel.parent_categories.length > 0) {
            var parent_categories: any = [];
            let that = this;
            this.formModel.parent_categories.forEach(function (item: any, index: number) {
                if (index == 0) {
                    var is_parent: any = 'y';
                } else {
                    var is_parent: any = 'n';
                }
                if (item.category_4) {
                    parent_categories.push({
                        "category_1": item.category_1,
                        "category_2": item.category_2,
                        "category_3": item.category_3,
                        "category_id": item.category_4,
                        "is_parent": is_parent
                    });
                } else if (item.category_3) {
                    parent_categories.push({
                        "category_1": item.category_1,
                        "category_2": item.category_2,
                        "category_3": 0,
                        "category_id": item.category_3,
                        "is_parent": is_parent
                    });
                } else if (item.category_2) {
                    parent_categories.push({
                        "category_1": item.category_1,
                        "category_2": 0,
                        "category_3": 0,
                        "category_id": item.category_2,
                        "is_parent": is_parent
                    });
                } else {
                    parent_categories.push({
                        "category_1": 0,
                        "category_2": 0,
                        "category_3": 0,
                        "category_id": item.category_1,
                        "is_parent": is_parent
                    });
                }
            });
            data.parent_categories = parent_categories;
        }

        if (this.formModel.cover_image && this.formModel.cover_image.length) {
            if (this.formModel.cover_image[0]['_file']) {
                data.cover_image = '';
            } else if (this.formModel.cover_image[0]['name']) {
                data.cover_image = this.formModel.cover_image[0]['name'];
            } else {
                data.cover_image = '';
            }
        } else {
            data.cover_image = '';
        }
        
        if (this.formModel['image_meta_data'] && this.formModel['image_meta_data'].length) {
            if (this.formModel['image_meta_data'][0]['id']) {
                data.image_meta_data_edit.push(this.formModel['image_meta_data'][0]);
                data.image_meta_data = [];
            } else {
                data.image_meta_data.push(this.formModel['image_meta_data'][0]);
            }
        } else {
            data.image_meta_data.push({
                img_alt: '',
                img_title: '',
                img_order: 1,
                is_cover: 1,
                type: ''
            });
        }

        if (this.formModel['other_image'] && this.formModel['other_image'].length) {
            this.formModel['other_image'].forEach(function (item: any, index: number) {
                let meta_arr = {};
                meta_arr = item['image_meta_data'];
                meta_arr['img_order'] = index + 1;
                if (item['image_meta_data'].id) {
                    data.image_meta_data_edit.push(item['image_meta_data']);
                } else {
                    data.image_meta_data.push(item['image_meta_data']);
                }
            });
        }

        var form_data = new FormData();
        if (this.formModel.cover_image && this.formModel.cover_image.length) {
            if (this.formModel.cover_image[0].type == 1) {
                form_data.append('cover_url', this.formModel.cover_image[0].url);
            } else if (this.formModel.cover_image[0].type == 3) {
                data.image_library.push({
                    'img': this.formModel.cover_image[0]['name']
                });
                form_data.append('cover_url', '');
            } else {
                if (this.formModel.cover_image[0]._file) {
                    form_data.append('cover_image', this.formModel.cover_image[0]._file);
                } else {
                    form_data.append('cover_url', '');
                }
            }
        } else {
            form_data.append('cover_url', '');
        }
        if (this.formModel.other_image) {
            var other_files = [];
            var other_urls = {};
            other_urls['other_image'] = [];
            this.formModel.other_image.forEach(function (item: any) {
                if (item.image.type == 1) {
                    other_urls['other_image'].push(item.image.url);
                } else if (item.image.type == 3) {
                    data.image_library.push({
                        'img': item.image.name
                    });
                } else {
                    if (item.image._file) {
                        other_files.push(item.image._file);
                    }
                }
            });
            other_files.forEach(function (item: any) {
                form_data.append('other_image', item);
            });
            form_data.append('url', JSON.stringify(other_urls));
        } else {
            form_data.append('url', JSON.stringify({
                other_image: ''
            }));
        }
        form_data.append('data', JSON.stringify(data));
        let that = this;
        this._productService.basicInfoAddEdit(form_data, this.formModel.productId).subscribe(
            data => {
                this.response = data;
                if (this.response.status == 1) {
                    if (this.add_edit == 'add') {
                        this._cookieService.putObject('pid_add', this.response.api_status);
                        this._router.navigate(['/products/add/step2']);
                    } else {
                        this._router.navigate(['/products/edit/' + this.formModel.productId + '/step2']);
                    }
                } else {
                    this.errorMsg = this.response.message;
                    this._globalService.showToast(this.errorMsg);
                }
                that._globalService.showLoaderSpinner(false);
            },
            err => {
                this._globalService.showToast('Something went wrong. Please try again.');
                that._globalService.showLoaderSpinner(false);
            },
            function () {
                //completed callback
                that._globalService.showLoaderSpinner(false);
            }
        );
    }

    dialogRef: MatDialogRef<PopupImgDirective> | null;
    openImagePop(imgFor: string, multiple: boolean = false) {
        let data = {
            imgFor: imgFor,
            is_multiple: multiple,
            type: 'product'
        };

        this.dialogRef = this.dialog.open(PopupImgDirective, {
            data: data
        });
        this.dialogRef.afterClosed().subscribe(result => {
            for (let key in result) {
                if (multiple) { // alternate images ; multiple upload;
                    let that = this;
                    result[key].forEach(function (item: any) {
                        let img_arr = [];
                        img_arr = item;
                        img_arr['type'] = 2; // image upload type - 2 i.e upload from browse file
                        let img_meta = {};
                        img_meta['img_alt'] = '';
                        img_meta['img_title'] = '';
                        img_meta['img_order'] = 1;
                        img_meta['type'] = 2;
                        if (key == 'cover_image') {
                            img_meta['is_cover'] = 1;
                        } else {
                            img_meta['is_cover'] = 0;
                        }
                        if (that.formModel[key]) {
                            that.formModel[key].push({
                                image: img_arr,
                                image_meta_data: img_meta
                            });
                        } else {
                            that.formModel[key] = [];
                            that.formModel[key].push({
                                image: img_arr,
                                image_meta_data: img_meta
                            });
                        }

                        if (that.formModel['image_meta_data']) {
                            if (img_meta['is_cover']) {
                                that.formModel['image_meta_data'].push(img_meta);
                            }
                        } else {
                            that.formModel['image_meta_data'] = [];
                            if (img_meta['is_cover']) {
                                that.formModel['image_meta_data'].push(img_meta);
                            }
                        }
                    });

                } else {
                    let value = result[key][0];
                    if (value) {
                        value['type'] = 2; // image upload type - 2 i.e upload from browse file
                        let img_meta = {};
                        img_meta['img_alt'] = '';
                        img_meta['img_title'] = '';
                        img_meta['img_order'] = 1;
                        img_meta['type'] = 2;
                        if (key == 'cover_image') {
                            img_meta['is_cover'] = 1;
                        } else {
                            img_meta['is_cover'] = 0;
                        }
                        if (key == 'cover_image') {
                            if (this.formModel[key]) {
                                this.formModel[key].push(value);
                            } else {
                                this.formModel[key] = [];
                                this.formModel[key].push(value);
                            }

                            if (this.formModel['image_meta_data']) {
                                this.formModel['image_meta_data'].push(img_meta);
                            } else {
                                this.formModel['image_meta_data'] = [];
                                this.formModel['image_meta_data'].push(img_meta);
                            }
                        } else {
                            if (this.formModel[key]) {
                                this.formModel[key].push({
                                    image: value,
                                    image_meta_data: img_meta
                                });
                            } else {
                                this.formModel[key] = [];
                                this.formModel[key].push({
                                    image: value,
                                    image_meta_data: img_meta
                                });
                            }
                        }
                    }
                }
            }
        });
    }

    // preview images which are added via url/google drive/dropbox
    ngAfterViewInit() {
        this.imgsubscriber = this._globalService.imageArrayChange$.subscribe(result => {
            for (let key in result) {
                let value = result[key];
                value['type'] = 1; // image upload type - 1 i.e upload from inserted link,google picker, dropbox picker
                let img_meta = {};
                img_meta['img_alt'] = '';
                img_meta['img_title'] = '';
                img_meta['img_order'] = 1;
                img_meta['type'] = 1;
                if (key == 'cover_image') {
                    img_meta['is_cover'] = 1;
                } else {
                    img_meta['is_cover'] = 0;
                }
                if (key == 'cover_image') {
                    if (this.formModel[key]) {
                        this.formModel[key].push(value);
                    } else {
                        this.formModel[key] = [];
                        this.formModel[key].push(value);
                    }

                    if (this.formModel['image_meta_data']) {
                        this.formModel['image_meta_data'].push(img_meta);
                    } else {
                        this.formModel['image_meta_data'] = [];
                        this.formModel['image_meta_data'].push(img_meta);
                    }

                } else {
                    if (this.formModel[key]) {
                        this.formModel[key].push({
                            image: value,
                            image_meta_data: img_meta
                        });
                    } else {
                        this.formModel[key] = [];
                        this.formModel[key].push({
                            image: value,
                            image_meta_data: img_meta
                        });
                    }
                }

            }
        });

        this.imgsubscriber = this._globalService.libArrayChange$.subscribe(result => {
            for (let key in result) {
                if (key == 'other_image') { // alternate images ; multiple upload;
                    let that = this;
                    result[key].forEach(function (item: any) {
                        let img_arr = [];
                        img_arr = item;
                        img_arr['name'] = img_arr['url'];
                        img_arr['url'] = GlobalVariable.S3_URL + 'product/200x200/' + img_arr['url'];
                        img_arr['type'] = 3; // image upload type - 3 i.e upload from s3 library
                        let img_meta = {};
                        img_meta['img_alt'] = '';
                        img_meta['img_title'] = '';
                        img_meta['img_order'] = 1;
                        img_meta['type'] = 3;
                        img_meta['is_cover'] = 0;
                        if (that.formModel[key]) {
                            that.formModel[key].push({
                                image: img_arr,
                                image_meta_data: img_meta
                            });
                        } else {
                            that.formModel[key] = [];
                            that.formModel[key].push({
                                image: img_arr,
                                image_meta_data: img_meta
                            });
                        }
                        if (that.formModel['image_meta_data']) {
                            that.formModel['image_meta_data'].push(img_meta);
                        } else {
                            that.formModel['image_meta_data'] = [];
                            that.formModel['image_meta_data'].push(img_meta);
                        }
                    });

                } else {
                    let value = result[key][0];
                    if (value) {
                        value['name'] = value['url'];
                        value['url'] = GlobalVariable.S3_URL + 'product/200x200/' + value['url'];
                        value['type'] = 3; // image upload type - 3 i.e upload from s3 library
                        let img_meta = {};
                        img_meta['img_alt'] = '';
                        img_meta['img_title'] = '';
                        img_meta['img_order'] = 1;
                        img_meta['type'] = 3;
                        img_meta['is_cover'] = 1;
                        if (this.formModel[key]) {
                            this.formModel[key].push(value);
                        } else {
                            this.formModel[key] = [];
                            this.formModel[key].push(value);
                        }
                        if (this.formModel['image_meta_data']) {
                            this.formModel['image_meta_data'].push(img_meta);
                        } else {
                            this.formModel['image_meta_data'] = [];
                            this.formModel['image_meta_data'].push(img_meta);
                        }
                    }
                }
            }
        });
    }
    // Unsubscribe observables and detach event handlers to avoid memory leaks.
    ngOnDestroy() {
        this.imgsubscriber.unsubscribe();
    }

    // Delete image from array and unlink from server at the time of update
    delImg(is_remove: number, scope_var: string, file_var: string, is_arr: number, index: number) {
        if (is_remove > 0) { // delete image from server through webservice call
            var form_data: any = {};
            form_data.field = 'img';
            if (is_arr) {
                if (file_var == 'cover_image') {
                    form_data.id = this[scope_var][file_var][index]['id'];
                    form_data.file_name = this[scope_var][file_var][index]['name'];
                } else {
                    form_data.id = this[scope_var][file_var][index]['image']['id'];
                    form_data.file_name = this[scope_var][file_var][index]['image']['name'];
                }

            } else {
                if (file_var == 'cover_image') {
                    form_data.id = this[scope_var][file_var][index]['id'];
                    form_data.file_name = this[scope_var][file_var]['name'];
                } else {
                    form_data.id = this[scope_var][file_var][index]['image']['id'];
                    form_data.file_name = this[scope_var][file_var]['image']['name'];
                }
            }
            if (form_data.file_name) { //call webservice
                this._productService.productImageDelete(form_data).subscribe(
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
        }
        // delete image from local array
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
        if (file_var == 'cover_image') {
            this.formModel['image_meta_data'].splice(index, 1);
        }
    };

    //image additional information dialog reference 
    dialogMetaDataRef: MatDialogRef<ImageMetaDataDialog> | null;
    // open image additional information dialog box
    addImageMeta(index: number, type: number, is_cover: number) {
        let data = {};
        data['type'] = type; // 1= from url / 2= browse
        data['index'] = index;
        data['is_cover'] = is_cover;
        if (is_cover) {
            if (this.formModel['image_meta_data']) {
                data['meta'] = this.formModel['image_meta_data'][index];
            }
        } else {
            if (this.formModel.other_image) {
                data['meta'] = this.formModel.other_image[index]['image_meta_data'];
            }
        }
        //open dialog box
        this.dialogMetaDataRef = this.dialog.open(ImageMetaDataDialog, {
            data: data
        });
        // after close dialog box subscription method
        this.dialogMetaDataRef.afterClosed().subscribe(result => {
            if(result && result.hasOwnProperty('altName')) {
                let img_meta = {};
                img_meta['img_alt'] = (result['altName']) ? result['altName'] : '';
                img_meta['img_title'] = (result['imgTitle']) ? result['imgTitle'] : '';
                img_meta['img_order'] = (result['imgOrder']) ? result['imgOrder'] : 1;
                img_meta['type'] = result['type'];
                img_meta['is_cover'] = result.is_cover;
                console.log(result)
                if (result['id']) {
                    img_meta['id'] = result['id'];
                    if (result.is_cover) {
                        if (this.formModel['image_meta_data_edit']) {
                            this.formModel['image_meta_data_edit'][result['index']] = img_meta;
                        } else {
                            this.formModel['image_meta_data_edit'] = [];
                            this.formModel['image_meta_data_edit'].push(img_meta);
                        }
                    } else {
                        if(this.formModel.other_image.length) {
                            this.formModel.other_image[result['index']]['image_meta_data'] = img_meta;
                        }
                    }

                } else {
                    if (result.is_cover) {
                        if (this.formModel['image_meta_data']) {
                            this.formModel['image_meta_data'][result['index']] = img_meta;
                        } else {
                            this.formModel['image_meta_data'] = [];
                            this.formModel['image_meta_data'].push(img_meta);
                        }
                    } else {
                        if(this.formModel.other_image.length) {
                            this.formModel.other_image[result['index']]['image_meta_data'] = img_meta;
                        }
                    }
                }
            }
        });
    }

    // set an image as cover image
    set_cover_image(product_id: number, id: number) {
        if (product_id && id) {
            let data = {};
            data['id'] = id;
            data['product_id'] = product_id;
            this._productService.setCoverImage(data).subscribe(
                data => {
                    this.response = data;
                    if (this.response.status == 1) {
                        this.ngOnInit();
                        this._globalService.showToast(this.response.message);
                    } else {
                        this._globalService.showToast(this.response.message);
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

    //image additional information dialog reference 
    dialogEditorRef: MatDialogRef<EditorDialog> | null;
    //open text editor 
    openEditor(scope_var: string, field_var: string) {
        let data = {};
        data['scope_var'] = scope_var;
        data['field_var'] = field_var;
        data['value'] = this[scope_var][field_var];
        // data['lang_code'] = lang_code;
        //open dialog box
        this.dialogEditorRef = this.dialog.open(EditorDialog, {
            data: data
        });
        // after close dialog box subscription method
        this.dialogEditorRef.afterClosed().subscribe(result => {
            if (result) {
                if (result.scope_var != '') {
                    this[result.scope_var][result.field_var] = result.value;
                } else {
                    this[result.field_var] = result.value;
                }
            }
        });
    }

    //image order change dialog reference 
    dialogImageOrderRef: MatDialogRef<ImageReorderDialog> | null;
    openReorder() {
        let data = [];
        data = this.formModel.other_image;
        this.dialogImageOrderRef = this.dialog.open(ImageReorderDialog, {
            data: data
        });
    }
}

@Component({
    templateUrl: './templates/image_order.html',
    providers: [ProductService]
})
export class ImageReorderDialog {
    constructor(
        public dialogRef: MatDialogRef<ImageReorderDialog>,
        public dialog: MatDialog, @Inject(MAT_DIALOG_DATA) public data: any
    ) {
        dialog.afterOpen.subscribe(() => {
            let containerElem: HTMLElement = <HTMLElement>document.getElementsByClassName('mat-dialog-container')[0];
            containerElem.classList.remove('pop-box-up');
        });
    }

    public images = this.data;
    saveOrder() {
        this.dialogRef.close(this.images);
    }

    closeDialog() {
        this.dialogRef.close();
    }
}

@Component({
    templateUrl: './templates/add_product2.html',
    providers: [ProductService],
    // animations: [AddEditStepFlipTransition],
    // host: {
    //     '[@AddEditStepFlipTransition]': ''
    // },
})
export class ProductAdvanceInfoComponent implements OnInit {
    public response: any;
    public errorMsg: string;
    public successMsg: string;
    public formModel: any = {};
    private sub: any;
    public tabIndex: number;
    public parentId: number = 0;
    public add_edit: any = '';
    public default_list: any = [];
    public compulsory_list: any = [];
    public optional_list: any = [];
    public channel_list: any = [];
    public custom_list: any = [];
    public api_status: any = [];
    public custom_lang_data: any = []
    constructor(
        private _productService: ProductService,
        public _globalService: GlobalService,
        private _router: Router,
        private _route: ActivatedRoute,
        private _cookieService: CookieService
    ) { }
    ngOnInit() {
        this.loadData(6);
    }
    loadData(channel) {
        this.tabIndex = +this._globalService.getCookie('active_tabs');
        this.parentId = this._globalService.getParentTab(this.tabIndex);
        this.add_edit = this._cookieService.getObject('action');
        if (this.add_edit == 'add') {
            this.formModel.productId = this._cookieService.getObject('pid_add');
        } else {
            this.formModel.productId = this._cookieService.getObject('pid_edit');
        }
        this.compulsory_list = [];
        this.optional_list = [];
        this.default_list = [];
        this.custom_list = [];
        this.api_status = [];
        this.custom_lang_data = []
        this._productService.productAdvanceInfoLoad(this.formModel.productId, channel).subscribe(
            data => {
                this.response = data;
                this.channel_list = this.response.channel;
                this.default_list = this.response.custom_data;
                this.api_status = this.response.api_status;
                this.custom_lang_data = this.response.lang_data;
                let that = this;

                this.default_list.forEach(function (item: any) {
                    that.formModel[item.field_id] = item.default_values;
                    ////////////Custom values///
                    if (item.custom_values == '' && that.response.api_status.length == 0) {
                        item.custom_values = '';
                    } else {
                        var array = [];
                        var array_default = [];
                        var lang_array_default = [];
                        if (that.response.api_status.length > 0) {
                            var custom_list: any = that.response.api_status;
                            custom_list.forEach(function (item_custom: any) {
                                if (item_custom.value && item_custom.field_id == item.field_id) {
                                    array_default = item_custom.value.split('##');
                                    that.formModel[item.field_id] = item_custom.value;
                                }
                            });
                        } else {
                            array_default = item.default_values.split('##');
                            that.formModel[item.field_id] = item.default_values;
                        }
                        array = item.custom_values.split('##');
                        if (item.input_type=="Dropdown"){
                            if (item.lang_data !=undefined){
                                item.lang_data.forEach(function (list_lang_data: any, index: number) {
                                    // item.lang_data[index]['custom_values_'+list_lang_data.language_code] = list_lang_data.field_lable_value.split('##')
                                    item.lang_data[index]['custom_values_list'] = list_lang_data.field_lable_value.split('##')                                    
                                });
                            }
                        }
                        ///////Checkobox////////
                        if ((item.input_type == 'Checkbox')) {
                            array.forEach(function (item_default: any) {
                                if (array_default.includes(item_default)) {
                                    that.formModel[item_default] = true;
                                }
                            });
                        }
                        item.custom_values = array;
                    }
                    ///////Generate List/////
                    if (item.is_optional == 1) {
                        that.compulsory_list.push(item);
                    } else {
                        that.optional_list.push(item);
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

    addEditAdvanceInfo() {
        this._globalService.showLoaderSpinner(true);
        var data: any = [];
        let that = this;
        // console.log(this.default_list)
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
            }
            ///////Others////////  
            else if (that.formModel[item.field_id]) {
                var default_value: any = that.formModel[item.field_id];
            } else {
                var default_value: any = '';
            }
            
            let language_data:any=[]

            item.lang_data.forEach(function (lang_item: any) {
                Object.keys(lang_item).forEach(key => {
                    let res = key;
                    let value = lang_item[key];
                    if (res=="field_name") { 
                        language_data.push({
                            "lang_field_value":that.formModel[value],
                            "lang_field_name":value
                        });
                    }
                });                    
            });
            
            data.push({
                "product_id": that.formModel.productId,
                "channel_id": 6,
                "field_id": item.field_id,
                "value": default_value,
                "website_id": 1,
                "field_name": item.field_label,
                "field_label": item.field_label,
                "lang_data":language_data
            })
        });
        this._productService.productAdvanceInfoAddEdit(data).subscribe(
            data => {
                this.response = data;
                if (this.response.status == 1) {

                    if (this.add_edit == 'add') {
                        this._router.navigate(['/products/add/step3']);
                    } else {
                        this._router.navigate(['/products/edit/' + this.formModel.productId + '/step3']);
                    }
                } else {
                    this.errorMsg = this.response.message;
                }
                this._globalService.showLoaderSpinner(false);
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
    templateUrl: './templates/add_product3.html',
    providers: [ProductService],
    animations: [AddEditStepFlipTransition],
    host: {
        '[@AddEditStepFlipTransition]': ''
    },
})
export class ProductDefaultPriceComponent implements OnInit, AfterContentInit {
    public response: any;
    public errorMsg: string;
    public successMsg: string;
    public formModel: any = {};
    public formModelPrice: any = {};
    public formModelImage: any = {};
    private sub: any;
    public tabIndex: number;
    public parentId: number = 0;
    public add_edit: any = '';
    public channel_list: any = [];
    public currency_list: any = [];
    public custom_list: any = [];
    public varient_list: any = [];
    public imgsubscriber: any;
    constructor(
        private _productService: ProductService,
        public _globalService: GlobalService,
        private _router: Router,
        private _route: ActivatedRoute,
        private _cookieService: CookieService,
        public dialog: MatDialog,
    ) { }

    ngOnInit() {
        this.tabIndex = +this._globalService.getCookie('active_tabs');
        this.parentId = this._globalService.getParentTab(this.tabIndex);
        this.add_edit = this._cookieService.getObject('action');
        if (this.add_edit == 'add') {
            this.formModel.productId = this._cookieService.getObject('pid_add');
        } else {
            this.formModel.productId = this._cookieService.getObject('pid_edit');
        }
        this.formModel.varients = [];
        this.currency_list = [];
        this.custom_list = [];
        this.varient_list = [];
        this._productService.productDefaultPriceLoad(this.formModel.productId).subscribe(
            data => {
                this.response = data;
                this.formModel.default_price = this.response.products[0].default_price;
                this.formModel.product = this.response.products[0];
                this.channel_list = this.response.channel;
                let that = this;
                this.currency_list = this.response.currency;
                var channelData: any = [];
                this.formModel.channel = this.response.CurrencyProductPrice;
                this.custom_list = this.response.custom_data;
                this.custom_list.forEach(function (item_cus: any) {
                    that.formModel[item_cus.field_id] = item_cus.default_values;
                    var array = [];
                    var array_default = [];
                    array_default = item_cus.default_values.split('##');
                    // }
                    array = item_cus.custom_values.split('##');
                    /////Checkobox////////
                    if ((item_cus.input_type == 'Checkbox')) {
                        array.forEach(function (item_default: any) {
                            if (array_default.includes(item_default)) {
                                that.formModel[item_default] = true;
                            }
                        });
                    }
                    item_cus.custom_values = array;
                });

                ////////////////Varient Start........................./////
                var variant = [];
                let img_base = GlobalVariable.S3_URL + 'product/200x200/';
                this.response.variant_product.forEach(function (item: any, index: number) {
                    var channel_varient = item.channel_varient;
                    var custom_field = item.custom_data_varient;
                    item = item.products_varient;
                    if (item.img != "") {
                        that.formModel['index'] = [];
                        let cover_img = {};
                        let meta_data = {};
                        cover_img['name'] = item.img;
                        cover_img['url'] = img_base + item.img;
                        cover_img['id'] = item.imgid;
                        meta_data['id'] = item.id;
                        meta_data['img_alt'] = item.img_alt;
                        meta_data['img_order'] = item.img_order;
                        meta_data['img_title'] = item.img_title;
                        meta_data['is_cover'] = 1;
                        that.formModelImage[index] = cover_img;
                        that.formModelImage[index] = cover_img;
                        that.formModelImage[index]['image_meta_data'] = (meta_data);
                    }

                    var var_curr: any = [];
                    var var_custom: any = [];
                    var curr_price = that.response.CurrencyProductPriceVariant;
                    if (curr_price) {
                        curr_price.forEach(function (item_price: any) {
                            if (item.id == item_price.product_id) {
                                var_curr.push(item_price);
                            }
                        });
                    } else {
                        // item[item.currency_id]=item.default_price*(item.currency_exchange_rate);
                    }
                    custom_field.forEach(function (item_customM: any) {
                        var custom_data: any;
                        custom_data = '';
                        // custom_data=item_customM.CustomData
                        custom_data = item_customM.value
                        item_customM = item_customM.CustomData
                        item_customM.value = custom_data
                        var array_var = [];
                        var array_default_var = [];
                        array_default_var = item_customM.value.split('##');
                        // }
                        array_var = item_customM.custom_values.split('##');
                        /////Checkobox////////
                        if ((item_customM.input_type == 'Checkbox')) {
                            array_var.forEach(function (item_default: any) {
                                if (array_default_var.includes(item_default)) {
                                    item_customM[item_default] = true;
                                }
                            });
                        }
                        item_customM.custom_values = array_var;
                        var_custom.push(item_customM);
                    });
                    that.formModel.varients.push({
                        "variation_id": item.id,
                        "variation_price": item.default_price,
                        "variation_sku": item.sku,
                        "var_curr": var_curr,
                        "var_custom": var_custom,
                        "channel_list": channel_varient
                    });
                });
                ////////////////Varient End........................./////
            },
            err => {
                this._globalService.showToast('Something went wrong. Please try again.');
            },
            function () {
                //completed callback
            }
        );

    }
    ngAfterContentInit() { }
    addRow() {
        var channel_list: any = [];
        this.channel_list.forEach(function (item: any) {
            channel_list.push({
                "basecurrency": item.basecurrency,
                "currency_id": item.currency_id,
                "channel_id": item.channel_id,
                "channel_name": item.channel_name,
                "price": ""
            });
        });
        // var var_custom:any=[];
        // this.custom_list.forEach(function(itemC:any){
        //  var_custom.push(itemC);
        // });
        this.formModel.varients.push({
            "variation_id": 0,
            "channel_list": channel_list
        });
    }

    removeRow(index: number) {
        this.formModel.varients.splice(index, 1);
    }
    deleteVarient(id: any) {
        this._productService.deleteVariant(id).subscribe(
            data => {
                this.response = data;
                if (this.response.status == 1) {
                    this._globalService.showToast(this.response.message);
                    this.ngOnInit();
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
    dialogRef: MatDialogRef<ProductPriceComponent> | null;
    show_pop(data: any, type: any, channel: any) {
        var Pdata: any = {};
        Pdata.currency = this.currency_list;
        Pdata.data = data;
        Pdata.type = type;
        Pdata.channel = channel;
        if (Pdata.type == 'P') {
            Pdata.channelData = this.formModel.channel;
        } else {
            Pdata.channelData = this.formModel.varients[Pdata.data].var_curr;
        }
        this.dialogRef = this.dialog.open(ProductPriceComponent, {
            data: Pdata
        });
        this.dialogRef.afterClosed().subscribe(result => {
            if (result) {
                if (Pdata.type == 'P') {
                    this.formModel.channel = result.channel;
                    if (result.price) {
                        this.formModel.default_price = result.price;
                    }

                } else {
                    this.formModel.varients[Pdata.data].var_curr = result.channel;
                }
            }
        });
    }

    dialogRefImg: MatDialogRef<PopupImgDirective> | null;
    openImagePop(imgFor: string, multiple: boolean = false) {

        let data = {
            imgFor: imgFor,
            is_multiple: multiple,
            type: 'product'
        };

        this.dialogRefImg = this.dialog.open(PopupImgDirective, {
            data: data
        });
        this.dialogRefImg.afterClosed().subscribe(result => {
            for (let key in result) {
                let value = result[key][0];
                if (value) {
                    value['type'] = 2; // image upload type - 2 i.e upload from browse file
                    let img_meta = {};
                    img_meta['img_alt'] = '';
                    img_meta['img_title'] = '';
                    img_meta['img_order'] = 1;
                    img_meta['type'] = 2;
                    if (key == 'cover_image') {
                        img_meta['is_cover'] = 1;
                    } else {
                        img_meta['is_cover'] = 0;
                    }
                    this.formModelImage[key] = value;

                    if (this.formModelImage['image_meta_data']) {
                        this.formModelImage['image_meta_data'].push(img_meta);
                    } else {
                        this.formModelImage['image_meta_data'] = [];
                        this.formModelImage['image_meta_data'].push(img_meta);
                    }

                }

            }

        });

        this._globalService.imageArrayChange$.subscribe(result => {
            for (let key in result) {
                let value = result[key];
                value['type'] = 1; // image upload type - 1 i.e upload from inserted link,google picker, dropbox picker
                this.formModelImage[key] = value;
            }
        });


    }
    //image additional information dialog reference 
    dialogMetaDataRef: MatDialogRef<ImageMetaDataDialog> | null;

    // open image additional information dialog box
    addImageMeta(index: number, type: number, is_cover: number) {
        let data = {};
        data['type'] = type; // 1= from url / 2= browse
        data['index'] = index;
        data['is_cover'] = is_cover;
        if (this.formModelImage[index]['image_meta_data']) {
            data['meta'] = this.formModelImage[index]['image_meta_data'];
        }
        //open dialog box
        this.dialogMetaDataRef = this.dialog.open(ImageMetaDataDialog, {
            data: data
        });
        // after close dialog box subscription method
        this.dialogMetaDataRef.afterClosed().subscribe(result => {
            if (result) {
                let img_meta = {};
                img_meta['img_alt'] = (result['altName']) ? result['altName'] : '';
                img_meta['img_title'] = (result['imgTitle']) ? result['imgTitle'] : '';
                img_meta['img_order'] = result['index'];
                img_meta['type'] = result['type'];
                img_meta['is_cover'] = result['is_cover'];
                if (result['id']) {
                    img_meta['id'] = result['id'];
                    this.formModelImage[result['index']]['image_meta_data'] = img_meta;

                } else {
                    this.formModelImage[result['index']]['image_meta_data'] = img_meta;
                }
            }
        });
    }
    ngAfterViewInit() {
        this.imgsubscriber = this._globalService.libArrayChange$.subscribe(result => {
            for (let key in result) {
                let value = result[key][0];
                value['name'] = value['url'];
                value['url'] = GlobalVariable.S3_URL + 'product/200x200/' + value['url'];
                value['type'] = 3; // image upload type - 3 i.e upload from s3 library
                this.formModelImage[key] = value;
            }
        });
    }
    // Delete image from array and unlink from server at the time of update
    delImg = function (is_remove: number, scope_var: string, file_var: string, is_arr: number, index: number) {
        if (is_remove > 0) {
            var form_data: any = {};
            form_data.id = is_remove;
            form_data.field = "img";
            form_data.file_name = this[scope_var][file_var]['name'];
            form_data.id = this[scope_var][file_var]['id'];
            if (form_data.id) {
                this._productService.productImageDelete(form_data).subscribe(
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
            } else {
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

    // preview images which are added via url/google drive/dropbox  
    addEditPrice(form: any) {
        this._globalService.showLoaderSpinner(true);
        let that = this;
        this.errorMsg = '';
        var dataRequest: any = {};
        dataRequest.product = this.formModel.product;
        dataRequest.default_price = this.formModel.default_price;
        var channel: any = [];
        this.channel_list.forEach(function (item_channel: any) {
            if (item_channel.price) {
                channel.push({
                    "channel_id": item_channel.channel_id,
                    "currency_id": item_channel.currency_id,
                    "price": item_channel.price
                })
            }
        });
        if (this.formModel.channel) {
            this.formModel.channel.forEach(function (item_channelWeb: any) {
                if (item_channelWeb.currency_id != 25 && item_channelWeb.price) {
                    channel.push({
                        "channel_id": item_channelWeb.channel_id,
                        "currency_id": item_channelWeb.currency_id,
                        "price": item_channelWeb.price
                    })
                }
            })
        }

        dataRequest.channel = channel;
        dataRequest.updatedby = this._globalService.getUserId();
        var varient: any = [];
        var form_data = new FormData();
        var image_library: any = [];
        this.formModel.varients.forEach(function (item: any, index) {
            var varient_custom: any = [];
            var varient_channel: any = [];
            if (item.variation_id) {
                item.var_custom.forEach(function (item_cus: any) {
                    var default_value: any;
                    ///////Checkobox////////
                    if (item_cus.input_type == 'Checkbox') {
                        var checked_values: any = '';
                        var cus_values: any = item_cus.custom_values;

                        cus_values.forEach(function (item_default: any) {
                            if (item_cus[item_default]) {

                                item_default = item_default + "##";
                                checked_values += item_default;
                            }
                        });
                        default_value = checked_values;
                    }
                    ///////Others//////// 
                    else {
                        default_value = item_cus.value;
                    }

                    varient_custom.push({
                        "field_id": item_cus.field_id,
                        "field_label": item_cus.field_label,
                        "field_name": item_cus.field_label,
                        "value": default_value
                    })
                });
                var variation_id: any = item.variation_id;

            } else {

                that.custom_list.forEach(function (item_cus: any) {

                    var default_value: any;
                    ///////Checkobox////////
                    if (item_cus.input_type == 'Checkbox') {
                        var checked_values: any = '';

                        item_cus.custom_values.forEach(function (item_default: any) {
                            if (item[item_default]) {
                                item_default = item_default + "##";
                                checked_values += item_default
                            }
                        });
                        default_value = checked_values;
                    }
                    ///////Others//////// 
                    else {
                        default_value = item[item_cus.field_id]
                    }
                    varient_custom.push({
                        "field_id": item_cus.field_id,
                        "field_label": item_cus.field_label,
                        "field_name": item_cus.field_label,
                        "value": default_value
                    })
                });
                var variation_id: any = 0;

            }

            var channelVariant: any = [];
            item.channel_list.forEach(function (item_channelVariant: any) {
                if (item_channelVariant.price) {
                    channelVariant.push({
                        "channel_id": item_channelVariant.channel_id,
                        "currency_id": item_channelVariant.currency_id,
                        "price": parseInt(item_channelVariant.price)
                    })
                }
            });
            if (item.var_curr) {
                item.var_curr.forEach(function (item_channelWebVariant: any) {
                    if (item_channelWebVariant.currency_id != 25 && item_channelWebVariant.price) {
                        channelVariant.push({
                            "channel_id": item_channelWebVariant.channel_id,
                            "currency_id": item_channelWebVariant.currency_id,
                            "price": parseInt(item_channelWebVariant.price)
                        })
                    }
                })
            }

            varient.push({
                "variation_id": item.variation_id,
                "sku": item.variation_sku,
                "default_price": item.variation_price,
                "visibility": 4,
                "channels": channelVariant,
                "custom": varient_custom
            });

            var vindex: any = index + 1;
            if (that.formModelImage[index]) {
                if (that.formModelImage[index].type == 1) {
                    form_data.append('cover_url' + vindex, that.formModelImage[index].url);
                } else if (that.formModelImage[index].type == 3) {
                    varient[index].img = that.formModelImage[index].name;
                    form_data.append('cover_url' + vindex, '');
                } else {
                    if (that.formModelImage[index]._file) {
                        form_data.append('cover_image' + vindex, that.formModelImage[index]._file);
                    } else {
                        varient[index].img = that.formModelImage[index].name;
                        form_data.append('cover_url' + vindex, '');
                    }
                }
                if (that.formModelImage[index]['image_meta_data']) {
                    varient[index].img_alt = that.formModelImage[index]['image_meta_data']['img_alt'];
                    varient[index].img_title = that.formModelImage[index]['image_meta_data']['img_title'];;
                } else {
                    varient[index].img_alt = '';
                    varient[index].img_title = '';
                }

            } else {
                varient[index].img = '';
                varient[index].img_alt = '';
                varient[index].img_title = '';
                form_data.append('cover_url' + vindex, '');
            }
        })
        dataRequest.varient = varient;


        form_data.append('data', JSON.stringify(dataRequest));

        this._productService.defaultPriceAddEdit(form_data, this.formModel.productId).subscribe(
            data => {
                this.response = data;
                if (this.response.status == 1) {
                    if (this.add_edit == 'add') {
                        this._router.navigate(['/products/add/step4']);
                    } else {
                        this._router.navigate(['/products/edit/' + this.formModel.productId + '/step4']);
                    }
                } else {
                    this.errorMsg = this.response.message;
                }
                this._globalService.showLoaderSpinner(false);
            },
            err => {
                this._globalService.showToast('Something went wrong. Please try again.');
            },
            function () {
                //completed callback
            }
        );
    }
    ngOnDestroy() {
        this.imgsubscriber.unsubscribe();
    }

}

@Component({
    templateUrl: './templates/add_mapped_price.html',
    providers: [ProductService, Global, CurrencyService],
})
export class ProductPriceComponent implements OnInit {
    public add_edit: any = '';
    public response: any;
    public errorMsg: string;
    public successMsg: string;
    public formModel: any = {};
    private sub: any;
    public tabIndex: number;
    public parentId: number = 0;
    public mapOpt: string = 'Manual';
    public currency_list: any = [];
    public base_currency: any;


    constructor(
        private _productService: ProductService,
        public _globalService: GlobalService,
        private global: Global,
        private _router: Router,
        private _route: ActivatedRoute,
        private _cookieService: CookieService,
        private dialogRef: MatDialogRef<ProductPriceComponent>,
        private _currencyService: CurrencyService,
        public dialog: MatDialog, @Inject(MAT_DIALOG_DATA) public data: any
    ) {
        dialog.afterOpen.subscribe(() => {
            let containerElem: HTMLElement = <HTMLElement>document.getElementsByClassName('mat-dialog-container')[0];
            containerElem.classList.remove('pop-box-up');
        });
    }

    ngOnInit() {
        this.tabIndex = +this._globalService.getCookie('active_tabs');
        this.parentId = this._globalService.getParentTab(this.tabIndex);
        this.add_edit = this._cookieService.getObject('action');
        if (this.add_edit == 'add') {
            this.formModel.productId = this._cookieService.getObject('pid_add');
        } else {
            this.formModel.productId = this._cookieService.getObject('pid_edit');
        }

        var curr_url = this._router.url;
        this.currency_list = this.data.currency;
        this.formModel.type = this.data.type;
        this.formModel.channel = this.data.channel;
        var curr_price = this.data.channelData;
        let that = this;
        if (this.data.channelData) {
            curr_price.forEach(function (item_price: any) {
                that.formModel[item_price.currency_id] = item_price.price;
            });
        }
        this.currency_list.forEach(function (item: any) {
            if (item.isbasecurrency == 'y') {
                that.base_currency = item;
            }
        });

    }
    sync() {
        let base_curr = this.base_currency.currency_code;
        let that = this;
        this._currencyService.syncCurr(that._globalService.getUserId()).subscribe(
            data => {
                this.response = data;
                this.response.AllCurrencyRates.forEach(function (item: any) {
                    if (item.isbasecurrency == 'y') {
                        that.base_currency = item;
                        if (!that.formModel[item.engageboost_currency_master_id]) {
                            
                            that.formModel[item.engageboost_currency_master_id] == 1;
                            //alert(that.formModel[item.engageboost_currency_master_id]);
                        }
                        base_curr = that.formModel[item.engageboost_currency_master_id];

                    } else {
                        that.formModel[item.engageboost_currency_master_id] = item.exchange_rate * base_curr;
                    }
                });
            },
            err => console.log(err),
            function () {
                //completed callback
            }
        );

    }
    setMappedPrice(form: any) {
        var channel: any = [];
        var data: any = {};
        let that = this;
        this.currency_list.forEach(function (item: any) {
            if (that.formModel.type == 'P' && item.isbasecurrency == 'y') {
                data.price = +that.formModel[item.currency_id];
            }
            channel.push({
                "currency_id": item.currency_id,
                "channel_id": that.formModel.channel,
                "price": +that.formModel[item.currency_id]
            })
        });
        data.channel = channel;
        this.dialogRef.close(data);
    }
    closeDialog() {
        this.dialogRef.close();
    }
}

@Component({
    templateUrl: './templates/add_product4.html',
    providers: [ProductService, Global],
    animations: [AddEditStepFlipTransition],
    host: {
        '[@AddEditStepFlipTransition]': ''
    },
})
export class ProductRelatedComponent implements OnInit {
    public add_edit: any = '';
    public response: any;
    public errorMsg: string;
    public successMsg: string;
    public formModel: any = {};
    private sub: any;
    public tabIndex: number;
    public parentId: number = 0;
    public bulk_ids: any = [];
    public rel_data: any = [];
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
    public step_type: any;
    public search_text: string;


    constructor(
        private _productService: ProductService,
        public _globalService: GlobalService,
        private global: Global,
        private _router: Router,
        private _route: ActivatedRoute,
        private _cookieService: CookieService
    ) { }

    ngOnInit() {
        this.tabIndex = +this._globalService.getCookie('active_tabs');
        this.parentId = this._globalService.getParentTab(this.tabIndex);
        this.add_edit = this._cookieService.getObject('action');
        if (this.add_edit == 'add') {
            this.formModel.productId = this._cookieService.getObject('pid_add');
        } else {
            this.formModel.productId = this._cookieService.getObject('pid_edit');
        }

        var curr_url = this._router.url;
        if (curr_url.indexOf('step6') > 0) {
            this.step_type = 1;
        }
        if (curr_url.indexOf('step7') > 0) {
            this.step_type = 5;
        }
        if (curr_url.indexOf('step8') > 0) {
            this.step_type = 3;
        }
        if (curr_url.indexOf('step9') > 0) {
            this.step_type = 4;
        }
        this.generateGrid(0, '', '', '', '');
    }
    generateGrid(reload: any, page: any, sortBy: any, filter: any, search: any) {
        this.total_list = [];
        this.selectedAll = false;
        this.filter = filter;
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
        this.post_data = {
            "product_id": this.formModel.productId,
            "userid": this.userId,
            "search": search,
            "order_by": sortBy,
            "order_type": this.sortOrder,
            "status": filter
        }
        this._productService.doGridRelated(this.post_data, page).subscribe(
            data => {
                this.response = data;
                if (this.response.count > 0) {
                    this.result_list = this.response.results[0].result;
                    this.result_list.forEach(function (item: any) {
                        if (item.isblocked == 'n') {
                            item.isblocked = 'Active';
                        } else {
                            item.isblocked = 'Inactive';
                        }

                        if (item.visibility_id == 1) {
                            item.visibility_id = 'Catalog Search';
                        } else {
                            item.visibility_id = 'Not Visible';
                        }

                    })
                    for (var i = 0; i < this.response.count; i++) {
                        this.total_list.push(i);
                    }

                    /////////////////////////////////
                    this._productService.doRelatedProduct(this.formModel.productId, this.step_type).subscribe(
                        data => {
                            var response_res: any = data;
                            let that = this;
                            this.result_list.forEach(function (item_res: any) {
                                var id = item_res.id;
                                response_res.api_status.forEach(function (item_rel: any) {
                                    if (item_rel.related_product_id == id) {
                                        item_res.selected = true;
                                        that.bulk_ids.push(item_rel.related_product_id);
                                    }
                                });

                            });
                        },
                        err => {
                            this._globalService.showToast('Something went wrong. Please try again.');
                        },
                        function () { }
                    );
                    //////////////////////////////////////////

                } else {
                    this.result_list = [];
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

            },
            err => {
                this._globalService.showToast('Something went wrong. Please try again.');
            },
            function () { }
        );
    }
    ////////////////////////////Check/Uncheck//////////////

    toggleCheckAll(event: any) {
        let that = this;
        that.bulk_ids = [];
        this.selectedAll = event.checked;
        this.result_list.forEach(function (item: any) {
            item.selected = event.checked;
            if (item.selected) {
                that.bulk_ids.push(item.id);
            }
        });
    }
    toggleCheck(id: any, event: any) {
        let that = this;
        this.result_list.forEach(function (item: any) {
            if (item.id == id) {
                item.selected = event.checked;
                if (item.selected) {
                    that.bulk_ids.push(item.id);
                } else {
                    var index = that.bulk_ids.indexOf(item.id);
                    that.bulk_ids.splice(index, 1);
                }
            }
        });
    }
    /////////////////////////Filter Grid//////////////////////

    updateGrid(isdefault: any) {

        this.global.doGridFilter('EngageboostProducts', isdefault, this.cols, "list_related").subscribe(
            data => {
                this.response = data;
                this.generateGrid(0, '', '', '', '');
            },
            err => {
                this._globalService.showToast('Something went wrong. Please try again.');
            },
            function () { }
        );
    }
    addEditRelatedProduct() {
        let that = this;
        var step: any;
        if (that.step_type == 1) {
            step = 'step7';
        }
        //console.log(that.step_type)
        if (that.bulk_ids.length > 0) {
            this.errorMsg = '';
            var data: any = {};
            that.bulk_ids.forEach(function (item: any) {
                var obj = {
                    "product_id": that.formModel.productId,
                    "related_product_id": item,
                    "related_product_type": that.step_type
                };
                that.rel_data.push(obj);
            });
            this._productService.doRelatedProductAddEdit(that.rel_data).subscribe(
                data => {
                    this.response = data;
                    if (this.response.status == 1) {
                        if (that.step_type != 5) {
                            if (this.add_edit == 'add') {
                                this._router.navigate(['/products/add/' + step]);
                            } else {
                                this._router.navigate(['/products/edit/' + this.formModel.productId + '/' + step]);
                            }
                        } else {
                            this._globalService.deleteTab(this.tabIndex, this.parentId);
                            if (this.add_edit == 'add') {
                                this._cookieService.remove('pid_add');
                            } else {
                                this._cookieService.remove('pid_edit');
                            }
                            this._cookieService.remove('action');
                        }
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
            var obj = [{
                "product_id": that.formModel.productId,
                "related_product_id": 0,
                "related_product_type": that.step_type  
            }];
            
            this._productService.doRelatedProductAddEdit(obj).subscribe(
                data => {

                }, err => {

            })

            if (that.step_type != 5) {
                if (this.add_edit == 'add') {
                    this._router.navigate(['/products/add/' + step]);
                } else {
                    this._router.navigate(['/products/edit/' + this.formModel.productId + '/' + step]);
                }
            } else {
                this._globalService.deleteTab(this.tabIndex, this.parentId);
                if (this.add_edit == 'add') {
                    this._cookieService.remove('pid_add');
                } else {
                    this._cookieService.remove('pid_edit');
                }
                this._cookieService.remove('action');
            }
        }
    }
}
//SUBSTITUTE PRODUCTS COMPONENT START 
@Component({
    templateUrl: './templates/add_product4.html',
    providers: [ProductService, Global],
    animations: [AddEditStepFlipTransition],
    host: {
        '[@AddEditStepFlipTransition]': ''
    },
})
export class ProductSubstituteComponent implements OnInit {
    public add_edit: any = '';
    public response: any;
    public errorMsg: string;
    public successMsg: string;
    public formModel: any = {};
    private sub: any;
    public tabIndex: number;
    public parentId: number = 0;
    public bulk_ids: any = [];
    public rel_data: any = [];
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
    public step_type: any;
    public search_text: string;


    constructor(
        private _productService: ProductService,
        public _globalService: GlobalService,
        private global: Global,
        private _router: Router,
        private _route: ActivatedRoute,
        private _cookieService: CookieService
    ) { }

    ngOnInit() {
        this.tabIndex = +this._globalService.getCookie('active_tabs');
        this.parentId = this._globalService.getParentTab(this.tabIndex);
        this.add_edit = this._cookieService.getObject('action');
        if (this.add_edit == 'add') {
            this.formModel.productId = this._cookieService.getObject('pid_add');
        } else {
            this.formModel.productId = this._cookieService.getObject('pid_edit');
        }

        var curr_url = this._router.url;
        if (curr_url.indexOf('step4') > 0) {
            this.step_type = '1';
        }
        if (curr_url.indexOf('step5') > 0) {
            this.step_type = '2';
        }
        if (curr_url.indexOf('step6') > 0) {
            this.step_type = '3';
        }
        if (curr_url.indexOf('step7') > 0) {
            this.step_type = '4';
        }
        if (curr_url.indexOf('step8') > 0) {
            this.step_type = '5';
        }

        /*this._router.events
            .filter((event) => event instanceof NavigationEnd)
            .map(() => this._route)
            .map((route) => {
                while (route.firstChild) route = route.firstChild;
                return route;
            })
            .filter((route) => route.outlet === 'primary')
            .mergeMap((route) => route.data)
            .subscribe((event) => {
                this.step_type = event['step_type'];
                
            });*/
        this.generateGrid(0, '', '', '', '');
    }
    generateGrid(reload: any, page: any, sortBy: any, filter: any, search: any) {
        this.total_list = [];
        this.selectedAll = false;
        this.filter = filter;
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
        this.post_data = {
            "product_id": this.formModel.productId,
            "userid": this.userId,
            "search": search,
            "order_by": sortBy,
            "order_type": this.sortOrder,
            "status": filter
        }
        this._productService.doGridRelated(this.post_data, page).subscribe(
            data => {
                this.response = data;
                if (this.response.count > 0) {
                    this.result_list = this.response.results[0].result;
                    this.result_list.forEach(function (item: any) {
                        if (item.isblocked == 'n') {
                            item.isblocked = 'Active';
                        } else {
                            item.isblocked = 'Inactive';
                        }

                    })
                    for (var i = 0; i < this.response.count; i++) {
                        this.total_list.push(i);
                    }

                    /////////////////////////////////
                    this._productService.doRelatedProduct(this.formModel.productId, this.step_type).subscribe(
                        data => {
                            var response_res: any = data;
                            let that = this;
                            this.result_list.forEach(function (item_res: any) {
                                var id = item_res.id;
                                response_res.api_status.forEach(function (item_rel: any) {
                                    if (item_rel.related_product_id == id) {
                                        item_res.Selected = true;
                                        that.bulk_ids.push(item_rel.related_product_id);
                                    }
                                });
                            });
                        },
                        err => {
                            this._globalService.showToast('Something went wrong. Please try again.');
                        },
                        function () { }
                    );
                    //////////////////////////////////////////

                } else {
                    this.result_list = [];
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

            },
            err => {
                this._globalService.showToast('Something went wrong. Please try again.');
            },
            function () { }
        );


    }
    ////////////////////////////Check/Uncheck//////////////

    toggleCheckAll(event: any) {
        let that = this;
        that.bulk_ids = [];
        this.selectedAll = event.checked;
        this.result_list.forEach(function (item: any) {
            item.selected = event.checked;
            if (item.selected) {
                that.bulk_ids.push(item.id);
            }
        });
    }
    toggleCheck(id: any, event: any) {
        let that = this;
        this.result_list.forEach(function (item: any) {
            if (item.id == id) {
                item.selected = event.checked;
                if (item.selected) {
                    that.bulk_ids.push(item.id);
                } else {
                    var index = that.bulk_ids.indexOf(item.id);
                    that.bulk_ids.splice(index, 1);
                }
            }
        });
    }
    /////////////////////////Filter Grid//////////////////////

    updateGrid(isdefault: any) {

        this.global.doGridFilter('EngageboostProducts', isdefault, this.cols, "list_related").subscribe(
            data => {
                this.response = data;
                this.generateGrid(0, '', '', '', '');
            },
            err => {
                this._globalService.showToast('Something went wrong. Please try again.');
            },
            function () { }
        );
    }
    addEditRelatedProduct() {
        let that = this;
        var step: any;
        if (that.step_type == 1) {
            step = 'step5';
        }
        if (that.step_type == 2) {
            step = 'step6';
        }
        if (that.step_type == 3) {
            step = 'step7';
        }
        if (that.step_type == 4) {
            step = 'step8';
        }

        if (that.bulk_ids.length > 0) {
            this.errorMsg = '';

            var data: any = {};
            that.bulk_ids.forEach(function (item: any) {
                var obj = {
                    "product_id": that.formModel.productId,
                    "related_product_id": item,
                    "related_product_type": that.step_type
                };
                that.rel_data.push(obj);
            });
            this._productService.doRelatedProductAddEdit(that.rel_data).subscribe(
                data => {
                    this.response = data;
                    if (this.response.status == 1) {
                        if (that.step_type != 5) {
                            if (this.add_edit == 'add') {
                                this._router.navigate(['/products/add/' + step]);
                            } else {
                                this._router.navigate(['/products/edit/' + this.formModel.productId + '/' + step]);
                            }
                        } else {
                            this._globalService.deleteTab(this.tabIndex, this.parentId);
                            if (this.add_edit == 'add') {
                                this._cookieService.remove('pid_add');
                            } else {
                                this._cookieService.remove('pid_edit');
                            }
                            this._cookieService.remove('action');
                        }

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

            var obj = [{
                "product_id": that.formModel.productId,
                "related_product_id": 0,
                "related_product_type": that.step_type  
            }];
            
            this._productService.doRelatedProductAddEdit(obj).subscribe(
                data => {

                }, err => {

            })
            
            if (that.step_type != 5) {
                if (this.add_edit == 'add') {
                    this._router.navigate(['/products/add/' + step]);
                } else {
                    this._router.navigate(['/products/edit/' + this.formModel.productId + '/' + step]);
                }
            } else {
                this._globalService.deleteTab(this.tabIndex, this.parentId);
                if (this.add_edit == 'add') {
                    this._cookieService.remove('pid_add');
                } else {
                    this._cookieService.remove('pid_edit');
                }
                this._cookieService.remove('action');
            }
        }
    }

}

@Component({
    templateUrl: './templates/variant_products.html',
    providers: [ProductService, Global],
    animations: [AddEditStepFlipTransition],
    host: {
        '[@AddEditStepFlipTransition]': ''
    },
})
export class VariantProductComponent implements OnInit {
    public add_edit: any = '';
    public response: any;
    public errorMsg: string;
    public successMsg: string;
    public formModel: any = {};
    private sub: any;
    public tabIndex: number;
    public parentId: number = 0;
    public bulk_ids: any = [];
    public rel_data: any = [];
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
    public add_btn: string;
    public post_data = {};
    public page: number = 1;
    public maxSize: number = 10;
    public directionLinks: boolean = true;
    public autoHide: boolean = false;
    public config: any = {};
    public permission: any = [];
    
    public userId: any;
    public step_type: any;
    public search_text: string = '';
    public filter: string = '';
    public visibility_id: number=1;
    constructor(
        private _productService: ProductService,
        public _globalService: GlobalService,
        private global: Global,
        private _router: Router,
        private _route: ActivatedRoute,
        private _cookieService: CookieService,
        public dialog: MatDialog
    ) {

    }

    ngOnInit() {
        this.tabIndex = +this._globalService.getCookie('active_tabs');
        this.parentId = this._globalService.getParentTab(this.tabIndex);
        this.add_edit = this._cookieService.getObject('action');
        if (this.add_edit == 'add') {
            this.formModel.productId = this._cookieService.getObject('pid_add');
        } else {
            this.formModel.productId = this._cookieService.getObject('pid_edit');
        }
        var curr_url = this._router.url;
        if (curr_url.indexOf('step6') > 0) {
            this.step_type = '1';
        }
        if (curr_url.indexOf('step7') > 0) {
            this.step_type = '2';
        }
        if (curr_url.indexOf('step8') > 0) {
            this.step_type = '3';
        }
        if (curr_url.indexOf('step9') > 0) {
            this.step_type = '4';
        }

        if (this.formModel.productId > 0) {
            this._productService.productBasicInfoEdit(this.formModel.productId).subscribe(
                data => {
                        this.visibility_id = data.api_status.visibility_id;
                 },
                err => {
                    this._globalService.showToast('Something went wrong. Please try again.');
                },
                function() {}
            );
        }


        this.generateGrid(0, '', '', '', '');
    }

    generateGrid(reload: any, page: any, sortBy: any, filter: any, search: any) {
        // search = search.trimLeft();
        if(search == '') {
            this.search_text = '';
        } else {
            this.search_text = search;
        }
        this.total_list = [];
        this.selectedAll = false;
        this.filter = filter;
        this.sortBy = sortBy;
        this._productService.doGridVariant(this.formModel.productId, this.search_text.trim()).subscribe(
            data => {
                this.response = data;
                if (this.response["status"] == 1) {
                    if (this.response.result.length > 0) {
                        this.result_list = this.response.result;
                        let that = this;
                        that.bulk_ids = [];
                        this.result_list.forEach(function (item: any) {
                            that.bulk_ids.push(item.cross_product.id);
                        })
                        for (var i = 0; i < this.response.count; i++) {
                            this.total_list.push(i);
                        }
                    } else {
                        this.result_list = [];
                    }
                } else {
                    this.result_list = [];
                }
                this.cols = this.response.layout;
            },
            err => {
                this._globalService.showToast('Something went wrong. Please try again.');
            },
            function() {}
        );
    }

    saveVariations() {
        if (this.add_edit == 'add') {
            this._router.navigate(['/products/add/step6']);
        } else {
            this._router.navigate(['/products/edit/' + this.formModel.productId + '/step6']);
        }
    }

    dialogRefVariants: MatDialogRef<ProductVariantListComponent> | null;
    add_variant_products() {
        let that=this;
        let all_product_id = '';
        if(that.bulk_ids.length > 0) {
            all_product_id =  that.bulk_ids.join(',');
            
        }
        this.dialogRefVariants = this.dialog.open( ProductVariantListComponent, { data: {all_product_id : all_product_id, product_id: that.formModel.productId }});
        this.dialogRefVariants.afterClosed().subscribe(result => {
            that.generateGrid(0, '', '', '', '');
        });
    }
}

@Component({
  templateUrl: './templates/product_list.html',
  providers: [ProductService, Global]
})
export class ProductVariantListComponent implements OnInit {
    public response: any;
    public errorMsg: string;
    public successMsg: string;
    public bulk_ids: any = [];
    public bulk_ids_exist: any = [];
    public search_text: string;
    public pagination:any = {};
    public pageIndex : number = 0;
    public pageList : number = 0;
    public sortBy:any = '';
    public sortOrder:any = '';
    public sortClass:any = '';
    public sortRev:boolean = false;
    public selectedAll:any=false;
    public website_id:number = 1;
    public stat:any = {};
    public result_list:any=[];
    public total_list:any=[];
    public cols:any=[]
    public post_data = [];
    public page: number = 1;
    public filter: string = '';
    public maxSize: number = 10;
    public directionLinks: boolean = true;
    public autoHide: boolean = false;
    public config: any = {};
    public product_id: number;

    public individualRow:any={};
    public tabIndex: number;
    public parentId: number = 0;

    constructor(
        public _globalService:GlobalService,
        private _productService: ProductService,
        public dialog: MatDialog,
        @Inject(DOCUMENT) private document: any,
        public dialogRef: MatDialogRef<ProductVariantListComponent>,
        @Optional() @Inject(MAT_DIALOG_DATA) public data: any
    ) {

    }

    ngOnInit() {
        if(this.data['product_id']){
            this.product_id = this.data['product_id'];  
        }
        if(this.data['all_product_id']){
            this.bulk_ids = this.data['all_product_id'].split(",").map(Number);
            console.log('this.bulk_ids');
            console.log(this.bulk_ids);
        }
            this.generateGrid(0, '' , '', '', '');
    }

    closeDialog(){
        this.dialogRef.close();
    }

    generateGrid(reload: any, page: any, sortBy: string='', filter: any, search: any) {
        // search = search.trimLeft();
        if(search == '') {
            this.search_text = '';
        } else {
            this.search_text = search;
        }
        this.sortBy = sortBy;
        if(sortBy != '' && sortBy != undefined){ 
            if(this.sortRev) {
              this.sortOrder = '-'
              this.sortRev = !this.sortRev;
              this.sortClass = 'icon-down';
            }else{
              this.sortOrder = '+'
              this.sortRev = !this.sortRev;
              this.sortClass = 'icon-up';
            }
        }

        if(this.sortBy == '') {
            this.sortBy = 'id';
            this.sortOrder = '-'
        }
        let data = {};
        data['search'] = this.search_text.trim();
        data['order_by'] = this.sortBy;
        data['order_type'] = this.sortOrder;
        data['product_id'] = this.product_id;
        this._productService.productLoadPaging(data, page).subscribe(
            data => {
                let that = this;
                this.response = data;
                this.total_list = [];
                if(this.response.count > 0) {
                    this.result_list = this.response.results;
                    this.result_list.forEach(function(item:any){
                        if(that.bulk_ids.indexOf(item.id)>-1){
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
            function() {
               //completed callback
            }
        );
    }
    ////////////////////////////Check/Uncheck//////////////
    toggleCheckAll(event:any){
        this.bulk_ids=[];
        this.selectedAll = event.checked;
        this.result_list.forEach(item => {
            item.Selected = event.checked;    
            if(item.Selected) {
                this.bulk_ids.push(item.id);
            }
        });
        console.log(this.bulk_ids);
        
    }
    
    toggleCheck(id:any,event:any){
        this.result_list.forEach(item => {
            if(item.id==id) {
                item.Selected = event.checked;    
                if(item.Selected) {
                    this.bulk_ids.push(item.id);
                } else {
                    let index = this.bulk_ids.indexOf(item.id);
                    this.bulk_ids.splice(index, 1);
                }    
            }
        });
        console.log(this.bulk_ids);
    }

    saveVariantProduct() {
        let that = this;
        this.bulk_ids.forEach(function(item:any) {
            var obj = {
                "cross_product_id": item,
            };
            that.post_data.push(obj);
        });
        let data={
            "product_id": that.product_id,
            "post_data": this.post_data
        }
        this._productService.saveVariantProduct(data).subscribe(
            data => {
                this.response = data;
                if (this.response.status == 1) {
                   this._globalService.showToast('Variant products saved successfully');
                   this.dialogRef.close();
                } else {
                    this._globalService.showToast(this.response.message);
                    this.dialogRef.close();
                }
            },
            err => {
                this._globalService.showToast('Something went wrong. Please try again.');
            },
            function() {
                //completed callback
                that.dialogRef.close();
            }
        );
    }
}

//SUBSTITUTE PRODUCTS COMPONENT END
@Component({
    templateUrl: './templates/supplier_list.html',
    providers: [ProductService, Global],
    animations: [AddEditStepFlipTransition],
    host: {
        // '[@AddEditStepFlipTransition]': ''
    },
})
export class ProductSupplierComponent implements OnInit {
    public add_edit: any = '';
    public response: any;
    public errorMsg: string;
    public successMsg: string;
    public formModel: any = {};
    private sub: any;
    public tabIndex: number;
    public parentId: number = 0;
    public bulk_ids: any = [];
    public rel_data: any = [];
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
    public step_type: any;
    public search_text: string;
    public warehouse_supplier_count:number=0;
    public warehouse_list: any = [];
    constructor(
        private _productService: ProductService,
        public _globalService: GlobalService,
        private global: Global,
        private _router: Router,
        private _route: ActivatedRoute,
        private _cookieService: CookieService,
        public dialog: MatDialog,
        private dialogsService: DialogsService,
        //private dialogRef: MatDialogRef<SupplierList>,
        //@Inject(MAT_DIALOG_DATA) public data: any
    ) { }

    ngOnInit() {
        this.tabIndex = +this._globalService.getCookie('active_tabs');
        this.parentId = this._globalService.getParentTab(this.tabIndex);
        this.add_edit = this._cookieService.getObject('action');
        if (this.add_edit == 'add') {
            this.formModel.productId = this._cookieService.getObject('pid_add');
        } else {
            this.formModel.productId = this._cookieService.getObject('pid_edit');
        }
        this.get_warehouse_list(this.formModel.productId);
    }

    delete_supplier(warehouse_id, supplier_id) {
        this.dialogsService.confirm('Warning', "Are you sure to delete this?").subscribe(res => {
            if (res) {
                let post_data = {
                    'product': this.formModel.productId,
                    'warehouse': warehouse_id,
                    'supplier': supplier_id
                }
                this.global.getWebServiceData('warehousesuppliermapdelete', 'POST', post_data, '').subscribe(data => {
                    if (data.status == 1) {
                        this.get_warehouse_list(this.formModel.productId);
                        this._globalService.showToast(data.message);

                    } else {
                        this._globalService.showToast('Something went wrong. Please try again.');
                    }
                })
            }
        });
        

    }    

    dialogRefSuppliers: MatDialogRef<SupplierList> | null;
    add_supplier() {
        let that = this;
        this.dialogRefSuppliers = this.dialog.open(SupplierList, { data: {product_id: this.formModel.productId } });
        this.dialogRefSuppliers.afterClosed().subscribe(result => {
            that.get_warehouse_list(that.formModel.productId);
        });

    }

    get_warehouse_list(pro_id) {
        let data = {
            'product': pro_id
        };
        this._productService.wareHousList(data).subscribe(data => {
            this.warehouse_supplier_count=0;
            this.warehouse_list = data;
            this.warehouse_list.forEach(element => {
                if(element.data.length>0) {
                    this.warehouse_supplier_count=1;
                }
            });
        })
    }

    addEditSupplierForm() {
        console.log(this.warehouse_list);
        let userData = this._cookieService.getObject('userData');
        let userId = userData['uid'];
        let values: any = []
        let website_id = this._globalService.getWebsiteId();
        let that = this;
        this.warehouse_list.forEach(element => {
            let appliedItems = element.data;
            if (appliedItems.length > 0) {
                appliedItems.forEach(priceData => {
                    let rows = {
                        "product": that.formModel.productId,
                        "website_id": website_id,
                        "supplier_id": priceData.supplier,
                        "warehouse_id": priceData.warehouse,
                        "createdby": userId,
                        "modifiedby":userId,
                        "base_cost": priceData.base_cost,
                        "supplier_sku": priceData.supplier_sku,
                    }
                    values.push(rows);            
                });
            }
        });
        let data = { 'values': values }
        // POST DATA HERE
        this.global.getWebServiceData('warehousesuppliermap', 'POST', data, '').subscribe(
            data => {
                if (data.status == 1) {

                    this._globalService.showToast('Saved successfully');
                    if (this.add_edit == 'add') {
                        this._router.navigate(['/products/add/step5']);
                    } else {
                        this._router.navigate(['/products/edit/' + this.formModel.productId + '/step5']);
                    }
                } else {
                    this._globalService.showToast('Something went wrong. Please try again.');
                }
            },
            err => {
                this._globalService.showToast('Something went wrong. Please try again.');
            },
        );
    }
}

//SUPLIER LIST DIALOG COMPONENT
@Component({
    templateUrl: 'templates/suppliers.html',
    providers: [ProductService, Global]
})
export class SupplierList implements OnInit {
    public response: any;
    public errorMsg: string;
    public successMsg: string;
    public bulk_ids: any = [];
    public bulk_ids_exist: any = [];
    public search_text: string;
    public pagination:any = {};
    public pageIndex : number = 0;
    public pageList : number = 0;
    public sortBy:any = '';
    public sortOrder:any = '';
    public sortClass:any = '';
    public sortRev:boolean = false;
    public selectedAll:any=false;
    public website_id:number = 1;
    public stat:any = {};
    public result_list:any=[];
    public total_list:any=[];
    public cols:any=[]
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
    public popupLoder: boolean = false;
    constructor(
        private _globalService: GlobalService,
        private _productService: ProductService,
        private _global: Global,
        public dialog: MatDialog,
        private _router: Router,
        private _cookieService: CookieService,
        private dialogRef: MatDialogRef<SupplierList>,
        @Optional() @Inject(MAT_DIALOG_DATA) public data: any
        ) {
            this.formModel.product_id = data.product_id;
            this.get_warehouse_list(this.formModel.product_id);
            this.formModel.warehouse_id=[4];
            _global.reset_dialog();
        }
        
        ngOnInit() {
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
            "model": 'EngageboostSuppliers',
            "screen_name": 'list',
            "userid": this.userId,
            "search": this.search_text,
            "order_by": sortBy,
            "order_type": this.sortOrder,
            "status": 'n',
            "website_id": this._globalService.getWebsiteId()
        }
        this._productService.supplierList(data,page).subscribe(data => {
            let that = this;
            this.response = data;
            this.total_list = [];
            if(this.response.count > 0) {
                this.result_list = this.response.results[0].result;
                this.result_list.forEach(function(item:any){
                    if(that.bulk_ids.indexOf(item.id)>-1){
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
        }, err => {
            this._globalService.showToast("Something went wrong. Please try again.");
        }, function () {
            //completed callback
        });
    }
    ////////////////////////////Check/Uncheck//////////////
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

    saveSuppliers() {
        this.popupLoder = true;
        let supplier_ids: string = "";
        supplier_ids = this.bulk_ids.join(",");
        let that = this;
        this.bulk_ids.forEach(function (item: any) {
            that.result_list.forEach(function (inner_item: any) {

                if (that.bulk_ids.indexOf(item.id) > -1) {
                    item.Selected = true;
                }
            });
        });
        let add_suppliers = JSON.parse("[" + supplier_ids + "]");
        let values: any = []
        add_suppliers.forEach(element => {
            let rows = {
                "product": this.formModel.product_id,
                "website_id": this._globalService.getWebsiteId(),
                "supplier_id": element
            }
            values.push(rows);
        });
        let warehouse_ids=this.formModel.warehouse_id;
        if(warehouse_ids.length==0){
            warehouse_ids=[4];
        }
        let data = { 'values': values,'warehouse_ids': warehouse_ids }
        // POST DATA HERE
        this._global.getWebServiceData('warehousesuppliermap', 'POST', data, '').subscribe(
            data => {
                if (data.status == 1) {
                    
                    this._globalService.showToast('Saved successfully');

                    this.dialogRef.close();
                } else {
                    this._globalService.showToast('Something went wrong. Please try again.');
                }
                this.popupLoder = false;
            },
            err => {
                this.popupLoder = false;
                this._globalService.showToast('Something went wrong. Please try again.');
            },
        );

    }

    get_warehouse_list(pro_id) {
        let data = {
            'product': pro_id
        };
        this._productService.wareHousList(data).subscribe(data => {
            this.warehouse_list = data;

        })
    }
}
/////////////////////////////// price setup /////////////////////////////////////
@Component({
    templateUrl: './templates/price_setup.html',
    styleUrls: ['./templates/price_setup.css'],
    providers: [ProductService],
})

export class ProductPriceSetupComponent implements OnInit {
    public response: any;
    public errorMsg: string;
    public successMsg: string;
    public formModel: any = {};
    private sub: any;
    public tabIndex: number;
    public parentId: number = 0;
    public add_edit: any = '';
    public custom_list: any = [];
    public search_text: string;
    public productPriceArr: any = [];
    public priceMasterList: any = [];
    public warehouselist:any=[];
    warehouse_id:any;
    pricetype_id:any;
    constructor(
        private _productService: ProductService,
        public _globalService: GlobalService,
        private _global: Global,
        private _router: Router,
        private _route: ActivatedRoute,
        private _cookieService: CookieService,
        public dialog: MatDialog,
        private dialogsService: DialogsService,
    ) { }

    ngOnInit() {
        let website_id = this._globalService.getWebsiteId();
        this.tabIndex = +this._globalService.getCookie('active_tabs');
        this.parentId = this._globalService.getParentTab(this.tabIndex);
        this.add_edit = this._cookieService.getObject('action');

        this.loadPriceTypeMasterData();
        if (this.add_edit == 'add') {
            this.formModel.productId = this._cookieService.getObject('pid_add');
        } else {
            this.formModel.productId = this._cookieService.getObject('pid_edit');
        }
        let requestData: any = {};
        requestData.product = this.formModel.productId;
        requestData.website_id = website_id;
        requestData.product = this.formModel.productId;
        this.webseiteWarehouseList(website_id);

        let that = this;
        this._global.getWebServiceData('productwarehouselist', 'POST', requestData, '').subscribe(
            Res => {
                if (Res["status"] == 1) {
                    this.productPriceArr = Res.api_status;
                    this.productPriceArr.forEach(element => {
                        element.data.forEach((item,index) => {
                            item.warehousedata.forEach(el => {
                                console.log(el);
                                el.mrp=parseFloat(el.mrp).toFixed(2);
                                el.cost=parseFloat(el.cost).toFixed(2);
                                el.price=parseFloat(el.price).toFixed(2);
                                el.profit=el.price-el.cost;
                                el.profit=parseFloat(el.profit).toFixed(2);
                                el.margin=(el.profit/el.price)*100;
                                el.margin=parseFloat(el.margin).toFixed(2);

                                if(el.margin=='Infinity' || el.margin=='NaN' || el.margin==0){
                                    el.margin=0.0;
                                }
                                if(el.cost=='Infinity' || el.cost=='NaN' || el.cost==0){
                                    el.cost=0.0;
                                }
                                if(el.price=='Infinity' || el.price=='NaN' || el.price==0){
                                    el.price=0.0;
                                }
                                if(el.profit=='Infinity' || el.profit=='NaN' || el.profit==0){
                                    el.profit=0.0;
                                }
                                if(el.start_date==''){
                                    el.start_date = new Date(new Date().setHours(0,0,0,0));
                                }
                                if(el.end_date==''){
                                    // el.end_date = new Date(new Date().setHours(0,0,0,0));
                                    // el.end_date.setDate(el.end_date.getDate() + 1);
                                }
                            });
                        });
                    });
                }
            }, err => {

            }
        )
    }

    price_change(event:number,masterIndex:number,quantityIndex:number){
        this.productPriceArr.forEach((element,n) => {
            if(n==masterIndex){
                element.data.forEach((item,index) => {
                    if(index==quantityIndex){
                        item.warehousedata.forEach((el,i) => {
                            el.price=event;
                            el.profit=event-el.cost;
                            el.profit=el.profit.toFixed(2);
                            el.margin=(el.profit*100)/el.price;
                            el.margin=el.margin.toFixed(2);
                            
                            if(el.margin=='Infinity' || el.margin=='NaN' || el.margin==0){
                                el.margin=0.0;
                            }
                            if(el.cost=='Infinity' || el.cost=='NaN' || el.cost==0){
                                el.cost=0.0;
                            }
                            if(el.price=='Infinity' || el.price=='NaN' || el.price==0){
                                el.price=0.0;
                            }
                            if(el.profit=='Infinity' || el.profit=='NaN' || el.profit==0){
                                el.profit=0.0;
                            }
                        });
                    }
                });
            }
        });
    }
    
    margin_change(event:number,masterIndex:number,quantityIndex:number){
        this.productPriceArr.forEach((element,n) => {
            if(n==masterIndex){
                element.data.forEach((item,index) => {
                    if(index==quantityIndex){
                        item.warehousedata.forEach((el,i) => {
                            el.margin=event;

                            var add= (el.cost*event)/100;
                            el.price=parseFloat(el.cost) + add;
                            
                            el.profit=el.price - el.cost;
                            el.profit=el.cost.toFixed(2);
                            // el.profit=(event*el.price)/100;
                            // el.profit=el.profit.toFixed(2);


                            if(el.margin=='Infinity' || el.margin=='NaN' || el.margin==0){
                                el.margin=0.0;
                            }
                            if(el.cost=='Infinity' || el.cost=='NaN' || el.cost==0){
                                el.cost=0.0;
                            }
                            if(el.price=='Infinity' || el.price=='NaN' || el.price==0){
                                el.price=0.0;
                            }
                            if(el.profit=='Infinity' || el.profit=='NaN' || el.profit==0){
                                el.profit=0.0;
                            }
                        });
                    }
                });
            }
        });  
    }

    cost_change(event:number,masterIndex:number,quantityIndex:number){
        //console.log(event);
        this.productPriceArr.forEach((element,n) => {
            if(n==masterIndex){
                element.data.forEach((item,index) => {
                    if(index==quantityIndex){
                        item.warehousedata.forEach((el,i) => {
                            el.cost=event;
                            el.profit=el.price-event;
                            el.profit=el.profit.toFixed(2);
                            el.margin=(el.profit*100)/el.price;
                            el.margin=el.margin.toFixed(2);
                            if(el.margin=='Infinity' || el.margin=='NaN' || el.margin==0){
                                el.margin=0.0;
                            }
                            if(el.cost=='Infinity' || el.cost=='NaN' || el.cost==0){
                                el.cost=0.0;
                            }
                            if(el.price=='Infinity' || el.price=='NaN' || el.price==0){
                                el.price=0.0;
                            }
                            if(el.profit=='Infinity' || el.profit=='NaN' || el.profit==0){
                                el.profit=0.0;
                            }
                        });
                    }
                });
            }
        });
    }
    
    webseiteWarehouseList(website_id) {
        this._global.getWebServiceData('warehousestockmanagement', 'GET', '', website_id).subscribe(
            Res => {
                this.warehouselist = Res.warehouse;
            }, err => {

            }
        )
    }
    
    dialogPriceTypeMaster: MatDialogRef<AddPriceTypeMasterComponent> | null;
    addPriceType() {
        let postData:any = {};
        postData.product_id = this.formModel.productId
        postData.priceMasterList = this.priceMasterList; // assinged the price master data
        postData.warehouselist = this.warehouselist; // assigned the warehouse list into popup
        this.dialogPriceTypeMaster = this.dialog.open(AddPriceTypeMasterComponent, {
            data: postData,
            width: '450px'
        });
        this.dialogPriceTypeMaster.afterClosed().subscribe(result => {
            this.ngOnInit();
        });
    }

    priceSetup() {
        if (this.productPriceArr.length > 0) {
            let data: any = {};
            let priceData = [];
            let priceInfo: any = {};
            let counter: number = 0;
            let that=this;
            this._globalService.showLoaderSpinner(true);
            this.productPriceArr.forEach(function (priceTypeMaster) {
                let priceArr = priceTypeMaster.data;
                priceArr.forEach(function (priceList) {
                    let priceListArr = priceList.warehousedata
                    priceListArr.forEach(function (items) {
                        counter++;
                        priceInfo = {};
                        priceInfo.price = items.price;
                        priceInfo.cost = items.cost;
                        priceInfo.channel_id = 6; //items.channel_id; // 6 - Website
                        if (items.min_quantity != "") {
                            priceInfo.min_quantity = items.min_quantity;
                        } else {
                            priceInfo.min_quantity = 0;
                        }
                        if (items.max_quantity != "") {
                            priceInfo.max_quantity = items.max_quantity;
                        } else {
                            priceInfo.max_quantity = 0;
                        }
                        if (items.mrp != "") {
                            priceInfo.mrp = items.mrp;
                        } else {
                            priceInfo.mrp = 0;
                        }
                        if (items.price != "") {
                            priceInfo.price = items.price;
                        } else {
                            priceInfo.mrp = 0;
                        }
                        if (items.start_date != "") {
                            priceInfo.start_date = items.start_date;
                        } else {
                            priceInfo.start_date = new Date(new Date().setHours(0,0,0,0));
                            // startDate: new FormControl(new Date(new Date().setHours(0,0,0,0)))
                        }
                        if (items.end_date != "") {
                            priceInfo.end_date = items.end_date;
                        } else {
                            priceInfo.end_date = "";
                        }
                        priceInfo.product_price_type = items.product_price_type;
                        priceInfo.warehouse_id = priceList.warehouse_id;
                        priceInfo.product_id = items.product;
                        priceData.push(priceInfo);
                    });
                })
            })
            if(priceInfo.end_date!='' || priceInfo.start_date!=''){

                data.values = priceData;
                data.product_id = this.formModel.productId;
                if (counter > 0) {
                    this._global.getWebServiceData("channelcurrencyproductprice", "POST", data, '').subscribe(response => {
                        if(response.status==1){
                            // this._globalService.showToast('Successfully Saved.');
                                that._globalService.showLoaderSpinner(false);

                            if (this.add_edit == 'add') {
                                this._router.navigate(['/products/add/step4']);
                            } else {
                                this._router.navigate(['/products/edit/' + this.formModel.productId + '/step4']);
                            }
                        }else{
                            this._globalService.showToast('Something went wrong. please try later.');

                        }
                    }, err => {
                        this._globalService.showToast('Something went wrong. please try later.');
                    })
                }
            }else{
                this._globalService.showLoaderSpinner(false);
                this._globalService.showToast('Please start & end date.');
            }
        } else {
            this._globalService.showToast('Please configure product price.');
            this._globalService.showLoaderSpinner(false);

        }

    }

    warehouse_change(event){
        var data:any={};
        this.warehouse_id=event.join(',');
        data.warehouse_id=this.warehouse_id;
        data.price_type_id=this.pricetype_id;
        data.website_id=this._globalService.getWebsiteId();
        data.product=this.formModel.productId;

        this._global.getWebServiceData('productwarehouselist', 'POST', data, '').subscribe(data=>{
            if(data.status==1){
                this.productPriceArr=data.api_status;
                this.productPriceArr.forEach(element => {
                    element.data.forEach((item,index) => {
                        item.warehousedata.forEach(el => {
                            el.profit=el.price-el.cost;
                            el.profit=el.profit.toFixed(2);
                            el.margin=(el.profit/el.cost)*100;
                            el.margin=el.margin.toFixed(2);
                            el.price=el.price.toFixed(2);
                            el.cost=el.cost.toFixed(2);
                            el.mrp=el.mrp.toFixed(2);
                            if(el.margin=='NaN'){
                                el.margin=0.0;
                            }
                            if(el.margin=='Infinity'){
                                el.margin=0.0;
                            }
                        });
                    });
                });
            }else{
                this.productPriceArr.length=0;
            }
        })
    }
    pricetype_change(event){
        var data:any={};
        this.pricetype_id=event.join(',');
        data.price_type_id=this.pricetype_id;
        data.warehouse_id=this.warehouse_id;
        data.website_id=this._globalService.getWebsiteId();
        data.product=this.formModel.productId;
        this._global.getWebServiceData('productwarehouselist', 'POST', data, '').subscribe(data=>{
            if(data.status==1){
                this.productPriceArr=data.api_status;
                this.productPriceArr.forEach(element => {
                    element.data.forEach((item,index) => {
                        item.warehousedata.forEach(el => {
                            el.profit=el.price-el.cost;
                            el.profit=el.profit.toFixed(2);
                            el.margin=(el.profit/el.cost)*100;
                            el.margin=el.margin.toFixed(2);
                            el.price=el.price.toFixed(2);
                            el.cost=el.cost.toFixed(2);
                            el.mrp=el.mrp.toFixed(2);
                            if(el.margin=='NaN'){
                                el.margin=0.0;
                            }
                            if(el.margin=='Infinity'){
                                el.margin=0.0;
                            }
                        });
                    });
                });
            }else{
                this.productPriceArr.length=0;
            }
        })
    }

    del_pricetype_row(price_type_index:number,row_index:number){
        this.productPriceArr[price_type_index].data.splice(row_index,1);
    }
    addMoreQuantityRnage(masterIndex, itemIndex, warehouseIndexNumber, productId, warehouseId, priceTypeId) {
        let defaultSettings: any = {}
        defaultSettings.max_quantity = "";
        defaultSettings.min_quantity = "";
        defaultSettings.price = 0;
        defaultSettings.cost = 0;
        defaultSettings.channel_id = 6;
        defaultSettings.product_id = productId;
        defaultSettings.product_price_type = priceTypeId;
        defaultSettings.currency_id = 13; // USD
        defaultSettings.warehouse_id = warehouseId;
        defaultSettings.website_id = this._globalService.getWebsiteId();
    }

    removeQuantity(masterIndex, itemIndex, warehouseIndexNumber, productId, warehouseId, priceTypeId,tableId) {
        this.productPriceArr[masterIndex].data[itemIndex].warehousedata.splice(warehouseIndexNumber, 1); // remove the price columsn
        if(tableId > 0) {
            this.deleteProductPriceIndividual(tableId, 'individual','',0);
        }
    }

    deleteProductPriceIndividual(id: any, actionType:any,warehouseId:any,productTypeId:number) {
        this.dialogsService.confirm('Warning', "Are you sure to delete this?").subscribe(res => {
            if (res) {
                if (actionType == 'individual') {
                    let data: any = {};
                    data["id"] = id;
                    if (id > 0) {
                        this._productService.deletePrice(data).subscribe(result => {

                        }, err => {

                        })
                    }
                } else if (actionType == 'all') {
                    let data: any = {};
                    data["product_id"] = this.formModel.productId;
                    data["product_price_type"] = productTypeId;
                    this._productService.deletePrice(data).subscribe(result => {
                        this.ngOnInit();
                    }, err => {

                    })
                }
            }
        });
    }

    loadPriceTypeMasterData() {
        this.priceMasterList = [];
        let tmpVar: any = {};
        tmpVar.id = 1;
        tmpVar.name = "Regular Price";
        this.priceMasterList.push(tmpVar);
        // tmpVar = {};
        // tmpVar.id = 2;
        // tmpVar.name = "Quantity Price";
        // this.priceMasterList.push(tmpVar);
        // tmpVar = {};
        // tmpVar.id = 3;
        // tmpVar.name = "Label Price";
        // this.priceMasterList.push(tmpVar);
        return this.priceMasterList;
    }    
}

@Component({
    templateUrl: './templates/product_type_master.html',
    providers: [ProductService, Global]
})
export class AddPriceTypeMasterComponent implements OnInit {
    public response: any;
    public errorMsg: string;
    public successMsg: string;
    public formModel: any = {};
    public ipaddress: any;
    public priceMasterList: any = [];
    public productId: number;
    public isbuttonDisable: boolean = false;
    public warehouse_list:any = [];
    public priceTypeId: any;

    visible = true;
    selectable = true;
    removable = true;
    addOnBlur = true;
    public popupLoder: boolean = false;
    readonly separatorKeysCodes: number[] = [ENTER, COMMA];
    warehouseList: warehouseArr[] = [];

    constructor(
        private _globalService: GlobalService,
        private _global: Global,
        private _router: Router,
        private _products: ProductService,
        private dialogRef: MatDialogRef<AddPriceTypeMasterComponent>,
        public dialog: MatDialog,
        @Optional() @Inject(MAT_DIALOG_DATA) public data: any
    ) {
        _global.reset_dialog();

        this.ipaddress = _globalService.getCookie('ipaddress');
    }

    ngOnInit() {
        this.productId = this.data.product_id; // Product Id is coming here 
        this.priceMasterList = this.data.priceMasterList; // Product Id is coming here 
        this.warehouse_list = this.data.warehouselist;   
        if (this.formModel.id > 0) {

        } else {
            this.formModel.id = 0;
        }
        this.formModel.priceTypeId = null;
       // this.webseiteWarehouseList(website_id);
       
    }

    /////// AAPPLY PRICE TYPE IN THE PRODUCT TABLE //////////////////
    addProductType(form: any) {
        this.popupLoder = true;
        this.errorMsg = '';
        var data: any = {};
        data.website_id = this._globalService.getWebsiteId();
        data.name = this.formModel.name;
        data.product_id = this.productId;
        data.price_type_id = this.formModel.priceTypeId; // this is the product type ID
        data.min_quantity = this.formModel.min_quantity;
        data.max_quantity = this.formModel.max_quantity;
        data.warehouse_id = this.formModel.warehouse_id.join(',');
        // cds is working
        this.isbuttonDisable = true;
        let that = this;    
        console.log(data);
            
        this._global.getWebServiceData('productpricetype', 'POST', data, '').subscribe(res => {
            that.isbuttonDisable = false;
            if (res["status"] == 1) {
                this.popupLoder = false;
                that.closeDialog();
                that._globalService.showToast(res["message"]);
            }
        }, err => {

        })
    }

    loadDefaultProductMasterSettings(price_type_id: number) {
        console.log(this.formModel.priceTypeId)
        let data: any = {};
        data.product_id = this.productId;
        data.price_type_id = price_type_id;
        this._global.getWebServiceData('productpricetypelist', 'POST', data, '').subscribe(
            responseData => {
                if (responseData["status"] == 1) {
                    this.formModel.name = responseData.api_status.name;
                    this.formModel.priceTypeId = responseData.api_status.price_type.id;
                    this.formModel.min_quantity = responseData.api_status.min_quantity;
                    this.formModel.max_quantity = responseData.api_status.max_quantity;
                    var ware_house = responseData.api_status.warehouse_id;
                    var array = ware_house.split(",").map(Number);
                    this.formModel.warehouse_id = array;
                }else{
                    this.formModel.name = '';
                }
            }, err => {

            }
        )
    }
    deleteProductPrice(warehouse_id, product_price_type) {
        let productId = this.productId;
        let data: any = {}
        data.warehouse_id = warehouse_id;
        data.product_price_type = product_price_type;
        data.product_id = productId;
        data.website_id = this._globalService.getWebsiteId();
        this._products.deletePrice(data).subscribe(res => {
        }, err => {

        });
    }

    closeDialog() {
        this.dialogRef.close();
    }
    webseiteWarehouseList(website_id) {
        this._global.getWebServiceData('warehousestockmanagement', 'GET', '', website_id).subscribe(
            Res => {
               // this.warehouselist = Res.warehouse;
            }, err => {

            }
        )
    }
}

@Component({
    templateUrl: 'templates/import-product-price-file.html',
    providers: [ProductService,Global]
})
export class ImportProductPriceImportComponent implements OnInit {
    public response: any;
    public errorMsg: string;
    public formModel: any = {};
    public ipaddress: any;
    public sample_xls: any;
    public sample_csv: any;
    public xls_file: any;
    public website_id: any;
    public importOpt: any;
    public file_selection_tool: any;
    private userId: number;
    public parentId: number = 0;
    public tabIndex: number;
    public imported_file_name: string;
    constructor(
        private _globalService: GlobalService,
        private _router: Router,
        private dialogRef: MatDialogRef<ImportProductPriceImportComponent>,
        public dialog: MatDialog,
        private _cookieService: CookieService,
        // private _promotionService: PromotionService,
        private _productService: ProductService,
        private global: Global,
        @Optional() @Inject(MAT_DIALOG_DATA) public data: any
    ) { 
            global.reset_dialog();
        }

    ngOnInit() {
        this.sample_xls = window.location.protocol + '//' + window.location.hostname + ':8062' + '/media/importfile/sample/price_import_sheet.xls';
        this.importOpt = 'xls';
        this.tabIndex = +this._globalService.getCookie('active_tabs');
        this.parentId = this._globalService.getParentTab(this.tabIndex);
        this.file_selection_tool = 'No file choosen';
        let userData = this._cookieService.getObject('userData');
        this.userId = userData['uid'];
        this.website_id = this._globalService.getWebsiteId();
    }

    import_file_promotion(e: Event) {
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
        this.file_selection_tool = filename;
        this.xls_file = files.import_file._file;
        var extn = filename.split(".").pop();
        if (extn == 'xls' || extn == 'xlsx') {
        } else {
            this._globalService.showToast('Please choose XLS/XLSX file');
        }
    }

    send_file_data(form: any) {
        var form_data = new FormData();
        form_data.append("import_file", this.xls_file);
        form_data.append('website_id', this.website_id);
        form_data.append("import_file_type", 'price');
        if (this.xls_file != undefined) {
            
            this._productService.import_product_price(form_data).subscribe(
                data => {
                    this.response = data;
                    this.imported_file_name = data.filename;
                    this._cookieService.putObject('produce_price_imported_data', '');
                    // this.save_promotion_file_data();
                    this._globalService.showToast('Price will be updated soon.');
                    this.dialogRef.close();
                    this._globalService.showLoaderSpinner(false);
                    
                },
                err => console.log(err)
            );
        } else {
            this._globalService.showToast('Please choose XLS/XLSX file');
            
        }
    }
    save_promotion_file_data() {
        
        setTimeout(() => {
            // this._globalService.showLoaderSpinner(true);
        });
        var data: any = {};
        var form_data: any = {};
        data.website_id = this._globalService.getWebsiteId();
        data.filename = this.imported_file_name;
        data.category_id = 3;
        this._productService.save_product_price(data).subscribe(
            res => {
                this.response = data;
                let imported_result: any = {};
                this._cookieService.putObject('produce_price_imported_data', '');
                imported_result.imported_filename = this.imported_file_name;
                imported_result.website_id = this._globalService.getWebsiteId();
                this._cookieService.putObject('produce_price_imported_data', imported_result);
                this._globalService.addTab('priviewproductsprice', 'products/preview_product_price', 'Preview Price', this.parentId)
                this._router.navigate(['/products/preview_product_price']);
                this._globalService.showLoaderSpinner(false);
                this._globalService.showToast('Price will be updated soon.');
                
            },
            err => {
                this._globalService.showLoaderSpinner(false);

                this._globalService.showToast('Something went wrong. Please try again.');
            },
            function () {
                //completed callback
            }
        )
    }

    closeDialog() {
        this.dialogRef.close();
    }
}

@Component({
    selector: 'my-app',
    templateUrl: `./templates/product_price_preview.html`,
    providers: [Global, ProductService],
})

export class ProductPricePreviewComponent implements OnInit {

    constructor(
        public globalService: GlobalService,
        // private _globalService: GlobalService,
        private _cookieService: CookieService,
        public dialog: MatDialog,
        // private _promotionService: PromotionService,
        private _productService: ProductService,        
        private dialogsService: DialogsService,
        private _router: Router,
        @Inject(DOCUMENT) private document: any
    ) { }

    public response: any;
    public errorMsg: string;
    public bulk_ids: any = [];
    public columns: any = [];
    public temp_result_list: any = [];
    public result_list: any = [];
    public selectedAll: any = false;
    public tabIndex: number;
    public parentId: number = 0;
    public userId: any;
    public individualRow: any = {};
    //////////////////////////Initilise////////////////////////////

    ngOnInit() {

        this.tabIndex = +this.globalService.getCookie('active_tabs');
        this.parentId = this.globalService.getParentTab(this.tabIndex);
        let userData = this._cookieService.getObject('userData');
        let produce_price_imported_data = this._cookieService.getObject('produce_price_imported_data');
        this.userId = userData['uid'];
        let post_data: any = {};
        post_data.filename = produce_price_imported_data['imported_filename'];
        post_data.website_id = this.globalService.getWebsiteId();//produce_price_imported_data.website_id;
        post_data.model = 'discount';
        this.columns = [
            { 'field_name': 'sku', 'label': 'SKU' },
            { 'field_name': 'warehouse_code', 'label': 'Warehouse Code' },
            { 'field_name': 'price_type', 'label': 'Price Type' },
            { 'field_name': 'price', 'label': 'Price' },
            { 'field_name': 'cost', 'label': 'Cost' },
            { 'field_name': 'mrp', 'label': 'MRP' },
            { 'field_name': 'min_quantity', 'label': 'Min Quantity' },
            { 'field_name': 'max_quantity', 'label': 'Max Quantity' },
            { 'field_name': 'start_date', 'label': 'Start Date' },
            { 'field_name': 'end_date', 'label': 'End Date' },
        ]
        this._productService.load_product_price_preview_grid(post_data, 1).subscribe(
            data => {
                this.temp_result_list = data.preview_data;
                console.log(data);
                
                let that = this;
                this.temp_result_list.forEach(function (item: any) {
                    if (item.err_flag == 0) {
                        item.selected = true;
                    }
                    if (item.selected && item.err_flag == 0) {
                        that.bulk_ids.push(item.id);
                        //elements[0].classList.add('show');
                    } else {
                        //elements[0].classList.remove('show');
                    }
                });
            },
            err => {
                this.globalService.showToast('Something went wrong. Please try again.');
            },
            function () {
                //completed callback
            }
        );
    }

    ////////////////////////////Check/Uncheck//////////////

    toggleCheckAllPreview(event: any) {
        let that = this;
        that.bulk_ids = [];
        this.selectedAll = event.checked;
        this.temp_result_list.forEach(function (item: any) {
            item.selected = event.checked;
            if (item.selected && item.err_flag == 0) {
                that.bulk_ids.push(item.id);
                //elements[0].classList.add('show');
            } else {
                //elements[0].classList.remove('show');
            }
        });
    }

    toggleCheckPreview(id: any, event: any) {
        let that = this;
        this.temp_result_list.forEach(function (item: any) {
            if (item.id == id) {
                item.selected = event.checked;
                if (item.selected && item.error == 0) {
                    that.bulk_ids.push(item.id);
                } else {
                    var index = that.bulk_ids.indexOf(item.id);
                    that.bulk_ids.splice(index, 1);
                    if (that.bulk_ids.length == 0) {
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
    }

    ImportPriceData(form: any) {
        if (this.bulk_ids.length > 0) {
            var msg = 'Are you sure to import selected price?';
            this.dialogsService.confirm('Warning', msg).subscribe(res => {
                if (res) {
                    setTimeout(() => {
                        this.globalService.showLoaderSpinner(true);
                    });
                    let post_data: any = {};
                    let produce_price_imported_data = this._cookieService.getObject('produce_price_imported_data');
                    post_data.filename = produce_price_imported_data['imported_filename'];
                    post_data.website_id = this.globalService.getWebsiteId();
                    post_data.selected_ids = this.bulk_ids.join(); // convert array to string for selected ids
                    this._productService.show_all_product_price_imported(post_data).subscribe(
                        data => {
                            this.globalService.showLoaderSpinner(false);
                            this.globalService.deleteTab(this.tabIndex, this.parentId);
                            
                        },
                        err => {
                            this.globalService.showToast('Something went wrong. Please try again.');
                            this.globalService.showLoaderSpinner(false);
                            
                        },
                        function () {
                        }
                    );
                }
            });
        } else {
            this.dialogsService.alert('Error', ' Please select atleast one record!').subscribe(res => { });
        }
    }
}