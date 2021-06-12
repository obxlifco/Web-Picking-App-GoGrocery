import {Component, ElementRef, OnInit, Input, Inject, AfterViewInit, Optional, ɵConsole } from '@angular/core';
import { GlobalService } from '../../global/service/app.global.service';
import { CookieService } from 'ngx-cookie';
import { Global } from '../../global/service/global';
import { Router, ActivatedRoute } from '@angular/router';
import { AddEditTransition, AddEditStepFlipTransition } from '../.././addedit.animation';
import { OrderService } from '../../order/order/order.order.service';
@Component({
    selector: 'app-review.addedit',
    templateUrl: 'templates/review.addedit.html',
    animations: [AddEditTransition],
    host: {
        '[@AddEditTransition]': ''
    },
    providers: [OrderService]
})

export class ReviewAddeditComponent implements OnInit {
    public currentRate:number = 0;
    public currentRateValidate:boolean= true;
    public ipaddress: any;
    public response: any;
    public errorMsg: string;
    public successMsg: string;
    public formModel: any = {};
    private sub: any;
    public tabIndex: number;
    public parentId: number = 0;
    public userId: any;
    public country_list: any = [];
    public state_list:any=[];
    public customer_list:any=[];
    public productsList:any =[];
    public selectedProductData:Object = {};
    public cus_field_mode:boolean = false;
    public sku;
    constructor(
        public _globalService: GlobalService,
        private _orderService:OrderService,
        private global: Global,
        private _router: Router,
        private _route: ActivatedRoute,
        private _cookieService: CookieService,
    ) {
        this.ipaddress = _globalService.getCookie('ipaddress');
    }
    ngOnInit() {
        let userData = this._cookieService.getObject('userData');
        this.userId = userData['uid'];

        this.tabIndex = +this._globalService.getCookie('active_tabs');
        this.parentId = this._globalService.getParentTab(this.tabIndex);
        this.sub = this._route.params.subscribe(params => {
            this.formModel.formId = +params['id']; // (+) converts string 'id' to a number
        });
        this._orderService.loadCountry().subscribe(res=>{
           this.country_list=res.countrylist;
        });
        if (this.formModel.formId > 0) {
            this.global.getWebServiceData('reviews','GET','',this.formModel.formId).subscribe(Response => {
                this.cus_field_mode = true;
                let data=Response.api_status;
                //console.log(data.user_country);
                this.formModel.customer_name = data.user_name;
                this.formModel.customer_id = data.user.id;
                this.formModel.product_id = data.product.id;
                this.formModel.product_name = data.product.name;
                this.formModel.sku = data.product.sku;
                this.formModel.city = data.user_city;
                if(data.user_state == null){
                    this.formModel.state = null;
                }else{
                    this.formModel.state= +data.user_state;
                }
                if(data.user_country == null){
                    this.formModel.country = null;
                }else{
                    this.formModel.country = +data.user_country;
                }
                this.formModel.title = data.title;
                this.formModel.description = data.review;
                this.currentRate = data.rating;
                if(this.formModel.country = null){
                    this.get_state(0);
                }else{
                    this.get_state(this.formModel.country);
                }
                //console.log(this.currentRate);
            }, err => {
                console.log(err)
            })
        }else{
            this.cus_field_mode = false;
            this.formModel.formId=0;
            //this.get_state(this.formModel.country);
        }
    }
    onRate($event:{oldValue:number, newValue:number}) {
        this.currentRate = $event.newValue;
    }
    get_state(cId){
        this._orderService.loadStates(cId).subscribe(data => {
            this.state_list = data.states;
        }, err => console.log(err), function() {});
    }

    getState(cId){
        this.formModel.state = null;
        this._orderService.loadStates(cId).subscribe(data => {
            this.state_list = data.states;
        }, err => console.log(err), function() {});
    }
    filterCustomer(val: any,event) {
        if (event.keyCode != 13 && event.keyCode != 38 && event.keyCode != 40) {
            let data: any = {};
            data.search = val;
            this._orderService.filterCustomerList(data).subscribe(data => {
                console.log(data);
                if (data.status == 1) {
                    this.customer_list = data.api_status;
                } else {
                    this.customer_list = [];
                }
            }, err => { }, function () { });
        }
    }
    displayFnCustomer(obj: any) {
        console.log(obj);
        return obj ? obj.first_name : obj;
    }
    getProductDetails(sku:string,event) {
        console.log(event);
        if (event.keyCode != 13 && event.keyCode != 38 && event.keyCode != 40) {
            let filterValue: any = '';
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
                filterValue = filterValue.replace("/", "\\", filterValue);
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
    setDetails(customer:any){
        this.formModel.customer_name = customer.first_name+ ' ' +customer.last_name;
        this.formModel.customer_id = customer.id;
    }
    setSku(item :any){
        this.formModel.sku = item.sku;
        this.formModel.product_id = item.id;
        this.formModel.product_name = item.name;
       //alert(itemDetails);
    }
    addEditReview(form: any){
        if(this.currentRate <= 0){
            this.currentRateValidate = false;
        }else{
            this.currentRateValidate = true;
        }
        if(this.currentRateValidate){
            setTimeout(() => {
                this._globalService.showLoaderSpinner(false);
            });
            let data: any = {};
            if (this.formModel.formId > 0) {
                data.id = this.formModel.formId;
            }
            data.website_id = this._globalService.getWebsiteId();
            data.user_ip = this.ipaddress;
            data.user_name = this.formModel.customer_name;
            data.user_city = this.formModel.city;
            data.user_state = this.formModel.state;
            data.user_country = this.formModel.country;
            data.title= this.formModel.title;
            data.review = this.formModel.description;
            data.rating = this.currentRate;
            data.product_id = this.formModel.product_id;
            data.user_id = this.formModel.customer_id;
            //data={"value":data};
            console.log(data)
            this.global.getWebServiceData('product_reviews','POST',data,'').subscribe(res => { 
                if (res['status'] == '1') { // success response 
                    this._globalService.showToast(res['message']);
                    this._router.navigate(['/review/']);
                } else {
                    this._globalService.showToast(res['message']);
                }
                setTimeout(() => {
                    this._globalService.showLoaderSpinner(false);
                });
            }, err => {

            })
        }
    }
    
}