import { Component, OnInit } from '@angular/core';
import { Data } from '@angular/router';
import { ApiService } from 'src/app/services/api/api.service';
import { DatabaseService } from 'src/app/services/database/database.service';
import { GlobalitemService } from 'src/app/services/globalitem/globalitem.service';

@Component({
  selector: 'app-returns',
  templateUrl: './returns.component.html',
  styleUrls: ['./returns.component.scss']
})
export class ReturnsComponent implements OnInit {

  userOrderdata = {
    warehouse_id: '',
    website_id: '',
    user_id: ''
  }
  ordernumber: any
  billnumber: any
  date: any=null
  productName:any;
  returnproductData: any = []
  constructor(public apiservice: ApiService, public db: DatabaseService,public globalitem:GlobalitemService) {
    this.searchreturnproduct()
  }

  ngOnInit(): void {
    this.returnproductData["data"] = []
  }

  searchreturnproduct() {
    this.db.getUserData().then(res => {
      this.userOrderdata.warehouse_id = res.warehouse_id
      this.userOrderdata.website_id = res.website_id
      this.userOrderdata.user_id = res.user_id

      let data = {
        website_id: res.website_id,
        order_date: this.date,
        order_no: '50003759',
        invoice_no: this.billnumber,
        search: this.productName,
        warehouse_id: res.warehouse_id
      }
      this.apiservice.postData("picker-searchreturn/", data).subscribe((data: any) => {
        if (data.status === 1) {
          this.returnproductData["data"] = data.response[0]
        }else{
          this.globalitem.showError(data.message,"")
        }

      })
    });
  }

  cleardatefield(){
    this.date=null
  }
  increment(index: any) {
    for (var i = 0; i < this.returnproductData["data"]?.order_products.length; i++) {
      if (i === index) {
        console.log("entered : ", this.returnproductData["data"]);
        if (this.returnproductData["data"]?.order_products[i].returns < this.returnproductData["data"]?.order_products[i].quantity) {

          let templength = this.returnproductData["data"]?.order_products[i].returns + 1 //increment the quantity
          this.returnproductData["data"].order_products[i].returns = templength; //assaign quantity to input
          // this.updateMoreProductQuantity(this.orderDetaildata["data"][0].order_products[index].grn_quantity, order_product_id, product_id, shortage, index)
        }
      }
    }
  }
  decrement(index: any) {
    for (var i = 0; i < this.returnproductData['data']?.order_products.length; i++) {
      if (i == index) {
        let templength = this.returnproductData['data']?.order_products[i].returns - 1
        if (templength < 0) {
          this.returnproductData["data"].order_products[i].returns = 0;
        } else {
          this.returnproductData["data"].order_products[i].returns = templength;
        }
      }

    }
  }

  confirmReturn(){
    let returnDetail:any=[]
    
    for (var i = 0; i < this.returnproductData['data']?.order_products.length; i++) {
      if(this.returnproductData['data']?.order_products[i]?.returns > 0){
        let data={
          product_id: this.returnproductData['data']?.order_products[i]?.product.id,
              order_product_id: this.returnproductData['data']?.order_products[i]?.id,
              return_qty: this.returnproductData['data']?.order_products[i]?.returns
        }
        returnDetail.push(data)
      }
    }

    let data={
      user_id: this.userOrderdata.user_id,
      trent_picklist_id:  this.returnproductData["data"].trent_picklist_id,
      shipment_id: this.returnproductData["data"].shipment_id,
      website_id: this.userOrderdata.website_id,
      order_id: this.returnproductData["data"].id,
      product_tax_price:0,
      return_details:returnDetail
  }
  this.apiservice.postData("picker-confirmreturn/", data).subscribe((data: any) => {
    console.log("response data : ",data);
    
    if (data.status === 1) {
      this.globalitem.showSuccess(data.message,"")
    }else{
      this.globalitem.showError(data.message,"")
    }

  })
  }
}
