import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { ApiService } from '../services/api/api.service';
import { from } from 'rxjs';
import { DatabaseService } from '../services/database/database.service';
import { OrdersComponent } from './pages/orders/orders.component';
@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit {

  orderdata: any = []
  constructor(public router: Router,
    public db: DatabaseService,
    public apiService: ApiService) {

  }

  ngOnInit(): void {
    this.getorderData();
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
      console.log("user data inside dashboard : ", res);

      let data = {
        warehouse_id: res.warehouse_id,
        website_id: res.website_id
      }
      this.apiService.postData("picker-dashboard/", data).subscribe((data: any[]) => {
        console.log(data);
        this.orderdata["data"] = data
      })
    })

  }

  navigateOrder(orderstatus:any){
    this.router.navigate(['orders',{orderstatus: orderstatus}])
  }
}
