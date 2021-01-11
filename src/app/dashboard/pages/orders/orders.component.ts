import { Component, ElementRef, NgModule, OnInit, ViewChild } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
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
import { Subscription, timer } from 'rxjs';
import { switchMap } from 'rxjs/operators';
import { DashboardComponent } from '../../dashboard.component';
import { AddproductasSubtituteComponent } from 'src/app/components/addproductas-subtitute/addproductas-subtitute.component';
import { CommonfunctionService } from 'src/app/core/utilities/commonfunction.service';
import { AssaignpickerComponent } from 'src/app/components/assaignpicker/assaignpicker.component';

declare var window: any
@Component({
  selector: 'app-orders',
  templateUrl: './orders.component.html',
  styleUrls: ['./orders.component.scss'],
})
export class OrdersComponent implements OnInit {
  @ViewChild('bnumber', { static: false }) billnumber: ElementRef | any;
  @ViewChild('footer', { static: false }) footerid: ElementRef | any;
  // @ViewChild('printwithsku', { static: false }) withsku: ElementRef | any;
  // @ViewChild('printwithOutsku', { static: false }) withoutsku: ElementRef | any;

  pdfMake: any;
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
    orderlistType: "new",
    ordernonlistType: '',
    payment_type_id: '',
    order_id_for_substitute_checking: 0,
    PickerCounter: 0, //set the counter to check if product selected in list
    warehouseName: '',
    storename: '',//for generic data
    storecode: ''
  }
  keyValueOF_superStore = {
    key: 0,
    value: '',
    apistatus: ''
  }
  paymentonlineTimer = false
  isOrderList = false
  order_Substitute_Time: any
  currenttime: any = new Date()
  isTimerStart = false
  isProductSendFor_Approval = true
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
  leftTime: any = 5 * 60000
  isdownload = false
  //below date var is sample max and min date
  // minValue: any = new Date();
  // maxValue: any = this.minValue.getDate() + 3;
  datetime: any;
  customErrorStateMatcher: any
  printerTotalcost: any = 0; //for total cost of products printing
  totalProductItems: any = 0//for printer product quantity
  //testing tabs
  navTablink: any = [
    {
      name: 'New Order',
      type: 'new',
      key: 0,
    },
    {
      name: 'In-Processing',
      type: 'In-Processing',
      key: 100,
    },
    {
      name: 'Shipped',
      type: 'shipped',
      key: 1

    },
    {
      name: 'Cancelled',
      type: 'cancelled',
      key: 2

    }, {
      name: 'Completed',
      type: 'complete',
      key: 4
    }
  ]
  activeLink = this.navTablink[0];

  constructor(public router: Router,
    public dialog: MatDialog,
    public commonfunc: CommonfunctionService,
    public appcom: DashboardComponent,
    public datePipe: DatePipe,
    public db: DatabaseService,
    public apiService: ApiService,
    public modalservice: ModalService,
    private activated_route: ActivatedRoute,
    public globalitem: GlobalitemService) {
      
    // console.log("picker Nme : ", this.userOrderdata.picker_name);
    // this.datetime = this.datetime.getHours() + ':' + this.datetime.getMinutes()
    // this.getuserData()
    this.activated_route.params.subscribe(v => {
      // console.log("activated route data :", v)
      if (v.key)
        this.keyValueOF_superStore.value = v.value
      this.keyValueOF_superStore.key = parseInt(v.key)
      this.keyValueOF_superStore.apistatus = "dashboard"
      if (v.orderstatus) {
        // console.log("order status  ");
        
        this.userOrderdata.orderlistType = v.orderstatus
        for (let i = 0; i < this.navTablink.length; i++) {
          if (this.navTablink[i].type === this.userOrderdata.orderlistType) {
            console.log("conditions true : ",this.navTablink[i].type ,this.userOrderdata.orderlistType);
            this.activeLink = this.navTablink[i];
          }
        }
        if (this.userOrderdata.orderlistType === "cancelled" || this.userOrderdata.orderlistType === "shipped") {
          this.appcom.setbadge(0)
        }
      }
    })
    
    console.log("order type : ",this.userOrderdata.orderlistType);
    if(this.userOrderdata.orderlistType === "new"){
      
      this. setNewOrderApiAttribute()
    }else{
      this.getOrderlistData()
      this.startcounter()
    }

  }

  setNewOrderApiAttribute(){
    this.getnewOrders()
  }

  getuserData(){
    this.db.getUserData().then(res => {
      this.userOrderdata.warehouse_id = res.warehouse_id
      this.userOrderdata.website_id = res.website_id
      this.userOrderdata.user_id = res.user_id
    })
  }

  ngOnInit(): void {
    this.orderlistdata["data"] = []
    this.orderDetaildata["data"] = []
    
  }
  setordertype(type: any, key: any, value: any) {
    this.keyValueOF_superStore.key = key
    this.keyValueOF_superStore.value = value
    this.userOrderdata.orderlistType = type;
    if(this.userOrderdata.orderlistType !== "new"){
      this.getOrderlistData()
    }else{
      this.setNewOrderApiAttribute()
    }
  }
  movetofooter(value: any) {
    let innerContents: any;
    if (value === "header") {
      innerContents = document.getElementById("footer");
    } else {
      innerContents = document.getElementById("header");
    }
    // const targetElement = this.footerid.nativeElement
    innerContents.scrollIntoView({ behavior: "smooth" })
  }
  navigate(link: any) {
    this.router.navigate([link]);
  }
  //call when we completing the order
  processOrder() {
    this.getcounter()
    console.log("value : ", this.billnumber.nativeElement.value);
    if (this.billnumber.nativeElement.value) {
      if (this.userOrderdata.PickerCounter === 0) {
        this.openConfirmationDialog()
      } else {
        this.globalitem.showError("First you need to select all product from picker order list", "Select product")
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
      // console.log("user data inside dashboard : ", res);

      let data = {
        warehouse_id: res.warehouse_id,
        website_id: res.website_id,
        page: this.currentPage,
        per_page: 100,
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
      if (res.warehouse_id !== null && this.userOrderdata.orderlistType !== 'complete') {
        this.apiService.postData("picker-orderlist/", data).subscribe((data: any) => {
          // console.log(data);
          if (data.status !== 0) {
            this.isOrderList = false
            this.orderlistdata["data"] = data.response //json response
            this.totalProductpage = data.total_page//total page
            this.orderlistdata["data"].payment_type_id = data?.response?.payment_type_id
            this.orderlistDetaildata()

            if (this.currentPage === 1) {
              this.orderlistdata["data"] = data.response
              this.totalProductpage = data.total_page
            } else {
              // console.log("page n");
              this.orderlistdata["data"] = [...  this.orderlistdata["data"], ...data.response];
            }
          } else {
            this.isOrderList = true
            this.orderlistdata["data"] = []
            this.globalitem.showError("No Orderlist found ", "No Order")
          }
        })
      } if (this.userOrderdata.orderlistType === 'complete') {
        this.getCompletedOrders()
      } else if (this.keyValueOF_superStore.apistatus === 'dashboard' && res.warehouse_id === null) {
        console.log("else if");

        this.getCompletedOrders()
      }
    })
  }
  orderlistDetaildata(){
    let temarray :any=[]
    for(let i=0;i<this.orderlistdata["data"].length;i++){
      if(this.orderlistdata["data"][i].order_status !== 0){
        temarray.push(this.orderlistdata["data"][i])
      }
    }
    console.log("length of order list :",temarray);
    // isOrderList
    if(temarray.length > 0){
      this.orderlistdata["data"]=temarray
      this.getOrderDetailData(this.orderlistdata["data"][0].id, this.orderlistdata["data"][0].shipment_id, this.orderlistdata["data"][0].order_status,
                this.orderlistdata["data"][0].picker_name, this.orderlistdata["data"][0].substitute_status, this.userOrderdata.storename, this.userOrderdata.storecode)
    }else{
      this.orderlistdata["data"].length=0
      this.isOrderList=true
  
    }
   
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
      // console.log(data);
      // this.orderlistdata["data"] = data
      this.globalitem.showSuccess(data.message, "Success")
      // this.reloadpage()
      if(this.userOrderdata.orderlistType !== "new"){
        this.getOrderlistData()
      }else{
        this.getnewOrders()
      }
      
      // this.getOrderDetailData( this.userOrderdata.order_id,  this.userOrderdata.shipment_id,  this.userOrderdata.order_status,  this.userOrderdata.picker_name,  this.userOrderdata.substitute_status)
    })
  }

  getOrderDetailData(orderid: any, shipment_id: string, order_status: string, picker_name: any, substitute_status: any, storename: any, storecode: any) {
    // this.IsTimeComplete = ''
    // console.log("order id :", orderid, "shipment_id: ", shipment_id, " order_status: ", order_status, " picker_name: ", picker_name, " substitute_status: ", substitute_status);
    if(picker_name === undefined){
      this.userOrderdata.picker_name = null;
    }else{
      this.userOrderdata.picker_name = picker_name;
    }
   
    this.userOrderdata.order_id = orderid
    this.userOrderdata.order_status = order_status
    this.userOrderdata.shipment_id = shipment_id
    this.userOrderdata.substitute_status = substitute_status
    this.userOrderdata.storename = storename
    this.userOrderdata.storecode = storecode
    // console.log("store name : ", storename);

    let data = {
      website_id: this.userOrderdata.website_id,
      order_id: orderid,
    }
    this.userOrderdata.order_id_for_substitute_checking = this.orderlistdata["data"][0]?.id
    // console.log("order list data inside detail : ", this.orderlistdata["data"]);
    this.apiService.postData("picker-orderdetails/", data).subscribe((data: any) => {
      // console.log("order list data inside detail : ",this.orderlistdata);
      // console.log(data);

      let temdata: any = []
      temdata = data
      this.orderDetaildata["data"] = temdata.response
      this.product_billnumber=this.orderDetaildata['data'][0]?.channel_order_id
      this.paymentOnlineTime = this.datePipe.transform(this.orderDetaildata["data"][0]?.created, "MMM d, y, h:mm:ss a");
      this.currenttime = this.datePipe.transform(new Date(), "MMM d, y, h:mm:ss a");
      this.orderDetaildata['data'][0].time_slot_id=this.orderDetaildata['data'][0]?.time_slot_id.slice(-9)
      
      if (this.orderDetaildata["data"][0]?.order_substitute_products) {
        // console.log("entered in if ",this.orderDetaildata["data"]?.order_substitute_products);
        this.order_Substitute_Time = this.datePipe.transform(this.orderDetaildata["data"][0]?.order_substitute_products[0]?.created, "MMM d, y, h:mm:ss a")
        // console.log(" order_Substitute_Time ", this.order_Substitute_Time);
        //  this.leftTime= 0.6*60000
        // console.log("added 10 minutes to substitute  ", this.order_Substitute_Time + (30 * 60 * 1000));
        if (this.userOrderdata.substitute_status === 'pending') {
          this.timerProductSentApproval(this.order_Substitute_Time, 10)
        } else {
          this.paymentonlineTimer = true
        }
      }//payment id 2 for payment online 
      if (this.orderDetaildata["data"][0]?.payment_type_id === 2) {
        // console.log("timer");
        this.timerProductSentApproval(this.paymentOnlineTime, 30)
      }
      this.userOrderdata.shipment_id = this.orderDetaildata["data"][0].shipment_id
      this.userOrderdata.trent_picklist_id = this.orderDetaildata["data"][0].trent_picklist_id
      // if(this.userOrderdata.orderlistType !== 'complete'){
      //   this.userOrderdata.order_id_for_substitute_checking = this.orderlistdata['data'][0].id
      // }else{
      //   console.log("order llist data inside detail : ",this.orderlistdata["data"][0]);
      //   this.userOrderdata.order_id_for_substitute_checking = this.orderlistdata["data"][0]?.id
      // }

      if (this.userOrderdata.orderlistType === 'cancelled' || this.userOrderdata.orderlistType === 'complete' || this.userOrderdata.orderlistType === 'shipped') {
      } else {
        if(this.userOrderdata.orderlistType === "new"){
          this.getLatestOrder(this.userOrderdata.order_id_for_substitute_checking, 'insidePage')
        }
        
      }

      // let time: any = this.orderDetaildata['data'][0]?.order_activity[0]?.activity_date;
      this.getsubtitteStatus()
      // this.datetime = time.getTime()
      // console.log("Date Time : ", this.datetime);
      // this.addCustomVariable();

      this.gettotalCost()
    })
  }

  openmap(latlang: any) {
    console.log("latlang : ", latlang);
    // MapmodalComponent
    this.modalservice.openModal(latlang, MapmodalComponent)
  }

  printdata(skustatus: any, printstatus: any, pdfName: any) {
    this.isdownload = true
    var innerContents: any
    let templayout: any;
    if (skustatus === "withoutsku") {
      // templayout = document.getElementById("printwithOutsku")?.innerHTML;
      templayout = "printwithOutsku"
    } else {
      templayout = "printwithsku"
      // templayout = document.getElementById("printwithsku")?.innerHTML;
    }

    if (printstatus === "print") {
      const popupWinindow: any = window.open();
      popupWinindow.document.open();
      setTimeout(() => {
        innerContents = document.getElementById(templayout)?.innerHTML;
        popupWinindow.document.write('<html><head></head><body onload="window.print()">' + innerContents + '</html>');
        popupWinindow.document.write(`<style>
        .printdata{
          background: white;
          line-height: 2;
          // width: 50px !important;
        }
          .h6{
            font-size: 15px;
            font-weight: bolder;
            margin: 1% 0% 1% 0%;
          }
          .table1{
              line-height: normal;
              width:100%;
          }
          .th{
              text-align: inherit;
              background: white;
              color: black;
          } 
          .mat-divider{
              margin: 4px 0px 4px 0px;
              border: 1px solid #8a8484;
          }
          .printfooter{
              text-align: center;
              margin-top:4% !important;
              h6{
                font-size: 15px;
                margin: 2% 0% 2% 0%;
                font-weight: bolder;
              }
          }
          .leftcol{
              text-align: end;
              padding-right: 6% !important;
          }
          .rightcol{
            text-align: -webkit-right;
        }.sku{
          text-align:center;
        }
    
          @media print 
    {
       @page
       {
        size: 5.5in 8.5in ;
        size: portrait;
        margin:minimum;
        destination:pdf !important
      }
    }
    </style>
      `);
        // this.isdownload=false
        popupWinindow.document.close();
        this.isdownload = false;
      }, 20);

    } else {
      setTimeout(() => {
        innerContents = document.getElementById(templayout);
        this.commonfunc.generatePDF(innerContents,pdfName)
        this.isdownload = false
      }, 1600)
    }
  }
  //edit unit weight and price
  openEditModal(data: any) {
    let user_ids = {
      website_id: this.userOrderdata.website_id,
      user_id: this.userOrderdata.user_id,
      user_name: this.userOrderdata.picker_name,
      order_id: this.userOrderdata.order_id
    }
    Object.assign(data, user_ids)
    const dialogRef = this.dialog.open(EditproductweightComponent, { width: '500px', data: { data: data } });
    dialogRef.afterClosed().subscribe(result => {
      // console.log('The dialog was closed', result);
      this.getOrderDetailData(this.userOrderdata.order_id, this.userOrderdata.shipment_id, this.userOrderdata.order_status, this.userOrderdata.picker_name, this.userOrderdata.substitute_status, this.userOrderdata.storename, this.userOrderdata.storecode)
    });
  }

  //send product subtitution for approval
  sendProductSubtituteApproval(approvalProducst: any, bill_value: any, product_billnumber: any) {
    this.getcounter()
    let temarray = new Array()
    for (let i = 0; i < approvalProducst.length; i++) {
      temarray.push({ product_id: approvalProducst[i].product.id, order_product_id: approvalProducst[i].id })
    }
    // console.log("subtitue array : ", temarray);
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
          this.timerProductSentApproval(this.order_Substitute_Time, 10)
          this.getOrderDetailData(this.userOrderdata.order_id, this.userOrderdata.shipment_id, this.userOrderdata.order_status, this.userOrderdata.picker_name, this.userOrderdata.substitute_status, this.userOrderdata.storename, this.userOrderdata.storecode)
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

    const dialogRef = this.dialog.open(AddnewproductComponent, { width: '700px',height:"650px", data: { data: data } });
    dialogRef.afterClosed().subscribe(result => {
      // console.log('The dialog was closed', result);
      this.getOrderDetailData(this.userOrderdata.order_id, this.userOrderdata.shipment_id, this.userOrderdata.order_status, this.userOrderdata.picker_name, this.userOrderdata.substitute_status, this.userOrderdata.storename, this.userOrderdata.storecode)

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
  updateMoreProductQuantity(quantity: any, order_product_id: any, product_id: any, shortage: any, index: any) {
    // console.log("prouct Quantity ", quantity);
    // substitute_product_id:any,product_id:any
    // console.log("order product id 1: ", order_product_id, " product id 1: ", product_id);
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
      // console.log("updategrnquantity : ", data);
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
            this.updateMoreProductQuantity(templength, product_id, order_product_id, shortage, index)
          }
        } else if (productType === 2) {
          let templength = this.orderDetaildata['data'][0]?.order_products[i].shortage - 1
          if (templength < 0) {
            this.orderDetaildata["data"][0].order_products[i].shortage = 0;
            // this.updateMoreProductQuantity(quantity, product_id, order_product_id, shortage, index)
          } else {
            this.orderDetaildata["data"][0].order_products[i].shortage = templength;
            // console.log("shortage length", templength);
            this.updateMoreProductQuantity(templength, order_product_id, product_id, templength, index)
            // this.updateMoreProductQuantity(quantity, product_id, order_product_id, templength, index)
          }
          // this.openDialog(apiURL,sub_apiUrl, pageTitle, productid,productType)
        }
      }
    }
  }

  productIncrment(grn_quantity: any, product_id: any, order_product_id: any, shortage: any, index: any,
    apiURL: any, sub_apiUrl: any, pageTitle: any, productid: any, productType: any, ean: any) {
    // console.log("order product id : ", order_product_id, " product id : ", product_id);

    var modaldata = {
      shortage: shortage,
      grn_quantity: grn_quantity,
      product_id: product_id,
      order_product_id: order_product_id
    }
    for (var i = 0; i < this.orderDetaildata['data'][0]?.order_products.length; i++) {
      if (i === index) {
        if (productType === '') {
          if (this.orderDetaildata['data'][0]?.order_products[i].grn_quantity + this.orderDetaildata['data'][0]?.order_products[i].shortage < this.orderDetaildata['data'][0]?.order_products[i].quantity) {
            let templength = this.orderDetaildata['data'][0]?.order_products[i].grn_quantity + 1 //increment the quantity
            this.orderDetaildata["data"][0].order_products[i].grn_quantity = templength; //assaign quantity to input
            this.updateMoreProductQuantity(this.orderDetaildata["data"][0].order_products[index].grn_quantity, order_product_id, product_id, shortage, index)
          }
        } else if (productType === 2) {
          if (this.orderDetaildata['data'][0]?.order_products[i].grn_quantity + this.orderDetaildata['data'][0]?.order_products[i].shortage < this.orderDetaildata['data'][0]?.order_products[i].quantity) {
            let templength = this.orderDetaildata['data'][0]?.order_products[i].shortage + 1
            this.orderDetaildata["data"][0].order_products[i].shortage = templength;
            this.updateMoreProductQuantity(this.orderDetaildata["data"][0].order_products[index].grn_quantity, order_product_id, product_id, templength, index)
            this.openDialog(apiURL, sub_apiUrl, pageTitle, productid, productType, templength, modaldata, ean)
          }
        }
      }
    }
  }

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
  }

  PickernameModal(){
    
    let data = {
      website_id: this.userOrderdata.website_id,
      order_id: this.userOrderdata.order_id,
      user_id: this.userOrderdata.user_id,
      order_status: this.userOrderdata.order_status,
      shipment_id: this.userOrderdata.shipment_id,
    }
    const dialogRef = this.dialog.open(AssaignpickerComponent, {
      width: '500px',
      data: { data: data }
    });
    dialogRef.afterClosed().subscribe(result => {
      console.log('The dialog was closed', result);
      this.userOrderdata.picker_name = result.pickername
      this.userOrderdata.orderlistType="In-Processing"
    this.activeLink = this.navTablink[1];
      this.getOrderlistData()
    });
  }

  // to notfy customer using bell icon with badge
  declinedProduct() {
    let data = {
      website_id: this.userOrderdata.website_id,
      order_id: this.userOrderdata.order_id,
    }
    this.apiService.postData("picker-resetsendapproval/", data).subscribe((data: any) => {
      // console.log("updategrnquantity : ", data);
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
      // console.log("insidePage data : ", temData);
      temData = data
    } else if (reqestType === "outsidePage") {
      // console.log("outside data : ", temData);

      temData = orderData
    }
    this.apiService.postData("picker-latestorders/", temData).subscribe((data: any) => {
      // console.log("latestorders : ", data);
      this.appcom.setbadge(data.response.no_of_latest_order)
      this.db.setOrderIDS(temData)
    })
  }
  updatePrice(order_amount: any, unitweight: any, netAmount: any, productinfo: any, URL: any, pricestatus: any) {
    // console.log("order mount : ", order_amount);
    if (order_amount === null) {
      order_amount = netAmount
    }

    let data = {
      website_id: this.userOrderdata.website_id,
      order_id: this.userOrderdata.order_id,
      user_id: this.userOrderdata.user_id,
      order_amount: order_amount,
      user_name: this.userOrderdata.picker_name,
      productinfo: productinfo,
      URL: URL,
      pricestatus: pricestatus,
      unitweight: unitweight
    }
    const dialogRef = this.dialog.open(EditpriceComponent, {
      width: '500px',
      data: { data: data }
    });
    dialogRef.afterClosed().subscribe(result => {
      // console.log('The dialog was closed', result);
      this.price = result.price
      this.getOrderDetailData(this.userOrderdata.order_id, this.userOrderdata.shipment_id, this.userOrderdata.order_status, this.userOrderdata.picker_name, this.userOrderdata.substitute_status, this.userOrderdata.storename, this.userOrderdata.storecode)
    });
  }

  //update detail order data with time
  timeChangeHandler(event: any, starttime: any) {
    this.datetime = event
    console.log("date Event : ", this.datetime)
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
        this.getOrderDetailData(this.userOrderdata.order_id, this.userOrderdata.shipment_id, this.userOrderdata.order_status, this.userOrderdata.picker_name, this.userOrderdata.substitute_status, this.userOrderdata.storename, this.userOrderdata.storecode)
        this.gettotalCost()
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
        // console.log("true");
        this.IS_Subtitute = false
      }
    }
    if (this.orderDetaildata['data'][0]?.order_substitute_products.length === 0) {
      this.IS_Subtitute = true
    }
  }
  handleEvent(event: any) {
    // console.log("event occur : ", event);
    if (event.action === "done") {
      this.IsTimeComplete = false
      this.isProductSendFor_Approval = true
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
    // console.log("timer started");
    this.db.getNotificationTime().then(res => {
      // console.log("user timer : ", res);
      this.subscription = timer(0, res).pipe(
        switchMap(async () => {
          this.db.getOrderIDS().then(res => {
            // console.log(" Type : ", this.userOrderdata.orderlistType);
            if (this.userOrderdata.orderlistType === 'cancelled' || this.userOrderdata.orderlistType === 'shipped' || this.userOrderdata.orderlistType === 'complete') {
              this.appcom.setbadge(0)
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

  ApprovalTimer(timeValue: any) {
    this.isTimerStart = true
    this.userOrderdata.substitute_status = "pending"
    this.subscription = timer(0, timeValue).pipe(
      switchMap(async () => {
        this.getOrderlistData()
        this.getOrderDetailData(this.userOrderdata.order_id, this.userOrderdata.shipment_id, this.userOrderdata.order_status, this.userOrderdata.picker_name, this.userOrderdata.substitute_status, this.userOrderdata.storename, this.userOrderdata.storecode)
        if (this.userOrderdata.substitute_status === "none") {
          this.isProductSendFor_Approval = true
        }
      })
    ).subscribe(result => {
      // console.log("timer started");
    })
  }

  //timer for sent product approval
  timerProductSentApproval(productTime: any, totaltime: any) {
    const originalDate = new Date(productTime);
    const modifiedTime: any = this.datePipe.transform(new Date(originalDate.valueOf() + (totaltime * 60000)), "MMM d, y, h:mm:ss a")
    // const subst_modifiedTime:any = this.datePipe.transform(new Date(originalDate.valueOf() + (2 * 60000)),"MMM d, y, h:mm:ss a")
    // console.log(" modifiedTime ", modifiedTime, " currenttime : ", this.currenttime);
    this.leftTime = Date.parse(modifiedTime) - Date.parse(this.currenttime)
    //assaign difference to timer between subs time and current time
    let milisecond = Date.parse(modifiedTime) - Date.parse(this.currenttime) //when subs product sent for a approval, thne time will start for ten minutes
    var seconds: any = (milisecond / 1000).toFixed(0);
    this.leftTime = Math.floor(seconds / 60) * 60000 / 900;
    if (Date.parse(modifiedTime) > Date.parse(this.currenttime)) {
      this.paymentonlineTimer = false
      // console.log("timer is greater false");
      if (this.userOrderdata.substitute_status === "none") {
        this.isProductSendFor_Approval = true
      } else if (this.userOrderdata.substitute_status === "pending") {
        this.isProductSendFor_Approval = false
      }
    } else {
      this.paymentonlineTimer = true
      this.isProductSendFor_Approval = true
      this.IsTimeComplete = false
      // console.log("timer is less than true");
    }
  }
  //unsubscribe timer
  destroyCounter() {
    this.subscription.unsubscribe();
  }

  //show confirmation dialog
  openConfirmationDialog(): void {
    let binddatawithHtml: any = '<div class="confirmationdlg"><strong>Total Product Value = ' + this.orderDetaildata["data"][0]?.currency_code + ' ' + this.orderDetaildata["data"][0]?.gross_amount + '</strong><br>' +
      '<strong>Shipping Charge = ' + this.orderDetaildata["data"][0]?.currency_code + ' ' + this.orderDetaildata["data"][0]?.shipping_cost + '</strong><br>' +
      '<strong>Bill Number = ' + this.billnumber.nativeElement.value + '</strong> <br><strong>Confirm?</strong>' +
      '</div>'
    let data = {
      pagestatus: 'order',
      info: binddatawithHtml
    }
    const dialogRef = this.dialog.open(AddproductasSubtituteComponent, {
      width: '500px',
      data: { data: data }
    });

    dialogRef.afterClosed().subscribe(result => {
      // console.log('The dialog was closed', result);
      if (result.data === undefined) {
        // this.subcategory = result.data;
      } else if (result.data === "none") {
        this.getcounter()
        let data1 = {
          website_id: this.userOrderdata.website_id,
          warehouse_id: this.userOrderdata.warehouse_id,
          order_id: this.userOrderdata.order_id,
          user_id: this.userOrderdata.user_id,
          shipment_id: this.userOrderdata.shipment_id,
          trent_picklist_id: this.userOrderdata.trent_picklist_id,
        }
        // console.log("Total counter : ", this.userOrderdata.PickerCounter);
        this.apiService.postData("picker-grn-complete/", data1).subscribe((data: any[]) => {
          // console.log("picker-grn-complete : ", data);
          let tempdata: any = data
          if (tempdata.status === 1) {
            this.globalitem.showSuccess(tempdata.message, "Order Placed")
            this.reloadpage()
          } else {
            this.globalitem.showError(tempdata.message, "Wait for 30 min")
          }
        })
      } else {
        // console.log("modal closed");
      }
    });
  }

  downloadCSV(orderproducts: any) {
    console.log("order produts list : ", orderproducts);
    let counter = 0
    let temarray: any = []
    for (let i = 0; i < orderproducts.length; i++) {
      let data = {
        'Product Name': orderproducts[i].product.name,
        'SKU': orderproducts[i].product.sku,
        'Unit Weight': orderproducts[i].weight * orderproducts[i]?.quantity / orderproducts[i]?.quantity + " " + orderproducts[i].product.uom.uom_name,
        'Unit Price': orderproducts[i].product_price,
        'Quantity': orderproducts[i].quantity,
      }
      counter++
      temarray.push(data)
      // console.log("Index: ", counter);
      if (orderproducts.length === counter) {
        // console.log("CSV file : ", temarray, orderproducts.length, i)
        let paramdata: any = ['Product Name', 'SKU', 'Unit Weight', 'Unit Price', 'Quantity',]
        this.commonfunc.downloadFile(temarray, "Picker order products", paramdata, 'footerdata')
      }
    }
  }
  conertvaluetodecimal(value: any): any {
    return this.commonfunc.precise_round(value, 0)
  }

  //get completed orders list
  getCompletedOrders() {
    var today = new Date();
    let data = {
      advanced_search: [{
        comparer: 1,
        field: "order_status",
        field_id: 76,
        input_type: "multi_select",
        key: [this.keyValueOF_superStore.key],
        key2: this.keyValueOF_superStore.value,
        name: "order_status",
        show_name: "Order Status",
      }],
      warehouse_id: this.userOrderdata.warehouse_id,
      date: "2020-03-27##" + today.getFullYear() + "-" + String(today.getMonth() + 1).padStart(2, '0') + "-" + String(today.getDate()).padStart(2, '0'),
      website_id: this.userOrderdata.website_id,
      per_page: 500,
      // page :1,
      model: "EngageboostOrdermaster",
      order_by: "",
      order_type: "",
      screen_name: "list",
      search: "",
      status: "",
      userid: this.userOrderdata.user_id,
      warehouse_status: "",
    }
    this.apiService.postData("global_list/", data).subscribe((data: any) => {
      if (data.count > 0) {
        this.orderlistdata["data"] = data.results[0].result //json response
        this.totalProductpage = data.per_page_count//total page
        this.getOrderDetailData(this.orderlistdata["data"][0].id, this.orderlistdata["data"][0].shipment_id, this.orderlistdata["data"][0].order_status,
          this.orderlistdata["data"][0].picker_name, "done", this.orderlistdata["data"][0].assign_wh_name, 123)
        if (this.currentPage === 1) {
          this.orderlistdata["data"] = data.results[0].result
          this.totalProductpage = data.total_page
        } else {
          // console.log("page n");
          this.orderlistdata["data"] = [...  this.orderlistdata["data"], ...data.results[0].result];
        }
      } else {
        this.isOrderList = true
        this.orderlistdata["data"] = []
      }
    })
  }

  //totalcost for print
  gettotalCost() {
    this.totalProductItems = 0;
    this.printerTotalcost = 0
    let tempcost: any = 0
    let tempproductitem: any = 0
    this.db.getwarehouseName().then(res => { this.userOrderdata.warehouseName = res });
    for (let i = 0; i < this.orderDetaildata['data'][0]?.order_products.length; i++) {
      this.totalProductItems += this.orderDetaildata['data'][0]?.order_products[i]?.quantity
      this.printerTotalcost += this.orderDetaildata['data'][0]?.order_products[i]?.product_price * this.orderDetaildata['data'][0]?.order_products[i]?.quantity;
    }
    for (let i = 0; i < this.orderDetaildata['data'][0]?.order_substitute_products.length; i++) {
      tempproductitem += this.orderDetaildata['data'][0]?.order_substitute_products[i]?.quantity
      tempcost += this.orderDetaildata['data'][0]?.order_substitute_products[i]?.product_price * this.orderDetaildata['data'][0]?.order_substitute_products[i]?.quantity;
    }
    this.totalProductItems += tempproductitem
    this.printerTotalcost += tempcost
  }

 //get new orders
 getnewOrders(){
  this.db.getUserData().then(res => {
    this.userOrderdata.warehouse_id = res.warehouse_id
    this.userOrderdata.website_id = res.website_id
    this.userOrderdata.user_id = res.user_id
 
  let data={
    advanced_search: [{
      comparer: 1,
      field: "order_status",
      field_id: 76,
      input_type: "multi_select",
      key: [0],
      key2: "Pending",
      name: "order_status",
      show_name: "Order Status",
    }
    ],
    model: "EngageboostOrdermaster",
    screen_name: "list",
    userid: this.userOrderdata.user_id,
    warehouse_id: this.userOrderdata.warehouse_id,
    website_id: this.userOrderdata.website_id
  }
  this.apiService.postData("global_list/", data).subscribe((data: any) => {
    this.orderlistdata["data"]=data.results[0].result
    // console.log("order list data : ",this.orderlistdata["data"]);
    if(data.results[0].result.length > 0){
      this.getOrderDetailData(this.orderlistdata["data"][0].id, this.orderlistdata["data"][0].shipment_id, this.orderlistdata["data"][0].order_status,
      this.orderlistdata["data"][0].picker_name, this.orderlistdata["data"][0].substitute_status, this.userOrderdata.storename, this.userOrderdata.storecode)
      // this.getLatestOrder(this.userOrderdata.order_id_for_substitute_checking, 'insidePage')
    }else{
      this.orderlistdata["data"]=[]
      this.isOrderList=true
    }
   
  })
})
}
}