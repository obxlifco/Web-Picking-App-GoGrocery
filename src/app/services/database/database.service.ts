import { Inject, Injectable } from '@angular/core';
import {LocalStorageService} from 'ngx-webstorage';

@Injectable({
  providedIn: 'root'
})
export class DatabaseService {

  STORAGE_KEY: any = "cartlist"
  USER_DATA:any="user";
  IP_ADDRESS:any="userip"

  constructor(private storage:LocalStorageService) { }

  setUserData(data: any) {
    console.log("data inside :", data);
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
}
