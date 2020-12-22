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
  totalorders:any
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
    // this.apiService.postParamData("picker-dashboard/").subscribe((data: any[])=>{  
    //   console.log(data);   
    //   this.orderdata["data"]=data
    // })  

    this.db.getUserData().then(res => {
      // console.log("user data inside dashboard : ", res);

      let data = {
        warehouse_id: res.warehouse_id,
        website_id: res.website_id,
        order_status: 'complete',
      }
      this.apiService.postData("picker-dashboard/", data).subscribe((data: any[]) => {
        // console.log(data);
        this.orderdata["data"] = data
      })
    })
  }

  navigateOrder(orderstatus: any,value:any) {
    if(value !== 0){
      this.router.navigate(['dashboard/orders', { orderstatus: orderstatus }])
    }
    }
      
  navigatePocessingOrder() {
    if(this.orderdata['data'].processing_order !== 0){
    this.router.navigate(['dashboard/orders'])
    }
  }


  getcompleteCounter() {
    this.db.getUserData().then(res => {
      // console.log("payment method ID : ", this.rangeFormGroup.controls.paymentmethodid.value);
      let data = {
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
      this.apiService.postData("global_list/", data).subscribe((data: any) => {
        // console.log("completed Data : ",data.results[0].result);
        this.orderdata["data"]["completeorders"]=data.count
        if(data.results[0].result.length !== 0){
          // console.log("if conditions");
        this.totalorders = this.orderdata['data'].pending_order + this.orderdata['data'].pending_order +
          this.orderdata['data'].processing_order + this.orderdata['data']?.shipped_order +
          this.orderdata['data']?.cancel_order + this.orderdata['data']['completeorders'] 
          let data={
            cancelledorders:this.orderdata['data']?.cancel_order,
            completedOrders:this.orderdata['data']['completeorders'],
            totaloreders: this.totalorders
          }
          this.db.setcancellationRate(data)
        }else{
          this.totalorders = this.orderdata['data'].pending_order + this.orderdata['data'].pending_order +
          this.orderdata['data'].processing_order + this.orderdata['data']?.shipped_order +
          this.orderdata['data']?.cancel_order 
          // console.log("total orders : ",this.totalorders,this.orderdata['data'].pending_order);
          let data={
            cancelledorders:this.orderdata['data']?.cancel_order,
            completedOrders:this.orderdata['data']['completeorders'],
            totaloreders: this.totalorders
          }
          this.db.setcancellationRate(data)
        }
      })
    })
  }
}
