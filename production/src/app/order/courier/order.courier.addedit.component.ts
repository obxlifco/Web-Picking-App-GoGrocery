import { Component, OnInit, Inject, Optional } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA, MatDialog } from '@angular/material';
import { Router,ActivatedRoute } from '@angular/router';
import { DOCUMENT } from '@angular/platform-browser';
import { AddEditTransition, AddEditStepFlipTransition } from '../.././addedit.animation';
import { DialogsService } from '../../global/dialog/confirm-dialog.service';
import { CookieService } from 'ngx-cookie';
import { CourierService } from './order.courier.service';
import { GlobalService } from '../../global/service/app.global.service';
import { Global } from '../../global/service/global';
@Component({
  templateUrl: './templates/create_courier.html',
  providers: [CourierService],
  animations: [ AddEditTransition ],
  host: {
    '[@AddEditTransition]': ''
  },
})
export class CourierAddEditComponent implements OnInit { 
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
    constructor(
      private _courierService:CourierService,
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
          this.formModel.id = +params['id']; // (+) converts string 'id' to a number
      });
      if(this.formModel.id > 0) {
          this._courierService.loadCourierDetails(this.formModel.id).subscribe(
              data => {
                 this.formModel = data.api_status[0];
                 this.formModel.awb_numbers =  data.api_status[0].awb_numbers.join();
                 this.formModel.edit_type = 'edit'; 
              },
              err=> {
                   this._globalService.showToast('Something went wrong. Please try again.');
              } , 
              function() {
              }
              );
        //this.formModel.tracking_type = "Awb";
        //this.formModel.method_type = "Manual";
         
      } else {
        this.formModel.tracking_type = "Awb";
        this.formModel.method_type = "Manual";
        this.formModel.edit_type = 'add';
      }
    }

    radioChange(event) {
      this.formModel.tracking_type = event.value;
    }

    addEditCourier(form:any) {
        this.errorMsg = '';
        var data: any = {};
        data = Object.assign({}, this.formModel);
        data.zip_routing_codes = '700046@@CCW/AB###700045@@CCW/CD';
        data.shipping_type = 'courier';
        data.website_id = this._globalService.getWebsiteId();
        this._courierService.saveCourierDetails(data,this.formModel.id).subscribe(
           data => {
            this.response = data;
            this._globalService.showToast(this.response.message);
            this._globalService.deleteTab(this.tabIndex,this.parentId);
            this._router.navigate(['/courier/']);

        },
       err => {
           this._globalService.showToast('Something went wrong. Please try again.');
       },
       function(){
        //completed callback
       });     
    }
}


@Component({
  templateUrl: './templates/add_awb_numbers.html',
  providers: [CourierService]
})
export class AwbMasterComponent implements OnInit { 
  public response: any;
  public errorMsg: string;
  public successMsg: string;
  public formModel: any = {};
  constructor(
    private _courierService:CourierService,
    private _globalService:GlobalService,
    private _router: Router,
    private dialogRef: MatDialogRef<AwbMasterComponent>,
    public dialog: MatDialog,
    @Optional() @Inject(MAT_DIALOG_DATA) public data: any
  ) {
    dialog.afterOpen.subscribe(() => {
           let containerElem:HTMLElement = <HTMLElement>document.getElementsByClassName('mat-dialog-container')[0];
           containerElem.classList.remove('pop-box-up');
        }); 
  }
  
  ngOnInit(){
      this.formModel.shipping_method_id = +this.data.id;
      this.formModel.tracking_company_name = this.data.method_name;
      console.log(this.data);
  }

  addAWBNumbers(form:any) {
    var data: any = {};
    data.shipping_method_id = this.formModel.shipping_method_id;
    data.awb_number = this.formModel.awb_numbers;
    data.tracking_company_name = this.formModel.tracking_company_name;
    console.log(data);
    this._courierService.addAwbMasters(data).subscribe(
       data => {
          this.dialogRef.close();
          if(data.status == 1) {
            this._globalService.showToast(data.message);
          } else {
            this._globalService.showToast(data.message);
          }         
       },
       err => console.log(err) ,
       function(){
        //completed callback
       }
    );
  }

  closeDialog(){
    this.dialogRef.close();
  }
}


@Component({
  templateUrl: './templates/awb_master.html',
  providers: [CourierService]
})
export class ViewAwbComponent implements OnInit {
    public add_edit:any='';
    public response: any;
    public errorMsg: string;
    public successMsg: string;
    public formModel: any = {};
    private sub: any;
    public tabIndex: number;
    public parentId: number = 0;
    public bulk_tags_ids:any = [];
    public rel_data:any = [];
    public pagination:any = {};
    public pageIndex : number = 0;
    public pageList : number = 0;
    public sortBy:any = '';
    public sortOrder:any = '';
    public sortClass:any = '';
    public sortRev:boolean = false;
    public selectedAllTagList:any=false;
    public stat:any = {};
    public result_list_tags:any=[];
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
    public search_text:string;
    public childData:any={};
    public individualRow:any={};
    public shipping_method_id:any;

  constructor(
    private _courierService:CourierService,
    private _globalService:GlobalService,
    private _router: Router,
    private dialogRef: MatDialogRef<ViewAwbComponent>,
    public dialog: MatDialog,
    @Optional() @Inject(MAT_DIALOG_DATA) 
    //private document: any ,
    private data:any
  ) {
    dialog.afterOpen.subscribe(() => {
           let containerElem:HTMLElement = <HTMLElement>document.getElementsByClassName('mat-dialog-container')[0];
           containerElem.classList.remove('pop-box-up');
        }); 
  }
  
  ngOnInit() {
        this.tabIndex = +this._globalService.getCookie('active_tabs');
        this.parentId = this._globalService.getParentTab(this.tabIndex);
        this.shipping_method_id = +this.data;
        this.childData = {
            table : 'EngageboostAwbMasters',
            heading : 'AWB Numbers',
            tabparrentid:this.parentId,
            screen:'list-in-courier',            
        }
        this.generateGrid(0,'','','','');
    }
    generateGrid(reload:any,page:any,sortBy:any,filter:any,search:any) {
         /* let elements: NodeListOf<Element> = this.document.getElementsByClassName('manage-tags');    
          elements[0].classList.remove('show-pop'); */
          this.total_list=[];
          this.selectedAllTagList=false;
          this.filter=filter;
          this.bulk_tags_ids=[];
          this.individualRow={};
          this.sortBy=sortBy;
          if(sortBy!='' && sortBy!=undefined) { 
                if(this.sortRev) {
                  this.sortOrder = '-'
                  this.sortRev = !this.sortRev;
                  this.sortClass = 'icon-down';
                } else {
                  this.sortOrder = '+'
                  this.sortRev = !this.sortRev;
                  this.sortClass = 'icon-up';
                }
            } 
            this.userId =  277;
            this.post_data={"model":this.childData.table,"screen_name":this.childData.screen,"userid": this.userId,"search":search,"order_by":sortBy,"order_type":this.sortOrder,"status":filter,'shipping_method_id' : this.shipping_method_id}        
            this._courierService.doGrid(this.post_data,page).subscribe(
            data => {
                this.response = data;
                console.log(this.response);
                if(this.response.count>0){
                    this.result_list_tags = this.response.results[0].result;
                    this.result_list_tags.forEach(function(item:any){
                        if(item.isblocked =='n') {
                            item.isblocked = 'Active';
                        } else { 
                            item.isblocked = 'Inactive';
                        }  
                    })
                    for (var i = 0; i < this.response.count; i++) {
                        this.total_list.push(i);
                    }                 
                } else {
                    this.result_list_tags =[];
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
            function(){
            });
    }

    search_awb_number(seach_keyword :string,short_by :string) {
        this.generateGrid(1,1,short_by,'',seach_keyword);           
    }
        ////////////////////////////Check/Uncheck//////////////
       /*
    toggleCheckAllTags(event:any){  
        let elements: NodeListOf<Element> = this.document.getElementsByClassName('manage-tags');
        let that=this;
        that.bulk_tags_ids=[];
        this.selectedAllTagList = event.checked;
        this.result_list_tags.forEach(function(item:any){
          item.selected = event.checked;  
          if(item.selected) {
          that.bulk_tags_ids.push(item.id);
              elements[0].classList.add('show-pop');
          } else{
              elements[0].classList.remove('show-pop');
          }
          console.log(item);  
        });
      } 
    toggleCheckTags(id:any,event:any){
        let elements: NodeListOf<Element> = this.document.getElementsByClassName('manage-tags');
        let that=this;
        this.result_list_tags.forEach(function(item:any){
          if(item.id==id){
            item.selected = event.checked;    
            console.log(item);
            if(item.selected) {
                that.bulk_tags_ids.push(item.id);
                 elements[0].classList.add('show-pop');
              } else {
                  var index = that.bulk_tags_ids.indexOf(item.id);
                that.bulk_tags_ids.splice(index, 1);
                elements[0].classList.remove('show-pop');
              }    
        }

        if(that.bulk_tags_ids.length==1){
        that.bulk_tags_ids.forEach(function(item_id:any){
              if(item_id==item.id){
                  that.individualRow=item;
                  }
                });
        } 
        that.selectedAllTagList=false;  
      });
    }         */                 

  closeDialog(){
    this.dialogRef.close();
  }
}






