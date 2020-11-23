import { Injectable } from '@angular/core';
import { DatabaseService } from '../services/database/database.service';

@Injectable({
  providedIn: 'root'
})
export class CommonfunctionService {

  constructor(public db: DatabaseService) { }
  public warehouse_id: any = ''
  public website_id: any = ''
   data = {
    warehouse_id:'',
    website_id: ''
  }

  set setWarehouseIDS(val: any) {
    this.db.getUserData().then(res => {
      console.log("user data inside dashboard : ", res);
      this.data.warehouse_id = res.warehouse_id,
        this.data.website_id = res.website_id
    })
  }
  get getWarehouseIDS(): any {
    return this.data;
  }

}
