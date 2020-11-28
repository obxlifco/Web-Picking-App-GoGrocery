import { Component, Inject, OnInit } from '@angular/core';
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { DialogData } from 'src/app/components/addnewproduct/addnewproduct.component';
import { AddproductcategoryComponent } from 'src/app/components/addproductcategory/addproductcategory.component';
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
    category_id:''
  }
  pickerProductList:any=[]
  stockStatus:any;
  parentcategory: any = []
  subcategory: any = []
  cat_price:any='';

  constructor(private modalservice : ModalService,public db :DatabaseService,
    public apiService : ApiService,
    public dialog: MatDialog,
    ) {
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
  opencategory_modal():void{
    let data = {
      categoryURl: "picker-stockcategory/",
     parent_id: null,
     
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
    });

  }

  
  opensub_category_modal():void{
    let data = {
      website_id: this.userOrderdata.website_id,
      warehouse_id: this.userOrderdata.warehouse_id,
      parent_id: this.parentcategory.parent_id,
      categoryURl: "picker-stockcategory/",
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

  searchProducts() {
    console.log("stockStatus : ",this.stockStatus);
    
    let data = {
      product_stock_ids: 1,
      website_id: this.userOrderdata.website_id,
      warehouse_id: this.userOrderdata.warehouse_id,
      page: 1,
      per_page: 15,
      category_id: this.userOrderdata.category_id,
      in_stock: this.stockStatus
    }

    this.apiService.postData("picker-searchstock/", data).subscribe((data: any[]) => {
      console.log(data);
      this.pickerProductList["data"] = data
    })
  }

}
