import { Inject, Injectable } from '@angular/core';
import {LocalStorageService} from 'ngx-webstorage';

@Injectable({
  providedIn: 'root'
})
export class DatabaseService {

  STORAGE_KEY: any = "cartlist"
  USER_DATA:any="user";
  IP_ADDRESS:any="userip"
  NOTIFICATION_TIME:any="notiTime"
  ORDER_IDS:any="orderids"
  AVERAGE_DATA:any="aeveragedata"//for sae report

  constructor(private storage:LocalStorageService) { }

  setUserData(data: any) {
    // console.log("data inside :", data);
    this.storage.store(this.USER_DATA, data);
  }

  async getUserData() {
    return this.storage.retrieve(this.USER_DATA)
  }
  
  clearstorage() {
    this.storage.clear(this.USER_DATA);
  }

  // Returns true when user is looged in and email is verified
  isLoggedIn(): boolean {
    const user =this.storage.retrieve(this.USER_DATA);
    return (user !== null) ? true : false;
  }

  setToken(token:any){
    // this.storage.store(this.USER_TOEKN, token);
  }

  // Sign out
  SignOut() {
    this.storage.store(this.USER_DATA, null);
  }

  // Ip Address data
  setIP(data:any){
    this.storage.store(this.IP_ADDRESS, data);
  }

  async getIP(){
    return this.storage.retrieve(this.IP_ADDRESS)
  }

  //set notification time for api calling
  setNotificationTime(data: any) {
    // console.log("data inside :", data);
    this.storage.store(this.NOTIFICATION_TIME, data);
  }

  async getNotificationTime() {
    let data=this.storage.retrieve(this.NOTIFICATION_TIME)
    // console.log("timer data : ",data);
    
    if(data === null){
      return 5*60000 
    }else{
      return data
    }
  }

  //store latest ids for notifications
  setOrderIDS(data: any) {
    // console.log("data inside :", data);
    this.storage.store(this.ORDER_IDS, data);
  }
  async getOrderIDS() {
    return this.storage.retrieve(this.ORDER_IDS)
  }
  //set cancellation rates

  setcancellationRate(data:any){
    this.storage.store(this.AVERAGE_DATA, data);
  }
  async getcancellationRate(){
    return this.storage.retrieve(this.AVERAGE_DATA)
  }
  
}
