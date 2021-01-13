import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { Data } from '@angular/router';
import { ApiService } from 'src/app/services/api/api.service';
import { DatabaseService } from 'src/app/services/database/database.service';
import { GlobalitemService } from 'src/app/services/globalitem/globalitem.service';
import { DatePipe } from '@angular/common';
@Component({
  selector: 'app-returns',
  templateUrl: './returns.component.html',
  styleUrls: ['./returns.component.scss']
})
export class ReturnsComponent implements OnInit {
  @ViewChild('ordernumberstatus', { static: false }) ordernumberstatus: ElementRef | any;
  userOrderdata = {
    warehouse_id: '',
    website_id: '',
    user_id: ''
  }
  ordernumber: any = ""
  billnumber: any = ""
  date: any = null
  productName: any = "";
  customcolor: any
  returnproductData: any = []
  isConfirmreturn = false
  isFullreturn = false
  constructor(public apiservice: ApiService, public db: DatabaseService, public globalitem: GlobalitemService,
    public datePipe: DatePipe,
  ) {
    // this.searchreturnproduct()
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
        order_date: this.datePipe.transform(this.date, "yyyy-MM-d"),
        order_no: this.ordernumber,
        invoice_no: this.billnumber,
        search: this.productName,
        warehouse_id: res.warehouse_id
      }
      if (this.ordernumber !== "") {
        this.apiservice.postData("picker-searchreturn/", data).subscribe((data: any) => {
          if (data.status === 1) {
            this.returnproductData["data"] = data.response[0]
            this.setcustomreturnvalue()
            this.buttondisablerfunc()
          } else {
            this.globalitem.showError("Order Not Found", "")
          }

        })
      } else {
        this.getbillValidator()
      }

    });
  }

  setcustomreturnvalue() {
    for (var i = 0; i < this.returnproductData["data"]?.order_products.length; i++) {
      let customreturn = {
        custom_return: this.returnproductData["data"]?.order_products[i].returns,
        commentStatus: 0
      }
      Object.assign(this.returnproductData["data"]?.order_products[i], customreturn)
    }

    for (var i = 0; i < this.returnproductData["data"]?.order_substitute_products.length; i++) {
      let customreturn = {
        custom_return: this.returnproductData["data"]?.order_substitute_products[i].returns,
        commentStatus: 0
      }
      Object.assign(this.returnproductData["data"]?.order_substitute_products[i], customreturn)
    }
  }

  cleardatefield() {
    this.date = null
  }
  increment(index: any, listStatus: any) {
    if (listStatus === "orderprodt") {
      for (var i = 0; i < this.returnproductData["data"]?.order_products.length; i++) {
        if (i === index) {
          if (this.returnproductData["data"]?.order_products[i].returns < this.returnproductData["data"]?.order_products[i].quantity) {
            let templength = this.returnproductData["data"]?.order_products[i].returns + 1 //increment the quantity
            this.returnproductData["data"].order_products[i].returns = templength; //assaign quantity to input
          }
        }
      }
      this.orderproductlist(index)
    } else {
      for (var i = 0; i < this.returnproductData["data"]?.order_substitute_products.length; i++) {
        if (i === index) {
          // console.log("entered : ", this.returnproductData["data"]);
          if (this.returnproductData["data"]?.order_substitute_products[i].returns < this.returnproductData["data"]?.order_substitute_products[i].quantity) {
            let templength = this.returnproductData["data"]?.order_substitute_products[i].returns + 1 //increment the quantity
            this.returnproductData["data"].order_substitute_products[i].returns = templength; //assaign quantity to input
          }
        }
      }
      this.Substituteproductlist(index)
    }
  }

  decrement(index: any, listStatus: any) {
    if (listStatus === "orderprodt") {
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
      this.orderproductlist(index)
    } else {
      for (var i = 0; i < this.returnproductData['data']?.order_substitute_products.length; i++) {
        if (i == index) {
          let templength = this.returnproductData['data']?.order_substitute_products[i].returns - 1
          if (templength < 0) {
            this.returnproductData["data"].order_substitute_products[i].returns = 0;
          } else {
            this.returnproductData["data"].order_substitute_products[i].returns = templength;
          }
        }
      }
      this.Substituteproductlist(index)
    }

  }

  orderproductlist(index: any) {
    // console.log("before ", this.returnproductData["data"]?.order_products[index].custom_return);
    if (this.returnproductData["data"]?.order_products[index].custom_return === 0) {
      if (this.returnproductData["data"].order_products[index].commentStatus === 0) {
        this.returnproductData["data"].order_products[index].commentStatus = 1
      } else {
        this.returnproductData["data"].order_products[index].commentStatus = 0
      }
    }
    this.buttondisablerfunc()
  }

  Substituteproductlist(index: any) {
    // console.log("before ", this.returnproductData["data"]?.order_substitute_products[index].custom_return);
    if (this.returnproductData["data"]?.order_substitute_products[index].custom_return === 0) {
      if (this.returnproductData["data"].order_substitute_products[index].commentStatus === 0) {
        this.returnproductData["data"].order_substitute_products[index].commentStatus = 1
      } else {
        this.returnproductData["data"].order_substitute_products[index].commentStatus = 0
      }
    }
    this.buttondisablerfunc()
  }

  buttondisablerfunc() {
    let prodlistcounter = 0;
    let substitutecounter = 0
    let fullreturncounter = 0
    for (var i = 0; i < this.returnproductData["data"]?.order_substitute_products.length; i++) {
      // console.log("status ", this.returnproductData["data"]?.order_substitute_products[i]?.commentStatus);
      if (this.returnproductData["data"]?.order_substitute_products[i]?.commentStatus === 1 || this.returnproductData["data"]?.order_products[i]?.commentStatus === 1) {
        prodlistcounter++;
      }
      if (this.returnproductData["data"]?.order_substitute_products[i]?.returns === 0) {
        fullreturncounter++
      }
    }
    for (var i = 0; i < this.returnproductData["data"]?.order_products.length; i++) {
      // console.log("status ", this.returnproductData["data"]?.order_products[i]?.commentStatus);
      if (this.returnproductData["data"]?.order_products[i]?.commentStatus === 1 || this.returnproductData["data"]?.order_substitute_products[i]?.commentStatus === 1) {
        substitutecounter++;
      }
      if (this.returnproductData["data"]?.order_products[i]?.returns === 0) {
        fullreturncounter++
      }
    }
    if (fullreturncounter > 0) {
      this.isFullreturn = false;
    } else {
      // console.log("counter : ",fullreturncounter);
      // this.isFullreturn = true;
    }

    if (substitutecounter + prodlistcounter > 0) {
      // console.log("true");
      this.isConfirmreturn = true;
    } else {
      this.isConfirmreturn = false;
      // console.log("false");
    }
  }
  
  confirmReturn(returnstatus: any) {
    let returnDetail: any = []
    if (returnstatus === "partial") {
      returnDetail = this.populatePartialOrder()
    } else if (returnstatus === "full") {
      returnDetail = this.populateFullOrder()
    }

    let data = {
      user_id: this.userOrderdata.user_id,
      trent_picklist_id: this.returnproductData["data"].trent_picklist_id,
      shipment_id: this.returnproductData["data"].shipment_id,
      website_id: this.userOrderdata.website_id,
      order_id: this.returnproductData["data"].id,
      product_tax_price: 0,
      return_details: returnDetail
    }
    // console.log("data is : ", data);
    this.apiservice.postData("picker-confirmreturn/", data).subscribe((data: any) => {
      // console.log("response data : ", data);

      if (data.status === 1) {
        this.globalitem.showSuccess(data.message, "")
      } else {
        this.globalitem.showError("Order Not Found", "")
      }
    })
  }

  populatePartialOrder() {
    let returnDetail: any = []
    for (var i = 0; i < this.returnproductData['data']?.order_products.length; i++) {
      if (this.returnproductData['data']?.order_products[i]?.returns > 0 && this.returnproductData["data"]?.order_products[i].custom_return === 0) {
        let data = {
          product_id: this.returnproductData['data']?.order_products[i]?.product.id,
          order_product_id: this.returnproductData['data']?.order_products[i]?.id,
          return_qty: this.returnproductData['data']?.order_products[i]?.returns
        }
        returnDetail.push(data)
      }
    }
    for (var i = 0; i < this.returnproductData['data']?.order_substitute_products.length; i++) {
      if (this.returnproductData['data']?.order_substitute_products[i]?.returns > 0 && this.returnproductData["data"]?.order_substitute_products[i].custom_return === 0) {
        let data = {
          product_id: this.returnproductData['data']?.order_substitute_products[i]?.product.id,
          order_product_id: this.returnproductData['data']?.order_substitute_products[i]?.id,
          return_qty: this.returnproductData['data']?.order_substitute_products[i]?.returns
        }
        returnDetail.push(data)
      }
    }

    return returnDetail
  }
  populateFullOrder() {
    let returnDetail: any = []
    for (var i = 0; i < this.returnproductData['data']?.order_products.length; i++) {
      let data = {
        product_id: this.returnproductData['data']?.order_products[i]?.product.id,
        order_product_id: this.returnproductData['data']?.order_products[i]?.id,
        return_qty: this.returnproductData['data']?.order_products[i]?.quantity
      }
      returnDetail.push(data)
    }
    for (var i = 0; i < this.returnproductData['data']?.order_substitute_products.length; i++) {
      let data = {
        product_id: this.returnproductData['data']?.order_substitute_products[i]?.product.id,
        order_product_id: this.returnproductData['data']?.order_substitute_products[i]?.id,
        return_qty: this.returnproductData['data']?.order_substitute_products[i]?.quantity
      }
      returnDetail.push(data)
    }

    return returnDetail
  }
  getbillValidator() {
    this.ordernumberstatus?.nativeElement.focus();
    this.customcolor = "#FF0000"
    this.globalitem.showError("First you need to enter order number", "Order Number Empty")
  }
}
