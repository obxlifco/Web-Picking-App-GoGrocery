import { Component, ElementRef, OnInit, Input, Inject, AfterViewInit, Optional } from '@angular/core';
import { GlobalService } from '../../global/service/app.global.service';
import { CookieService } from 'ngx-cookie';
import { DOCUMENT } from '@angular/platform-browser';
import { Global } from '../../global/service/global';
import { Router, ActivatedRoute } from '@angular/router';
import { AddEditTransition } from '../.././addedit.animation';
import { ProductService } from '../product/products.product.service';
import { PopupImgDirective, ImageUploadUrlDialog } from '../.././global/directive/popup-image.directive';
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material';
import { GlobalVariable } from '../../global/service/global';
import { ProductListComponent } from '../promotion/products.promotion.conditions.component';
import { PromotionService } from '../promotion/products.promotion.service';
import { DialogsService } from '../../global/dialog/confirm-dialog.service';

@Component({
    selector: 'app-category-banner-addedit',
    templateUrl: './templates/category-banner-addedit.component.html',
    styleUrls: ['./templates/category-banner-addedit.component.css'],
    animations: [AddEditTransition],
    host: {
        '[@AddEditTransition]': ''
    },
    providers: [ProductService]
})
export class CategoryBannerAddeditComponent implements OnInit {
    public response: any;
    public errorMsg: string;
    public successMsg: string;
    public formModel: any = {};
    private sub: any;
    public tabIndex: number;
    public parentId: number = 0;
    public userId: any;
    public method: string;
    public post_url;
    public category_list: any = [];
    public imgsubscriber: any;
    public image_array: any = [];
    public linkBannerData:any=[];
    public home_image_rows:any=[{'start_date':'','end_date':''}];
    public catgory_home_mobile_image=[];
    public catgory_home_desktop_image=[];
    public categoryBanner:any=[];
    public warehouseList:any = [];
    public selected_warehouses:any = [];
    public bannerId:any;
    constructor(
        public _globalService: GlobalService,
        private global: Global,
        private _router: Router,
        private _route: ActivatedRoute,
        private _cookieService: CookieService,
        private _productService: ProductService,
        private dialogsService: DialogsService,
        public dialog: MatDialog,

    ) {}
    
    ngOnInit() {
        this.formModel['catgory_banner_image'] = [];
        this.formModel['catgory_home_desktop_image'] = [];
        this.formModel['catgory_home_mobile_image'] = [];
        
        let userData = this._cookieService.getObject('userData');
        this.userId = userData['uid'];
        
        this.formModel.banner_type = 1;
        this.tabIndex = +this._globalService.getCookie('active_tabs');
        this.parentId = this._globalService.getParentTab(this.tabIndex);
        this.sub = this._route.params.subscribe(params => {
            this.formModel.formId = +params['id']; // (+) converts string 'id' to a number
            this.bannerId = this.formModel.formId;
        });
        this.load_category();
        this.add_more_image(); // pushing first select object for home page banner
        this.getWarehouseList();
        // 1=category
        // 2=home
        if (this.formModel.formId > 0) {
            this.global.getWebServiceData('categorybanner','GET','',this.formModel.formId).subscribe(
                data => {
                    if(data["status"] == 1) { // 
                        let responses = data.api_status;
                        this.formModel.banner_type = responses.banner_type == "C" ? 'category': 'home';
                        this.formModel.bannerId = responses.id;
                        this.formModel.banner_name = responses.banner_name;

                        // let warehouse_ids = responses.category_id.join(',');
                        // let warehouse_ids = responses.category_id;
                        // var array = responses.category_id.split(",").map(Number);
                        // this.formModel.category_id = array;
                        this.formModel.category_id = responses.category_id;
                        this.selected_warehouses = responses.warehouse_id.map(function (item) {
                            return item.id;
                        });
                        console.log(this.selected_warehouses);
                        
                        if (responses.warehouse != null) {
                            this.formModel.warehouse_id = responses.warehouse.id;
                        } else {
                            this.formModel.warehouse_id = null ;
                        }
                        
                        if (responses.banner_type == 'C') {
                            responses.category_banners_images.forEach(element => {
                                element.url = element.image_url + '200x200/' + element.primary_image_name;
                            });
                            this.formModel.catgory_banner_image = responses.category_banners_images;
                        } else { // assign home page data
                            responses.category_banners_images.forEach(element => {
                                if (element.web != undefined) {
                                    element.web.url = element.web.image_url + '200x200/' + element.web.primary_image_name;
                                } else {
                                    //element.web.url = "";
                                }
                                if (element.mobile != undefined) {
                                    element.mobile.url = element.mobile.image_url + '200x200/' + element.mobile.primary_image_name;
                                } else {
                                    //element.mobile.url = "";
                                }
                                

                            });
                            this.formModel.catgory_home_desktop_image = responses.category_banners_images;
                            console.log(this.formModel.catgory_home_desktop_image);
                        }
                        console.log(this.formModel);
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
            this.bannerId = 0;
            this.formModel.banner_type = 'category';
        }
    }

    getWarehouseList() {
        let userId = this._globalService.getUserId();
        let websiteId = this._globalService.getWebsiteId();
        this._productService.warehouseLoad(websiteId, userId).subscribe(
            result => {
                this.warehouseList = result["warehouse"];
            }, err => {

            });
    }
    

    dialogRef: MatDialogRef<PopupImgDirective> | null;
    openImagePop(imgFor: string, multiple: boolean = false, i) {
        let websiteId:any = this._globalService.getWebsiteId();
        let data = {
            imgFor: imgFor,
            is_multiple: multiple,
            type: 'category'
        };
        this.dialogRef = this.dialog.open(PopupImgDirective, {
            data: data
        });
        this.dialogRef.afterClosed().subscribe(res => {
            //console.log(result);
            if (res != undefined) {
                let result = res;
                let data: any = {}
                data.website_id = this._globalService.getWebsiteId();
                data.imageType = 'CategoryBanner'
                var form_data = new FormData();
                setTimeout(() => {
                    this._globalService.showLoaderSpinner(true);
                });
                if (result.hasOwnProperty('catgory_banner_image')) { // this is the category page image
                    var other_files = [];
                    result.catgory_banner_image.forEach(element => {
                        if (element._file ) {
                            //element.newImage = 1;
                            //this.formModel.catgory_banner_image.push(element);
                            other_files.push(element._file);
                        }
                    });
                    other_files.forEach(function (item: any) {
                        form_data.append('catgory_banner_image', item);
                    });
                    form_data.append('website_id', websiteId);
                    form_data.append('imageType', 'CategoryBanner');
                    let that = this;
                    this.global.uploadFile('upload-image','POST',form_data).subscribe(
                        results => { // Assign the Uploaded data into formModel
                            setTimeout(() => {
                                this._globalService.showLoaderSpinner(false);
                            });
                            results.data.forEach(function (items: any, key: any) { 
                                // console.log(items);
                                let newItemObj:any={};
                                newItemObj.primary_image_name = items.file_name;
                                newItemObj.url = GlobalVariable.S3_URL+'CategoryBanner/200x200/' + items.file_name;
                                that.formModel.catgory_banner_image.push(newItemObj);
                            });
                            /*
                            this.formModel.catgory_banner_image.forEach(function (items: any,key:any) { 
                                items.primary_image_name = results.data[key].file_name;
                            });*/
                            // console.log(this.formModel);
                        },
                        err => {
                            setTimeout(() => {
                                this._globalService.showLoaderSpinner(false);
                            });
                        }
                    )
                }


                if (result.hasOwnProperty('catgory_home_desktop_image')) {   // this is for desktop banner image
                    this.formModel.catgory_home_desktop_image[i].web.url = result.catgory_home_desktop_image[0].url;
                    form_data.append('catgory_banner_image', result.catgory_home_desktop_image[0]._file);    
                    form_data.append('website_id', websiteId);
                    form_data.append('imageType', 'CategoryBanner');
                    this.global.uploadFile('upload-image', 'POST', form_data).subscribe(
                        results => { // Assing the Uploaded data into formModel
                            this.formModel.catgory_home_desktop_image[i].web.primary_image_name = results.data[0].file_name;
                            setTimeout(() => {
                                this._globalService.showLoaderSpinner(false);
                            });
                        },
                        err => {

                            setTimeout(() => {
                                this._globalService.showLoaderSpinner(false);
                            });
                        }
                    )
                }

                if (result.hasOwnProperty('catgory_home_mobile_image')) { // this is for mobile banner 
                    this.formModel.catgory_home_desktop_image[i].mobile.url = result.catgory_home_mobile_image[0].url;
                    form_data.append('catgory_banner_image', result.catgory_home_mobile_image[0]._file);   
                    form_data.append('website_id', websiteId);
                    form_data.append('imageType', 'CategoryBanner');
                    this.global.uploadFile('upload-image', 'POST', form_data).subscribe(
                        results => { // Assign the Uploaded data into formModel
                            console.log(data);
                            this.formModel.catgory_home_desktop_image[i].mobile.primary_image_name = results.data[0].file_name;
                            setTimeout(() => {
                                this._globalService.showLoaderSpinner(false);
                            });
                        },
                        err => {
                            setTimeout(() => {
                                this._globalService.showLoaderSpinner(false);
                            });
                        }
                    )
                }
            }
        });
    }

    categoryBannerAddEdit() {
        let data:any={};
        if (this.formModel.banner_type == 'category') { // category Banner data
            data.website_id = this._globalService.getWebsiteId();
            data.banner_name = this.formModel.banner_name;
            console.log(this.formModel.category_id)
            data.category_id = this.formModel.category_id;
            data.banner_type = this.formModel.banner_type;
            //data.warehouse_id = this.formModel.warehouse_id;
            data.warehouse_id = this.selected_warehouses.join(",");
            if (this.formModel.bannerId > 0) {
                data.banner_id = this.formModel.bannerId;
            }
            let catgory_banner_image:any = [];
            this.formModel.catgory_banner_image.forEach(element => {
                let imageData: any = {};
                imageData.primary_image_name = element.primary_image_name;
                imageData.id = element.id;
                imageData.banner_linkto = element.banner_linkto;
                imageData.item_ids = element.item_ids;
                imageData.link = element.external_link;
                imageData.banner_caption1 = element.banner_caption1;
                imageData.banner_caption2 = element.banner_caption1;       
                imageData.start_date = '';
                imageData.end_date = '';
                catgory_banner_image.push(imageData);
            });
            data.catgory_banner_image = catgory_banner_image;
            console.log(data);
            this.global.getWebServiceData('categorybanner-new','POST',data,'').subscribe(response => {
                if (response["status"] == 1) {
                    this._globalService.showToast(response.message);
                    this._router.navigate(['/category-banner/']);
                } else {
                    this._globalService.showToast(response.message);
                }
            } ,err => {

            }) 
        } else { // home page banner 
            data.website_id = this._globalService.getWebsiteId();
            data.banner_name = this.formModel.banner_name;
            data.banner_type = this.formModel.banner_type;
            data.warehouse_id = this.formModel.warehouse_id;
            if (this.formModel.bannerId > 0) {
                data.banner_id = this.formModel.bannerId;
            }
            let catgory_banner_image: any = [];
            this.formModel.catgory_home_desktop_image.forEach(element => {
                let imageDataWeb: any = {};
                imageDataWeb.primary_image_name = element.web.primary_image_name;
                imageDataWeb.id = element.id;
                imageDataWeb.banner_linkto = element.web.banner_linkto;
                imageDataWeb.item_ids = element.web.item_ids;
                imageDataWeb.link = element.web.external_link != undefined ? element.web.external_link : '';
                imageDataWeb.banner_caption1 = element.web.banner_caption1 != undefined ? element.web.banner_caption1 : '';
                imageDataWeb.banner_caption2 = element.web.banner_caption2 != undefined ? element.web.banner_caption2 : '';
                imageDataWeb.start_date = element.web.start_date;
                imageDataWeb.end_date = element.web.end_date;
                let imageDataMobile: any = {};
                imageDataMobile.primary_image_name = element.mobile.primary_image_name;
                imageDataMobile.id = element.id;
                imageDataMobile.banner_linkto = element.mobile.banner_linkto;
                imageDataMobile.item_ids = element.mobile.item_ids;
                imageDataMobile.link = element.mobile.external_link != undefined ? element.mobile.external_link : '';
                imageDataMobile.banner_caption1 = element.mobile.banner_caption1 != undefined ? element.mobile.banner_caption1 : '';
                imageDataMobile.banner_caption2 = element.mobile.banner_caption2 != undefined ? element.mobile.banner_caption2 : '';
                imageDataMobile.start_date = element.mobile.start_date;
                imageDataMobile.end_date = element.mobile.end_date;
                let bannerData:any = {};
                bannerData.web = imageDataWeb;
                bannerData.mobile = imageDataMobile;
                catgory_banner_image.push(bannerData);
            });
            data.catgory_banner_image = catgory_banner_image;
            console.log(data);
            this.global.getWebServiceData('categorybanner-new', 'POST', data, '').subscribe(response => {
                if (response["status"] == 1) {
                    this._globalService.showToast(response.message);
                    this._router.navigate(['/category-banner/']);
                } else {
                    if (response == 'primary_image_name') {
                        this._globalService.showToast("Select a image");
                    } else {
                        this._globalService.showToast(response.message);
                    }
                }
            }, err => {
            })
        }
    }
    
    
    delImg (is_remove: number, scope_var: string, file_var: string, is_arr: number, index: number) {
        this.dialogsService.confirm('Warning', 'Are you sure to remove this?').subscribe(res => {
            if (res) {
                if (is_remove > 0) {
                    var form_data: any = {};
                    form_data.id = is_remove;
                    //form_data.field = file_var;
                    //form_data.file_name = this[scope_var][file_var]['name'];
                    this._productService.categoryBannerDelete(form_data).subscribe(
                        data => {
                            this.response = data;
                            if (this.response.status == 1) {
                                this._globalService.showToast(this.response.message);
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
            }
        });
    };



    dialogRefLinkBanner: MatDialogRef<linkBannerComponent> | null;
    linkBanner(columnIndex:any,bannerType:any) { 
        if (bannerType == 'Category') {
            this.dialogRefLinkBanner = this.dialog.open(linkBannerComponent, {
                data: { index: columnIndex, settingData: this.formModel.catgory_banner_image[columnIndex] },
                height: '500px',
                width: '600px',
            });
            this.dialogRefLinkBanner.afterClosed().subscribe(result => {
                if (result != undefined && result != '') {
                    let bannerData: any = {}
                    this.formModel.catgory_banner_image[columnIndex].banner_linkto = result.banner_linkto;
                    this.formModel.catgory_banner_image[columnIndex].external_link = result.external_link;
                    this.formModel.catgory_banner_image[columnIndex].link = result.external_link;
                    this.formModel.catgory_banner_image[columnIndex].banner_caption1 = result.banner_caption1;
                    this.formModel.catgory_banner_image[columnIndex].banner_caption2 = result.banner_caption2;
                    //this.formModel.catgory_banner_image[columnIndex].column_index = result.column_index;
                    this.formModel.catgory_banner_image[columnIndex].index = result.index;
                    this.formModel.catgory_banner_image[columnIndex].item_ids = result.item_ids;
                    this.formModel.catgory_banner_image[columnIndex].send_notification = result.send_notification;
                }
            })
        } else {
            if (bannerType == 'Web') {
                this.dialogRefLinkBanner = this.dialog.open(linkBannerComponent, {
                    data: { index: columnIndex, settingData: this.formModel.catgory_home_desktop_image[columnIndex].web },
                    height: '500px',
                    width: '600px',
                });
                this.dialogRefLinkBanner.afterClosed().subscribe(result => {
                    if (result != undefined && result != '') {
                        this.formModel.catgory_home_desktop_image[columnIndex].web.banner_linkto = result.banner_linkto;
                        this.formModel.catgory_home_desktop_image[columnIndex].web.external_link = result.external_link;
                        this.formModel.catgory_home_desktop_image[columnIndex].web.link = result.external_link;
                        this.formModel.catgory_home_desktop_image[columnIndex].web.banner_caption1 = result.banner_caption1;
                        this.formModel.catgory_home_desktop_image[columnIndex].web.banner_caption2 = result.banner_caption2;
                        //this.formModel.catgory_home_desktop_image[columnIndex].web.column_index = result.column_index;
                        this.formModel.catgory_home_desktop_image[columnIndex].web.index = result.index;
                        this.formModel.catgory_home_desktop_image[columnIndex].web.item_ids = result.item_ids;
                        this.formModel.catgory_home_desktop_image[columnIndex].web.send_notification = result.send_notification;
                    }
                })
            }

            if (bannerType == 'Mobile') {
                this.dialogRefLinkBanner = this.dialog.open(linkBannerComponent, {
                    data: { index: columnIndex, settingData: this.formModel.catgory_home_desktop_image[columnIndex].mobile },
                    height: '500px',
                    width: '600px',
                });
                this.dialogRefLinkBanner.afterClosed().subscribe(result => {
                    if (result != undefined && result != '') {
                        this.formModel.catgory_home_desktop_image[columnIndex].mobile.banner_linkto = result.banner_linkto;
                        this.formModel.catgory_home_desktop_image[columnIndex].mobile.external_link = result.external_link;
                        this.formModel.catgory_home_desktop_image[columnIndex].mobile.link = result.external_link;
                        this.formModel.catgory_home_desktop_image[columnIndex].mobile.banner_caption1 = result.banner_caption1;
                        this.formModel.catgory_home_desktop_image[columnIndex].mobile.banner_caption2 = result.banner_caption2;
                        //this.formModel.catgory_home_desktop_image[columnIndex].mobile.column_index = result.column_index;
                        this.formModel.catgory_home_desktop_image[columnIndex].mobile.index = result.index;
                        this.formModel.catgory_home_desktop_image[columnIndex].mobile.item_ids = result.item_ids;
                        this.formModel.catgory_home_desktop_image[columnIndex].mobile.send_notification = result.send_notification;
                    }
                })
            }
        }
    }
    
    del_image(index:number,bannerType:any){
        this.dialogsService.confirm('Warning', 'Are you sure to remove this?').subscribe(res => {
            if (res) {
                if (bannerType == 'Web') { // Remove image data from Web
                    this.formModel.catgory_home_desktop_image[index].web.url = '';
                }
                if (bannerType == 'Mobile') { // Remove image data mobile
                    this.formModel.catgory_home_desktop_image[index].mobile.url = '';
                }
            }
        });        
    }

    del_img_row(index:number) {
        console.log(index);
        console.log(this.formModel.catgory_home_desktop_image);
        if( index ==0 && this.formModel.catgory_home_desktop_image.length==1){
            this.formModel.catgory_home_desktop_image.splice(index,1);
            this.formModel.catgory_home_desktop_image=[{'start_date':'','end_date':''}];
        } else {
            this.formModel.catgory_home_desktop_image.splice(index,1);
        }
    }
    
    add_more_image(){
        var start_date = new Date(); 
        var end_date = new Date(); 
        end_date.setDate(end_date.getDate() + 30); // Set now + 30 days as the new date
        console.log(end_date);
        let newElements={
            web: { url: '', start_date: start_date, end_date: end_date, banner_linkto: 'external link', link: '', caption1: '', caption2: '', column_index: '', item_ids: '', send_notification: ''},
            mobile: { url: '', start_date: start_date, end_date: end_date, banner_linkto: 'external link', link: '', caption1: '', caption2: '', column_index: '', item_ids: '', send_notification: ''}
        }
        this.formModel.catgory_home_desktop_image.push(newElements);
        //console.log(this.formModel.catgory_home_desktop_image);
    }

    load_category() {
        this._productService.productBasicInfoLoad().subscribe(
            data => {
                this.category_list = data.category;
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
    templateUrl: './templates/link-banner.html',
    providers: [ProductService, Global]
})
export class linkBannerComponent implements OnInit {
    public response: any;
    public errorMsg: string;
    public successMsg: string;
    public formModel: any = {};
    public ipaddress: any;
    public bannerId: number;
    public bannerLinkDataArr=[];
    public all_item_ids: any;
    item_ids:any
    promotion_arr=[];
    public userId: any;
    public popupLoder:boolean = false;
    public category_list:any = [];
    constructor(
        private _globalService: GlobalService,
        private _global: Global,
        private _router: Router,
        private _products: ProductService,
        private _cookieService: CookieService,
        private dialogRef: MatDialogRef<linkBannerComponent>,
        public dialog: MatDialog,
        @Optional() @Inject(MAT_DIALOG_DATA) public data: any
    ) {
        _global.reset_dialog();
        this.ipaddress = _globalService.getCookie('ipaddress');
    }

    ngOnInit() {
        let exsitingData = this.data.settingData;
        console.log("Load Existing Data");
        console.log(exsitingData);
        this.formModel.applicable_for = exsitingData.applicable_for; 
        this.formModel.send_notification='no';
        this.formModel.banner_linkto = exsitingData.banner_link_to;
        if (this.formModel.banner_linkto== '') {
            this.formModel.banner_linkto='external link';
        }        
        this.formModel.external_link = exsitingData.link;
        this.formModel.banner_caption1 = exsitingData.banner_caption1;
        if (this.formModel.banner_linkto == 'promotion') {
            this.load_promotion();
            this.formModel.item_ids = exsitingData.promotion_id;
        }
        if (this.formModel.banner_linkto == 'category') {
            this.formModel.item_ids = +exsitingData.category_id;
            //this.getCategoryDetails(this.formModel.item_ids);
        }
        this.formModel.banner_caption2 = exsitingData.banner_caption2;

        console.log(this.formModel);
        let userData = this._cookieService.getObject('userData');
        this.userId = userData['uid'];
        this.loadCategory();        
    }
    senBannerLinkData(form:any){
        var data: any = {};
        data.column_index = this.data.column_index;
        data.index=this.data.index;
        data.banner_linkto = this.formModel.banner_linkto;
        data.external_link = this.formModel.external_link;
        data.item_ids = this.formModel.item_ids;
        data.banner_caption1 = this.formModel.banner_caption1;
        data.banner_caption2 = this.formModel.banner_caption2;
        data.send_notification = this.formModel.send_notification;
        console.log("=====================");
        console.log(data);
        this.closeDialog(data)
    }

    closeDialog(data:any='') {
        this.dialogRef.close(data);
    }

    loadBannerSettingsData(bannerFor:any) {
        if (bannerFor == 'promotion') {
            this.openPopup(2);
        }
    }
    openPopup(type:number) {
        let data: any = {};
        this.popupLoder = true;
        if(type==3) {
            this.item_ids=null;
            data['all_item_ids'] = this.all_item_ids;
            this.dialogCatBannerRef = this.dialog.open(CatBannerProductListComponent, { data: data });
            this.dialogCatBannerRef.afterClosed().subscribe(result => {
                if (result) {
                    this.popupLoder = false;
                    console.log(result)
                    this.formModel.item_ids = result.product_names;
                    this.item_ids = result.product_ids;
                }
            }); 
        }
        if(type==2){
            //PROMOTIONS
            this.load_promotion();
            this.item_ids=null;
            this.item_ids = this.formModel.item_ids;
            console.log(this.item_ids);
            this.popupLoder = false;
        }
        if( type==1 ) {
            //CATEGORY LIST
            this.item_ids=null;
            data['all_item_ids'] = this.all_item_ids;
            this.dialogCatBannerCatRef = this.dialog.open(CatBannerCategoryListComponent, { data: data });
            this.dialogCatBannerCatRef.afterClosed().subscribe(result => {
                if (result) {
                    console.log("************ Category banner data **************");
                    console.log(result)
                    this.formModel.item_ids = result.category_names;
                    this.item_ids = result.category_ids;
                }
                this.popupLoder = false;
            }); 
        }
        
    }

    dialogCatBannerRef: MatDialogRef<CatBannerProductListComponent> | null;
    dialogCatBannerCatRef: MatDialogRef<CatBannerCategoryListComponent> | null;

    load_promotion() {
        this.popupLoder = true;
        let data={
            "model": "EngageboostDiscountMasters",
            "screen_name": "list2",
            "userid": 1,
            "search": "",
            "order_by": "",
            "order_type": "",
            "status": "",
            "website_id": this._globalService.getWebsiteId(),
            "show_all": 1
          }
        this._global.getWebServiceData('global_list','POST',data,'').subscribe(res => {
            if(res){
                this.popupLoder = false;
                let resultSet = res[0].result;
                //console.log(resultSet);
                this.promotion_arr = resultSet;
                
            } else {
                this._globalService.showToast('Something went wrong. Please try again.'); 
            }
            
        }, err => {
            console.log(err)
        })
    }

    loadCategory() {
        let data = {
            "model": "EngageboostCategoryMasters",
            "screen_name": "list",
            "userid": 1,
            "search": "",
            "order_by": "",
            "order_type": "",
            "status": "",
            "website_id": this._globalService.getWebsiteId(),
            "show_all": 1
        }
        this._global.getWebServiceData('global_list', 'POST', data, '').subscribe(res => {
            if (res) {
                let resultSet = res[0].result;
                this.category_list = resultSet;
            } else {
                this._globalService.showToast('Something went wrong. Please try again.');
            }

        }, err => {
            console.log(err)
        })
    }

    getCategoryDetails(categoryId: number) {
        this._global.getWebServiceData('category', 'GET', '', categoryId ).subscribe(res => {
            if (res) {
                this.formModel.item_ids = res.api_status.name;
                this.item_ids = res.api_status.id;
            } else {
                this._globalService.showToast('Something went wrong. Please try again.');
            }

        }, err => {
            console.log(err)
        })
    }
}


@Component({
    templateUrl: './templates/products.html',
    providers: [ProductService]
})
export class CatBannerProductListComponent implements OnInit {
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
    public orderId: number;
    public webshop_id: any;
    showSkeletonLoaded: boolean = false;
    public temp_result = [];
    public temp_col = [];
    constructor(
        public _globalService: GlobalService,
        private _productService: ProductService,
        public dialog: MatDialog,
        private _cookieService: CookieService,
        @Inject(DOCUMENT) private document: any,
        public dialogRef: MatDialogRef<CatBannerProductListComponent>,
        @Optional() @Inject(MAT_DIALOG_DATA) public data: any
    ) {

    }

    ngOnInit() {
        if (this.data) {
            this.webshop_id = this.data.webshop_id;
            // this.index = this.data.index;
            this.userId = this.data.userId;
            if (this.data['all_product_id']) {
                this.bulk_ids = this.data['all_product_id'].split(",").map(Number);
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
        this._productService.getProductsES(elasticData, websiteId).subscribe(
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
        this.bulk_ids.forEach(function (item: any) {
            that.product_list.forEach(function (inner_item: any) {
                if (item == inner_item.id) {
                    products.push(inner_item.sku);
                }
            });
        });
        product_names = products.join(',');
        returnData['product_ids'] = product_ids;
        //console.log(returnData);
        this.dialogRef.close(returnData);
    }
}

@Component({
	templateUrl: './templates/categories.html',
	providers: [PromotionService]
})
export class CatBannerCategoryListComponent implements OnInit {

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
		private dialogRef: MatDialogRef<CatBannerCategoryListComponent>,
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
						}
						else {
							this.sub_child_category_list[index] = [];
							this.sub_sub_child_category_list[index] = [];
							this.sub_child_category_list[index] = this.response.category;
							this.formModel.parent_categories[index].category_3 = 0;
							this.formModel.parent_categories[index].category_4 = 0;
						}
					}
					else { //level 3 category
						if (reset == 0) {
							this.sub_sub_child_category_list[index] = this.response.category;
						}
						else {
							this.sub_sub_child_category_list[index] = [];
							this.sub_sub_child_category_list[index] = this.response.category;
							this.formModel.parent_categories[index].category_4 = 0;
						}
					}
				} else { }
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