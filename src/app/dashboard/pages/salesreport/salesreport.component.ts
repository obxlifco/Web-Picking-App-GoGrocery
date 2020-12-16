import { DatePipe } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { ThemePalette } from '@angular/material/core';
import { CommonfunctionService } from 'src/app/core/utilities/commonfunction.service';
import { ApiService } from 'src/app/services/api/api.service';
import { DatabaseService } from 'src/app/services/database/database.service';
import { GlobalitemService } from 'src/app/services/globalitem/globalitem.service';
// import * as monthname from '../../../core/utilities/monthname/monthname.json';

export interface PaymentMethodInter {
  name: string;
  completed: boolean;
  id:any;
  type:any
  color: ThemePalette;
  subtasks?: PaymentMethodInter[];
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
  saleData={
    totalorder:0,
    shippingcost:0,
    subtotal:0,
    grandtotal:0
  }
  advancedsearch:any=[]
  generalcounter:any=0
  paymentmethodid:any='both'
  paymentmultyids:any= new Array;
  paymentmethodname:any=''
  rangeFormGroup = new FormGroup({  
    start: new FormControl(null, Validators.required),  
    end: new FormControl(null, Validators.required),
  })  
 primarycolor:any="#007bff"
  paymentmethod: PaymentMethodInter = {
    name: 'Online Payment/Cash Payment',
    type:"Select All",
    completed: false,
    color: this.primarycolor,
    id:'both',
    subtasks: [
      {name: 'Cash On Delivery',id:16,type:"Cash On Delivery", completed: false, color: 'primary'},
      {name: 'Card On Delivery',id:59,type:"Cash On Delivery", completed: false, color: 'primary'},
      {name: 'Online Payment',type:"Online Payment",id:51, completed: false, color: 'primary'},
    ]
  };
  allComplete: boolean = false;

  
  constructor(public apiService: ApiService, public commonfunc: CommonfunctionService,
    public datePipe: DatePipe,
    public globalitem: GlobalitemService,
    public db: DatabaseService) {
      this.monthname=this.commonfunc.monthname;
      this.lastdate = this.getyear + "-" + this.getmonth + "-" + 1 + "##" + this.getyear + "-" + this.getmonth + "-" + this.getDaysInMonth(12, this.getyear)
      setTimeout(() => {
        // this.getpaymentmethodlist()
      }, 1500);
    }

  ngOnInit(): void {
    this.setfieldEmpty()
    this.getOrderlistData(this.lastdate)
  
  }
  datemodal() {

  }
 
  setcompleteparam(){
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

  getOrderlistData(date: any) {
    console.log("advanced search : ",this.advancedsearch);
    this.setfieldEmpty()
    this.db.getUserData().then(res => {
      // console.log("payment method ID : ", this.rangeFormGroup.controls.paymentmethodid.value);
      let data = {
        advanced_search:this.advancedsearch,
        warehouse_id:  '',
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
        this.advancedsearch=[]
        this.setcompleteparam()
        if (data.results[0].result) {
          if (data.count > this.generalcounter) {
            let incomingdata = this.commonfunc.getcompletedOrders(data.results[0].result,this.paymentmethodid)
            this.saleData.grandtotal =parseFloat(this.commonfunc.precise_round(incomingdata.grandtotal, 2)) 
            this.saleData.shippingcost += parseFloat(this.commonfunc.precise_round(incomingdata.shpcost, 2))
            this.saleData.subtotal += parseFloat(this.commonfunc.precise_round(incomingdata.subtotal, 2))
            this.generalcounter +=data.results[0].result.length
            // console.log("total price : ", this.completelist["data"]["grandtotal"]);

            if(this.currentpage > data.per_page_count){
              this.currentpage=data.per_page_count
            }else if(data.per_page_count > this.currentpage){
              this.currentpage++
              this.pageurl = "/?page=" + this.currentpage
              this.getOrderlistData(this.lastdate)
            }           
          }if(this.currentpage > data.per_page_count){
              this.currentpage=data.per_page_count
            }if(data.count === this.generalcounter) {  
            // console.log("true");/
            this.saleData.totalorder =data.count        
            this.completelist["data"]["currency_code"] = data?.results[0]?.result[0]?.currency_code
          }
        } if (data.results[0].result.length === 0 || data.results[0].result === []) {
          // console.log("else is executed");
          this.setfieldvalue()
        }
      })
    })
  }

  //set value to 0.00
  setfieldvalue() {
    // this.completelist["data"].length = 0
    this.completelist['data']['currency_code']='0.'
    this.saleData.grandtotal =parseFloat('00') 
    this.saleData.shippingcost =parseFloat('00')
    this.saleData.subtotal =parseFloat('00')
    this.generalcounter =parseFloat('00')
  }

  Searchorders() {
    this.pageurl= '/'
    this.setfieldvalue()
    this.currentpage = 1
  
    
    if(this.paymentmethodid !== "both"){
      // let lastindex:any=this.paymentmultyids.slice(-1)
      // this.paymentmultyids=this.commonfunc.filterArray(this.paymentmultyids)
      let temparray:any=this.paymentmethod.subtasks
      console.log("paymentmethod ids: ",this.paymentmethod.subtasks,temparray);
      this.advancedsearch=[]
      this.setcompleteparam()
      for(let i=0;i<temparray.length;i++){
        if(temparray[i].completed === true){
          console.log("paymentmethod ids true");
          this.advancedsearch.push({
            comparer: 1,
            field: "payment_method_id",
            field_id: 73,
            input_type: "select",
            key:temparray[i].id,
            key2: temparray[i].name,
            name: "payment_method_id",
            show_name: "Payment Method"})
        }
      }
    }
    if(this.rangeFormGroup.value.start !== null && this.rangeFormGroup.value.end !== null){
      this.getmonth = "nomonth"
      this.getyear= "2020";
      this.lastdate = this.datePipe.transform(this.rangeFormGroup.value.start, "yyyy-M-d")+"##"+this.datePipe.transform(this.rangeFormGroup.value.end, "yyyy-M-d");
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
    let data1: any = {
      'Total Orders': this.saleData.totalorder,
      'Subtotal': this.saleData.subtotal,
      'Shipping Costs': this.saleData.shippingcost,
      'Grand Total': this.saleData.grandtotal +" "+this.completelist['data']['currency_code']
    }
 
    if (this.saleData.totalorder !== 0) {
      let paramdata = ['Total Orders', 'Subtotal', 'Shipping Costs', 'Grand Total']
      // console.log("csv file : ", paramdata);
      temarray.push(data1)
      this.commonfunc.downloadFile(temarray, 'sales report', paramdata)
    } else {
      this.globalitem.showError("Orders not found ", "no Orders")
    }
  }

  cleardatefield(){
    this.rangeFormGroup.controls.start.setValue(null);
    this.rangeFormGroup.controls.end.setValue(null);
    const d = new Date();
    // alert(d.getMonth()+1);
    this.getmonth =d.getMonth()+1
    this.lastdate = this.getyear + "-" + this.getmonth + "-" + 1 + "##" + this.getyear + "-" + this.getmonth + "-" + this.getDaysInMonth(this.getmonth, this.getyear)
    this.Searchorders()
  }

  //checkbox
  updateAllComplete() {
    this.allComplete = this.paymentmethod.subtasks != null && this.paymentmethod.subtasks.every(t => t.completed);
    if(this.allComplete){
      console.log("all true");
      
      this.advancedsearch=[]
      this.setcompleteparam()
      this.paymentmethodid= this.paymentmethod.id;
      this.paymentmethodname=this.paymentmethod.name;
    }else if(!this.allComplete){
      
      this.paymentmethodid= this.paymentmethod.id;
      this.advancedsearch=[]
      this.setcompleteparam()
      console.log("not complete",this.paymentmethodid ,this.allComplete);
    }
    // console.log("not complete",this.paymentmethodid ,this.allComplete);
    // console.log("updateAll Complete : ",this.allComplete);
  }

  someComplete(): boolean {
    console.log("some completed : ");
    
    if (this.paymentmethod.subtasks == null) {
      return false;
    }
    let counter=0
    if(this.paymentmethod.subtasks.filter(t => t.completed).length > 0 && !this.allComplete){
      for(var i=0;i<this.paymentmethod.subtasks.length;i++){
        if(this.paymentmethod.subtasks[i].completed === true){
          counter++;
          this.paymentmethodid=this.paymentmethod.subtasks[i].id
          this.paymentmultyids.push(this.paymentmethod.subtasks[i].id)
          this.paymentmethodname=this.paymentmethod.subtasks[i].name
          // console.log("id : ",this.paymentmethod.subtasks[i].id);
          // console.log("counter value ",counter);
          // console.log("some  complete ",this.paymentmethodid);
        }else{
          // console.log("some not complete ",this.paymentmethodid);
          // this.paymentmethodid=this.paymentmethod.id
          // this.advancedsearch=[]
          // this.setcompleteparam()
          
        }
      }
    }else if(this.paymentmethod.subtasks.filter(t => t.completed).length === 0 && !this.allComplete){
      console.log("not all completed", this.paymentmethod.subtasks);
      this.advancedsearch=[]
      this.setcompleteparam()
    }
    
    return this.paymentmethod.subtasks.filter(t => t.completed).length > 0 && !this.allComplete;
  }

  setAll(completed: boolean) {
    this.paymentmethodid=this.paymentmethod.id
    this.paymentmethodname=this.paymentmethod.name
    // console.log("method complete : ",this.paymentmethodid);
    
    this.allComplete = completed;
    // console.log("setAll : ",this.allComplete);
    if(this.allComplete === false){
      this.advancedsearch=[]
      this. setcompleteparam()
    }
    if (this.paymentmethod.subtasks == null) { 
      return;
    }
    this.paymentmethod.subtasks.forEach(t => t.completed = completed);
  }
}
