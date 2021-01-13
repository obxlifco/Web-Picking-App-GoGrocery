import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { ApiService } from 'src/app/services/api/api.service';
import { DatabaseService } from 'src/app/services/database/database.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {


  orderdata: any = []
  genericOrderData:any=[]
  totalorders: any;
  userdata: any = [];
  currentpage: any = 1;
  totalpagecounter:any=0
orderAttribute={
    completeorders:0,
    cancel_order:0,
    shipped_order:0,
    processing_order:0,
    pending_order:0,
  }
  pageurl: any = '/'
  constructor(public router: Router,
    public db: DatabaseService,
    public apiService: ApiService) {

  }

  ngOnInit(): void {
    this.getorderData();
    this.getcompleteCounter()
    // this.oredrcom.startcounter()
    this.orderdata["data"] = []
  }

  navigate(link: any) {
    this.router.navigate([link]);
  }
  returnpage() {
    this.router.navigate(["returns"]);
  }

  getorderData() {
    this.db.getUserData().then(res => {
      // console.log("user data inside dashboard : ", res);
      this.userdata = res
      let data = {
        warehouse_id: res.warehouse_id,
        website_id: res.website_id,
        // order_status: 'complete',
      }
      this.apiService.postData("picker-dashboard/", data).subscribe((data: any[]) => {
        // console.log(data);
        this.orderdata["data"] = data
      })
    })
  }

  navigateOrder(orderstatus: any, datavalue: any,key:any,value:any) {
    if (datavalue !== 0) {
      this.router.navigate(['dashboard/orders', { orderstatus: orderstatus,key :key,value:value }])
    }
  }

  navigatePocessingOrder(key:any,value:any) {
    // console.log("processing order : ", this.orderdata['data'].processing_order);

    if (this.orderdata['data'].processing_order + this.orderdata['data'].pending_order !== 0) {
      // this.router.navigate(['dashboard/orders',{ key :key,value:value }])
      this.router.navigate(['dashboard/orders', { orderstatus: 'In-Processing',key :key,value:value }])
    }
  }
  navigateNewOrder(key:any,value:any){
this.router.navigate(['dashboard/orders',{ key :key,value:value }])
  }

  getcompleteCounter() {
    var today = new Date();
    // console.log("New Date Is : 2020-03-27##" + today.getFullYear() + "-" + String(today.getMonth() + 1).padStart(2, '0') + "-" + String(today.getDate()).padStart(2, '0'));
    this.db.getUserData().then(res => {
      // console.log("payment method ID : ", this.rangeFormGroup.controls.paymentmethodid.value);
      let data: any;
      if (res.warehouse_id === null) {
        let data1 = {
          advanced_search: [{
            comparer: 1,
            field: "order_status",
            field_id: 76,
            input_type: "multi_select",
            key: [0, 100, 1, 2, 4],
            key2: "Pending,Processing,Shipped,Cancelled,Completed",
            name: "order_status",
            show_name: "Order Status",
          }],
          date: "2020-03-27##" + today.getFullYear() + "-" + String(today.getMonth() + 1).padStart(2, '0') + "-" + String(today.getDate()).padStart(2, '0'),
          warehouse_id: res.warehouse_id,
          website_id: res.website_id,
          user_id: res.user_id,
          model: "EngageboostOrdermaster",
          order_by: "",
          order_type: "",
          screen_name: "list",
          search: "",
          status: "",
          userid: res.user_id,
          warehouse_status: "",
        }
        data = data1
      } else {
        let data1 = {
          advanced_search: [{
            comparer: 1,
            field: "order_status",
            field_id: 76,
            input_type: "multi_select",
            key: [4],
            key2: "Completed",
            name: "order_status",
            show_name: "Order Status",
          }],
          warehouse_id: res.warehouse_id,
          website_id: res.website_id,
          date: "2020-03-27##" + today.getFullYear() + "-" + String(today.getMonth() + 1).padStart(2, '0') + "-" + String(today.getDate()).padStart(2, '0'),
          // per_page: 500,
          // page :1,
          user_id: res.user_id,
          model: "EngageboostOrdermaster",
          order_by: "",
          order_type: "",
          screen_name: "list",
          search: "",
          status: "",
          userid: res.user_id,
          warehouse_status: "",
        }
        data = data1
      }

      this.apiService.postData("global_list" + this.pageurl, data).subscribe((data: any) => {
        // console.log("completed Data : ",data.results[0].result);
        this.orderdata["data"]["completeorders"] = data.count
       if(res.warehouse_id === null || res.warehouse_id === ""){
        this.orderdata["data"]["completeorders"]=0
        this.getgenericData(data.results[0].result,data.count)
       }else{
        this.setOrderData(data.results[0].result)
       }

       if (this.currentpage > data.per_page_count) {
        this.currentpage = data.per_page_count
        // console.log("pages are equal",this.currentpage,data.per_page_count);
        
      } else if (data.per_page_count > this.currentpage) {
        this.currentpage++
        // console.log("current page : ",this.currentpage +" list page :",data.per_page_count);
        this.pageurl = "/?page=" + this.currentpage
        this.getcompleteCounter()
      }
      
      // this.setOrderData(data.results[0].result)
      })
    })
  }

  setOrderData(data:any[]){
   
    if (data.length !== 0) {
      this.totalorders = this.orderdata['data'].pending_order +
        this.orderdata['data'].processing_order + this.orderdata['data']?.shipped_order +
        this.orderdata['data']?.cancel_order + this.orderdata['data']['completeorders']
      let data = {
        cancelledorders: this.orderdata['data']?.cancel_order,
        completedOrders: this.orderdata['data']['completeorders'],
        totaloreders: this.totalorders
      }
      this.db.setcancellationRate(data)
    } else {
      this.totalorders = this.orderdata['data'].pending_order + this.orderdata['data'].pending_order +
        this.orderdata['data'].processing_order + this.orderdata['data']?.shipped_order +
        this.orderdata['data']?.cancel_order
      // console.log("total orders : ",this.totalorders,this.orderdata['data'].pending_order);
      let data = {
        cancelledorders: this.orderdata['data']?.cancel_order,
        completedOrders: this.orderdata['data']['completeorders'],
        totaloreders: this.totalorders
      }
      this.db.setcancellationRate(data)
    }
  }
  getgenericData(data:any=[],totaldatalength:any){
    // console.log("else is executed",data.length,this.orderdata['data']);
     this.totalpagecounter +=data.length
    for(let i=0;i<data.length;i++){
      // console.log("order status : ",data[i].order_status)
      if(data[i].order_status === 0){
        this.orderAttribute.pending_order++
      }else if(data[i].order_status === 100){
        this.orderAttribute.processing_order++
      }else if(data[i].order_status === 1){
        this.orderAttribute.shipped_order++
      }else if(data[i].order_status === 2){
        this.orderAttribute.cancel_order++
        // console.log("cancelorder : "+ this.orderdata['data'].cancel_order);
        
      }else if(data[i].order_status === 4){
        // compcounter++;
        this.orderAttribute.completeorders++
        // console.log("complete Order : ", this.orderdata['data']['completeorders'] );
        
      }

      // console.log("length : ",totaldatalength ," index: ",this.totalpagecounter);
      
      if(totaldatalength === this.totalpagecounter){
        this.orderdata['data'].pending_order = this.orderAttribute.pending_order
        this.orderdata['data'].processing_order= this.orderAttribute.processing_order
        this.orderdata['data'].shipped_order= this.orderAttribute.shipped_order
        this.orderdata['data'].cancel_order= this.orderAttribute.cancel_order
        this.orderdata['data']['completeorders']= this.orderAttribute.completeorders
        // console.log("else is executed",data.length,this.orderdata['data']);
        this.totalorders =  this.orderdata['data'].pending_order +
        this.orderdata['data'].processing_order + this.orderdata['data']?.shipped_order +
        this.orderdata['data']?.cancel_order + this.orderdata['data']['completeorders']
      let data2 = {
        cancelledorders: this.orderdata['data']?.cancel_order,
        completedOrders: this.orderdata['data']['completeorders'],
        totaloreders: this.totalorders
      }
      this.db.setcancellationRate(data2)
      }
    }
  }

 
}
