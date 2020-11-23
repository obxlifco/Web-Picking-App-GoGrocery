import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { ApiService } from 'src/app/services/api/api.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {
  orderdata:any=[]
  constructor(public router: Router, public apiService: ApiService) {
   
   }

  ngOnInit(): void {
    this.getorderData();
    this.orderdata["data"]=[]
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
      
    // this.apiService.postParamData("picker-login/").subscribe((data: any[])=>{  
    //   console.log(data);   
    //   this.orderdata["data"]=data
    // })
    // this.apiService.postParamData("picker-dashboard/").then(data => {
    //   console.log("api data",data);
    // }).catch(error => {
    //   console.log("error :",error);
      
    // })
  }
}
