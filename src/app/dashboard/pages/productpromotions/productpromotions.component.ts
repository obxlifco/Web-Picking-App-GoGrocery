import { CommonfunctionService } from './../../../core/utilities/commonfunction.service';
import { DatabaseService } from './../../../services/database/database.service';
import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { AddproductcategoryComponent } from 'src/app/components/addproductcategory/addproductcategory.component';
import { ApiService } from 'src/app/services/api/api.service';
import { GlobalitemService } from 'src/app/services/globalitem/globalitem.service';
import { ProductpromotionmodelComponent } from 'src/app/components/productpromotionmodel/productpromotionmodel.component';
import { FormArray, FormBuilder, FormGroup } from '@angular/forms';

@Component({
  selector: 'app-productpromotions',
  templateUrl: './productpromotions.component.html',
  styleUrls: ['./productpromotions.component.scss']
})
export class ProductpromotionsComponent implements OnInit {

  parentcategory: any = []
  subcategory: any = []
  productForm: any = FormGroup;
  masterconditionsinputSelectins: any = 'category'
  public selectedMoment = new Date();
  promotionsAttribute = {
    warehouse_id: '',
    website_id: '',
    user_id: 0,
    pricelistCategoryIDS: '',
    productSku: '',
    orderAmount: 0,
    applybyprice: '',
    // percentageAmount: 0,
    priority: '',
    storeName: '',
    offerType: 'Normal Offers',
    discountName: '',
    oldprice: 0,
    newprice: '',
    discountID: 0,
    productID: 0
  }
  userdata: any = []
  promocodelist: any = []
  discountStartDate: any = new Date()
  discountEndDate: any = new Date()
  promoconditions: any = '=='
  addnewpromotions = false
  dynamicAttributArray: any = []
  constructor(public dialog: MatDialog, public apiService: ApiService, private fb: FormBuilder,
    public globalitem: GlobalitemService, public db: DatabaseService, public commonfunct: CommonfunctionService) {
    this.productForm = this.fb.group({
      name: '',
      quantities: this.fb.array([]),
    });

    this.promocodelist["data"] = []
    this.getuserData();
  }

  ngOnInit(): void {

  }
  // getting store info
  getuserData() {
    this.db.getUserData().then(res => {
      // console.log("user data inside dashboard : ", res);

      this.promotionsAttribute.warehouse_id = res.warehouse_id
      this.promotionsAttribute.website_id = res.website_id
      this.promotionsAttribute.user_id = res.user_id
      this.userdata = res
      let data = {
        warehouse_id: res.warehouse_id,
        website_id: res.website_id,
      }
      this.getDiscountlist()
    }
    );
  }
  setDiscountbased(event: any) {
    console.log("event value : ", event);
    this.masterconditionsinputSelectins = event.target.value
    if (this.masterconditionsinputSelectins === "sku") {
      this.promotionsAttribute.productSku = ''
    }
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
    if (this.masterconditionsinputSelectins === "sku") {
      this.promotionsAttribute.pricelistCategoryIDS = ''
    }
    let data = {
      data: this.userdata,
      categoryID: this.promotionsAttribute.pricelistCategoryIDS
    }
    const dialogRef = this.dialog.open(ProductpromotionmodelComponent, {
      width: '800px',
      height: '650px',
      data: { data: data }
    });

    dialogRef.afterClosed().subscribe(result => {
      console.log('The dialog was closed', result);
      if (result.data) {
        this.promotionsAttribute.productSku = result.data.sku
        this.promotionsAttribute.oldprice = result.data.channel_currency_product_price.price
        // console.log("json converter ", JSON.stringify(result.data))
      }
    });
  }
  updatePromotioncode() {
    // console.log("start Date : ",this.discountStart);
    // console.log("start Date : ",this.discountEndDate);
    let data = {
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
          }, {
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
          }, {
            condition: "<=",
            condition_type: "AND",
            discount_master_id: 379,
            fields: -1,
            // ip_address: "192.168.0.125",
            updatedby: 1,
            value: "2"
          },
          {
            condition: ">=",
            condition_type: "AND",
            discount_master_id: 379,
            fields: -1,
            // ip_address: "192.168.0.125",
            updatedby: 1,
            value: "4"
          }
        ],
        DiscountMastersCoupons: [],
        // amount: this.promotionsAttribute.percentageAmount,
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
        disc_start_date: this.discountStartDate,
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
    console.log("api data : ", data);
    this.apiService.updateData("discount/" + this.promotionsAttribute.discountID + "/", data).subscribe((data: any) => {
      console.log("data response : ", data);
    })
  }

  addNewPromocode() {
    // console.log("start Date : ",this.discountStart);

    console.log("new price : ", this.promotionsAttribute.newprice);
    if (this.promotionsAttribute.newprice) {
      if (parseInt(this.promotionsAttribute.newprice) < this.promotionsAttribute.oldprice) {
        let amount: any;
        let diff = this.promotionsAttribute.oldprice - parseInt(this.promotionsAttribute.newprice)
        let percent = (diff / this.promotionsAttribute.oldprice) * 100
        console.log("percentage value ", (percent | percent), " diff : ", diff);
        amount = this.commonfunct.precise_round(percent, 2)
        let promotionarray: any = []
        if (this.masterconditionsinputSelectins === "sku") {
          promotionarray = this.setpromotionArrayAttribute('', this.promotionsAttribute.productID, this.promotionsAttribute.productSku, 0, 13633, this.promotionsAttribute.productID)
          // this.setpromotionArrayAttribute(catIDs,productid,productvalue,discountmasterid,fieldvalue,productID)
        } else if (this.masterconditionsinputSelectins === "category") {
          promotionarray = this.setpromotionArrayAttribute(this.promotionsAttribute.pricelistCategoryIDS, this.promotionsAttribute.productID, this.promotionsAttribute.productSku, 0, 0, this.promotionsAttribute.productID)
        } else if (this.masterconditionsinputSelectins === "amount") {
          promotionarray = this.setpromotionArrayAttribute('', '', this.promotionsAttribute.orderAmount, 0, -1, '')
        }
        //check date comparison
        if (this.discountStartDate <= this.discountEndDate) {
          // console.log("start date greater");
          if (this.promotionsAttribute.discountName) {
            let data = {
              value: {
                DiscountMastersConditions: promotionarray,
                DiscountMastersCoupons: [],
                amount: amount,
                coupon_type: 1,
                createdby: 1,
                disc_end_date: this.discountEndDate,
                disc_start_date: this.discountStartDate,
                disc_type: "1",
                discountId: 0,
                discount_master_type: 0,
                discount_priority: "1",
                generate_couponcode: "single",
                has_multiplecoupons: "n",
                ip_address: "",
                isblocked: "n",
                name: this.promotionsAttribute.discountName,
                offer_type: "Normal Offers",
                updatedby: 1,
                used_coupon: 0,
                warehouse: [this.promotionsAttribute.warehouse_id],
                warehouse_id: this.promotionsAttribute.warehouse_id,
                website_id: this.promotionsAttribute.website_id,
              }
            }
            // console.log("api data : ", data);
            this.apiService.postData("discount/", data).subscribe((data: any) => {
              // console.log("data response : ", data);
              this.promotionsAttribute.discountID = data?.api_status?.id
              this.addnewpromotions = !this.addnewpromotions
              this.clearField()
            })
          } else {
            this.globalitem.showError("Please Enter Promotion name", "")
          }
        } if (this.discountStartDate > this.discountEndDate) {
          this.globalitem.showError("Please choose correct date", "")
        }
      } else {
        this.globalitem.showError("New Price should be less than old Price", "")
      }
    } else {
      this.globalitem.showError("Please Enter Fields value", "")
    }
  }
  //get discount list
  getDiscountlist() {
    // let data = {
    //   advanced_search: [],
    //   model: "EngageboostDiscountMasters",
    //   order_by: "",
    //   order_type: "",
    //   screen_name: "list2",
    //   search: "",
    //   status: "",
    //   userid: this.promotionsAttribute.user_id,
    //   warehouse_id: this.promotionsAttribute.warehouse_id,
    //   website_id: this.promotionsAttribute.website_id,
    //   // model: "EngageboostOrdermaster",
    //   // warehouse_status: "",
    // }
    let data = {
      advanced_search: [],
      model: "EngageboostDiscountMasters",
      order_by: "",
      order_type: "",
      screen_name: "list2",
      search: "",
      status: "",
      userid: 1,
      warehouse_id: this.promotionsAttribute.warehouse_id,
      website_id: 1,
    }
    this.apiService.postData("global_list/", data).subscribe((data: any) => {
      // console.log("discount list : ", data);
      this.promocodelist["data"] = data.results[0].result
    })
  }

  //dynamic form
  quantities(): FormArray {
    return this.productForm.get("quantities") as FormArray
  }

  newQuantity(): FormGroup {
    return this.fb.group({
      discountbased: '',
      conditions: '',
      values: ''
    })
  }
  addQuantity() {
    this.quantities().push(this.newQuantity());
  }
  removeQuantity(i: number) {
    this.quantities().removeAt(i);
  }
  onSubmit() {
    console.log(this.productForm.value);
  }
  addnewUI() {
    this.addnewpromotions = !this.addnewpromotions
  }
  setupdateStatus(listdata: any) {
  }

  // set object attribute
  setpromotionArrayAttribute(catIDs: any, productid: any, productvalue: any, discountmasterid: any, fieldvalue: any, productID: any) {
    //field value
    //-1 for amount
    //0 for category
    //13633 for sku 
    this.dynamicAttributArray = [{
      all_category_id: this.promotionsAttribute.pricelistCategoryIDS,
      all_customer_id: null,
      all_product_id: productID,
      all_product_qty: null,
      condition: "==",
      condition_type: "AND",
      discount_master_id: discountmasterid,
      fields: fieldvalue,
      // ip_address: "192.168.0.125",
      updatedby: 1,
      value: productvalue
    }]
    return this.dynamicAttributArray
  }

  // clear filed
  clearField() {
    this.promotionsAttribute.newprice = ''
    this.promotionsAttribute.oldprice = 0
    this.promotionsAttribute.pricelistCategoryIDS = ''
    this.promotionsAttribute.productSku = ''
    this.promotionsAttribute.orderAmount = 0
    this.promotionsAttribute.storeName = ''
    this.promotionsAttribute.discountName = ''
    this.promotionsAttribute.newprice = ''
  }
}