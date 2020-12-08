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
import { DashboardComponent } from '../../dashboard.component';


@Component({
  selector: 'app-orders',
  templateUrl: './orders.component.html',
  styleUrls: ['./orders.component.scss'],
})
export class OrdersComponent implements OnInit {
  @ViewChild('bnumber', { static: true }) billnumber: ElementRef | any;
  subscription: Subscription | any;
  statusText: string | any;
  orderlistdata: any = []
  orderDetaildata: any = []
  userOrderdata = {
    warehouse_id: '',
    website_id: '',
    user_id: '',
    picker_name: null,
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
    ordernonlistType: '',
    payment_type_id:'',
    order_id_for_substitute_checking: 0,
    PickerCounter: 0, //set the counter to check if product selected in list
  }
  paymentonlineTimer=false
  order_Substitute_Time:any
  currenttime: any = new Date()
  isTimerStart = false
  isProductSendFor_Approval=true
  paymentOnlineTime: any
  price: any = ''
  currentPage: any = 1//pagination
  totalProductpage: any = 0
  countDownTimer: any
  IsTimeComplete: any
  customcolor: any
  product_billnumber: any = '';
  IS_Subtitute = false;
  timer: any
  leftTime: any = 5*60000

  //below date var is sample max and min date
  minValue: any = new Date();
  maxValue: any = this.minValue.getDate() + 3;
  datetime: any = new Date();
  customErrorStateMatcher: any

  constructor(public router: Router,
    public dialog: MatDialog,
    public appcom: DashboardComponent,
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
    console.log("picker Nme : ", this.userOrderdata.picker_name);

    this.datetime = this.datetime.getHours() + ':' + this.datetime.getMinutes()
    this.activated_route.params.subscribe(v => {
      console.log("activated route data :", v.orderstatus)
      if (v.orderstatus) {
        this.userOrderdata.orderlistType = v.orderstatus
        if (this.userOrderdata.orderlistType === "cancelled" || this.userOrderdata.orderlistType === "shipped") {
          this.appcom.setbadge(0)
        }

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

  getbillValidator() {
    this.billnumber?.nativeElement.focus();
    this.customcolor = "#FF0000"
    this.globalitem.showError("First you need to enter bill number", "Bill Number Empty")
  }
  getcounter() {
    this.userOrderdata.PickerCounter = 0
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
        page: this.currentPage,
        per_page: 100
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
      this.apiService.postData("picker-orderlist/", data).subscribe((data: any) => {
        // console.log(data);
        this.orderlistdata["data"] = data.response //json response
        this.totalProductpage = data.total_page//total page
        this.orderlistdata["data"].payment_type_id=data?.response?.payment_type_id
        this.getOrderDetailData(this.orderlistdata["data"][0].id, this.orderlistdata["data"][0].shipment_id, this.orderlistdata["data"][0].order_status,
          this.orderlistdata["data"][0].picker_name, this.orderlistdata["data"][0].substitute_status)
          
        if (this.currentPage === 1) {
          this.orderlistdata["data"] = data.response
          this.totalProductpage = data.total_page
        } else {
          console.log("page n");
          this.orderlistdata["data"] = [...  this.orderlistdata["data"], ...data.response];
        }


      })
    })



  }

  //when to assaign user name to order
  AssaignorderToUser(value: any) {
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
      // this.reloadpage()
      this.getOrderlistData()
      // this.getOrderDetailData( this.userOrderdata.order_id,  this.userOrderdata.shipment_id,  this.userOrderdata.order_status,  this.userOrderdata.picker_name,  this.userOrderdata.substitute_status)

    })
  }

  getOrderDetailData(orderid: any, shipment_id: string, order_status: string, picker_name: any, substitute_status: any) {
    // this.IsTimeComplete = ''
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

      this.paymentOnlineTime = this.datePipe.transform(this.orderDetaildata["data"][0]?.created, "MMM d, y, h:mm:ss a");
      this.currenttime = this.datePipe.transform(new Date(), "MMM d, y, h:mm:ss a");
      if(this.orderDetaildata["data"][0]?.order_substitute_products){
        // console.log("entered in if ",this.orderDetaildata["data"]?.order_substitute_products);
        
        this.order_Substitute_Time = this.datePipe.transform(this.orderDetaildata["data"][0]?.order_substitute_products[0]?.created, "MMM d, y, h:mm:ss a")
       console.log(" order_Substitute_Time ",this.order_Substitute_Time  );
       
      //  this.leftTime= 0.6*60000
       console.log("added 10 minutes to substitute  ",this.order_Substitute_Time + (30 * 60 * 1000));
       
        // let milisecond =Date.parse(this.currenttime) - Date.parse(this.order_Substitute_Time) //when subs product sent for a approval, thne time will start for ten minutes
        //   var seconds:any = (addedminutes_milisecond / 1000).toFixed(0);
        //     var minutes = Math.floor(seconds / 60);
        //     console.log("Date true",minutes ,"left minutes : ",this.leftTime);
        this.timerProductSentApproval(this.order_Substitute_Time,10)
      }
      // if(this.orderDetaildata["data"]?.payment_type_id === 2){
      if(true){
        console.log("timer");
        this.timerProductSentApproval(this.paymentOnlineTime,30)
      }
  
      // let timediff=Date.parse( this.currenttime) - Date.parse(this.paymentOnlineTime)
    

      // // test timer
      // if(timediff === 30){
      //   console.log("Date true",Date.parse(this.currenttime) - Date.parse(this.paymentOnlineTime));
      //   let milisecond =Date.parse(this.currenttime) - Date.parse(this.paymentOnlineTime)
      //   var seconds:any = (milisecond / 1000).toFixed(0);
      //     var minutes = Math.floor(seconds / 60);
      //     console.log("Date true",minutes);
      // }else{
      //   console.log(" Date false");
      // }


      this.userOrderdata.shipment_id = this.orderDetaildata["data"][0].shipment_id
      this.userOrderdata.trent_picklist_id = this.orderDetaildata["data"][0].trent_picklist_id
      this.userOrderdata.order_id_for_substitute_checking = this.orderlistdata['data'][0].id
      if (this.userOrderdata.orderlistType === 'cancelled' || this.userOrderdata.orderlistType === 'shipped') {
      } else {
        this.getLatestOrder(this.userOrderdata.order_id_for_substitute_checking, 'insidePage')
      }

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
    const dialogRef = this.dialog.open(EditproductweightComponent, { width: '500px', data: { data: data } });
    dialogRef.afterClosed().subscribe(result => {
      console.log('The dialog was closed', result);
      this.getOrderDetailData(this.userOrderdata.order_id, this.userOrderdata.shipment_id, this.userOrderdata.order_status, this.userOrderdata.picker_name, this.userOrderdata.substitute_status)
    });
  }

  //send product subtitution for approval
  sendProductSubtituteApproval(approvalProducst: any, bill_value: any, product_billnumber: any) {

    this.getcounter()
    let temarray = new Array()
    for (let i = 0; i < approvalProducst.length; i++) {
      temarray.push({ product_id: approvalProducst[i].product.id, order_product_id: approvalProducst[i].id })
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
    if (this.userOrderdata.PickerCounter === 0) {
      // if (this.billnumber.nativeElement.value) {
      this.apiService.postData("picker-sendapproval/", data).subscribe((data: any) => {
        if (data.status === 1) {
          this.timerProductSentApproval(this.order_Substitute_Time,10)
          this.getOrderDetailData(this.userOrderdata.order_id, this.userOrderdata.shipment_id, this.userOrderdata.order_status, this.userOrderdata.picker_name, this.userOrderdata.substitute_status)
          this.globalitem.showSuccess(data.message, "Subtitute Sent")
          this.ApprovalTimer(10000)
          // this.reloadpage()
        }
      })

      // } else {
      //   this.getbillValidator()
      // }
    } else {
      this.globalitem.showError("Picking list not completed yet", "Warning")
    }

  }

  // dialog
  openDialog(apiURL: any, sub_apiUrl: any, pageTitle: any, productid: any, productType: any, shortage: any, substituteData: any, ean: any
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

    const dialogRef = this.dialog.open(AddnewproductComponent, { width: '500px', data: { data: data } });
    dialogRef.afterClosed().subscribe(result => {
      console.log('The dialog was closed', result);
      this.getOrderDetailData(this.userOrderdata.order_id, this.userOrderdata.shipment_id, this.userOrderdata.order_status, this.userOrderdata.picker_name, this.userOrderdata.substitute_status)

      // if (result.data.subtitutestatus === "productadded") {
      //   setTimeout(() => {
      //     // this.reloadpage()
      //     this.getOrderDetailData(this.userOrderdata.order_id, this.userOrderdata.shipment_id, this.userOrderdata.order_status, this.userOrderdata.picker_name, this.userOrderdata.substitute_status)
      //   }, 100);
      // } else if (result.subtitutestatus === 'no_productadded') {
      //   this.updateMoreProductQuantity(result.substituteData.grn_quantity, result.substituteData.product_id, result.substituteData.order_product_id, result.substituteData.shortage, 0)
      //   setTimeout(() => {
      //     this.getOrderDetailData(this.userOrderdata.order_id, this.userOrderdata.shipment_id, this.userOrderdata.order_status, this.userOrderdata.picker_name, this.userOrderdata.substitute_status)
      //   }, 100);
      // }

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

  productIncrment(grn_quantity: any, product_id: any, order_product_id: any, shortage: any, index: any,
    apiURL: any, sub_apiUrl: any, pageTitle: any, productid: any, productType: any, ean: any) {
    var modaldata = {
      shortage: shortage,
      grn_quantity: grn_quantity,
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
          this.openDialog(apiURL, sub_apiUrl, pageTitle, productid, productType, templength, modaldata, ean)
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
  getLatestOrder(orderData: any, reqestType: any) {
    let temData: any;
    let data = {
      website_id: this.userOrderdata.website_id,
      warehouse_id: this.userOrderdata.warehouse_id,
      order_id_for_substitute_checking: this.userOrderdata.order_id,
      order_id: orderData,
    }
    if (reqestType === "insidePage") {
      console.log("insidePage data : ", temData);
      temData = data
    } else if (reqestType === "outsidePage") {
      console.log("outside data : ", temData);

      temData = orderData
    }


    this.apiService.postData("picker-latestorders/", temData).subscribe((data: any) => {
      console.log("latestorders : ", data);
      this.appcom.setbadge(data.response.no_of_latest_order)
      this.db.setOrderIDS(temData)
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
  timeChangeHandler(event: any, starttime: any) {

    var medium = this.datePipe.transform(new Date(), "'h:mm");
    console.log("date Event : ", medium)
    let data = {
      website_id: this.userOrderdata.website_id,
      user_id: this.userOrderdata.user_id,
      order_id: this.userOrderdata.order_id,
      slot_start_time: starttime,
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
      this.isProductSendFor_Approval=true
    }

  }

  // this will refresh the page
  reloadpage() {
    this.router.routeReuseStrategy.shouldReuseRoute = () => false;
    this.router.onSameUrlNavigation = 'reload';
    this.router.navigate(['dashboard/orders']);
  }

  //start time counter for getting latest orders
  startcounter() {
    console.log("timer started");
    this.db.getNotificationTime().then(res => {
      // console.log("user timer : ", res);
      this.subscription = timer(0, res).pipe(
        switchMap(async () => {
          this.db.getOrderIDS().then(res => {
            console.log(" Type : ", this.userOrderdata.orderlistType);
            if (this.userOrderdata.orderlistType === 'cancelled' || this.userOrderdata.orderlistType === 'shipped') {
            } else {
              this.getLatestOrder(res, 'outsidePage')
            }
          })
        })

      ).subscribe(result => {
      }
      );
    })
  }

  onScrollDown(ev: any) {
    console.log('scrolled!!', ev);
    this.currentPage++;
    // this.getOrderlistData()
    if (this.currentPage <= this.totalProductpage) {
      this.getOrderlistData()
    } else {
      // this.globalitem.showError("No more data is available ","No Data")
    }

  }

  ApprovalTimer(timeValue:any) {
    this.isTimerStart = true
    this.userOrderdata.substitute_status = "pending"
    this.subscription = timer(0, timeValue).pipe(
      switchMap(async () => {
        this.getOrderlistData()
        this.getOrderDetailData(this.userOrderdata.order_id, this.userOrderdata.shipment_id, this.userOrderdata.order_status, this.userOrderdata.picker_name, this.userOrderdata.substitute_status)
        if(this.userOrderdata.substitute_status === "none"){
          this.isProductSendFor_Approval=true
        }
      })
    ).subscribe(result => {
      console.log("timer started");
    })
  }

  //timer for sent product approval
  timerProductSentApproval(productTime:any,totaltime:any){
    const originalDate = new Date(productTime);
    const modifiedTime:any = this.datePipe.transform(new Date(originalDate.valueOf() + (1 * 60000)),"MMM d, y, h:mm:ss a")
    // const subst_modifiedTime:any = this.datePipe.transform(new Date(originalDate.valueOf() + (2 * 60000)),"MMM d, y, h:mm:ss a")
    console.log(" modifiedTime ",modifiedTime ," currenttime : ",this.currenttime);
    this.leftTime = Date.parse(modifiedTime) - Date.parse(this.currenttime)
    //assaign difference to timer between subs time and current time
    let milisecond =Date.parse(modifiedTime) - Date.parse(this.currenttime) //when subs product sent for a approval, thne time will start for ten minutes
        var seconds:any = (milisecond / 1000).toFixed(0);
        this.leftTime = Math.floor(seconds / 60)*60000/900;
          console.log("left minutes : ",this.leftTime);

    //check if timer is available ore not
    console.log("current Time : ",this.currenttime,"modifiedTime ",modifiedTime);
    
    if(Date.parse(modifiedTime)  > Date.parse(this.currenttime)){
      this.paymentonlineTimer=false
      console.log("timer is greater false");
      if(this.userOrderdata.substitute_status === "none"){
        this.isProductSendFor_Approval=true
      }else if(this.userOrderdata.substitute_status === "pending"){
        this.isProductSendFor_Approval=false
      }
    }else{
      this.paymentonlineTimer=true
      this.isProductSendFor_Approval=true
      this.IsTimeComplete=false
      console.log("timer is less than true");
    }
  }

     //unsubscribe timer
     destroyCounter(){
      this.subscription.unsubscribe();
    }

}