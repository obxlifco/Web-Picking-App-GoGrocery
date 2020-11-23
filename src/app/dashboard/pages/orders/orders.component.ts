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

export interface DialogData {
  animal: string;
  name: string;
}
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
    order_status: ''
  }
 
  minValue: any = new Date();
  maxValue: any = this.minValue.getDate() + 3;
  datetime: any;
  customErrorStateMatcher: any
  constructor(public router: Router,
    public dialog: MatDialog,
    public db: DatabaseService,
    public apiService: ApiService,
    public modalservice:ModalService,
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

  // dialog
  openDialog(apiURL:any,pageTitle:any,productid:any,productType:any): void {
    let data={
      order_id:this.userOrderdata.order_id,
      apiURL:apiURL,
      pageTitle:pageTitle,
      ean:"",
      product_id:productid,
      productType:productType
    }


    this.modalservice.openCategoryModal(data).then(data => {
      console.log("closed Modal : ", data); 
      this.modalservice.closeCategoryModal().then(data => {
        console.log("closed Modal : ", data);
      })
    })
  }

  processOrder() {

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
        this.orderlistdata["data"].response[0].picker_name)
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

    this.apiService.postData("picker-generatepicklist/", data).subscribe((data: any[]) => {
      console.log(data);
      // this.orderlistdata["data"] = data
    })
  }

  getOrderDetailData(orderid: any, shipment_id: string, order_status: string,picker_name: string) {
    console.log("order id :", orderid);
    this.userOrderdata.picker_name=picker_name;
    this.userOrderdata.order_id = orderid
    this.userOrderdata.order_status = order_status
    this.userOrderdata.shipment_id = shipment_id
    let data = {
      website_id: this.userOrderdata.website_id,
      order_id: orderid,
    }
    this.apiService.postData("picker-orderdetails/", data).subscribe((data: any[]) => {
      console.log(data);
      let temdata: any = []
      temdata = data
      this.orderDetaildata["data"] = temdata.response
    })
  }

  openmap(latlang: any) {
    console.log("latlang : ", latlang);
    // MapmodalComponent
    this.modalservice.openModal(latlang,MapmodalComponent)
  }

  timeChangeHandler(event: any) {
    console.log("date Event : ", event)
  }
  invalidInputHandler() {
  }

  openEditModal(data:any){
    this.modalservice.openModal(data,EditproductweightComponent)
    this.modalservice.closeCategoryModal().then(data => {
      console.log("closed Modal : ", data);
    })
    }
}
