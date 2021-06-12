import {GlobalService } from '../../global/service/app.global.service';
import {CookieService} from 'ngx-cookie';
import {Component,ElementRef,OnInit,Input,Inject} from '@angular/core';
import {Global} from '../../global/service/global';
import {Router} from '@angular/router';
import {DomSanitizer } from '@angular/platform-browser';
import {PaginationInstance} from 'ngx-pagination';
import {DialogsService} from '../../global/dialog/confirm-dialog.service';
import { MatDialog,MatDialogRef,MAT_DIALOG_DATA } from '@angular/material';
import {DOCUMENT} from '@angular/platform-browser';
import {StockAdjustmentService} from './inventory.stock.adjustment.service';
@Component({
  selector: 'my-app',
  templateUrl: `./templates/stock-adjustment.html`,
  providers: [Global,StockAdjustmentService],  
})

export class StockAdjustmentComponent implements OnInit { 
// @Input() childData: {table: string, heading: string, tablink:string,tabparrentid:any,screen:any,ispopup:any};
constructor(  
       private globalService: GlobalService,
       private global: Global,
       private _router: Router,
       private sanitizer: DomSanitizer,
       private dialogsService: DialogsService,
       private elRef:ElementRef,
       private _cookieService:CookieService,
       public dialog: MatDialog,
       private _productService:StockAdjustmentService,
       @Inject(DOCUMENT) private document: any
       ) { }

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
    public cols:any=[]
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
    public individualRow:any={};
    public search_text:any;
    public childData:any={};
    public stock_type:any='';
//////////////////////////Initilise////////////////////////////

 ngOnInit(){
  let userData=this._cookieService.getObject('userData');
  this.userId = userData['uid']; 
  this.childData = {
        table : 'EngageboostPurchaseOrdersReceived',
        heading : 'Product',
        ispopup:'N',
        tablink:'stock_adjustment',
        screen:'list'
      } 
  this.generateGrid(0,'','','','','');
 }

/////////////////////////Grid//////////////////////////////////////////////
generateGrid(reload:any,page:any,sortBy:any,filter:any,search:any,stock_type:any)
    {  

      if(search==''){
        this.search_text='';
      }else{
        this.search_text = search;
      }
      let elements: NodeListOf<Element> = this.document.getElementsByClassName('action-box');
      elements[0].classList.remove('show');
      this.bulk_ids=[];
      this.individualRow={};
      this.total_list=[];
      this.selectedAll=false;
      this.filter=filter;
      this.filter=filter;
      this.stock_type=stock_type;
          

        if(sortBy!='' && sortBy!=undefined){ 
          if(this.sortRev){
            this.sortOrder = '-'
            this.sortRev = !this.sortRev;
            this.sortClass = 'icon-down';
          }else{
            this.sortOrder = '+'
            this.sortRev = !this.sortRev;
            this.sortClass = 'icon-up';
          }
        } 
      this.post_data={"screen_name":this.childData.screen,"userid":this.userId,"search":search.trim(),"order_by":sortBy,"order_type":this.sortOrder,"status":filter,"stock_type":stock_type}
            this._productService.doGrid(this.post_data,page).subscribe(
               data => {
                   this.response = data;
                   if(this.response.count>0){
                     this.result_list = this.response.results[0].result;
                     this.result_list.forEach(function(item:any){
                      if(item.isblocked =='n'){
                        item.isblocked = 'Active';
                      }else{
                        item.isblocked = 'Inactive';
                      } 
                      
                     })
                      for (var i = 0; i < this.response.count; i++) {
                      this.total_list.push(i);
                      }

                   }else{
                       this.result_list =[];
                   }

                  // this.cols = this.response.results[0].layout;
                  this.cols = this.response.results[0].applied_layout;
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

////////////////////////Delete/Block/Unblock///////////////////////////////

      updateStatusAll(type:number,id:number)
      {
          if(id)
          {  
            let that=this;
            that.bulk_ids=[];
            that.bulk_ids.push(id);
          }

          if(type==2){var msg='Do you really want to delete selected records?'; var perm=this.permission.delete;var msgp='You have no permission to delete!';}  
          else if(type==1){var msg='Do you really want to block selected records?';var perm=this.permission.block;var msgp='You have no permission to block!';}
          else{var msg='Do you really want to unblock selected records?';var perm=this.permission.block;var msgp='You have no permission to unblock!';}
          if(perm=='Y'){
              if(this.bulk_ids.length>0){
                  this.dialogsService.confirm('Warning', msg).subscribe(res => {
                        if(res){
                          this.global.doStatusUpdate(this.childData.table,this.bulk_ids,type).subscribe(
                               data => {
                                   this.response = data;
                                   this.globalService.showToast(this.response.Message);
                                   this.generateGrid(0,'','','','',1);
                                 },
                               err => console.log(err),
                               function(){
                               }
                            );
                        }
                      });
            }
            else
            {
                  this.dialogsService.alert('Error', 'Select Atleast One Record!').subscribe(res => {});
            }
        }
          else{
            this.dialogsService.alert('Permission Error', msgp).subscribe(res => {});
           }      

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
       this._productService.doGridFilter(this.childData.table,isdefault,this.cols,"list").subscribe(
           data => {
               this.response = data;
               this.generateGrid(0,'','','','','');
             },
           err => console.log(err),
           function(){
           }
        );
  }  


  dialogPoSentRef: MatDialogRef<PoProductViewComponent> | null;
  openPoProductPop(index: number){
    let products: any = [];
    products = this.result_list[index]['products'];
    this.dialogPoSentRef = this.dialog.open(PoProductViewComponent, {data: products});
    this.dialogPoSentRef.afterClosed().subscribe(result => {
      if(result){
        
      }
    });
  }
}

@Component({
  templateUrl: './templates/po_products.html',
  providers: [StockAdjustmentService]
})
export class PoProductViewComponent implements OnInit { 

  public products_list: any = [];

  constructor(
    public _globalService:GlobalService,
    private _stockAdjustmentService: StockAdjustmentService,
    public dialog: MatDialog,
    private dialogRef: MatDialogRef<PoProductViewComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any
  ) {
    this.products_list = data;
  }


  ngOnInit(){
      

  }

  closeDialog(){
    this.dialogRef.close();
  }


}
