import { Component, ElementRef, NgModule, OnInit, ViewChild } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
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
import { EditpriceComponent } from 'src/app/components/editprice/editprice.component';
import { DatePipe } from '@angular/common';
import { AppComponent } from 'src/app/app.component';
import { Subscription, timer } from 'rxjs';
import { switchMap } from 'rxjs/operators';


@Component({
  selector: 'app-orders',
  templateUrl: './orders.component.html',
  styleUrls: ['./orders.component.scss'],
})
export class OrdersComponent implements OnInit {
  @ViewChild('bnumber', { static: true }) billnumber: ElementRef | any;
  // @ViewChild('time', { static: true }) timer: ElementRef | any

  // item_available: any = 0;
  // item_not_available: any = 0;

  // name: any = "Pepsi";
  // category: any = "drink";


  subscription: Subscription | any;
  statusText: string  | any;
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
    substitute_status: '',
    shortage: '',
    grn_quantity: 0,
    product_id: '',
    order_product_id: '',
    orderlistType: null,
    order_id_for_substitute_checking:0,
   PickerCounter : 0 //set the counter to check if product selected in list
  }
  price: any = ''
  countDownTimer: any
  IsTimeComplete: any
  customcolor: any
  product_billnumber: any = '';
  IS_Subtitute = false;
  timer: any

  //below date var is sample max and min date
  minValue: any = new Date();
  maxValue: any = this.minValue.getDate() + 3;
  datetime: any = new Date();
  customErrorStateMatcher: any

  constructor(public router: Router,
    public dialog: MatDialog,
    public appcom: AppComponent,
    public datePipe: DatePipe,
    public db: DatabaseService,
    public apiService: ApiService,
    public modalservice: ModalService,
    private activated_route: ActivatedRoute,
    public globalitem: GlobalitemService) {
    // this.dataService.sendGetRequest().subscribe((data: any[])=>{
    //   console.log(data);
    //   this.products = data;
    // })  
    this.datetime = this.datetime.getHours() + ':' + this.datetime.getMinutes()
    this.activated_route.params.subscribe(v => {
      console.log("activated route data :", v.orderstatus)
      if (v.orderstatus) {
        this.userOrderdata.orderlistType = v.orderstatus

      }

    })
    this.startcounter()
  }

  ngOnInit(): void {
    this.orderlistdata["data"] = []
    this.orderDetaildata["data"] = []
    
    this.getOrderlistData()
  }

  navigate(link: any) {
    this.router.navigate([link]);
  }



  //call when we completing the order
  processOrder() {
   
    this.getcounter()

    // substitute_product_id:any,product_id:any
    let data = {
      website_id: this.userOrderdata.website_id,
      warehouse_id: this.userOrderdata.warehouse_id,
      order_id: this.userOrderdata.order_id,
      user_id: this.userOrderdata.user_id,
      shipment_id: this.userOrderdata.shipment_id,
      trent_picklist_id: this.userOrderdata.trent_picklist_id,
    }
    console.log("Total counter : ", this.userOrderdata.PickerCounter);

    if (this.billnumber.nativeElement.value) {
      if (this.userOrderdata.PickerCounter === 0) {
        this.apiService.postData("picker-grn-complete/", data).subscribe((data: any[]) => {
          console.log("picker-grn-complete : ", data);
          let tempdata: any = data
          // this.pickerProductList["data"] = data
          if (tempdata.status === 1) {
            this.globalitem.showSuccess(tempdata.message, "Order Placed")
            this.reloadpage()
          }

        })
      } else {
        this.globalitem.showError("First you need to select all product from list", "Select product")
      }
    } else {
      this.getbillValidator()
    }


  }

  getbillValidator(){
    this.billnumber?.nativeElement.focus();
    this.customcolor = "#FF0000"
    this.globalitem.showError("First you need to enter bill number", "Bill Number Empty")
  }
  getcounter(){
    this.userOrderdata.PickerCounter=0
    for (var i = 0; i < this.orderDetaildata['data'][0]?.order_products.length; i++) {
      if (this.orderDetaildata['data'][0]?.order_products[i].grn_quantity + this.orderDetaildata['data'][0]?.order_products[i].shortage === this.orderDetaildata['data'][0]?.order_products[i].quantity) {
        // counter=0
      } else {
        this.userOrderdata.PickerCounter++
      }
    }
  }

  getOrderlistData() {
    this.db.getUserData().then(res => {
      console.log("user data inside dashboard : ", res);

      let data = {
        warehouse_id: res.warehouse_id,
        website_id: res.website_id,
      }
      if (this.userOrderdata.orderlistType !== null) {
        let status = {
          order_status: this.userOrderdata.orderlistType
        }
        Object.assign(data, status)
      }

      this.userOrderdata.warehouse_id = res.warehouse_id
      this.userOrderdata.website_id = res.website_id
      this.userOrderdata.user_id = res.user_id
      this.apiService.postData("picker-orderlist/", data).subscribe((data: any[]) => {
        console.log(data);
        this.orderlistdata["data"] = data
        this.getOrderDetailData(this.orderlistdata["data"].response[0].id, this.orderlistdata["data"].response[0].shipment_id, this.orderlistdata["data"].response[0].order_status,
          this.orderlistdata["data"].response[0].picker_name, this.orderlistdata["data"].response[0].substitute_status)
      })
    })



  }

  //when to assaign user name to order
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
      this.reloadpage()
    })
  }

  getOrderDetailData(orderid: any, shipment_id: string, order_status: string, picker_name: string, substitute_status: any) {
    this.IsTimeComplete = ''
    console.log("order id :", orderid);
    this.userOrderdata.picker_name = picker_name;
    this.userOrderdata.order_id = orderid
    this.userOrderdata.order_status = order_status
    this.userOrderdata.shipment_id = shipment_id
    this.userOrderdata.substitute_status = substitute_status
    let data = {
      website_id: this.userOrderdata.website_id,
      order_id: orderid,
    }
    
    this.apiService.postData("picker-orderdetails/", data).subscribe((data: any[]) => {
      console.log(data);
      let temdata: any = []
      temdata = data
      this.orderDetaildata["data"] = temdata.response
      this.userOrderdata.shipment_id = this.orderDetaildata["data"][0].shipment_id
      this.userOrderdata.trent_picklist_id=this.orderDetaildata["data"][0].trent_picklist_id
      this.userOrderdata.order_id_for_substitute_checking=this.orderlistdata['data']?.response[0].id
      this.getLatestOrder( this.userOrderdata.order_id_for_substitute_checking,'insidePage')
      // let time: any = this.orderDetaildata['data'][0]?.order_activity[0]?.activity_date;

      this.getsubtitteStatus()
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



  openEditModal(data: any) {
    let user_ids = {
      website_id: this.userOrderdata.website_id,
      user_id: this.userOrderdata.user_id,
      user_name: this.userOrderdata.picker_name
    }
    Object.assign(data, user_ids)
    const dialogRef = this.dialog.open(EditproductweightComponent, {width: '500px', data: { data: data }});
    dialogRef.afterClosed().subscribe(result => {console.log('The dialog was closed', result);
    this.getOrderDetailData(this.userOrderdata.order_id, this.userOrderdata.shipment_id, this.userOrderdata.order_status, this.userOrderdata.picker_name, this.userOrderdata.substitute_status)
    });
  }

  //send product subtitution for approval
  sendProductSubtituteApproval(approvalProducst: any, bill_value: any, product_billnumber: any) {

    this.getcounter()
    let temarray = new Array()
    for (let i = 0; i < approvalProducst.length; i++) {
      temarray.push({ product_id: approvalProducst[i].product.id, order_product_id:approvalProducst[i].id})
    }
    console.log("subtitue array : ", temarray);
    let data = {
      website_id: this.userOrderdata.website_id,
      warehouse_id: this.userOrderdata.warehouse_id,
      order_id: this.userOrderdata.order_id,
      user_id: this.userOrderdata.user_id,
      approval_details: temarray
    }
    this.IsTimeComplete = true
    // console.log("subtitue array : ", data);
    if(this.userOrderdata.PickerCounter === 0){
      if (this.billnumber.nativeElement.value) {
        this.apiService.postData("picker-sendapproval/", data).subscribe((data: any) => {
          if (data.status === 1) {
            this.globalitem.showSuccess(data.message, "Subtitute Sent")
            // this.reloadpage()
          }
        })
  
      } else {
        this.getbillValidator()
      }
    }else {
      this.globalitem.showError("Picking list not completed yet", "Warning")
    }

  }

  // dialog
  openDialog(apiURL: any, sub_apiUrl: any, pageTitle: any, productid: any, productType: any, shortage: any, substituteData: any,ean:any
    // quantity: any, product_id: any, order_product_id: any, shortage: any, index: any
  ): void {
    // this.updateMoreProductQuantity(quantity,product_id,order_product_id,shortage,index)
    let data = {
      order_id: this.userOrderdata.order_id,
      apiURL: apiURL,
      pageTitle: pageTitle,
      ean: ean,
      product_id: productid,
      productType: productType,
      sub_apiUrl: sub_apiUrl,
      shipment_id: this.userOrderdata.shipment_id,
      trent_picklist_id: this.userOrderdata.trent_picklist_id,
      shortage: shortage,
      substituteData: substituteData
    }
    // this.modalservice.openCategoryModal(data)
    // this.modalservice.closeCategoryModal().then(data => {
    //   console.log("closed Modal : ", data);
    //   this.reloadpage()
    //   if (data.subtitutestatus === "productadded") {
    //     // this.updateMoreProductQuantity(data.substituteData.grn_quantity,data.substituteData.product_id,data.substituteData.order_product_id,data.substituteData.shortage,0)

    //   }
    // })

    const dialogRef = this.dialog.open(AddnewproductComponent, {width: '500px', data: { data: data }});
    dialogRef.afterClosed().subscribe(result => {console.log('The dialog was closed', result);
      setTimeout(() => {
        // this.reloadpage()
        this.getOrderDetailData(this.userOrderdata.order_id, this.userOrderdata.shipment_id, this.userOrderdata.order_status, this.userOrderdata.picker_name, this.userOrderdata.substitute_status)
      }, 100);
      if (result.subtitutestatus === "productadded") {
        // this.updateMoreProductQuantity(data.substituteData.grn_quantity,data.substituteData.product_id,data.substituteData.order_product_id,data.substituteData.shortage,0)

      }

    });
  }

  //update product quantity
  updateMoreProductQuantity(quantity: any, product_id: any, order_product_id: any, shortage: any, index: any) {
    console.log("prouct Quantity ", quantity);
    // substitute_product_id:any,product_id:any
    let data = {
      website_id: this.userOrderdata.website_id,
      // warehouse_id: this.userOrderdata.warehouse_id,
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
        if (productType === '') {
          let templength = this.orderDetaildata['data'][0]?.order_products[i].grn_quantity - 1
          if (templength < 0) {
            this.orderDetaildata["data"][0].order_products[i].grn_quantity = 0;
          } else {
            this.orderDetaildata["data"][0].order_products[i].grn_quantity = templength;
          }
        } else if (productType === 2) {
          let templength = this.orderDetaildata['data'][0]?.order_products[i].shortage - 1
          if (templength < 0) {
            this.orderDetaildata["data"][0].order_products[i].shortage = 0;
          } else {
            this.orderDetaildata["data"][0].order_products[i].shortage = templength;
          }

          // this.openDialog(apiURL,sub_apiUrl, pageTitle, productid,productType)
        }
      }
    }
    this.updateMoreProductQuantity(quantity, product_id, order_product_id, shortage, index)
  }

  productIncrment(quantity: any, product_id: any, order_product_id: any, shortage: any, index: any,
    apiURL: any, sub_apiUrl: any, pageTitle: any, productid: any, productType: any,ean:any) {
    var modaldata = {
      shortage: shortage,
      grn_quantity: quantity,
      product_id: product_id,
      order_product_id: order_product_id
    }
    for (var i = 0; i < this.orderDetaildata['data'][0]?.order_products.length; i++) {
      if (i === index) {
        if (productType === '') {
          let templength = this.orderDetaildata['data'][0]?.order_products[i].grn_quantity + 1 //increment the quantity
          this.orderDetaildata["data"][0].order_products[i].grn_quantity = templength; //assaign quantity to input
          this.updateMoreProductQuantity(this.orderDetaildata["data"][0].order_products[index].grn_quantity, product_id, order_product_id, shortage, index)
        } else if (productType === 2) {
          let templength = this.orderDetaildata['data'][0]?.order_products[i].shortage + 1
          this.orderDetaildata["data"][0].order_products[i].shortage = templength;
          this.updateMoreProductQuantity(this.orderDetaildata["data"][0].order_products[index].grn_quantity, product_id, order_product_id, templength, index)
          this.openDialog(apiURL, sub_apiUrl, pageTitle, productid, productType, templength, modaldata,ean)
        }
      }
    }

  }

  //this for assing bill number
  // BillnumberModal1(){
  //   if(this.product_billnumber === "Enter Bill Number"){
  //     this.product_billnumber=''
  //   }
  //   this.BillnumberModal(this.product_billnumber)
  // }
  BillnumberModal(billnumbr: any) {
    console.log("bill number : ", billnumbr);

    let data = {
      website_id: this.userOrderdata.website_id,
      order_id: this.userOrderdata.order_id,
      user_id: this.userOrderdata.user_id,
      billnumber: billnumbr
    }

    const dialogRef = this.dialog.open(BillnumberComponent, {
      width: '500px',
      data: { data: data }
    });

    dialogRef.afterClosed().subscribe(result => {
      console.log('The dialog was closed', result);
      this.product_billnumber = result.billnumber

    });
    // this.modalservice.openModal(data,BillnumberComponent).then(data =>{
    // })
    // this.modalservice.closeCategoryModal().then(data => {
    //   this.product_billnumber = data.billnumber
    //   console.log("closed Modal : ", data.billnumber);
    // })
  }

  // to notfy customer using bell icon with badge
  declinedProduct() {
    let data = {
      website_id: this.userOrderdata.website_id,
      order_id: this.userOrderdata.order_id,
    }
    this.apiService.postData("picker-resetsendapproval/", data).subscribe((data: any) => {
      console.log("updategrnquantity : ", data);
      if (data.status === 1) {
        this.globalitem.showSuccess(data.message, "Subtitute Declined")
        this.reloadpage()
      }
    })
  }
  //get latest order then add tit it notify status
  getLatestOrder(orderData:any,reqestType:any) {
    let temData:any;
    let data = {
      website_id: this.userOrderdata.website_id,
      warehouse_id: this.userOrderdata.warehouse_id,
      order_id_for_substitute_checking: this.userOrderdata.order_id,
      order_id: orderData,
    }
    if(reqestType === "insidePage"){
      temData=data
    }else if(reqestType === "outsidePage"){
      temData=orderData
    }

    this.db.setOrderIDS(temData)
    this.apiService.postData("picker-latestorders/", temData).subscribe((data: any) => {
      console.log("latestorders : ", data);
      this.appcom.setbadge(data.response.no_of_latest_order)
    })
  }
  updatePrice(order_amount: any, netAmount: any) {
    console.log("order mount : ", order_amount);
    if (order_amount === null) {
      order_amount = netAmount
    }

    let data = {
      website_id: this.userOrderdata.website_id,
      order_id: this.userOrderdata.order_id,
      user_id: this.userOrderdata.user_id,
      order_amount: order_amount
    }

    const dialogRef = this.dialog.open(EditpriceComponent, {
      width: '500px',
      data: { data: data }
    });

    dialogRef.afterClosed().subscribe(result => {
      console.log('The dialog was closed', result);
      this.price = result.price

    });

    // this.modalservice.openModal(data,EditpriceComponent)
    // this.modalservice.closeCategoryModal().then(data => {
    //   this.price = data.price
    //   console.log("closed Modal : ", data.price);
    // })
  }

  //update detail order data with time
  timeChangeHandler(event: any,starttime:any) {

    var medium = this.datePipe.transform(new Date(), "'h:mm");
    console.log("date Event : ", medium)
    let data = {
      website_id: this.userOrderdata.website_id,
      user_id: this.userOrderdata.user_id,
      order_id: this.userOrderdata.order_id,
      slot_start_time:starttime,
      slot_end_time: this.datePipe.transform(event, "'h:mm")
    }
    this.apiService.postData("picker-updateorderdetails/", data).subscribe((data: any) => {
      if (data.status === 1) {
        this.globalitem.showSuccess(data.message, "Time Updated")
      } else {
        this.globalitem.showError(data.message, "Warn")
      }
    })
  }
  invalidInputHandler() {
  }

  //on scroll we load more data
  getNextData() {
    console.log('scrolled!!');
  }


  //this method use for to check substitute is there are not 
  getsubtitteStatus() {
    for (var i = 0; i < this.orderDetaildata['data'][0]?.order_substitute_products.length; i++) {
      if (this.orderDetaildata['data'][0]?.order_substitute_products[i].send_approval === "approve" || this.orderDetaildata['data'][0]?.order_substitute_products[i].send_approval === "declined") {
        // counter=0
        this.IS_Subtitute = true
      } else {
        console.log("true");
        this.IS_Subtitute = false
      }
    }

    if (this.orderDetaildata['data'][0]?.order_substitute_products.length === 0) {
      this.IS_Subtitute = true
    }


  }
  handleEvent(event: any) {
    console.log("event occur : ", event);
    if (event.action === "done") {
      this.IsTimeComplete = false
    }

  }

  // this will refresh the page
  reloadpage() {
    this.router.routeReuseStrategy.shouldReuseRoute = () => false;
    this.router.onSameUrlNavigation = 'reload';
    this.router.navigate(['orders']);
  }

       //start time counter for getting latest orders
       startcounter(){
         console.log("timer is start");
         
        this.db.getNotificationTime().then(res => {
          console.log("user timer : ", res);
          this.subscription = timer(0, res).pipe(
            switchMap(async () => {
              this.db.getOrderIDS().then(res => {
                this.getLatestOrder(res,'outsidePage')})
            })
            
          ).subscribe(result =>{this.globalitem.showSuccess("Check your latest order ","Latest order");
          }
          );
        })
}



}