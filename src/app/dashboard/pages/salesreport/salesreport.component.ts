import { DatePipe } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { ThemePalette } from '@angular/material/core';
// import { Workbook } from 'exceljs';
import { CommonfunctionService } from 'src/app/core/utilities/commonfunction.service';
import { ApiService } from 'src/app/services/api/api.service';
import { DatabaseService } from 'src/app/services/database/database.service';
import { GlobalitemService } from 'src/app/services/globalitem/globalitem.service';
import { OrdersComponent } from '../orders/orders.component';
// import * as monthname from '../../../core/utilities/monthname/monthname.json';

export interface PaymentMethodInter {
  name: string;
  completed: boolean;
  id: any;
  type: any
  color: ThemePalette;
  subtasks?: PaymentMethodInter[];
}
export interface product {
  id: number
  name: string
  brand: string
  color: string
  price: number
}

@Component({
  selector: 'app-salesreport',
  templateUrl: './salesreport.component.html',
  styleUrls: ['./salesreport.component.scss']
})
export class SalesreportComponent implements OnInit {
  picker: any
  panelOpenState = false;
  monthname: any;
  completelist: any = []
  pageurl: any = '/'
  lastdate: any = "";
  currentpage: any = 1
  getmonth: any = "1"
  getyear: any = "2020";
  saleData = {
    totalorder: 0,
    shippingcost: 0,
    coupendiscount:0,
    shippingDiscount:0,
    subtotal: 0,
    grandtotal: 0,
    testorders:0
  }
  advancedsearch: any = []
  generalcounter: any = 0
  paymentmethodid: any = 'both'
  paymentmethodlastids: any;
  paymentmultyids: any = new Array;
  paymentmethodname: any = ''
  rangeFormGroup = new FormGroup({
    start: new FormControl(null, Validators.required),
    end: new FormControl(null, Validators.required),
  })
  primarycolor: any = "#007bff"
  paymentmethod: PaymentMethodInter = {
    name: 'Online Payment/Cash Payment',
    type: "Select All",
    completed: false,
    color: this.primarycolor,
    id: 'both',
    subtasks: [
      { name: 'Cash On Delivery', id: 16, type: "Cash On Delivery", completed: true, color: 'primary' },
      { name: 'Card On Delivery', id: 59, type: "Cash On Delivery", completed: true, color: 'primary' },
      { name: 'Online Payment', type: "Online Payment", id: 51, completed: true, color: 'primary' },
    ]
  };
  allComplete: boolean = false;
  averageData:any=[]

  //merging data for multi selection payment method
  orderlistsaleData: any = []
  // orderlistsaleMergrray:any=new Array()
  mergeFirstPaymentData: any = new Array()
  IsMerge = false;


  constructor(public apiService: ApiService, public commonfunc: CommonfunctionService,
    public datePipe: DatePipe,
    public globalitem: GlobalitemService,
    public db: DatabaseService) {
    this.monthname = this.commonfunc.monthname;
    this.lastdate = this.getyear + "-" + this.getmonth + "-" + 1 + "##" + this.getyear + "-" + this.getmonth + "-" + this.getDaysInMonth(12, this.getyear)

  }

  ngOnInit(): void {
    this.setcompleteparam()
    this.getCancellationandCompleteRate()
    this.setfieldEmpty()
    this.getOrderlistData(this.lastdate)

  }
  datemodal() {
   
  }

  setcompleteparam() {
    this.advancedsearch.push({
      comparer: 1,
      field: "order_status",
      field_id: 76,
      input_type: "multi_select",
      key: [4],
      key2: "Completed",
      name: "order_status",
      show_name: "Order Status",
    })
  }
  setfieldEmpty() {
    this.completelist["data"] = []
    // this.completelist["data"]["totalorder"] =0
    //   this.completelist["data"]["shippingcost"] =0
    // this.completelist["data"]["subtotal"] = 0
    // this.completelist["data"]["grandtotal"] = 0
  }

  getCancellationandCompleteRate(){
    this.db.getcancellationRate().then(res => {
      // console.log("cancellation report : ",res);
      this.averageData=res
    });
  }
  getOrderlistData(date: any) {
    // console.log("advanced search : ", this.advancedsearch);
    // console.log("before ids :", this.paymentmethodlastids);
    this.setfieldEmpty()
    this.db.getUserData().then(res => {
      // console.log("payment method ID : ", this.rangeFormGroup.controls.paymentmethodid.value);
      let data = {
        advanced_search: this.advancedsearch,
        warehouse_id: res.warehouse_id,
        website_id: res.website_id,
        per_page: 500,
        // page :1,
        user_id: res.user_id,
        date: date,
        model: "EngageboostOrdermaster",
        order_by: "",
        // order_status:4,
        order_type: "",
        screen_name: "list",
        search: "",
        status: "",
        userid: res.user_id,
        warehouse_status: "",
      }
      this.apiService.postData("global_list" + this.pageurl, data).subscribe((data: any) => {
        this.advancedsearch = []
        this.setcompleteparam()
        if (data.results[0].result) {
          let incomingdata:any;
          if (data.count > this.generalcounter) {
            incomingdata = this.commonfunc.getcompletedOrders(data.results[0].result, this.paymentmethodid)
            this.orderlistsaleData = [... this.orderlistsaleData, ...data.results[0].result]
            this.saleData.grandtotal += parseFloat(this.commonfunc.precise_round(incomingdata.grandtotal, 2))
            this.saleData.shippingcost += parseFloat(this.commonfunc.precise_round(incomingdata.shpcost, 2))
            this.saleData.subtotal += parseFloat(this.commonfunc.precise_round(incomingdata.subtotal, 2))
            this.saleData.coupendiscount += parseFloat(this.commonfunc.precise_round(incomingdata.coupendiscount, 2))
            this.saleData.shippingDiscount += parseFloat(this.commonfunc.precise_round(incomingdata.shippingdiscount, 2))
            this.saleData.testorders += incomingdata.testorderFound
            this.generalcounter += data.results[0].result.length
            if (this.currentpage > data.per_page_count) {
              this.currentpage = data.per_page_count
            } else if (data.per_page_count > this.currentpage) {
              this.currentpage++
              // console.log("current page : ",this.currentpage +" list page :",data.per_page_count);
              this.pageurl = "/?page=" + this.currentpage
              this.getOrderlistData(this.lastdate)
            }
          } if (this.currentpage > data.per_page_count) {
            this.currentpage = data.per_page_count
          } if (data.count === this.generalcounter) {
            // console.log("this.saleData:", this.saleData ," and test oreders : ",incomingdata.testorderFound);
            // console.log("test orders : ",incomingdata);
            //for test order removing we used testorderfound
            if(incomingdata?.testorderFound === undefined){

            }else{
              this.saleData.totalorder = data.count - this.saleData.testorders
              // this.saleData.testorders=incomingdata.testorderFound
            }

            this.completelist["data"]["currency_code"] = data?.results[0]?.result[0]?.currency_code
            //for multi selection checkbox, after getting data we set paymentmethodlastids value to undefined and calculate orders
            // console.log("paymentmethodlastids ",this.paymentmethodlastids);
            if (this.paymentmethodlastids === undefined) {
              // console.log("mergeFirstPaymentData ",this.mergeFirstPaymentData);
              
              if (this.mergeFirstPaymentData.length !== 0) {
                // console.log(" mergeFirstPaymentData enterd");
                
                this.saleData.totalorder += this.mergeFirstPaymentData.totalorder
                this.saleData.shippingcost += this.mergeFirstPaymentData.shippingcost
                this.saleData.subtotal += this.mergeFirstPaymentData.subtotal
                this.saleData.grandtotal += this.mergeFirstPaymentData.grandtotal
                this.mergeFirstPaymentData = []
                // console.log("subtotal : ", this.saleData.subtotal);
              }
            }//for first time ,if we have ids then we pass second ids and get again sale list and merg with old sale data
            if (this.paymentmethodlastids !== undefined) {
              // this.orderlistsaleMergrray['data']=data.results[0].result
              let tempdata = {
                totalorder: this.saleData.totalorder,
                shippingcost: this.saleData.shippingcost,
                subtotal: this.saleData.subtotal,
                grandtotal: this.saleData.grandtotal
              }
              // console.log("amounts are : ",tempdata);
              this.mergeFirstPaymentData = tempdata//merge data with old and set new value for ids
              if (this.paymentmethodlastids) {
                this.generalcounter = 0
                // this.mergeFirstPaymentData=[]
                this.advancedsearch = []
                this.setcompleteparam()
                this.advancedsearch.push({
                  comparer: 1,
                  field: "payment_method_id",
                  field_id: 73,
                  input_type: "select",
                  key: this.paymentmethodlastids,
                  key2: this.paymentmethodname,
                  name: "payment_method_id",
                  show_name: "Payment Method"
                })
                this.paymentmethodlastids = undefined
                this.getOrderlistData(this.lastdate)
              }
            }
          }
        } if (data.results[0].result.length === 0 || data.results[0].result === []) {
          // console.log("else is executed");
          this.saleData.totalorder=0
          this.setfieldvalue()
        }

      })
    })
  }

  //set filed value
  setfieldvalue() {
    // this.completelist["data"].length = 0
    this.saleData.totalorder=0
    this.saleData.testorders=0
    this.completelist['data']['currency_code'] = '0.'
    this.saleData.grandtotal = parseFloat('00')
    this.saleData.shippingcost = parseFloat('00')
    this.saleData.subtotal = parseFloat('00')
    this.generalcounter = parseFloat('00')
    this.saleData.shippingDiscount = parseFloat('00')
    this.saleData.coupendiscount = parseFloat('00')
  }
  //search orders on the base of selected date ,month,year ,date range and payment method
  Searchorders() {
    this.pageurl = '/'
    this.setfieldvalue()
    this.currentpage = 1

    this.orderlistsaleData = []
    // console.log("payment method id: ",this.paymentmethodid);
    
    if (this.paymentmethodid !== "both") {
      let temparray: any = this.paymentmethod.subtasks
      let secondtemarray: any = []
      // console.log("paymentmethod ids: ", this.paymentmethod.subtasks, temparray);
      this.advancedsearch = []
      this.setcompleteparam()
      for (let i = 0; i < temparray.length; i++) {
        if (temparray[i].completed === true) {
          secondtemarray.push(temparray[i])
          // console.log("paymentmethod ids true", secondtemarray);

          if (secondtemarray[1]) {
            this.paymentmethodlastids = secondtemarray[1].id
            this.paymentmethodname = secondtemarray[1].name
            // console.log("last payment ids :", this.paymentmethodlastids);
          } else if (secondtemarray[0]) {
            this.advancedsearch.push({
              comparer: 1,
              field: "payment_method_id",
              field_id: 73,
              input_type: "select",
              key: secondtemarray[0].id,
              key2: secondtemarray[0].name,
              name: "payment_method_id",
              show_name: "Payment Method"
            })
          }
        }
      }
    }
    if (this.rangeFormGroup.value.start !== null && this.rangeFormGroup.value.end !== null) {
      this.getmonth = "nomonth"
      this.getyear = "2020";
      this.lastdate = this.datePipe.transform(this.rangeFormGroup.value.start, "yyyy-M-d") + "##" + this.datePipe.transform(this.rangeFormGroup.value.end, "yyyy-M-d");
    } else if (this.getmonth === 'nomonth') {
      this.lastdate = this.getyear + "-" + 1 + "-" + 1 + "##" + this.getyear + "-" + 12 + "-" + this.getDaysInMonth(12, this.getyear)
    } else {
      // console.log("else part ");
      this.lastdate = this.getyear + "-" + this.getmonth + "-" + 1 + "##" + this.getyear + "-" + this.getmonth + "-" + this.getDaysInMonth(this.getmonth, this.getyear)
    }
    this.getOrderlistData(this.lastdate)
  }

  setSearchattribute(eventValue: any, status: any) {
    this.rangeFormGroup.controls.start.setValue(null);
    this.rangeFormGroup.controls.end.setValue(null);
    // this.rangeFormGroup.controls.paymentmethodid.setValue(eventValue?.target?.value)
    if (status === 'month') {
      this.getmonth = eventValue?.target?.value
    } else {
      this.getyear = eventValue?.target?.value
    }
  }

  getDaysInMonth = function (month: any, year: any) {
    return new Date(year, month, 0).getDate();
  };

  // download csv file
  getCSVFile() {
    // console.log(" data : ",this.completelist["data"]["subtotal"] ,this.completelist["data"]["grandtotal"]);
    let temarray: any = [] 
    console.log("this.saleData.shippingDiscount : ",this.saleData.shippingDiscount);
       
    let data1: any = {
      'Total Orders': this.saleData.totalorder,
      'Subtotal': this.saleData.subtotal,
      'Shipping Costs': this.saleData.shippingcost,
      'Shipping Discount': this.saleData.shippingDiscount,
      'Coupon Discount': this.saleData.coupendiscount,
      'Grand Total': this.saleData.grandtotal + " " + this.completelist['data']['currency_code'],
      'Cancel Rate':this.commonfunc.precise_round(this.averageData?.cancelledorders/(this.averageData?.cancelledorders + this.saleData.totalorder)*100, 1)+"%",
      'Average Value':this.commonfunc.precise_round(this.saleData.grandtotal/this.saleData.totalorder,3)
    }

    if (this.saleData.totalorder !== 0) {
      let paramdata = ['Total Orders', 'Subtotal', 'Shipping Costs','Shipping Discount','Coupon Discount', 'Grand Total','Cancel Rate','Average Value']
      // console.log("csv file : ", paramdata);
      temarray.push(data1)
      this.commonfunc.downloadFile(temarray, 'sales report', paramdata, 'footerdata')
    } else {
      this.globalitem.showError("Orders not found ", "no Orders")
    }
  }

  cleardatefield() {
    this.rangeFormGroup.controls.start.setValue(null);
    this.rangeFormGroup.controls.end.setValue(null);
    const d = new Date();
    // alert(d.getMonth()+1);
    this.getmonth = d.getMonth() + 1
    this.lastdate = this.getyear + "-" + this.getmonth + "-" + 1 + "##" + this.getyear + "-" + this.getmonth + "-" + this.getDaysInMonth(this.getmonth, this.getyear)
    this.Searchorders()
  }

  //checkbox
  updateAllComplete() {
    this.allComplete = this.paymentmethod.subtasks != null && this.paymentmethod.subtasks.every(t => t.completed);
    if (this.allComplete) {
      // console.log("all true");
      this.advancedsearch = []
      this.setcompleteparam()
      this.paymentmethodid =  this.paymentmethod.id;
      this.paymentmethodname = this.paymentmethod.name;
    } else if (!this.allComplete) {
      this.paymentmethodid =  this.paymentmethod.id;
      this.advancedsearch = []
      this.setcompleteparam()
      // console.log("not complete",this.paymentmethodid ,this.allComplete);
    }
    // console.log("not complete",this.paymentmethodid ,this.allComplete);
    // console.log("updateAll Complete : ",this.allComplete);
  }

  someComplete(): boolean {
    // console.log("some completed : ");
    if (this.paymentmethod.subtasks == null) {
      return false;
    }
    let counter = 0
    if (this.paymentmethod.subtasks.filter(t => t.completed).length > 0 && !this.allComplete) {
      for (var i = 0; i < this.paymentmethod.subtasks.length; i++) {
        if (this.paymentmethod.subtasks[i].completed === true) {
          counter++;
          this.paymentmethodid = this.paymentmethod.subtasks[i].id
          this.paymentmultyids.push(this.paymentmethod.subtasks[i].id)
          this.paymentmethodname = this.paymentmethod.subtasks[i].name
          if(counter === this.paymentmethod.subtasks.length){
            this.paymentmethodid=this.paymentmethod.id
          }
          // console.log("id : ",this.paymentmethod.subtasks[i].id);
          // console.log("counter value ",counter);
          // console.log("some  complete ",this.paymentmethodid);
        } else {
          // console.log("some not complete ",this.paymentmethodid);
          // this.paymentmethodid=this.paymentmethod.id
          // this.advancedsearch=[]
          // this.setcompleteparam()

        }
      }
    } else if (this.paymentmethod.subtasks.filter(t => t.completed).length === 0 && !this.allComplete) {
      // console.log("not all completed", this.paymentmethod.subtasks);
      this.advancedsearch = []
      this.setcompleteparam()
    }

    return this.paymentmethod.subtasks.filter(t => t.completed).length > 0 && !this.allComplete;
  }

  setAll(completed: boolean) {
    this.paymentmethodid = this.paymentmethod.id
    this.paymentmethodname = this.paymentmethod.name
    // console.log("method complete : ",this.paymentmethodid);

    this.allComplete = completed;
    // console.log("setAll : ",this.allComplete);
    if (this.allComplete === false) {
      this.advancedsearch = []
      this.setcompleteparam()
    }
    if (this.paymentmethod.subtasks == null) {
      return;
    }
    this.paymentmethod.subtasks.forEach(t => t.completed = completed);
  }

  //generate sale report
  generateSaleReport() {
    // console.log("order list :", this.orderlistsaleData);
    let counter = 0
    let diff :any
    //set footer with total charges
    let footerdata = {
      Subtotal: 0,
      ShippingCost: 0,
      ShippingDiscount: 0,
      OtherDiscount: 0,
      GrandTotal: 0
    }
    let temarray: any = []
    for (let i = 0; i < this.orderlistsaleData.length; i++) {
      if(!this.orderlistsaleData[i].customer?.first_name?.includes("Test") && !this.orderlistsaleData[i]?.customer?.first_name?.includes("test")&&
      !this.orderlistsaleData[i]?.customer?.last_name?.includes("Test") && !this.orderlistsaleData[i]?.customer?.last_name?.includes("test")){
      footerdata.Subtotal += this.orderlistsaleData[i].net_amount
      footerdata.ShippingCost += this.orderlistsaleData[i].shipping_cost
      footerdata.ShippingDiscount += this.orderlistsaleData[i].cart_discount
      footerdata.OtherDiscount += this.orderlistsaleData[i].gross_discount_amount
      footerdata.GrandTotal += this.orderlistsaleData[i].gross_amount
      let data: any = {
        'Order Number': this.orderlistsaleData[i].custom_order_id,
        'Order Date': this.datePipe.transform(this.orderlistsaleData[i].created, "yyyy-M-d"),
        'Customer Name': this.orderlistsaleData[i].customer.first_name + " " + this.orderlistsaleData[i].customer.last_name,
        // 'Prepared By':this.orderlistsaleData[i].assign_to,
        // 'Bill Number': this.orderlistsaleData[i].custom_order_id,
        'Payment Method': this.orderlistsaleData[i].payment_method_name,
        'Subtotal': this.orderlistsaleData[i].net_amount,
        'Shipping Cost': this.orderlistsaleData[i].shipping_cost,
        'Shipping Discount': this.orderlistsaleData[i].cart_discount,
        'Other Discount': this.orderlistsaleData[i].gross_discount_amount,
        'Grand Total': this.orderlistsaleData[i].gross_amount,
      }
      // let averagevalue = totalamount/total OrdersComponent
      //cancellation average  cancellation value /total oredsr * 100 will be in percentage
       counter++
      temarray.push(data)
      // console.log("Index: ", counter,this.saleData.testorders);
     
    } if (this.orderlistsaleData.length  === counter + this.saleData.testorders) {
      // console.log("CSV file : ", temarray, this.orderlistsaleData.length, i)
      let paramdata: any = ['Order Number', 'Order Date', 'Customer Name', 'Payment Method', 'Subtotal', 'Shipping Cost', 'Shipping Discount', 'Other Discount', 'Grand Total']
      this.commonfunc.downloadFile(temarray, "order products", paramdata, footerdata)
    }else{
      console.log("else is executed" ,this.orderlistsaleData.length ," others ",counter + this.saleData.testorders, " testorders : ",this.saleData.testorders);
      
    }
  }}
}
