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

  parentcategory: any = []
  subcategory: any = []
  userProductData = {
    warehouse_id: '',
    website_id: '',
    user_id: '',
    order_id: '',
    page: 1,
    per_page: 2,
    search: "5055179722036",
    ean: "",
    category_id: 188,
    searchproductvalue:''
  }
  item_quantity:any='1'
  incomingmodalData: any = []
  pickerProductList: any = []

  constructor(public router: Router, public dialog: MatDialog,
    public db: DatabaseService,
    public apiService: ApiService,
    public globalitem: GlobalitemService,
    public dialogRef: MatDialogRef<AddnewproductComponent>,
    @Inject(MAT_DIALOG_DATA) public data: DialogData) {
    this.pickerProductList["data"] = []
    console.log("modal incoming data : ", data);
    // this.userProductData.order_id = ""+data ;
    let temp: any = data
    this.incomingmodalData = temp.data
    this.userProductData.order_id = this.incomingmodalData.order_id
    this.getProductlistData()
  }

  ngOnInit(): void {


  }

  opencategory_modal(categoryURl: any): void {
    let data = {
      website_id: this.userProductData.website_id,
      warehouse_id: this.userProductData.warehouse_id,
      parent_id: null,
      categoryURl: categoryURl
    }
    const dialogRef = this.dialog.open(AddproductcategoryComponent, {
      width: '500px',
      data: { data: data }
    });

    dialogRef.afterClosed().subscribe(result => {
      console.log('The dialog was closed', result);
      this.parentcategory = result.data;
    });
  }

  openSubcategory_modal(categoryURl: any): void {
    let data = {
      website_id: this.userProductData.website_id,
      warehouse_id: this.userProductData.warehouse_id,
      parent_id: this.parentcategory.parent_id,
      categoryURl: categoryURl
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

  closeModal(): void {
    this.dialogRef.close();
  }

  addProduct() {
    // this.name = "changed name"
    // this.category = "changed Category"

    let data = {
      name: 'this.name',
      category: 'this.category',
      user_id: 2,
      order_id: 2223,
      warehouse_id: 33,
      shipment_id: 1182,
      trent_picklist_id: 1187,
      product_ids: [18614],
      action: 2,
      quantity: 1
    }
    this.dialogRef.close({ event: 'close', data: data });
  }

  getProductlistData() {
    this.db.getUserData().then(res => {
      console.log("user data inside dashboard : ", res);

      let data = {
        website_id: res.website_id,
        user_id: res.user_id,
        order_id: this.userProductData.order_id,
        warehouse_id: res.warehouse_id,
        page: 1,
        per_page: 2,
        search: "5055179722036",
        ean: "",
        // category_id: 188
      }
      if (this.incomingmodalData.productType === 1) { //product type 1 for add more product and 2 for substitute
        let category_ids = {
          category_id: 188
        }
        Object.assign(data, category_ids);
      } else {
        let product_ids = {
          product_id: this.incomingmodalData.product_id
        }
        Object.assign(data, product_ids);
      }
      console.log("product id checking : ", data);
      this.userProductData.warehouse_id = res.warehouse_id
      this.userProductData.website_id = res.website_id
      this.userProductData.user_id = res.user_id
      this.apiService.postData(this.incomingmodalData.apiURL, data).subscribe((data: any[]) => {
        console.log(data);
        this.pickerProductList["data"] = data
      })
    })
  }

  searchProducts() {
    let data = {
      website_id: this.userProductData.website_id,
      warehouse_id: this.userProductData.warehouse_id,
      product_stock_ids:1,
      page: 1,
      per_page: 15,
      category_id: this.parentcategory.id,
      in_stock:""
    }
      this.apiService.postData("picker-searchstock/", data).subscribe((data: any[]) => {
        console.log(data);
        this.pickerProductList["data"] = data
      })
  }
}
