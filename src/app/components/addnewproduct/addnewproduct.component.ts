import { Component, Inject, OnInit } from '@angular/core';
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { Router } from '@angular/router';
import { ApiService } from 'src/app/services/api/api.service';
import { DatabaseService } from 'src/app/services/database/database.service';
import { GlobalitemService } from 'src/app/services/globalitem/globalitem.service';
import { AddproductasSubtituteComponent } from '../addproductas-subtitute/addproductas-subtitute.component';
import { AddproductcategoryComponent } from '../addproductcategory/addproductcategory.component';
import { ImagemagnifyComponent } from '../imagemagnify/imagemagnify.component';

export interface DialogData {

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
  ISkeleton = false
  // for pagination on scroll
  productpage: any = 1
  totalProductpage: any;
  // modal object
  AddproductcategoryComponent: any = AddproductcategoryComponent
  item_quantity: any = 0
  incomingmodalData: any = []
  pickerProductList: any = []//list of product data
  productsIDS: any = []
  productQuantity: any = []
  subtituteSelectedProducts: any = []
  //for realtime selection we need to store selected product data 
  selectedproductids = {
    index: '',
    substitutestatus: '',
    relatedproductid: '',
    relatedproducttype: '',
    item: []

  }
  AddmoreProducts: any = []

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
    this.userProductData.shipment_id = this.incomingmodalData.shipment_id
    this.userProductData.trent_picklist_id = this.incomingmodalData.trent_picklist_id
    this.userProductData.ean = this.incomingmodalData.ean
    this.getProductlistData()
  }

  ngOnInit(): void {


  }

  opencategory_modal(categoryURl: any, catname: any): void {
    let data = {
      website_id: this.userProductData.website_id,
      warehouse_id: this.userProductData.warehouse_id,
      parent_id: null,
      URl: categoryURl,
      catname: catname
    }
    const dialogRef = this.dialog.open(AddproductcategoryComponent, {
      width: '500px',
      data: { data: data }
    });

    dialogRef.afterClosed().subscribe(result => {
      // console.log('The dialog was closed', result);
      this.parentcategory = result.data;
      this.subcategory.name = "Sub Category"
      this.subcategory.id = ''
      if (result.data === "undefined") {
        // this.subcategory.name="Sub Category"
        // this.subcategory.id=''
        this.parentcategory.id = ''
      }
    });
  }

  openSub_modal(ApiURl: any, product_id: any, related_product_id: any, related_product_type: any, modaltype: any, catname: any): void {
    let data = {
      website_id: this.userProductData.website_id,
      warehouse_id: this.userProductData.warehouse_id,
      parent_id: this.parentcategory.id,
      URl: ApiURl,
      product_id: product_id,
      related_product_id: related_product_id,
      related_product_type: related_product_type,
      catname: catname,
      pagestatus: 'addnewsubs',
      info: 'This is not subtitute product.Do you want to add this item as substitute product?'
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
        // this.getProductlistData()
        this.selectSubstituteproduct(this.selectedproductids.index, 1, this.selectedproductids.relatedproductid, this.selectedproductids.relatedproducttype, this.selectedproductids.item)
      } else {
        // console.log("modal closed");

      }

    });
  }

  closeModal(): void {
    // this.incomingmodalData.shortage=0
    this.dialogRef.close({ event: 'close', substituteData: this.incomingmodalData.substituteData, data: this.incomingmodalData.substituteData.shortage, subtitutestatus: "no_productadded" });
  }

  getProductlistData() {
    this.ISkeleton = true
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
        // ean: this.userProductData.ean,
        // category_id: 188
      }
      if (this.incomingmodalData.productType === 1) { //product type 1 for add more product and 2 for substitute
        let category_ids = {
          category_id: ''
        }
        this.userProductData.searchproductlist = 'picker-productlist/'
        Object.assign(data, category_ids);
      } else {
        let product_ids = {
          product_id: this.incomingmodalData.substituteData.product_id
        }
        Object.assign(data, product_ids);
        this.userProductData.searchproductlist = 'picker-substituteproductlist/'
      }
      // console.log("product id checking : ", data);
      this.userProductData.warehouse_id = res.warehouse_id
      this.userProductData.website_id = res.website_id
      this.userProductData.user_id = res.user_id
      this.apiService.postData(this.incomingmodalData.apiURL, data).subscribe((data: any) => {
        // console.log(data);

        this.addCustomAttribute(data.response)

      })
    })
  }
  addCustomAttribute(data: any) {
    let isselect = {
      Is_Select: 0,
      quantity: 1
    }
    this.ISkeleton = false
    if (this.userProductData.searchproductlist === 'picker-productlist/') {
      this.pickerProductList["data"] = data
      for (var i = 0; i < data.length; i++) {
        Object.assign(this.pickerProductList["data"][i], isselect)
      }

      // console.log("add prodcut list", data);
    } else {
      // console.log("substitute list");

      this.pickerProductList["data"] = data
    }
  }

  searchProducts(value: any) {
    this.ISkeleton = true
    if (value === "search") {
      this.totalProductpage = 0;
      this.productpage = 1
      this.pickerProductList["data"] = []
    }

    let temcategory: any = undefined;
    if (this.parentcategory.id !== undefined && this.parentcategory.id) {
      // console.log("else true ", this.parentcategory.id);
      temcategory = this.parentcategory.id
    }
    if (this.subcategory.id !== undefined && this.subcategory.id) {
      temcategory = this.subcategory.id
    }
    let data = {
      website_id: this.userProductData.website_id,
      warehouse_id: this.userProductData.warehouse_id,
      page: this.productpage,
      // per_page: 15,
      search: this.userProductData.searchproductvalue,
      ean: "",
      user_id: this.userProductData.user_id,
      order_id: this.userProductData.order_id,
      category_id: temcategory,
    }

    if (this.incomingmodalData.productType === 2) { //product type 1 for add more product and 2 for substitute
      let product_ids = {
        product_id: this.incomingmodalData.product_id
      }
      Object.assign(data, product_ids);
    } else if (this.incomingmodalData.productType === 1) {
      let category_ids = {
        category_id: temcategory,
      }
      Object.assign(data, category_ids);
    }
    this.apiService.postData(this.userProductData.searchproductlist, data).subscribe((data: any) => {
      this.ISkeleton = false
      this.addCustomAttribute(data.response)
      if (data.status === 0) {
        this.pickerProductList["data"] = []
        // console.log("data length ", this.pickerProductList["data"].length);
        //  this.globalitem.showError(data.message,"No Substitute")
      } else if (this.productpage === 1) {
        // this.pickerProductList["data"]=data.response
        this.pickerProductList["data"] = data.response
        this.totalProductpage = data.total_page
        console.log("page 1");
      } else {
        console.log("page n");
        this.pickerProductList["data"] = [... this.pickerProductList["data"], ...data.response];
      }
    })
  }

  //this is for remove product from list
  productDecerment(index: any, substitutestatus: any, relatedproductid: any, relatedproducttype: any) {
    // console.log("index --: ",index);
    for (var i = 0; i < this.pickerProductList["data"].length; i++) {
      if (i == index) {
        let templength = this.pickerProductList["data"][i].quantity - 1
        // console.log(templength);

        if (templength === 0) {
          // arr.splice(arr.indexOf('Orange'), 1);
          this.productsIDS.splice(this.productsIDS.indexOf(this.pickerProductList["data"][i].id), 1)
          this.productsIDS.splice(this.productsIDS.indexOf(this.pickerProductList["data"][i].quantity), 1)
          this.pickerProductList["data"][i].quantity = templength
        } else if (templength < 0) {
          this.pickerProductList["data"][i].quantity = 0;
        } else {
          this.pickerProductList["data"][i].quantity = templength
        }

      }
    }
  }
  // magnify image
  imagemagnifyModal(imageurl:any,imagename:any){
    imageurl=imageurl.slice(0, -8)
    // console.log("image url is :",imageurl);
    imageurl = imageurl +'400x400/'+imagename
    let data={
      data:imageurl
    }
    const dialogRef = this.dialog.open(ImagemagnifyComponent, {
      width: '500px',
      data: { data: imageurl }
    });
  }
  //Add product into list
  productIncrment(index: any, substitutestatus: any, relatedproductid: any, relatedproducttype: any) {
    // console.log("index ++: ", index, " substitutestatus : ", substitutestatus);
    if (substitutestatus !== 0) {
      for (var i = 0; i < this.pickerProductList["data"].length; i++) {
        if (i === index) {
          let templength = this.pickerProductList["data"][i].quantity + 1 //increment the quantity
          this.pickerProductList["data"][i].quantity = templength; //assaign quantity to input
          if (this.pickerProductList["data"][i].quantity > 0) {
            this.productsIDS.push(this.pickerProductList["data"][i].id) //push products ids
          }
        }
      }
      // this.productQuantity.push(this.pickerProductList["data"].response[index].quantity) //push quantity to arrays according to selected id's
      this.productsIDS = this.filterArray(this.productsIDS)
    } else {
      // this.openSub_modal('picker-add-product-as-substitute/', this.incomingmodalData.substituteData.product_id, relatedproductid, relatedproducttype, AddproductasSubtituteComponent,'Sub Category')
    }
  }

  addSubtituteProduct(subUrl: any) {
    this.productsIDS = []
    if (this.subtituteSelectedProducts.length) {

      for (var i = 0; i < this.subtituteSelectedProducts.length; i++) {
        // if (this.subtituteSelectedProducts[i].quantity > 0) {
        this.productQuantity.push(this.subtituteSelectedProducts[i].quantity)//push quantity to arrays according to selected id's
        this.productsIDS.push(this.subtituteSelectedProducts[i].id)
        // }
      }
      let data = {
        website_id: this.userProductData.website_id,
        warehouse_id: this.userProductData.warehouse_id,
        order_id: this.userProductData.order_id,
        user_id: this.userProductData.user_id,
        shipment_id: this.userProductData.shipment_id,
        trent_picklist_id: this.userProductData.trent_picklist_id,
        action: "increase",
        // product_qtys: this.productQuantity,
        product_id: this.incomingmodalData.substituteData.product_id,
        sub_product_ids: this.productsIDS,
        sub_product_qtys: this.productQuantity,
        // quantity:this.productQuantity
      }
      this.apiService.postData(subUrl, data).subscribe((data: any) => {

        if (data.status === 1 && data.api_status === 'success') {
          this.globalitem.showSuccess(data.message, "Product Addedd")
          let modaldataTemp = {
            data: data,
            subtitutestatus: "productadded"
          }
          this.dialogRef.close({ event: 'close', data: modaldataTemp, substituteData: this.incomingmodalData.substituteData });
        } else {
          this.globalitem.showError(data.message, "")
        }
      })
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
    this.productsIDS = []
    // console.log("add more products : ", this.AddmoreProducts);

    for (var i = 0; i < this.AddmoreProducts.length; i++) {
      if (this.pickerProductList["data"][i].id === this.productsIDS[i]) {
        // if(this.pickerProductList["data"][i].quantity === null){
        //   this.pickerProductList["data"][i].quantity = 1
        //   this.productQuantity.push(this.pickerProductList["data"][i].quantity )//push quantity to arrays according to selected id's
        // }else{
        //   this.productQuantity.push(this.pickerProductList["data"][i].quantity)//push quantity to arrays according to selected id's
        // }

      }
      this.productQuantity.push(this.AddmoreProducts[i].quantity)
      this.productsIDS.push(this.AddmoreProducts[i].id)
      this.productsIDS = this.filterArray(this.productsIDS)

      // if (this.pickerProductList["data"][i].quantity > 0) {

      // }
    }

    // console.log("productsIDS : ", this.productsIDS, ' Quantity : ', this.productQuantity, " Products : ", this.AddmoreProducts);
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
    if (this.AddmoreProducts.length > 0) {
      this.apiService.postData(searchURL, data).subscribe((data: any[]) => {
        let tempdata: any = data
        this.ISkeleton = false
        this.AddmoreProducts = []
        this.globalitem.showSuccess("Product has been added sucessfully in Picker order List !", "Product Addedd")
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
  selectMoreproduct(index: any, productid: any, item: any) {
    for (var i = 0; i < this.pickerProductList["data"].length; i++) {
      if (i === index) {
        if (this.pickerProductList["data"][i].Is_Select === 0) {
          this.pickerProductList["data"][i].Is_Select = 1;
          if (this.AddmoreProducts.length === 0) {
            this.AddmoreProducts.push(item)
          } else if (this.pickerProductList["data"][i].id !== this.AddmoreProducts[i]?.id) {
            this.AddmoreProducts.push(item)
          } else if (this.AddmoreProducts[i]?.id === undefined) {
            //nothing
            this.AddmoreProducts = []

          } else {
            // this.AddmoreProducts.push(item)
          }
        } else if (this.pickerProductList["data"][i].Is_Select === 1) {
          this.pickerProductList["data"][i].Is_Select = 0
          // this.productsIDS.splice(this.productsIDS.indexOf(this.pickerProductList["data"][index].id), 1)
          this.AddmoreProducts.splice(this.AddmoreProducts.indexOf(this.pickerProductList["data"][index]), 1)
          // this.AddmoreProducts.splice(this.AddmoreProducts.indexOf(index, 1))
        } else {

        }
      }
    }
  }

  //substitute products
  selectSubstituteproduct(index: any, substitutestatus: any, relatedproductid: any, relatedproducttype: any, item: any) {

    this.selectedproductids.index = index,
      this.selectedproductids.substitutestatus = substitutestatus,
      this.selectedproductids.relatedproductid = relatedproductid,
      this.selectedproductids.relatedproducttype = relatedproducttype,
      this.selectedproductids.item = item

    if (substitutestatus === 1) {
      for (var i = 0; i < this.pickerProductList["data"].length; i++) {
        if (i === index) {
          // if(this.subtituteSelectedProducts.length < 2){
          if (this.pickerProductList["data"][i].quantity === null || this.pickerProductList["data"][i].quantity === 0) {
            if (this.subtituteSelectedProducts.length < 2) {
              this.pickerProductList["data"][i].quantity = 1;
              this.productsIDS.push(this.pickerProductList["data"][i].id)
              this.productsIDS = this.filterArray(this.productsIDS)
              if (this.subtituteSelectedProducts.length === 0) {
                this.subtituteSelectedProducts.push(item)
              } else if (this.pickerProductList["data"][i].id !== this.subtituteSelectedProducts[i]?.id) {
                if (this.subtituteSelectedProducts.length < 2) {
                  this.subtituteSelectedProducts.push(item)
                } else {
                  this.globalitem.showError("You cannot select more than 2 items ", "Warning")
                }

              } else if (this.subtituteSelectedProducts[i]?.id === undefined) {
                //nothing
                this.subtituteSelectedProducts = []

              }
            } else {
              this.globalitem.showError("You cannot select more than 2 items ", "Warning")
            }

          } else if (this.pickerProductList["data"][i].quantity === 1) {
            this.pickerProductList["data"][i].quantity = 0
            this.productsIDS.splice(this.productsIDS.indexOf(this.pickerProductList["data"][index].id), 1)
            this.subtituteSelectedProducts.splice(this.subtituteSelectedProducts.indexOf(this.pickerProductList["data"][i].id), 1)
          } else {

          }
          //assaign quantity to input
          if (this.pickerProductList["data"][i].quantity > 0) {
            this.productsIDS.push(this.pickerProductList["data"][i].id) //push products ids
          }
        }
      }

      // console.log(" this.subtituteSelectedProducts list : ", this.subtituteSelectedProducts, this.pickerProductList["data"]);

    } else {
      this.openSub_modal('picker-add-product-as-substitute/', this.incomingmodalData.substituteData.product_id, relatedproductid, relatedproducttype, AddproductasSubtituteComponent, 'Sub Category')
    }
  }

  // scroll events
  onScrollDown(ev: any) {
    console.log('scrolled!!', ev);
    this.productpage++;
    if (this.productpage <= this.totalProductpage) {
      // console.log(" this.totalProductpage : ", this.totalProductpage);
      // console.log("  this.productpage : ", this.productpage);
      this.searchProducts("novalue")
    } else {
      // this.globalitem.showError("No more data is available ","No Data")
    }

  }
}
