import { Component, Inject, OnInit } from '@angular/core';
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { Router } from '@angular/router';
import { ApiService } from 'src/app/services/api/api.service';
import { DatabaseService } from 'src/app/services/database/database.service';
import { GlobalitemService } from 'src/app/services/globalitem/globalitem.service';
import { AddproductasSubtituteComponent } from '../addproductas-subtitute/addproductas-subtitute.component';
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
    trent_picklist_id: 0,
    // product_id: '',
    searchproductlist: ''
  }
  item_quantity: any = 0
  incomingmodalData: any = []
  pickerProductList: any = []//list of product data
  productsIDS: any = []
  productQuantity: any = []
  subtituteSelectedProducts:any=[]

  constructor(public router: Router,
    public db: DatabaseService,
    public apiService: ApiService,
    public globalitem: GlobalitemService,
    public dialog: MatDialog,
    public dialogRef: MatDialogRef<AddnewproductComponent>,
    @Inject(MAT_DIALOG_DATA) public data: DialogData) {
    this.pickerProductList["data"] = []
    // console.log("modal incoming data : ", data);
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
      // console.log('The dialog was closed', result);
      this.parentcategory = result.data;
    });
  }

  openSub_modal(ApiURl: any, product_id: any, related_product_id: any, related_product_type: any, modaltype: any): void {
    let data = {
      website_id: this.userProductData.website_id,
      warehouse_id: this.userProductData.warehouse_id,
      parent_id: this.parentcategory.parent_id,
      URl: ApiURl,
      product_id: product_id,
      related_product_id: related_product_id,
      related_product_type: related_product_type
    }
    const dialogRef = this.dialog.open(modaltype, {
      width: '500px',
      data: { data: data }
    });

    dialogRef.afterClosed().subscribe(result => {
      // console.log('The dialog was closed', result);
      if (result.data !== "none") {
        this.subcategory = result.data;
      } else if (result.data === "none") {
        // console.log("search text", this.userProductData.searchproductvalue);
        // this.searchProducts()
        this.getProductlistData()
      }

    });
  }

  closeModal(): void {
    this.dialogRef.close({ event: 'close', data: this.incomingmodalData.storage, subtitutestatus: "no_productadded" });
  }

  getProductlistData() {
    this.db.getUserData().then(res => {
      // console.log("user data inside dashboard : ", res);

      let data = {
        website_id: res.website_id,
        user_id: res.user_id,
        order_id: this.userProductData.order_id,
        warehouse_id: res.warehouse_id,
        // page: 1,
        // per_page: 2,
        // search: "5055179722036",
        ean: "",
        // category_id: 188
      }
      if (this.incomingmodalData.productType === 1) { //product type 1 for add more product and 2 for substitute
        let category_ids = {
          category_id: 188
        }
        this.userProductData.searchproductlist = 'picker-productlist/'
        Object.assign(data, category_ids);
      } else {
        let product_ids = {
          product_id: this.incomingmodalData.product_id
        }
        Object.assign(data, product_ids);
        this.userProductData.searchproductlist = 'picker-substituteproductlist/'
      }
      // console.log("product id checking : ", data);
      this.userProductData.warehouse_id = res.warehouse_id
      this.userProductData.website_id = res.website_id
      this.userProductData.user_id = res.user_id
      this.apiService.postData(this.incomingmodalData.apiURL, data).subscribe((data: any[]) => {
        // console.log(data);
        this.pickerProductList["data"] = data
      })
    })
  }

  searchProducts() {
    let data = {
      website_id: this.userProductData.website_id,
      warehouse_id: this.userProductData.warehouse_id,
      // page: 1,
      // per_page: 15,
      search: this.userProductData.searchproductvalue,
      ean: "",
      user_id: this.userProductData.user_id,
      order_id: this.userProductData.order_id,
    }

    if (this.incomingmodalData.productType === 2) { //product type 1 for add more product and 2 for substitute
      let product_ids = {
        product_id: this.incomingmodalData.product_id
      }
      Object.assign(data, product_ids);
    } else if (this.incomingmodalData.productType === 1) {
      let category_ids = {
        category_id: 188,
      }
      Object.assign(data, category_ids);
    }
    this.apiService.postData(this.userProductData.searchproductlist, data).subscribe((data: any[]) => {
      // console.log(data);
      this.pickerProductList["data"] = data
    })
  }


  productDecerment(index: any, substitutestatus: any, relatedproductid: any, relatedproducttype: any) {
    // console.log("index --: ",index);
    for (var i = 0; i < this.pickerProductList["data"].response.length; i++) {
      if (i == index) {
        let templength = this.pickerProductList["data"].response[i].quantity - 1
        // console.log(templength);

        if (templength === 0) {
          // arr.splice(arr.indexOf('Orange'), 1);
          this.productsIDS.splice(this.productsIDS.indexOf(this.pickerProductList["data"].response[i].id), 1)
          this.productsIDS.splice(this.productsIDS.indexOf(this.pickerProductList["data"].response[i].quantity), 1)
          this.pickerProductList["data"].response[i].quantity = templength
        } else if (templength < 0) {
          this.pickerProductList["data"].response[i].quantity = 0;
        } else {
          this.pickerProductList["data"].response[i].quantity = templength
        }

      }
    }
  }

  productIncrment(index: any, substitutestatus: any, relatedproductid: any, relatedproducttype: any) {
    // console.log("index ++: ", index, " substitutestatus : ", substitutestatus);
    if (substitutestatus !== 0) {
      for (var i = 0; i < this.pickerProductList["data"].response.length; i++) {
        if (i === index) {
          let templength = this.pickerProductList["data"].response[i].quantity + 1 //increment the quantity
          this.pickerProductList["data"].response[i].quantity = templength; //assaign quantity to input
          if (this.pickerProductList["data"].response[i].quantity > 0) {
            this.productsIDS.push(this.pickerProductList["data"].response[i].id) //push products ids
          }
        }
      }
      // this.productQuantity.push(this.pickerProductList["data"].response[index].quantity) //push quantity to arrays according to selected id's
      this.productsIDS = this.filterArray(this.productsIDS)
    } else {
      this.openSub_modal('picker-add-product-as-substitute/', this.incomingmodalData.product_id, relatedproductid, relatedproducttype, AddproductasSubtituteComponent)
    }
  }

  addSubtituteProduct(subUrl: any) {

    for (var i = 0; i < this.pickerProductList["data"].response.length; i++) {
      if (this.pickerProductList["data"].response[i].quantity > 0) {
        this.productQuantity.push(this.pickerProductList["data"].response[i].quantity)//push quantity to arrays according to selected id's
      }
    }
    let data = {
      website_id: this.userProductData.website_id,
      warehouse_id: this.userProductData.warehouse_id,
      order_id: this.userProductData.order_id,
      user_id: this.userProductData.user_id,
      shipment_id: this.userProductData.shipment_id,
      trent_picklist_id: this.userProductData.trent_picklist_id,
      action: "increase",
      product_qtys: this.productQuantity,
      product_id: this.incomingmodalData.product_id,
      sub_product_ids: this.productsIDS,
      sub_product_qtys: this.productQuantity,
    }

    if (this.productsIDS.length !== 0) {
      if (this.productsIDS.length <= 2) {
        this.apiService.postData(subUrl, data).subscribe((data: any[]) => {
          let tempdata: any = data
          // this.globalitem.showSuccess("Product has been added sucessfully in order List !","Product Addedd")
          if (tempdata.status === 1 && tempdata.api_status === 'success') {
            let modaldataTemp = {
              data: data,
              subtitutestatus: "productadded"
            }
            this.dialogRef.close({ event: 'close', data: modaldataTemp, substituteData: this.incomingmodalData.substituteData });
          } else {
            this.globalitem.showError(tempdata.message, "")
          }
        })
      } else {
        this.globalitem.showError("You can't select more than 2 products ", "")
      }
    } else {
      this.globalitem.showError("No Product Found, You need to add product first !", "No Product")
    }
  }

  filterArray(array: any = []): any {
    return array.filter(function (elem: any, index: any, self: string | any[]) {
      return index === self.indexOf(elem);
    })
  }

  //this method is for adding more than 0 products  
  addMoreProduct(searchURL: any) {
    this.productQuantity = []
    for (var i = 0; i < this.pickerProductList["data"].response.length; i++) {
      if (this.pickerProductList["data"].response[i].id === this.productsIDS[i]) {
        this.productQuantity.push(this.pickerProductList["data"].response[i].quantity)//push quantity to arrays according to selected id's
      }
      if (this.pickerProductList["data"].response[i].quantity > 0) {

      }
    }
    let data = {
      website_id: this.userProductData.website_id,
      warehouse_id: this.userProductData.warehouse_id,
      order_id: this.userProductData.order_id,
      user_id: this.userProductData.user_id,
      shipment_id: this.userProductData.shipment_id,
      trent_picklist_id: this.userProductData.trent_picklist_id,
      action: "increase",
      product_qtys: this.productQuantity,
      product_ids: this.productsIDS
    }
    // console.log("data objects ", data);
    if (this.productsIDS.length > 0) {
      this.apiService.postData(searchURL, data).subscribe((data: any[]) => {
        let tempdata: any = data
        this.globalitem.showSuccess("Product has been added sucessfully in order List !", "Product Addedd")
        if (tempdata.status === 1 && tempdata.api_status === 'success') {
          this.dialogRef.close();
        } else {
          this.globalitem.showSuccess(tempdata.message, "")
        }
      })
    } else {
      this.globalitem.showError("You need to select product first ", "No product found")
    }
  }

  openproductModalAsSubtituteProduct() {

  }

  //substitute products
  selectSubstituteproduct(index:any, substitutestatus: any, relatedproductid: any, relatedproducttype: any,item:any)
{

  // console.log("substitute product selected list : ",item);
  
  if (substitutestatus === 1) {
    for (var i = 0; i < this.pickerProductList["data"].response.length; i++) {
      if (i === index) {
        if(this.pickerProductList["data"].response[i].quantity === null || this.pickerProductList["data"].response[i].quantity === 0){
          this.pickerProductList["data"].response[i].quantity = 1;
          this.productsIDS.push(this.pickerProductList["data"].response[i].id)
          if( this.subtituteSelectedProducts.length === 0){
            this.subtituteSelectedProducts.push(item)
          }
          console.log("Index ",i);
          
          if(this.pickerProductList["data"].response[i].id !== this.subtituteSelectedProducts[i].id){
            this.subtituteSelectedProducts.push(item)
          }else{
            //nothing
          }
        }else if(this.pickerProductList["data"].response[i].quantity === 1)
        {
          this.pickerProductList["data"].response[i].quantity = 0
          this.productsIDS.splice(this.productsIDS.indexOf(this.pickerProductList["data"].response[i].id), 1)
          if(this.pickerProductList["data"].response[i].id === this.subtituteSelectedProducts[i].id){
            this.subtituteSelectedProducts.splice(this.subtituteSelectedProducts.indexOf(this.pickerProductList["data"].response[i].id), 1)
          }
          
        }
         //assaign quantity to input
        if (this.pickerProductList["data"].response[i].quantity > 0) {
          this.productsIDS.push(this.pickerProductList["data"].response[i].id) //push products ids
        }
      }
    }

    console.log(" this.subtituteSelectedProducts list : ", this.subtituteSelectedProducts);
    
}else {
  this.openSub_modal('picker-add-product-as-substitute/', this.incomingmodalData.product_id, relatedproductid, relatedproducttype, AddproductasSubtituteComponent)
}
}
}
