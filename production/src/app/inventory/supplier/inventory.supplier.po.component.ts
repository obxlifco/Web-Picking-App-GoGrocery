import { Component,ElementRef,OnInit,Input,Inject} from '@angular/core';
import {Global} from '../../global/service/global';
import {GlobalService} from '../../global/service/app.global.service';
import {Router,ActivatedRoute} from '@angular/router';
import { DomSanitizer } from '@angular/platform-browser';
import {PaginationInstance} from 'ngx-pagination';
import {DialogsService} from '../../global/dialog/confirm-dialog.service';
import {CookieService} from 'ngx-cookie';
import { MatDialog,MatDialogRef,MAT_DIALOG_DATA } from '@angular/material';

import {PurchaseOrderService} from '../purchase-order/inventory.purchase-order.service';
import {DOCUMENT} from '@angular/platform-browser';

@Component({
  templateUrl: './templates/suppliers_po.html',
  providers: [Global,PurchaseOrderService],            
})
export class SupplierPOComponent implements OnInit { 
    
    public tabIndex: number;
    public parentId: number = 0;

    public formModel: any = {};
    public sub: any;
    public response : any;
    public errorMsg: string;
    public successMsg: string;
    public bulk_ids:any = [];
    public pagination:any = {};
    public pageIndex : number = 0;
    public pageList : number = 0;
    public sortBy:any = '';
    public sortOrder:any = '';
    public sortClass:any = '';
    public sortRev:boolean = false;
    public selectedAll:any=false;
    public stat:any = {};
    public result_list:any=[];
    public total_list:any=[];
    public cols:any=[];
    public add_btn : string;
    public post_data = {};
    page: number = 1;
    public filter: string = '';
    public maxSize: number = 10;
    public directionLinks: boolean = true;
    public autoHide: boolean = false;
    public config: any = {};
    public permission:any=[];
    public show_btn:any={'add':true,'edit':true,'delete':true,'block':true};
    public userId:any;
    public user_type:any;
    public individualRow:any={};
    public search_text:any;
    public add_edit:any='';
    public colSpanCount = 4;
    public isManager: any;
    public isSuperAdmin = 'Y';

    constructor(  
       public _globalService: GlobalService,
       private global: Global,
       private _router: Router,
       private _route: ActivatedRoute,
       private sanitizer: DomSanitizer,
       private dialogsService: DialogsService,
       private elRef:ElementRef,
       private _cookieService:CookieService,
       public dialog: MatDialog,
       private _purchaseOrderService:PurchaseOrderService,
       @Inject(DOCUMENT) private document: any
       ) { 

        this.add_edit=this._cookieService.getObject('action');
        if(this.add_edit=='add'){
          this.formModel.supplierId=this._cookieService.getObject('supplier_add');
        }else{
          this.formModel.supplierId=this._cookieService.getObject('supplier_edit');
        }
      }

//////////////////////////Initilise////////////////////////////

  ngOnInit(){

    this.tabIndex = +this._globalService.getCookie('active_tabs');
    this.parentId = this._globalService.getParentTab(this.tabIndex); 
    
    let userData=this._cookieService.getObject('userData');
    this.userId = userData['uid'];
    this.user_type = userData['user_type'];
    this.isManager = userData['isManager'];
    this.isSuperAdmin = userData['isSuperAdmin']; 
    this.generateGrid(0,'','id','','');

  }

/////////////////////////Grid//////////////////////////////////////////////
generateGrid(reload:any,page:any,sortBy:any,filter:any,search:any)
    {  
      if(search==''){this.search_text='';}  
      let elements: NodeListOf<Element> = this.document.getElementsByClassName('action-box');
      elements[0].classList.remove('show');
      this.bulk_ids=[];
      this.individualRow={};
      this.total_list=[];
      this.selectedAll=false;
      this.filter=filter;
      this.sortBy=sortBy;
      if(sortBy!='' && sortBy!=undefined){ 
        if(this.sortRev){
          this.sortOrder = '-';
          this.sortRev = !this.sortRev;
          this.sortClass = 'icon-down';
        }else{
          this.sortOrder = '+';
          this.sortRev = !this.sortRev;
          this.sortClass = 'icon-up';
        }
      }else{
        this.sortBy='id';
        this.sortOrder = '+';
        this.sortRev = !this.sortRev;
        this.sortClass = 'icon-up';
      } 
      this.post_data={"userid":this.userId,"search":search,"order_by":this.sortBy,"order_type":this.sortOrder,"filter":filter, "is_supplier": (this.user_type=='Suppliers')?1:0, "supplier_id": (this.formModel.supplierId)?this.formModel.supplierId:0}
            this._purchaseOrderService.doGrid(this.post_data,page).subscribe(
              data => {
                  this.response = data;
                    if(this.response.count>0){
                      this.result_list = this.response.results[0].result.product;
                      
                      for (var i = 0; i < this.response.count; i++) {
                        this.total_list.push(i);
                      }


                    }else{
                      this.result_list =[];
                    }

                  // this.cols = this.response.results[0].layout;
                  this.cols = this.response.results[0].applied_layout;
                  this.colSpanCount = this.response.results[0].layout.length;
                  this.pagination.total_page = this.response.per_page_count;
                  this.pageList = this.response.per_page_count;
                  this.stat.active = this.response.results[0].active;
                  this.stat.inactive = this.response.results[0].inactive;
                  this.stat.all = this.response.results[0].all;
                  this.add_btn = this.response.results[0].add_btn;
                  this.config.currentPageCount = this.result_list.length
                  this.config.currentPage = page
                  this.config.itemsPerPage = this.response.page_size;
                  this.permission=this.response.results[0].role_permission;
                  
             },
               err => console.log(err),
               function(){
               }
            );

           }  


  ////////////////////////////Check/Uncheck//////////////

  toggleCheckAll(event:any){

    let elements: NodeListOf<Element> = this.document.getElementsByClassName('action-box');

          let that=this;
          that.bulk_ids=[];
        this.selectedAll = event.checked;
        this.result_list.forEach(function(item:any){
          item.selected = event.checked;  
          if(item.selected){
          that.bulk_ids.push(item.id);
          elements[0].classList.add('show');
          }
          else{
          elements[0].classList.remove('show');
          }  
      });
  } 
  toggleCheck(id:any,event:any){

    let elements: NodeListOf<Element> = this.document.getElementsByClassName('action-box');

      let that=this;
      //that.bulk_ids=[];
        this.result_list.forEach(function(item:any){
          if(item.id==id){
            item.selected = event.checked;  
            if(item.selected)
            {
              that.bulk_ids.push(item.id);
              elements[0].classList.add('show');
            }
            else{
              var index = that.bulk_ids.indexOf(item.id);
                      that.bulk_ids.splice(index, 1);
                      if(that.bulk_ids.length==0){
                      elements[0].classList.remove('show');
                      } 
            }  
          }
          if(that.bulk_ids.length==1){
            that.bulk_ids.forEach(function(item_id:any){
              if(item_id==item.id){
                that.individualRow=item;
              }
            });
          } 
          that.selectedAll=false;     

      });
   }
  /////////////////////////Filter Grid//////////////////////
  
  updateGrid(isdefault:any){
    this.global.doGridFilter('EngageboostPurchaseOrders',isdefault,this.cols,"list").subscribe(
       data => {
           this.response = data;
           this.generateGrid(0,'','','','');
         },
       err => console.log(err),
       function(){
       }
    );
  }  

  // dialogPoSentRef: MatDialogRef<PoSentComponent> | null;
  // dialogShipTrackRef: MatDialogRef<ShipTrackComponent> | null;
  // dialogPoReceivedRef: MatDialogRef<PoReceivedComponent> | null;
  // changePoStatus(id:number, status: string){

  //   let request_data:any = {};
  //   request_data['id'] = id;
  //   if(status=='Cancel'){
  //     request_data['status'] = status;

  //     this.poStatusCallback(request_data);
  //   }else if(status=='PO Sent'){

  //     let data: any = {};
  //     data['po_id'] = id;
  //     this.dialogPoSentRef = this.dialog.open(PoSentComponent, {data: data});
  //     this.dialogPoSentRef.afterClosed().subscribe(result => {
  //       if(result){
  //         this.poStatusCallback(result);
  //       }
  //     });
  //   }else if(status=='Shipped'){
  //     let data: any = {};
  //     data['po_id'] = id;
  //     this.dialogShipTrackRef = this.dialog.open(ShipTrackComponent, {data: data});
  //     this.dialogShipTrackRef.afterClosed().subscribe(result => {
  //       if(result){
  //         this.poStatusCallback(result);
  //       }
  //     });
  //   }else if(status=='Grn Pending'){
  //     let data: any = {};
  //     data['po_id'] = id;
  //     data['po_datails'] = this.individualRow;
  //     this.dialogPoReceivedRef = this.dialog.open(PoReceivedComponent, {data: data});
  //     this.dialogPoReceivedRef.afterClosed().subscribe(result => {
  //       if(result){
          
  //         let post_data: any = {};
  //         post_data['id'] = result['id'];
  //         post_data['status'] = result['status'];
  //         post_data['received_id'] = result['receipt_no'];
  //         post_data['received_date'] = result['received_date'];
  //         post_data['warehouse_id'] = result['warehouse_id'];
  //         this.poStatusCallback(post_data);
  //       }
  //     });
  //   }else if(status=='Received Full'){
      
  //     this._router.navigate(['/purchase_order/grn/'+id]);
  //     this._globalService.addTab('purchaseordergrn','/purchase_order/grn/'+id,'Purchase Order GRN',this.parentId);
  //   }


  // }

  poStatusCallback(request_data:any){

    this._purchaseOrderService.changePoStatus(request_data).subscribe(
      data => {
        this.generateGrid(0,'','','','');  
      },
      err => console.log(err),
      function(){
      }
    );
  }

  supplierExit(){

    if(this.add_edit=='add'){
      this._cookieService.remove('supplier_add');
    }else{
      this._cookieService.remove('supplier_edit');
    }
    this._cookieService.remove('action');
    this._router.navigate(['/suppliers']);
    this._globalService.deleteTab(this.tabIndex,this.parentId);
  }

}



// @Component({
//   templateUrl: '../purchase-order/templates/po_sent.html',
//   providers: [PurchaseOrderService]
// })
// export class PoSentComponent implements OnInit { 

//   public formModel:any = {};

//   constructor(
//     public _globalService: GlobalService,
//     private _purchaseOrderService: PurchaseOrderService,
//     public dialog: MatDialog,
//     private dialogRef: MatDialogRef<PoSentComponent>,
//     @Inject(MAT_DIALOG_DATA) public data: any
//   ) {
    
//   }

//   ngOnInit(){

//     this._purchaseOrderService.getSupplierEmail(this.data.po_id).subscribe(
//       data => {
//         this.formModel.supplier_email = data.email;
//       },
//       err => console.log(err),
//       function(){
//       }
//     );
//   }

//   poSent(form: any){

//     let returnData:any = {};
//     returnData['id'] = this.data.po_id;
//     returnData['status'] = 'PO Sent';
//     returnData['supplier_email'] = this.formModel.supplier_email;
//     if(this.formModel.send_email){
//       returnData['send_email'] = 1;
//     }else{
//       returnData['send_email'] = 0;
//     }
//     this.dialogRef.close(returnData);
//   }


// }


// @Component({
//   templateUrl: '../purchase-order/templates/shipping_track.html',
//   providers: [PurchaseOrderService]
// })
// export class ShipTrackComponent implements OnInit { 

//   public formModel:any = {};

//   constructor(
//     public _globalService:GlobalService,
//     private _purchaseOrderService: PurchaseOrderService,
//     public dialog: MatDialog,
//     private dialogRef: MatDialogRef<ShipTrackComponent>,
//     @Inject(MAT_DIALOG_DATA) public data: any
//   ) {
    
//   }

//   ngOnInit(){

    
//   }

//   shipTrack(form: any){

//     let returnData:any = {};

//     returnData = Object.assign({},this.formModel);
//     returnData['id'] = this.data.po_id;
//     returnData['status'] = 'Shipped';
    
//     if(!this.formModel['tracking_company']){
//       returnData['tracking_company'] = '';
//     }
//     if(!this.formModel['tracking_id']){
//       returnData['tracking_id'] = '';
//     }
//     if(!this.formModel['tracking_url']){
//       returnData['tracking_url'] = '';
//     }
//     this.dialogRef.close(returnData);
//   }


// }


// @Component({
//   templateUrl: '../purchase-order/templates/po_received.html',
//   providers: [PurchaseOrderService]
// })
// export class PoReceivedComponent implements OnInit { 

//   public formModel:any = {};
//   public minDate:any;

//   constructor(
//     public _globalService:GlobalService,
//     private _purchaseOrderService: PurchaseOrderService,
//     public dialog: MatDialog,
//     private dialogRef: MatDialogRef<ShipTrackComponent>,
//     @Inject(MAT_DIALOG_DATA) public data: any
//   ) {
    
//   }

//   ngOnInit(){

//     this.formModel = Object.assign({},this.data.po_datails);
    
//     var match = /(\d+)-(\d+)-(\d+)/.exec(this.formModel.order_date);
//     this.formModel.order_date = new Date(+match[3],(+match[2])-1,+match[1]);
//     this.minDate = new Date();
//     this.formModel.received_date = new Date();

//     this._purchaseOrderService.getPoReceived(this.formModel.id).subscribe(
//       data => {
//         this.formModel.receipt_no = data.received_code;
//         this.formModel.total_qty = data.total_qty;
//         this.formModel.warehouse_id = data.warehouse_id;
//       },
//       err => console.log(err),
//       function(){
//       }
//     );
//   }

//   poReceived(form: any){

//     let returnData:any = {};

//     returnData = Object.assign({},this.formModel);
//     returnData['status'] = 'Grn Pending';
    
//     this.dialogRef.close(returnData);
//   }


// }