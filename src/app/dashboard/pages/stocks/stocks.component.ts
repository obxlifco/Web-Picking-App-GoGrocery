import { Component, Inject, OnInit } from '@angular/core';
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { DialogData } from 'src/app/components/addnewproduct/addnewproduct.component';
import { AddproductcategoryComponent } from 'src/app/components/addproductcategory/addproductcategory.component';
import { MessagedialogComponent } from 'src/app/components/messagedialog/messagedialog.component';
import { ApiService } from 'src/app/services/api/api.service';
import { DatabaseService } from 'src/app/services/database/database.service';
import { GlobalitemService } from 'src/app/services/globalitem/globalitem.service';
import { ModalService } from 'src/app/services/modal/modal.service';

@Component({
  selector: 'app-stocks',
  templateUrl: './stocks.component.html',
  styleUrls: ['./stocks.component.scss']
})
export class StocksComponent implements OnInit {

  userOrderdata = {
    warehouse_id: '',
    website_id: '',
    user_id: '',
    picker_name: '',
    order_id: '',
    shipment_id: '',
    order_status: '',
    trent_picklist_id: 0,
    substitute_status:'',
    shortage:'',
    grn_quantity:0,
    product_id:'',
    order_product_id:'',
    category_id:'',
    searchProductvalue:''
  }
  
  pickerProductList:any=[]
  stockStatus:any='';
  parentcategory: any = []
  subcategory: any = []
  cat_price:any='';
  IsDataLoaded=false
  throttle = 300;
  scrollDistance = 2;
  scrollUpDistance = 1;
  productpage:any=1
  totalProductpage:any;
  constructor(private modalservice : ModalService,public db :DatabaseService,
    public apiService : ApiService,
    public globalitem : GlobalitemService,
    public dialog: MatDialog,
    ) {
      // this.pickerProductList=[]
      this.pickerProductList["data"]=[]
      
    this.getuserData()
   }

  ngOnInit(): void {
  }

  getuserData(){
    this.db.getUserData().then(res => {
      console.log("user data inside dashboard : ", res);

      this.userOrderdata.warehouse_id=res.warehouse_id
      this.userOrderdata.website_id=res.website_id
      this.userOrderdata.user_id=res.user_id

      let data = {
        warehouse_id: res.warehouse_id,
        website_id: res.website_id,
      }
  }
    );
}
  opencategory_modal(catname:any):void{
    let data = {
      URl: "picker-stockcategory/",
     parent_id: null,
     catname:catname,
     warehouse_id: this.userOrderdata.warehouse_id,
     website_id:  this.userOrderdata.website_id
     }
    //  this.modalservice.openSubCategoryModal(data)
    //  this.modalservice.closeCategoryModal().then(data => {
    //    console.log("closed Modal : ", data);
    //    if(data.subtitutestatus === "productadded"){
    //      // this.updateMoreProductQuantity(data.substituteData.grn_quantity,data.substituteData.product_id,data.substituteData.order_product_id,data.substituteData.shortage,0)
    //    }
    //  })
    const dialogRef = this.dialog.open(AddproductcategoryComponent, {
      width: '500px',
      data: { data: data }
    });

    dialogRef.afterClosed().subscribe(result => {
      console.log('The dialog was closed', result);
      this.parentcategory = result.data;
      this.subcategory.name="Sub Category"
      this.subcategory.id=''
      if(result.data === "undefined"){
        // this.subcategory.name="Sub Category"
        // this.subcategory.id=''
        this.parentcategory.id =''
      }
    });

  }

  
  opensub_category_modal(catname:any):void{
    let data = {
      website_id: this.userOrderdata.website_id,
      warehouse_id: this.userOrderdata.warehouse_id,
      parent_id: this.parentcategory.id,
      catname:catname,
      URl: "picker-stockcategory/",
    }
    const dialogRef = this.dialog.open(AddproductcategoryComponent, {
      width: '500px',
      data: { data: data }
    });

    dialogRef.afterClosed().subscribe(result => {
      console.log('The dialog was closed', result);
      this.subcategory = result.data;
    });
  }

  openDialog(): void {
    // this.updateMoreProductQuantity(quantity,product_id,order_product_id,shortage,index)
    let data = {
     categoryURl: "picker-stockcategory/",
    parent_id: null,
    warehouse_id: this.userOrderdata.warehouse_id,
    website_id:  this.userOrderdata.website_id
    }
    // this.modalservice.openCategoryModal(data)
    // this.modalservice.closeCategoryModal().then(data => {
    //   console.log("closed Modal : ", data);
    //   if(data.subtitutestatus === "productadded"){
    //     // this.updateMoreProductQuantity(data.substituteData.grn_quantity,data.substituteData.product_id,data.substituteData.order_product_id,data.substituteData.shortage,0)
    //   }
    // })


  }

  searchProducts(value:any) {
    console.log("stockStatus : ",this.stockStatus);
    if(value === "search"){
      this.totalProductpage=0;
      this.productpage=1
      this.pickerProductList["data"]=[]
      console.log("enter");
      
    }
    let temcategory:any;
    if(this.subcategory.id !== undefined){
      temcategory= this.subcategory.id
    }else{
      temcategory= this.parentcategory.id
    }
    console.log("child Category : ", this.subcategory.id , "Parent Category : ",this.parentcategory.id);
    
    this.IsDataLoaded = true
    let data = {
      website_id: this.userOrderdata.website_id,
      warehouse_id: this.userOrderdata.warehouse_id,
      page: this.productpage,
      search:this.userOrderdata.searchProductvalue,
      // per_page: 15,
      category_id: temcategory,
      in_stock: this.stockStatus,
      has_price:this.cat_price,
      // product_stock_ids: 1
    }
    this.apiService.postData("picker-searchstock/", data).subscribe((data: any) => {
      console.log(data);
      
      if(this.productpage === 1){
        this.pickerProductList["data"]=data.response
        this.totalProductpage=data.total_page
        console.log("page 1");
        
      }else{
        console.log("page n");
        this.pickerProductList["data"] = [... this.pickerProductList["data"], ...data.response];
      }
     
      
      this.IsDataLoaded = false
    })
  }
  onScrollDown(ev:any) {
    console.log('scrolled!!',ev);
    this.productpage++;
    if(this.productpage <= this.totalProductpage){
      console.log(" this.totalProductpage : ",this.totalProductpage );
      console.log("  this.productpage : ", this.productpage );
      
      this.searchProducts("novalue")
    }else{
      // this.globalitem.showError("No more data is available ","No Data")
    }
  
  }

  onChange(event:any,price:any,productid:any,productindex:any){
    this.userOrderdata.product_id=productid
    if(event.checked === true && price === 0){
      const dialogRef = this.dialog.open(MessagedialogComponent, {
        width: '500px',
        data: { data: 'novalue' }
      });
      dialogRef.afterClosed().subscribe(res => {
        this.searchProducts("novalue") 
      });
    }else{
      if(event.checked === true){
        this.updateProductPice(price,productid,100)
      }else{
        this.updateProductPice(price,productid,0)
      }
      
    }
  }
  updateProductPice(price:any,productid:any,stockstatus:any){

    let data = {
      website_id: this.userOrderdata.website_id,
      warehouse_id: this.userOrderdata.warehouse_id,
      user_id: this.userOrderdata.user_id,
      product_id: productid,
      price: price,
      stock:stockstatus
    }
    this.apiService.postData("picker-managestock/", data).subscribe((data: any[]) => {
      console.log(data);
      // this.pickerProductList["data"] = data
      // this.IsDataLoaded = false
      // this.searchProducts()

    })
  }
  editprice(event:any,price:any,productid:any,productindex:any,IsInstock:any){
    let data={
      checked:event.checked,
      price:price,
      productid:productid,
      IsInstock:IsInstock
    }
    const dialogRef = this.dialog.open(MessagedialogComponent, {
      width: '500px',
      data: { data: data }
    });

    dialogRef.afterClosed().subscribe(res => {
      console.log('Dialog result:',res,productindex);
      console.log("Modal Data : ",this.pickerProductList["data"]);
      this.pickerProductList["data"][productindex].channel_currency_product_price.price = res.price
      if(res.price > 0){
        this.pickerProductList["data"][productindex].product_stock.stock = IsInstock
        this.updateProductPice(res.price,res.data.data.productid,IsInstock);
      }else{
      }
    });
  }
}
