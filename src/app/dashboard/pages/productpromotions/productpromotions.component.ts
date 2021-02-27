import { DatabaseService } from './../../../services/database/database.service';
import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { AddproductcategoryComponent } from 'src/app/components/addproductcategory/addproductcategory.component';
import { ApiService } from 'src/app/services/api/api.service';
import { GlobalitemService } from 'src/app/services/globalitem/globalitem.service';
import { ProductpromotionmodelComponent } from 'src/app/components/productpromotionmodel/productpromotionmodel.component';

@Component({
  selector: 'app-productpromotions',
  templateUrl: './productpromotions.component.html',
  styleUrls: ['./productpromotions.component.scss']
})
export class ProductpromotionsComponent implements OnInit {

  parentcategory: any = []
  subcategory: any = []
  masterconditionsinputSelectins: any = 'category'
  public selectedMoment = new Date();
  promotionsAttribute = {
    warehouse_id: '',
    website_id: '',
    pricelistCategoryIDS: '',
    productSku: '',
    orderAmount: 0,
    applybyprice: '',
    percentageAmount: 0,
    priority: '',
    storeName: '',
    offerType: 'Normal Offers',
    discountName:''
  }

  discountStartDate: any = new Date()
  discountEndDate: any = new Date()

  constructor(public dialog: MatDialog, public apiService: ApiService,
    public globalitem: GlobalitemService,public db : DatabaseService) { 
      this.getuserData();
    }

  ngOnInit(): void {
  }
  // getting store info
  getuserData(){
    this.db.getUserData().then(res => {
      // console.log("user data inside dashboard : ", res);

      this.promotionsAttribute.warehouse_id=res.warehouse_id
      this.promotionsAttribute.website_id=res.website_id

      let data = {
        warehouse_id: res.warehouse_id,
        website_id: res.website_id,
      }
  }
    );
}
  setDiscountbased(event: any) {
    console.log("event value : ",event);
    
    this.masterconditionsinputSelectins = event.target.value
  }

  opencategory_modal(catname: any): void {
    let data = {
      URl: "picker-stockcategory/",
      parent_id: null,
      catname: catname,
      warehouse_id: this.promotionsAttribute.warehouse_id,
      website_id: this.promotionsAttribute.website_id
    }
    const dialogRef = this.dialog.open(AddproductcategoryComponent, {
      width: '500px',
      data: { data: data }
    });

    dialogRef.afterClosed().subscribe(result => {
      // console.log('The dialog was closed', result);
      this.parentcategory = result.data;
      this.promotionsAttribute.pricelistCategoryIDS = this.parentcategory.id
      this.subcategory.name = "Sub Category"
      this.subcategory.id = ''
      if (result.data === "undefined") {
        this.parentcategory.id = ''
      }
    });
  }
  opensub_category_modal(catname: any): void {
    let data = {
      website_id: this.promotionsAttribute.website_id,
      warehouse_id: this.promotionsAttribute.warehouse_id,
      parent_id: this.parentcategory.id,
      catname: catname,
      URl: "picker-stockcategory/",
    }
    const dialogRef = this.dialog.open(AddproductcategoryComponent, {
      width: '500px',
      data: { data: data }
    });

    dialogRef.afterClosed().subscribe(result => {
      this.subcategory = result.data;
      this.promotionsAttribute.pricelistCategoryIDS = this.subcategory.id
    });
  }
  // sku product list
  openproductSKU(catname: any): void {
    let data = {
      // URl: "picker-stockcategory/",
      // parent_id: null,
      // catname: catname,
      // warehouse_id: this.promotionsAttribute.warehouse_id,
      website_id: this.promotionsAttribute.website_id
    }
    const dialogRef = this.dialog.open(ProductpromotionmodelComponent, {
      width: '800px',
      height:'650px',
      data: { data: data }
    });

    dialogRef.afterClosed().subscribe(result => {
      console.log('The dialog was closed', result);
      if(result.data){
        this.promotionsAttribute.productSku=result.data
        console.log("json converter ",JSON.stringify(result.data));
        
      }
    });
  }
  promoteNow(){
    // console.log("start Date : ",this.discountStart);
    // console.log("start Date : ",this.discountEndDate);
    let data={
      value: {
DiscountMastersConditions: [
  {
  all_category_id: null,
  all_customer_id: null,
  all_product_id: "57537",
  all_product_qty: null,
  condition: "==",
  condition_type: "AND",
  discount_master_id: 379,
  fields: 13633,
  // ip_address: "192.168.0.125",
  updatedby: 1,
  value: "GOG100090041"
},{
  all_category_id: "733",
  all_customer_id: null,
  all_product_id: null,
  all_product_qty: null,
  condition: "!=",
  condition_type: "AND",
  discount_master_id: 379,
  fields: 0,
  // ip_address: "192.168.0.125",
  updatedby: 1,
  value: "Tea"
},{
  condition: "<=",
  condition_type: "AND",
  discount_master_id: 379,
  fields: -1,
  // ip_address: "192.168.0.125",
  updatedby: 1,
  value: "2"},
  {
  condition: ">=",
  condition_type: "AND",
  discount_master_id: 379,
  fields: -1,
  // ip_address: "192.168.0.125",
  updatedby: 1,
  value: "4"}
],
DiscountMastersCoupons: [],
amount:this.promotionsAttribute.percentageAmount,
condition_for_freebie_items: null,
coupon_code: null,
coupon_prefix: null,
coupon_suffix: null,
coupon_type: 1,
created: new Date(),
createdby: 1,
customer_group: null,
description: null,
disc_end_date: this.discountEndDate,
disc_start_date:  this.discountStartDate,
disc_type: "2",
discountId: 379,
discount_master_type: 0,
discount_priority: parseInt(this.promotionsAttribute.priority),
discount_type: "p",
free_items: null,
freebies_product_ids: null,
freebies_product_sku: null,
generate_couponcode: "single",
has_multiplecoupons: "n",
id: 379,
ip_address: "",
isblocked: "n",
isdeleted: "n",
modified: new Date(),
name: this.promotionsAttribute.discountName,
no_of_quantity_per: null,
offer_type: this.promotionsAttribute.offerType,
product_id: null,
product_id_qty: "",
product_name: null,
up_to_discount: null,
updatedby: 1,
used_coupon: 0,
warehouse: [this.promotionsAttribute.warehouse_id],
warehouse_id: this.promotionsAttribute.warehouse_id,
website_id: this.promotionsAttribute.website_id,
}
  }
  console.log("api data : ",data);
  this.apiService.updateData("discount/379/", data).subscribe((data: any) => {
    console.log("data response : ",data);
  })
  }
}
