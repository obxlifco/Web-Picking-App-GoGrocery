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
    searchproductvalue: '',
    shipment_id: 0,
    trent_picklist_id: 0
  }
  item_quantity: any = 0
  incomingmodalData: any = []
  pickerProductList: any = []//list of product data
  productsIDS: any = []
  productQuantity: any = []


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
      product_stock_ids: 1,
      page: 1,
      per_page: 15,
      category_id: this.parentcategory.id,
      in_stock: ""
    }
    this.apiService.postData("picker-searchstock/", data).subscribe((data: any[]) => {
      console.log(data);
      this.pickerProductList["data"] = data
    })
  }


  productDecerment(index: any) {
    // console.log("index --: ",index);
    for (var i = 0; i < this.pickerProductList["data"].response.length; i++) {
      if (i == index) {
        let templength = this.pickerProductList["data"].response[i].quantity - 1
        this.pickerProductList["data"].response[i].quantity = templength;        
      }
    }
  }

  productIncrment(index: any) {
    console.log("index ++: ",index);

    for (var i = 0; i < this.pickerProductList["data"].response.length; i++) {
      if (i === index) {     
           
          let templength = this.pickerProductList["data"].response[i].quantity + 1 //increment the quantity
          this.pickerProductList["data"].response[i].quantity = templength; //assaign quantity to input
          if(this.pickerProductList["data"].response[i].quantity > 0){
            this.productsIDS.push(this.pickerProductList["data"].response[i].id) //push products ids
          }
      }
    }
    // this.productQuantity.push(this.pickerProductList["data"].response[index].quantity) //push quantity to arrays according to selected id's
    this.productsIDS=  this.filterArray(this.productsIDS)
    console.log("productQuantity : ", this.productQuantity);
    // console.log("product list : ", this.pickerProductList["data"]);
    console.log("product ids : ", this.productsIDS);
    // this.pickerManageStocks()
  }

  addProduct(subUrl: any) {
    for (var i = 0; i < this.pickerProductList["data"].response.length; i++) {
      if(this.pickerProductList["data"].response[i].quantity > 0){
        this.productQuantity.push(this.pickerProductList["data"].response[i].quantity)//push quantity to arrays according to selected id's
      }
    }
    if(this.productsIDS.length !== 0){
      this.apiService.postData(subUrl, this.getObjectData()).subscribe((data: any[]) => {
        let tempdata:any=data
        this.globalitem.showSuccess("Product has been added sucessfully in order List !","Product Addedd")
        if(tempdata.status === 1 && tempdata.api_status === 'success'){
          this.dialogRef.close({ event: 'close', data: data});
        }else{
          this.globalitem.showSuccess(tempdata.message,"")
        }
        
      })
    }else{
      this.globalitem.showError("No Product Found, You need to add product first !","No Product")
    }

  }

  filterArray(array:any=[]):any{
    return  array.filter(function(elem: any, index: any, self: string | any[]) {
      return index === self.indexOf(elem);
  })
  }

  getObjectData():any{
    let data = {
      website_id: this.userProductData.website_id,
      warehouse_id: this.userProductData.warehouse_id,
      order_id: this.userProductData.order_id,
      user_id: this.userProductData.user_id,
      shipment_id: this.userProductData.shipment_id,
      trent_picklist_id: this.userProductData.trent_picklist_id,
      action: "increase",
      product_qtys:this.productQuantity,
      // id:177
    }
    if (this.incomingmodalData.productType === 1) { //product type 1 for add more product and 2 for substitute
      let product_ids = {
        category_id: 188,
        product_ids: this.productsIDS,
      }
      Object.assign(data, product_ids.category_id);
      Object.assign(data, product_ids.product_ids);
      
    } else {
      let product_ids = {
        product_id: this.incomingmodalData.product_id,
        sub_product_ids:this.productsIDS,
        sub_product_qtys:this.productQuantity,
      }
      Object.assign(data, product_ids);
      Object.assign(data, product_ids.sub_product_ids);
      Object.assign(data, product_ids.sub_product_qtys);
      
    }

    return data;
  }
}
