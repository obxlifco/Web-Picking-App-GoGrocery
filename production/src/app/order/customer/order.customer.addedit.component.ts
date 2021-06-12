import { Component, OnInit, Inject, Optional, ViewChild } from '@angular/core';
import { Router,ActivatedRoute } from '@angular/router';
import { AddEditTransition, AddEditStepFlipTransition } from '../.././addedit.animation';
import { CookieService } from 'ngx-cookie';
import { CustomerService } from './customers.customer.service';
import { GlobalService } from '../../global/service/app.global.service';
import { Global } from '../../global/service/global';
import { forEach } from '@angular/router/src/utils/collection';
import { MatAutocompleteSelectedEvent, MatAutocompleteTrigger, MatDialog, MatDialogRef, MAT_DIALOG_DATA, MatTabsModule } from '@angular/material';

@Component({
  templateUrl: './templates/add_customer_first.html',
  providers: [CustomerService],
  animations: [ AddEditTransition ],
  host: {
    '[@AddEditTransition]': ''
  },
})
export class CustomerAddEditComponent implements OnInit {
  public response: any;
  public errorMsg: string;
  public successMsg: string;

  public menu_list: any;
  public formModel: any = {};
  public List:any={}

  private sub: any;
  public tabIndex: number;
  public parentId: number = 0;

  public add_edit:any='';
  public customer_group:any = [];
  
  constructor(
    private _customerService:CustomerService,
    public _globalService:GlobalService,
    private _router: Router,
    private _route: ActivatedRoute,
    private _cookieService:CookieService,
    public dialog: MatDialog,
  ) {}
  
  ngOnInit() {
    this.tabIndex = +this._globalService.getCookie('active_tabs');
    this.parentId = this._globalService.getParentTab(this.tabIndex);

    this.sub = this._route.params.subscribe(params => {
        this.formModel.customer_id = +params['id']; // (+) converts string 'id' to a number
    });
    this.loadCustomerGroup();
    if(this.formModel.customer_id) {
      this._cookieService.putObject('cid_edit', this.formModel.customer_id);
      this._cookieService.putObject('action','edit'); 
      this.add_edit='edit';
    } else {
      this._cookieService.putObject('action','add');
      this.formModel.customer_id = this._cookieService.getObject('cid_add');
      this.add_edit='add';
      this.formModel.customer_id = 0;
    }
    if (this.formModel.customer_id > 0) {
      this._customerService.loadCustomerGeneralInfo(this.formModel.customer_id).subscribe(
        data => {
          this.formModel = Object.assign(this.formModel,data.api_status);
          if(this.formModel.group_id > 0) {
            this.formModel.group_id =  this.formModel.group_id;
          }         
        },
        err => console.log(err),
        function () {
          //completed callback
        }
      );
    } else {
      this.formModel.customer_id = 0;
      this.formModel.isblocked = 'n';
      //this.formModel.group_id = 1;
    }
  }

  addEditBasicInfoCustomer(form: any) {
    this.errorMsg = '';
    let userData = this._cookieService.getObject('userData');
    let data: any = {};
    data.website_id =  1;
    data.first_name =  this.formModel.first_name;
    data.last_name =  this.formModel.last_name;
    data.email =  this.formModel.email;
    if(this.formModel.vat) {
      data.vat =  this.formModel.vat;
    } else {
      data.vat = "";
    }
    if(this.formModel.tin) {
      data.tin =  this.formModel.tin;
    } else {
      data.tin = "";
    }
    data.customer_group_id =  this.formModel.group_id;
    data.updatedby =  userData['uid'];
    data.createdby =  userData['uid'];
    data.status =  this.formModel.isblocked;
    data.phone =  this.formModel.phone;
    data.company_id =  userData['company_id'];
    if(this.add_edit=='add') {
      data.password =  'Boost@1234';      
      data.insert_type =  'add';
    } else {
      data.password =  this.formModel.password;
      data.insert_type =  'edit';
      data.c_id =  this.formModel.customer_id;
    }
    
    this._customerService.saveBasicInfoCustomer(data,this.formModel.customer_id).subscribe(
     data => {
       this.response = data;
       if(this.response.status==1) {
          let inserted_id=this.response.last_inserted_id;
          if(this.add_edit=='add') {  
            this._router.navigate(['/customers/add/'+inserted_id+'/step2']);
          } else {
            this._router.navigate(['/customers/edit/'+this.formModel.customer_id+'/step2']);
          } 
        } else {
         this._globalService.showToast(this.response.message);
        }
      },
      err => {
       this._globalService.showToast('Something went wrong. Please try again.');
      },
       function(){
        //completed callback
      }
    );
  } 

  loadCustomerGroup() {
    this._customerService.loadCustomerGroup().subscribe(
    data => {
        if(data["status"] == 1) {
            this.customer_group = data.api_status;
        } else {
            this.customer_group = [];
        }
    },
    err => console.log(err),
    function () {
      //completed callback
    }
    );
  } 
}

@Component({
  templateUrl: './templates/customer_address_info.html',
  providers: [CustomerService],
  animations: [ AddEditTransition ],
  host: {
    '[@AddEditTransition]': ''
  },
})
export class CustomerAddEditAddressComponent implements OnInit { 
  public response: any;
  public errorMsg: string;
  public successMsg: string;
  public menu_list: any;
  public formModel: any = {};
  public List:any={}
  private sub: any;
  public tabIndex: number;
  public parentId: number = 0;
  public add_edit:any='';
  public country_list: any = [];
  public state_list: any = [];
  public address_list:any=[];
  public edit_id:number;
  public addNew:boolean;
  panelOpenState = true;
  @ViewChild(MatAutocompleteTrigger) trigger;
  country_name;
  country_id;
 constructor(
    private _customerService:CustomerService,
    public _globalService:GlobalService,
    private _router: Router,
    private _route: ActivatedRoute,
    private _cookieService:CookieService,
    public dialog: MatDialog,
    private global: Global,

  ) {}
  
  ngOnInit() {
    this.tabIndex = +this._globalService.getCookie('active_tabs');
    this.parentId = this._globalService.getParentTab(this.tabIndex);
    this.add_edit = this._cookieService.getObject('action');
    if(this.add_edit=='add') {
      this.formModel.customer_id=this._cookieService.getObject('cid_add');
    } else {
      this.formModel.customer_id=this._cookieService.getObject('cid_edit');
    }
    this.sub = this._route.params.subscribe(params => {
      this.formModel.customer_id = +params['id']; // (+) converts string 'id' to a number
    });
    // this.loadCountry();
    // this.formModel.country_ids = 99;
    if (this.formModel.customer_id > 0) {
        this.load_address();
    }
  }
  delete_address(id:number){
    let data={
      'customer_id':this.formModel.customer_id,
      'id':id
    }
    this.global.getWebServiceData('customeraddressdelete','POST',data,'').subscribe(res => {  
      if (res['status'] == '1') { // success response 
          this._globalService.showToast(res['response']);
          this.load_address();
        } else {
          this._globalService.showToast(res['response']);
        }
    }, err => {

    })
  }
  update_address(id) {
    this.errorMsg = '';
    if (this.formModel.customer_id > 0) {
      this.address_list.forEach(element=>{
        if(id == element.id) {
          let data:any={};
          data.id = element.id;
          data.customers_id=this.formModel.customer_id;
          data.delivery_name = element.delivery_name;
          data.delivery_email_address = element.delivery_email_address;
          data.delivery_phone = element.delivery_phone;
          data.delivery_street_address = element.delivery_street_address;
          data.delivery_street_address1 = element.delivery_street_address1;
          data.delivery_country = element.delivery_country.id;
          data.delivery_state = element.delivery_state;
          data.delivery_city = element.delivery_city;
          data.delivery_postcode = element.delivery_postcode;
          data.delivery_fax="1";
          data.delivery_landmark="1";
          //POST DATA
          this.global.getWebServiceData('customer_address_setup','POST',data,'').subscribe(res => {  
            if (res['status'] == '1') { // success response 
              this._globalService.showToast(res['message']);
                if(this.add_edit=='add') {  
                  this._router.navigate(['/customers/add/'+this.formModel.customer_id+'/step2']);
                } else {
                  this._router.navigate(['/customers/edit/'+this.formModel.customer_id+'/step2']);
                }
                this.load_address();
              } else {
                  this._globalService.showToast(res['message']);
              }
              setTimeout(() => {
                  this._globalService.showLoaderSpinner(false);
              });
            }, err => {

            })
          }
      });
    }  
  }
  add_new(){
    this.addNew=true;
  }
  cancel_add(){
    this.addNew=false;
  }
  addNewAddressSave(){
    let data:any={};
    data.customers_id=this.formModel.customer_id;
    data.delivery_name = this.formModel.delivery_name_add;
    data.delivery_email_address = this.formModel.delivery_email_address_add;
    data.delivery_phone = this.formModel.delivery_phone_add;
    data.delivery_street_address = this.formModel.delivery_street_address_add;
    data.delivery_street_address1 = this.formModel.delivery_street_address1_add;
    data.delivery_country = this.formModel.delivery_country_add.id;
    data.delivery_state = this.formModel.delivery_state_add;
    data.delivery_city = this.formModel.delivery_city_add;
    data.delivery_postcode = this.formModel.delivery_postcode_add;
    data.delivery_fax="1";
    data.delivery_landmark="1";
    this.global.getWebServiceData('customer_address_setup','POST',data,'').subscribe(res => {  
      if (res['status'] == '1') { // success response 
        this._globalService.showToast(res['message']);
        this.addNew=false;
        this.load_address();
      } else {
        this._globalService.showToast('Please enter all mandatory fields');
      }
        setTimeout(() => {
          this._globalService.showLoaderSpinner(false);
        });
      }, err => {
    })
  }
  load_address(){
    this.global.getWebServiceData('get_customer_address','GET','',this.formModel.customer_id).subscribe(data => { 
      this.country_list = data.countrylist;
      if(data.status == 1) { // if address is found in the database
        this.address_list=data.response;
        this.address_list.forEach((element)=>{
          this.get_states(+element.delivery_country);
          element.delivery_state = +element.delivery_state;
          this.global.getWebServiceData('countrylist/'+element.delivery_country,'GET','','').subscribe(result => { 
            let data=result.api_status
            if(result.status==1){
              let id=data.id;
              let name=data.country_name
              element.delivery_country = {id:id,country_name:name};
            }else{
              element.delivery_country = {id:99,country_name:'India'};
            }
          })
        })
      } else {
         this.address_list=[];
      }
    }, err => {
      console.log(err);
    })
  }
  
  loadCountry() {
    this._customerService.loadCountry().subscribe(
    data => {
      this.country_list = data.countrylist;
    },
    err => console.log(err),
    function () {
      //completed callback
    }
    );
  }
  
  // get countries
  filter_countries(val:any){
    let filterValue: string = '';
    if (val) {
      if(typeof val === 'object'){
        filterValue = val.country_name.toLowerCase();
      } else {
        filterValue = val.toLowerCase();
      }
    }
    let data = {
      "table_name": "EngageboostCountries",
      "search": filterValue,
      "company_id": this._globalService.getCompanyId(),
      "website_id": this._globalService.getWebsiteId()
    }
    this.global.globalAutocomplete(data).subscribe(
      data => {
        this.country_list = data.filter_data;
      },
      err => {
        this._globalService.showToast('Something went wrong. Please try again.');
      }
    );
  }
  
  displayFn(obj: any){
    return obj ? obj.country_name : obj;
  }

  get_country(country_id:number) {
    this._customerService.loadStates(country_id).subscribe(
      data => {
      
        this.country_name = 'India55as';
        this.country_id = 99;
      },
      err => console.log(err),
      function () {
      }
    );
  }
  get_states(country_id:number= this.formModel.delivery_country_add.id) {
    this._customerService.loadStates(country_id).subscribe(
      data => {
        this.state_list = data.states;
      },
      err => console.log(err),
      function () {
      }
    );
  }
  change_tab(id:any){
    this._router.navigate(['/customers/add/'+id+'/step3',]);
  }
}

//END OF ADDRESS COMPONENT
@Component({
  templateUrl: './templates/customer_order_list.html',
  providers: [CustomerService,Global],
  animations: [ AddEditStepFlipTransition ],
  host: {
    '[@AddEditStepFlipTransition]': ''
  },
})
export class CustomerOrderListComponent implements OnInit {
  public add_edit:any='';
  public response: any;
  public errorMsg: string;
  public successMsg: string;
  public formModel: any = {};
  private sub: any;
  public tabIndex: number;
  public parentId: number = 0;
  public bulk_ids:any = [];
  public rel_data:any = [];
  public pagination:any = {};
  public pageIndex : number = 0;
  public pageList : number = 0;
  public sortBy:any = '';
  public sortOrder:any = '';
  public sortClass:any = '';
  public sortRev:boolean = true;
  public selectedAll:any=false;
  public stat:any = {};
  public result_list:any=[];
  public total_list:any=[];
  public cols:any=[]
  public add_btn : string;
  public post_data = {};
  public page: number = 1;
  public filter: string = '';
  public maxSize: number = 10;
  public directionLinks: boolean = true;
  public autoHide: boolean = false;
  public config: any = {};
  public permission:any=[];
  public show_btn:any={'add':true,'edit':true,'delete':true,'block':true};
  public userId:any;
  public customer_steps:any;
  public search_text:string;
  public customer_module_name:string;
  constructor(
    private _customerService:CustomerService,
    public _globalService:GlobalService,
    private global:Global,
    private _router: Router,
    private _route: ActivatedRoute,
    private _cookieService:CookieService
  ) {}
    ngOnInit() {
      this.tabIndex = +this._globalService.getCookie('active_tabs');
      this.parentId = this._globalService.getParentTab(this.tabIndex);
      this.add_edit = this._cookieService.getObject('action');
      let curr_url=this._router.url;
      if(this.add_edit=='add') {
        this.formModel.customer_id=this._cookieService.getObject('cid_add');
      } else {
        this.formModel.customer_id=this._cookieService.getObject('cid_edit');
      }
      if( curr_url.indexOf('step3') > 0) { // this is for order list
        this.customer_steps = 1;
        this.customer_module_name = 'CustomerOrderList'
        this.generateCustomerGrid(0,'1','id','','',this.customer_module_name);
      } 
      if(curr_url.indexOf('step4') > 0) { // this is for invoice list
        this.customer_steps = 2 ;
        this.customer_module_name = 'CustomerInvoiceList'
        this.generateCustomerGrid(0,'1','id','','',this.customer_module_name);
      }
    }
    generateCustomerGrid(reload:any,page:any,sortBy:any,filter:any,search:any,module_name) {
      this.total_list=[];
      this.selectedAll=false;
      this.filter=filter;
      this.sortBy=sortBy;
      if(sortBy!='' && sortBy!=undefined) { 
        if(this.sortRev){
          this.sortOrder = '-'
          this.sortRev = !this.sortRev;
          this.sortClass = 'icon-down';
        } else {
          this.sortOrder = '+'
          this.sortRev = !this.sortRev;
          this.sortClass = 'icon-up';
        }
      }
      if(this.add_edit=='add') {
        let customer_id=this._router.url.split('/')[3];
        this.formModel.customer_id=+customer_id;
      }
      this.post_data={"customer_id":this.formModel.customer_id,"userid":this.userId,"search":search,"order_by":sortBy,"order_type":this.sortOrder,"status":filter}
            this._customerService.doGridCustomersAddEdit(this.post_data,page,this.customer_steps).subscribe(
               data => {
               this.response = data;
                let that = this;
                if(this.response.count>0){
                 this.result_list = this.response.results[0].result;
                 this.result_list.forEach(function(item:any){//////////// start the status settings //////////////////////
                      if(item.order_status =='99' && item.buy_status =='1') {
                        item.order_status = 'Waiting for approval';
                        item.class_name = 'status-box approval';
                      } else if(item.order_status =='0' && item.buy_status =='1') {
                         item.order_status = 'Pending';
                         item.class_name = 'status-box pendings';
                      } else if (item.order_status == '20' && item.buy_status == '1') {
                         item.order_status = 'Approved';
                         item.class_name = 'status-box pendings';
                      } else if(item.order_status =='100' && item.buy_status =='1') {
                         item.order_status = 'Processing';
                         item.class_name = 'status-box processing';
                      } else if(item.order_status =='1' && item.buy_status =='1') {
                         item.order_status = 'Shipped';
                         item.class_name = 'status-box shipped';
                      } else if(item.order_status =='2' && item.buy_status =='1') {
                         item.order_status = 'Cancelled';
                         item.class_name = 'status-box cancelled';
                      } else if(item.order_status =='4' && item.buy_status =='1') {
                         item.order_status = 'Completed';
                         item.class_name = 'status-box completed';
                      } else if(item.order_status =='5' && item.buy_status =='1') {
                         item.order_status = 'Full Refund';
                         item.class_name = 'status-box full-refund';
                      } else if(item.order_status =='6' && item.buy_status =='1') {
                         item.order_status = 'Partial Refund';
                         item.class_name = 'status-box partial-refund';
                      } else if(item.order_status =='11' && item.buy_status =='1') {
                         item.order_status = 'Partial Refund';
                         item.class_name = 'status-box paid';
                      } else if(item.order_status =='12' && item.buy_status =='1') {
                         item.order_status = 'Assingned to Showroom';
                         item.class_name = 'status-box assign-to-showroom';
                      } else if(item.order_status =='13' && item.buy_status =='1') {
                        item.order_status = 'Delivered';
                        item.class_name = 'status-box delivered';
                      } else if(item.order_status =='16' && item.buy_status =='1') {
                        item.order_status = 'Closed';
                        item.class_name = 'status-box closed';
                      } else if(item.order_status =='18' && item.buy_status =='1') {
                        item.order_status = 'Pending Service';
                        item.class_name = 'status-box pending-service';
                      } else if(item.order_status =='3' && item.buy_status =='0') {
                        item.order_status = 'Abondoned';
                        item.class_name = 'status-box abondoned';
                      } else if(item.order_status =='999' && item.buy_status =='0') {
                        item.order_status = 'Failed';
                        item.class_name = 'status-box failed';
                      } else {
                        item.order_status = 'Invoiced';
                        item.class_name = 'status-box invoiced';
                      } 
                      //////////////  end status settings /////////////////// 
                      if(item.created !='') {
                        item.created = that._globalService.convertDate(item.created,'dd-MM-yyyy h:mm a');
                      }
                      if(item.created_date !='') {
                        item.created_date = that._globalService.convertDate(item.created_date,'dd-MM-yyyy h:mm a');
                      }
                     })
                for (let i = 0; i < this.response.count; i++) {
                this.total_list.push(i);
                }
               }else{
                   this.result_list =[];
               }  
              this.cols = this.response.results[0].layout;
              // this.cols = this.response.results[0].applied_layout;
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
              }, function(){
              }
            );                   
           }
      ////////////////////////////Check/Uncheck//////////////

    toggleCheckAll(event:any){  
      let that=this;
      that.bulk_ids=[];
      this.selectedAll = event.checked;
      this.result_list.forEach(function(item:any){
        item.selected = event.checked;  
        if(item.selected){
        that.bulk_ids.push(item.id);
        }  
      });
    } 

    toggleCheck(id:any,event:any){
      let that=this;
        this.result_list.forEach(function(item:any){
          if(item.id==id){
            item.selected = event.checked;  
          if(item.selected) {
          that.bulk_ids.push(item.id);
        } else {
          let index = that.bulk_ids.indexOf(item.id);
            that.bulk_ids.splice(index, 1);
          }  
        }
      });
    }
  /////////////////////////Filter Grid//////////////////////
  
  updateGrid(isdefault:any) {
    this.global.doGridFilter(this.customer_module_name,isdefault,this.cols,"customer-order-invoice").subscribe(
      data => {
         this.response = data;
         this.generateCustomerGrid(0,'','','','',this.customer_module_name);
       },
      err => {
         this._globalService.showToast('Something went wrong. Please try again.');
      },
      function() { 
      }
    );
  } 

  customerOrderInvoiceList () {
    let customer_id:any;
    if(this.add_edit=='add') {
        customer_id=this._cookieService.getObject('cid_add');
    } else {
        customer_id =this._cookieService.getObject('cid_add');
    }

    if(this.customer_steps == 1) { // on clicking on this it will goes to invoice list page
      if(this.add_edit=='add') {
        let customer_id=this._router.url.split('/')[3];
        this._router.navigate(['/customers/add/'+customer_id+'/step4']);
      } else {
        this._router.navigate(['/customers/edit/' +customer_id+'/step4']);
      }
    } else if(this.customer_steps == 2 ) { // on clicking on this it will goes to customer list page
        this._globalService.deleteTab(this.tabIndex,this.parentId);
    }
  }

  customerOrderContinue() {
    this._globalService.deleteTab(this.tabIndex, this.parentId);
    this._router.navigate(['/customers']);
  }
}