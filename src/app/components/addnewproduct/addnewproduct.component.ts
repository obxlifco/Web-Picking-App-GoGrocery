import { Component, Inject, OnInit } from '@angular/core';
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { Router } from '@angular/router';
import { ApiService } from 'src/app/services/api/api.service';
import { DatabaseService } from 'src/app/services/database/database.service';
import { GlobalitemService } from 'src/app/services/globalitem/globalitem.service';
import { AddproductcategoryComponent } from '../addproductcategory/addproductcategory.component';

export interface DialogData {
  animal: string;
  name: string;
}
@Component({
  selector: 'app-addnewproduct',
  templateUrl: './addnewproduct.component.html',
  styleUrls: ['./addnewproduct.component.scss']
})
export class AddnewproductComponent implements OnInit {

  name: any = "Pepsi 2";
  category: any = "drink 2";
  userProductData = {
    warehouse_id: '',
    website_id: '',
    user_id: '',
    order_id: '',
    page: 1,
    per_page: 2,
    search: "5055179722036",
    ean: "",
    category_id: 188
  }

  incomingmodalData:any=[]
  pickerProductList:any=[]
  constructor(public router: Router, public dialog: MatDialog,
    public db: DatabaseService,
    public apiService: ApiService,
    public globalitem: GlobalitemService,
    public dialogRef: MatDialogRef<AddnewproductComponent>,
    @Inject(MAT_DIALOG_DATA) public data: DialogData) {
      this.pickerProductList["data"]=[]
    console.log("modal incoming data : ", data);
    // this.userProductData.order_id = ""+data ;
    let temp:any=data
    this.incomingmodalData=temp.data
    this.userProductData.order_id=this.incomingmodalData.order_id
    this.getProductlistData()
  }

  ngOnInit(): void {

    
  }

  opencategory_modal(categoryURl:any): void {
    const dialogRef = this.dialog.open(AddproductcategoryComponent, {
      width: '500px',
      data: { name: this.name, category: categoryURl }
    });

    dialogRef.afterClosed().subscribe(result => {
      console.log('The dialog was closed', result);
      this.category = result;
    });
  }

  openSubcategory_modal(categoryURl:any): void {
    const dialogRef = this.dialog.open(AddproductcategoryComponent, {
      width: '500px',
      data: { name: this.name, category: categoryURl }
    });

    dialogRef.afterClosed().subscribe(result => {
      console.log('The dialog was closed', result);
      this.category = result;
    });
  }

  closeModal(): void {
    this.dialogRef.close();
  }

  addProduct() {
    this.name = "changed name"
    this.category = "changed Category"
    let data = {
      name: this.name,
      category: this.category
    }
    this.dialogRef.close({ event: 'close', data: data });
  }

  getProductlistData() {
    this.db.getUserData().then(res => {
      console.log("user data inside dashboard : ", res);

      let data = {
        website_id: res.website_id,
        user_id:res.user_id,
        order_id: this.userProductData.order_id,
        warehouse_id: res.warehouse_id,
        page: 1,
        per_page: 2,
        search: "5055179722036",
        ean: "",
        // category_id: 188
      }
      if(this.incomingmodalData.productType === 1){
        let category_ids={
          category_id : 188
        } 
        Object.assign(data, category_ids);
      }else{
        let product_ids={
          product_id : this.incomingmodalData.product_id
        } 
        Object.assign(data,product_ids);
      }
      console.log("product id checking : ",data);
      
      this.userProductData.warehouse_id = res.warehouse_id
      this.userProductData.website_id = res.website_id
      this.userProductData.user_id = res.user_id
      this.apiService.postData(this.incomingmodalData.apiURL, data).subscribe((data: any[]) => {
        console.log(data);
        this.pickerProductList["data"] = data
      })
    })

  }
}
