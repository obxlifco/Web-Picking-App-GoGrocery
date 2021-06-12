import {Component, ElementRef, OnInit,ViewChild, Input, Inject, AfterViewInit, Optional } from '@angular/core';
import { GlobalService } from '../../global/service/app.global.service';
import { CookieService } from 'ngx-cookie';
import { Global } from '../../global/service/global';
import { Router, ActivatedRoute } from '@angular/router';
import {COMMA, ENTER} from '@angular/cdk/keycodes';
import {Observable} from 'rxjs';
import { MatAutocompleteTrigger, MatChipInputEvent } from '@angular/material';
@Component({
  selector: 'app-barcodeaddedit',
  templateUrl: './templates/barcodeaddedit.component.html', 
  styleUrls: ['./barcodeaddedit.component.css']
})
export class BarcodeaddeditComponent implements OnInit {
  @ViewChild(MatAutocompleteTrigger) trigger;	

  public ipaddress: any;
    public response: any;
    public errorMsg: string;
    public successMsg: string;
    public formModel: any = {};
    private sub: any;
    public tabIndex: number;
    public parentId: number = 0;
    public userId: any;
    public sample_xls;
    visible = true;
    selectable = true;
    removable = true;
    addOnBlur = true;
    barcode_list:any;
    public product_list:any=[];
    readonly separatorKeysCodes: number[] = [ENTER, COMMA];
    public product_id:number;
    public currentJoke:any;
    public product:number;
    constructor(
        public _globalService: GlobalService,
        private global: Global,
        private _router: Router,
        private _route: ActivatedRoute,
        private _cookieService: CookieService,
        private _global:Global,
    ) {
        this.ipaddress = _globalService.getCookie('ipaddress');
    }

    ngOnInit() {
        this.barcode_list = [];

		    this.sample_xls = window.location.protocol + '//' + window.location.hostname + ':8062' + '/media/importfile/sample/MultipleBarcode.xls';

        let userData = this._cookieService.getObject('userData');
        this.userId = userData['uid'];
        //this.get_products();

        this.tabIndex = +this._globalService.getCookie('active_tabs');
        this.parentId = this._globalService.getParentTab(this.tabIndex);
        this.sub = this._route.params.subscribe(params => {
            this.formModel.formId = +params['id']; // (+) converts string 'id' to a number
        });
        

        if (this.formModel.formId > 0) {
          
          let data={"id":this.formModel.formId};
          this.global.getWebServiceData('getbarcodedetails','POST',data,'').subscribe(Response => {
            let data=Response.data;
              let product=+data.product;
              this.get_product(product);
              this.global.getWebServiceData('multiplebarcodes/'+product,'GET','','').subscribe(Response => {
                let data=Response.api_status;
                  data.forEach(item=>{
                    this.barcode_list.push({'name':item.barcode});
                  })  
              }, err => {
                  console.log(err)
              })

          }, err => {
              console.log(err)
          })
          
        }

       
    }
    
    addEditBarcode(form: any) {
        setTimeout(() => {
            this._globalService.showLoaderSpinner(false);
        });
        let data: any = {};
        let barcode=[];
        this.barcode_list.forEach(element => {
          barcode.push({'barcode':element.name});
          data=barcode;
        });
        if (this.formModel.formId > 0) {
          data.id = this.formModel.formId;
        }
        data={"value":data,"website_id":this._globalService.getWebsiteId()};
        this.global.getWebServiceData('multiplebarcodes/'+this.product_id,'PUT',data,'').subscribe(res => { 
            if (res['status'] == '1') { // success response 
                this._globalService.showToast(res['message']);
                this._router.navigate(['barcodes/']);
            } else {
                this._globalService.showToast(res['message']);
            }
            setTimeout(() => {
                this._globalService.showLoaderSpinner(false);
            });
        }, err => {

        })
    }

    get_products(){
      let data = {
        "model": "EngageboostProducts","screen_name": "list","userid": this.userId,"search": "","order_by": "","order_type": "","status": "","website_id": this._globalService.getWebsiteId(),
        "visibility_id": 1
      };
      this.global.getWebServiceData('productlist','POST',data,'').subscribe(data => {
        this.product_list = data.results[0].result; // list of customer list
        
      }, err => {}, function() { // call back function when exection is done

      })
    }

    get_product(pro_id:number){
      console.log('get product')
      this.global.getWebServiceData('product_details/'+pro_id,'GET','','').subscribe(Response => {
        if(Response.status==1){
          let data=Response.product_details;
          this.product_id=pro_id;
          this.formModel.sku = data.sku;
          this.formModel.ean = data.ean;
        this.formModel.name_edit = data.name;
        }else{
          this.formModel.sku = '';
          this.formModel.ean = '';
        }
      }, err => {
        console.log(err)
      })
    }

    get_product_id(){

    }
    //CHIPS HANDLING START
    add(event: MatChipInputEvent): void {
      const input = event.input;
      const value = event.value;
  
      // Add our fruit
      if ((value || '').trim()) {
        this.barcode_list.push({name: value.trim()});
      }
  
      // Reset the input value
      if (input) {
        input.value = '';
      }
    }
  
    remove(item): void {
      const index = this.barcode_list.indexOf(item);
  
      if (index >= 0) {
        this.barcode_list.splice(index, 1);
      }
    }
    //CHIPS HANDLING END
    
    ngAfterViewInit() {
      if(this.trigger!=undefined){
        this.trigger.panelClosingActions
        .subscribe(e => {
          
          if (this.trigger.activeOption) {
            this.formModel.name = this.trigger.activeOption;
            this.trigger.closePanel();
          }else{
            if(typeof this.formModel.name != 'object'){
              this.formModel.name = null;
              this.product_list = [];
            }
          }
        });
      }

    }

    displayFn(obj: any){
      return obj ? obj.name : obj;
  	}

  	// get countries
  	filter_products(val:any){
	    let filterValue: string = '';
	    if (val) {

	      if(typeof val === 'object'){
          filterValue = val.name.toLowerCase();
          this.get_product(val.id)
	        
	      }else{
	        filterValue = val.toLowerCase();
	      }
	    }
	    let data = {
	      "table_name": "EngageboostProducts",
	      "search": filterValue,
	      "company_id": '',
		    "website_id": this._globalService.getWebsiteId()
	    }
	    this._global.globalAutocomplete(data).subscribe(
	      data => {
          this.product_list = data.filter_data;
          console.log(this.product_list);
			  
	      },
	      err => {
	        this._globalService.showToast('Something went wrong. Please try again.');
	      },
	      function(){
	      //completed callback
	      }
	    );
	  }	
}
