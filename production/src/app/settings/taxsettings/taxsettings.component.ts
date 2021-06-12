import { Component, OnInit } from '@angular/core';
import { Global } from '../../global/service/global';
import {CookieService} from 'ngx-cookie';
import { GlobalService } from '../../global/service/app.global.service';

@Component({
  selector: 'app-taxsettings',
  templateUrl: './taxsettings.component.html',
  styleUrls: ['./taxsettings.component.css']
})
export class TaxsettingsComponent implements OnInit {
  table: string;heading: string;tablink: string;tabparrentid: any;screen: any;ispopup: any;
  public tabIndex: number;
  public parentId: number = 0;
  public formModel: any = {};
  public userId: any;
  page: any;
  childData = {};
  post_data = {};
  public product_tax_list=[];
  constructor(
    public _globalService: GlobalService,
    private global: Global,
    private _cookieService: CookieService,
    private globalService: GlobalService,
    
  ) 
  { 
    this.tabIndex = +_globalService.getCookie('active_tabs');
    this.parentId = _globalService.getParentId(this.tabIndex);
  }

  ngOnInit() {
    let userData = this._cookieService.getObject('userData');
    this.userId = userData['uid'];
    this.getProductTax();
    let website_id = this._globalService.getWebsiteId();
    this.global.getTaxSettings(website_id).subscribe(
      res => {
          
        let data=res.api_status;
        this.formModel.shipping_tax_class = data.shipping_tax_class;
        this.formModel.tax_calculation_based_on = data.tax_calculation_based_on;
        this.formModel.catalog_prices = data.catalog_prices;
        this.formModel.shipping_price = data.shipping_price;
        this.formModel.apply_customer_tax = data.apply_customer_tax;
        this.formModel.apply_discount_on_prices = data.apply_discount_on_prices;
        this.formModel.display_product_prices_in_catalog = data.display_product_prices_in_catalog;
        this.formModel.display_shipping_prices = data.display_shipping_prices;
        this.formModel.cst_applicable=data.cst_applicable;
        this.formModel.excise_duty=data.excise_duty;
        this.formModel.display_prices = data.display_prices;
        this.formModel.display_subtotal = data.display_subtotal;
        this.formModel.display_shipping_amount = data.display_shipping_amount;
        this.formModel.include_tax_in_grand_total = data.include_tax_in_grand_total;
        this.formModel.display_full_tax_summary = data.display_full_tax_summary;
        this.formModel.display_zero_tax_subtotal = data.display_zero_tax_subtotal;
        this.formModel.shipping_tax_rate = data.shipping_tax_rate;
        
      },
      err => {
        this._globalService.showToast('Something went wrong. Please try again.');
      },
    );
  }

  updateTaxSettings(){
    setTimeout(() => {
      this._globalService.showLoaderSpinner(false);
    });
    let data: any = {};
    data.website_id=this._globalService.getWebsiteId();
    data.shipping_tax_class = this.formModel.shipping_tax_class;
    data.tax_calculation_based_on = this.formModel.tax_calculation_based_on;
    data.catalog_prices = this.formModel.catalog_prices;
    data.shipping_price = this.formModel.shipping_price;
    data.apply_customer_tax = this.formModel.apply_customer_tax;
    data.apply_discount_on_prices = this.formModel.apply_discount_on_prices;
    data.display_product_prices_in_catalog = this.formModel.display_product_prices_in_catalog;
    data.display_shipping_prices = this.formModel.display_shipping_prices;
    data.cst_applicable = this.formModel.cst_applicable;
    data.excise_duty = this.formModel.excise_duty;
    data.display_prices = this.formModel.display_prices;
    data.display_subtotal = this.formModel.display_subtotal;
    data.display_shipping_amount = this.formModel.display_shipping_amount;
    data.include_tax_in_grand_total = this.formModel.include_tax_in_grand_total;
    data.display_full_tax_summary = this.formModel.display_full_tax_summary;
    data.display_zero_tax_subtotal = this.formModel.display_zero_tax_subtotal;
    data.shipping_tax_rate = this.formModel.shipping_tax_rate;
    data={"value":data};
    this.global.getWebServiceData('taxsettings','POST',data,'').subscribe(res => { 
      if (res['status'] == '1') { // success response 
          this._globalService.showToast(res['message']);
      } else {
          this._globalService.showToast(res['message']);
      }
      setTimeout(() => {
          this._globalService.showLoaderSpinner(false);
      });
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
}
