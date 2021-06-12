import { Component, OnInit } from '@angular/core';
import { GlobalService } from '../../global/service/app.global.service';
import { CookieService } from 'ngx-cookie';
import { Global } from '../../global/service/global';
import { Router, ActivatedRoute } from '@angular/router';
import { AddEditTransition, AddEditStepFlipTransition } from '../.././addedit.animation';
import { AreaService } from '../../operations/area/operation.area.service';
@Component({
  selector: 'app-taxruleaddedit',
  templateUrl: 'templates/taxruleaddedit.component.html',
  providers: [AreaService],
  animations: [ AddEditTransition ],
  host: {
  '[@AddEditTransition]': ''
  },
})
export class TaxruleaddeditComponent implements OnInit {

  public ipaddress: any;
    public response: any;
    public errorMsg: string;
    public successMsg: string;
    public formModel: any = {};
    private sub: any;
    public tabIndex: number;
    public parentId: number = 0;
    public userId: any;

    public zipcode_list=[];
    public pincodes_str:any;
    public tax_rate_list=[];
    public product_tax_list=[];
    public customer_tax_list=[];

    constructor(
        public _globalService: GlobalService,
        private global: Global,
        private _router: Router,
        private _route: ActivatedRoute,
        private _cookieService: CookieService,
        private _areaService: AreaService,
    ) {
        this.ipaddress = _globalService.getCookie('ipaddress');
    }

    ngOnInit() {
      let userData = this._cookieService.getObject('userData');
      this.userId = userData['uid'];
      this.getTaxRates(); 
      this.getProductTax();
      this.getCustomerTax();
      this.tabIndex = +this._globalService.getCookie('active_tabs');
      this.parentId = this._globalService.getParentTab(this.tabIndex);
      this.sub = this._route.params.subscribe(params => {
          this.formModel.formId = +params['id']; // (+) converts string 'id' to a number
      });
      if (this.formModel.formId > 0) {
          this.global.getWebServiceData('view_taxrule','GET','',this.formModel.formId).subscribe(Response => {
            let data=Response.api_status;
              this.formModel.rule_name = data.rule_name;
              this.formModel.tax_rate_id = data.tax_rate.id;
              this.formModel.product_tax_class_id = data.product_tax_class_id;
              this.formModel.customer_tax_class_id = data.customer_tax_class_id;
              this.formModel.priority = data.priority;

              if (data.product_tax_class_id != '') {
                let product_tax_class_id = data.product_tax_class_id;
                this.formModel.product_tax_class_id = product_tax_class_id.split(',').map(function(item) {
                    return parseInt(item, 10);
                });
              } else {
                this.formModel.product_tax_class_id = [];
              }
              if (data.customer_tax_class_id != '') {
                let customer_tax_class_id = data.customer_tax_class_id;
                this.formModel.customer_tax_class_id = customer_tax_class_id.split(',').map(function(item) {
                    return parseInt(item, 10);
                });
              } else {
                this.formModel.product_tax_class_id = [];
              }
              this.formModel.zipcode = data.zipcode;
          }, err => {
              console.log(err)
          })
      }
  }

  addEdit(form: any) {
      setTimeout(() => {
          this._globalService.showLoaderSpinner(false);
      });
      let data: any = {};
      data.website_id = this._globalService.getWebsiteId();
      data.rule_name = this.formModel.rule_name;
      data.tax_rate_id = this.formModel.tax_rate_id;
      data.priority = this.formModel.priority;

      let product_tax_class_id=this.formModel.product_tax_class_id.toString()
      data.product_tax_class_id = product_tax_class_id;

      let customer_tax_class_id=this.formModel.customer_tax_class_id.toString()
      data.customer_tax_class_id = customer_tax_class_id;

      data.zipcode = this.formModel.zipcode;
      if (this.formModel.formId > 0) {
          data.id = this.formModel.formId;
      }
      data={"value":data};
      console.log(data)
      this.global.getWebServiceData('taxrule','POST',data,'').subscribe(res => { 
        if (res['status'] == '1') { // success response 
            this._globalService.showToast(res['message']);
            this._router.navigate(['/tax_rules/']);
        } else {
            this._globalService.showToast(res['message']);
        }
        setTimeout(() => {
            this._globalService.showLoaderSpinner(false);
        });
      }, err => {

      })

  }

  getTaxRates(){
    let data={
      "model": "EngageboostTaxRates",
      "screen_name": "list",
      "userid": this.userId ,
      "search": "",
      "order_by": "name",
      "order_type": "+",
      "status": "",
      "website_id": this._globalService.getWebsiteId()
    }
    this.global.getWebServiceData('global_list','POST',data,'').subscribe(Response => {  
      let data= Response.results[0].result;
      this.tax_rate_list=data;
    }, err => {

    })
  }

  getProductTax(){
    let data={
      "model": "EngageboostProductTaxClasses",
      "screen_name": "list",
      "userid": this.userId ,
      "search": "",
      "order_by": "name",
      "order_type": "+",
      "status": "",
      "website_id": this._globalService.getWebsiteId()
    }
    this.global.getWebServiceData('global_list','POST',data,'').subscribe(Response => {  
      let data= Response.results[0].result;
      this.product_tax_list=data;
    }, err => {

    })
  }

  getCustomerTax(){
    let data={
      "model": "EngageboostCustomerTaxClasses",
      "screen_name": "list",
      "userid": this.userId ,
      "search": "",
      "order_by": "tax_class_name",
      "order_type": "+",
      "status": "",
      "website_id": this._globalService.getWebsiteId()
    }
    this.global.getWebServiceData('global_list','POST',data,'').subscribe(Response => {  
      let data= Response.results[0].result;
      this.customer_tax_list=data;
    }, err => {

    })
  }
}
