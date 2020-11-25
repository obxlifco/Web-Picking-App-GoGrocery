import { Component, NgModule, OnInit } from '@angular/core';
import { Router } from '@angular/router';
// import {MatDialog, MatDialogRef, MAT_DIALOG_DATA} from '@angular/material';
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { AddnewproductComponent } from 'src/app/components/addnewproduct/addnewproduct.component';
import { GlobalitemService } from 'src/app/services/globalitem/globalitem.service';
import { DatabaseService } from 'src/app/services/database/database.service';
import { ApiService } from 'src/app/services/api/api.service';
import { ModalService } from 'src/app/services/modal/modal.service';
import { EditproductweightComponent } from 'src/app/components/editproductweight/editproductweight.component';
import { MapmodalComponent } from 'src/app/components/mapmodal/mapmodal.component';
import { BillnumberComponent } from 'src/app/components/billnumber/billnumber.component';

@Component({
  selector: 'app-orders',
  templateUrl: './orders.component.html',
  styleUrls: ['./orders.component.scss'],
})
export class OrdersComponent implements OnInit {

  item_available: any = 0;
  item_not_available: any = 0;
  name: any = "Pepsi";
  category: any = "drink";
  orderlistdata: any = []
  orderDetaildata: any = []
  userOrderdata = {
    warehouse_id: '',
    website_id: '',
    user_id: '',
    picker_name: '',
    order_id: '',
    shipment_id: '',
    order_status: '',
    trent_picklist_id: 0,
    substitute_status:''
  }

  product_billnumber: any = 'Enter Bill Number';
  minValue: any = new Date();
  maxValue: any = this.minValue.getDate() + 3;
  datetime: any;
  customErrorStateMatcher: any
  constructor(public router: Router,
    public dialog: MatDialog,
    public db: DatabaseService,
    public apiService: ApiService,
    public modalservice: ModalService,
    public globalitem: GlobalitemService) {
    // this.dataService.sendGetRequest().subscribe((data: any[])=>{
    //   console.log(data);
    //   this.products = data;
    // })  
  }

  ngOnInit(): void {
    this.orderlistdata["data"] = []
    this.orderDetaildata["data"] = []
    this.getOrderlistData()
  }
  navigate(link: any) {
    this.router.navigate([link]);
  }



  processOrder() {

    // substitute_product_id:any,product_id:any
    let data = {
      website_id: this.userOrderdata.website_id,
      warehouse_id: this.userOrderdata.warehouse_id,
      order_id: this.userOrderdata.order_id,
      user_id: this.userOrderdata.user_id,
      shipment_id: this.userOrderdata.shipment_id,
      trent_picklist_id: this.userOrderdata.trent_picklist_id,
    }
    this.apiService.postData("picker-grn-complete/", data).subscribe((data: any[]) => {
      console.log("picker-grn-complete : ", data);
      let tempdata: any = data
      // this.pickerProductList["data"] = data
      if (tempdata.status === 1) {
        this.globalitem.showSuccess(tempdata.message, "Subtitute Sent")
      }

    })

  }

  getOrderlistData() {
    this.db.getUserData().then(res => {
      console.log("user data inside dashboard : ", res);

      let data = {
        warehouse_id: res.warehouse_id,
        website_id: res.website_id,
      }
      this.userOrderdata.warehouse_id = res.warehouse_id
      this.userOrderdata.website_id = res.website_id
      this.userOrderdata.user_id = res.user_id
      this.apiService.postData("picker-orderlist/", data).subscribe((data: any[]) => {
        console.log(data);
        this.orderlistdata["data"] = data
        this.getOrderDetailData(this.orderlistdata["data"].response[0].id, this.orderlistdata["data"].response[0].shipment_id, this.orderlistdata["data"].response[0].order_status,
          this.orderlistdata["data"].response[0].picker_name,this.orderlistdata["data"].response[0].substitute_status)
      })
    })

    

  }
  AssaignorderToUser(value: string) {
    this.userOrderdata.picker_name = value;
    let data = {
      website_id: this.userOrderdata.website_id,
      user_id: this.userOrderdata.user_id,
      picker_name: value,
      order_id: this.userOrderdata.order_id,
      shipment_id: this.userOrderdata.shipment_id,
      order_status: this.userOrderdata.order_status
    }

    this.apiService.postData("picker-generatepicklist/", data).subscribe((data: any) => {
      console.log(data);
      // this.orderlistdata["data"] = data
      this.globalitem.showSuccess(data.message, "Success")
    })
  }

  getOrderDetailData(orderid: any, shipment_id: string, order_status: string, picker_name: string,substitute_status:any) {
    console.log("order id :", orderid);
    this.userOrderdata.picker_name = picker_name;
    this.userOrderdata.order_id = orderid
    this.userOrderdata.order_status = order_status
    this.userOrderdata.shipment_id = shipment_id
    this.userOrderdata.substitute_status=substitute_status
    let data = {
      website_id: this.userOrderdata.website_id,
      order_id: orderid,
    }
    this.getLatestOrder()
    this.apiService.postData("picker-orderdetails/", data).subscribe((data: any[]) => {
      console.log(data);
      let temdata: any = []
      temdata = data
      this.orderDetaildata["data"] = temdata.response
      let time: any = this.orderDetaildata['data'][0]?.order_activity[0]?.activity_date;
      // this.datetime = time.getTime()
      console.log("Date Time : ", this.datetime);
      // this.addCustomVariable();
    })
  }

  openmap(latlang: any) {
    console.log("latlang : ", latlang);
    // MapmodalComponent
    this.modalservice.openModal(latlang, MapmodalComponent)
  }

  timeChangeHandler(event: any) {
    console.log("date Event : ", event)
  }
  invalidInputHandler() {
  }

  openEditModal(data: any) {
    let user_ids = {
      website_id: this.userOrderdata.website_id,
      user_id: this.userOrderdata.user_id,
      user_name: this.userOrderdata.picker_name
    }
    Object.assign(data, user_ids)
    this.modalservice.openModal(data, EditproductweightComponent)
    this.modalservice.closeCategoryModal().then(data => {
      console.log("closed Modal : ", data);
    })
  }

  //send product subtitution for approval
  sendProductSubtituteApproval(approvalProducst: any) {
    // substitute_product_id:any,product_id:any
    let temarray = new Array()
    for (let i = 0; i < approvalProducst.length; i++) {
      temarray.push({ product_id: approvalProducst[i].product.id, order_product_id: approvalProducst[i].id })
    }
    console.log("subtitue array : ", temarray);

    let data = {
      website_id: this.userOrderdata.website_id,
      warehouse_id: this.userOrderdata.warehouse_id,
      // product_id:this.userOrderdata.order_id,
      order_id: this.userOrderdata.order_id,
      user_id: this.userOrderdata.user_id,
      approval_details: temarray
    }
    // let temp = {
    //   user_id: 587,
    //   approval_details: [
    //     {
    //       product_id: 6618,
    //       order_product_id: 764
    //     },
    //     {
    //       product_id: 6630,
    //       order_product_id: 763
    //     }],
    //   website_id: 1,
    //   order_id: 3499,
    //   warehouse_id: 33
    // }
    console.log("subtitue array : ", data);
    if (this.product_billnumber !== "Enter Bill Number") {
      this.apiService.postData("picker-sendapproval/", data).subscribe((data: any[]) => {
        console.log("sendapproval : ", data);
        let tempdata: any = data
        // this.pickerProductList["data"] = data
        if (tempdata.status === 1) {
          this.globalitem.showSuccess(tempdata.message, "Subtitute Sent")
        }
      })
    } else {
      this.globalitem.showError("Picking not completed yet", "Warning")
    }
  }

  // dialog
  openDialog(apiURL: any, sub_apiUrl: any, pageTitle: any, productid: any, productType: any
    // quantity: any, product_id: any, order_product_id: any, shortage: any, index: any
  ): void {
    // this.updateMoreProductQuantity(quantity,product_id,order_product_id,shortage,index)
    let data = {
      order_id: this.userOrderdata.order_id,
      apiURL: apiURL,
      pageTitle: pageTitle,
      ean: "",
      product_id: productid,
      productType: productType,
      sub_apiUrl: sub_apiUrl,
      shipment_id: this.userOrderdata.shipment_id,
      trent_picklist_id: this.userOrderdata.trent_picklist_id
    }
    this.modalservice.openCategoryModal(data).then(data => {
      console.log("closed Modal : ", data);
      this.modalservice.closeCategoryModal().then(data => {
        console.log("closed Modal : ", data);
      })
    })
  }

  //update product quantity
  updateMoreProductQuantity(quantity: any, product_id: any, order_product_id: any, shortage: any, index: any) {
    console.log("prouct Quantity ", quantity);
    // substitute_product_id:any,product_id:any
    let data = {
      website_id: this.userOrderdata.website_id,
      warehouse_id: this.userOrderdata.warehouse_id,
      product_id: product_id,
      order_product_id: order_product_id,
      order_id: this.userOrderdata.order_id,
      user_id: this.userOrderdata.user_id,
      grn_quantity: quantity,
      shortage: shortage
    }
    this.apiService.postData("picker-updategrnquantity/", data).subscribe((data: any[]) => {
      console.log("updategrnquantity : ", data);
      let tempdata: any = data
      // this.pickerProductList["data"] = data
      if (tempdata.status === 1) {
        // this.globalitem.showSuccess(tempdata.message,"Subtitute Sent")
        let tem: any = data
        // this.orderDetaildata['data'][0].order_products = tem.response[0]?.order_products
        // console.log("updadted shortage : ",this.orderDetaildata['data'][0].order_products);
      }

    })
  }

  // product increment and decrement funtion will be common 
  productDecerment(quantity: any, product_id: any, order_product_id: any, shortage: any, index: any,
    apiURL: any, sub_apiUrl: any, pageTitle: any, productid: any, productType: any) {
    // console.log("index --: ",index);
    for (var i = 0; i < this.orderDetaildata['data'][0]?.order_products.length; i++) {
      if (i == index) {
        if(productType === ''){
          let templength = this.orderDetaildata['data'][0]?.order_products[i].grn_quantity - 1
          this.orderDetaildata["data"][0].order_products[i].grn_quantity = templength;
        }else if(productType === 2){
          let templength = this.orderDetaildata['data'][0]?.order_products[i].shortage - 1
          this.orderDetaildata["data"][0].order_products[i].shortage = templength;
          // this.openDialog(apiURL,sub_apiUrl, pageTitle, productid,productType)
        }
      }
    }
    this.updateMoreProductQuantity(quantity, product_id, order_product_id, shortage, index)
  }

  productIncrment(quantity: any, product_id: any, order_product_id: any, shortage: any, index: any,
    apiURL: any, sub_apiUrl: any, pageTitle: any, productid: any, productType: any) {
    // console.log("index ++: ", index);
    for (var i = 0; i < this.orderDetaildata['data'][0]?.order_products.length; i++) {
      if (i === index) {
        if(productType === ''){
          let templength = this.orderDetaildata['data'][0]?.order_products[i].grn_quantity + 1 //increment the quantity
        this.orderDetaildata["data"][0].order_products[i].grn_quantity = templength; //assaign quantity to input
        }else if(productType === 2){
          let templength = this.orderDetaildata['data'][0]?.order_products[i].shortage + 1
          this.orderDetaildata["data"][0].order_products[i].shortage = templength;
          this.openDialog(apiURL,sub_apiUrl, pageTitle, productid,productType)
        }
      }
    }
    this.updateMoreProductQuantity(this.orderDetaildata["data"][0].order_products[index].grn_quantity, product_id, order_product_id, shortage, index)
  }

  //this for assing bill number
  // BillnumberModal1(){
  //   if(this.product_billnumber === "Enter Bill Number"){
  //     this.product_billnumber=''
  //   }
  //   this.BillnumberModal(this.product_billnumber)
  // }
  BillnumberModal(billnumbr:any){
    console.log("bill number : ",billnumbr);
    
    let data={
      website_id:this.userOrderdata.website_id,
      order_id:this.userOrderdata.order_id,
      user_id:this.userOrderdata.user_id,
      billnumber:billnumbr

    }
  this.modalservice.openModal(data,BillnumberComponent).then(data =>{

  })
  this.modalservice.closeCategoryModal().then(data => {
    this.product_billnumber = data.billnumber
    console.log("closed Modal : ", data.billnumber);
  })
  }

  notifyCustomer(){
    let data = {
      website_id: this.userOrderdata.website_id,
      order_id: this.userOrderdata.order_id,
    }
    this.apiService.postData("picker-resetsendapproval/", data).subscribe((data: any) => {
      console.log("updategrnquantity : ", data);
      if (data.status === 1) {
        this.globalitem.showSuccess(data.message,"Subtitute Sent")
      }

    })
  }

  getLatestOrder(){
      let data = {
        website_id: this.userOrderdata.website_id,
        warehouse_id: this.userOrderdata.warehouse_id,
        order_id_for_substitute_checking: 3470,
        order_id: this.userOrderdata.order_id,
      }
      this.apiService.postData("picker-latestorders/", data).subscribe((data: any[]) => {
        console.log("latestorders : ", data);
      })
  }
}



