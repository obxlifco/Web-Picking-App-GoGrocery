import { Injectable } from '@angular/core';
import { Subscription, timer } from 'rxjs';
import { switchMap } from 'rxjs/operators';
import { AppComponent } from './app.component';
import { ApiService } from './services/api/api.service';
import { DatabaseService } from './services/database/database.service';

@Injectable({
  providedIn: 'root'
})
export class NotificationserviceService {

  subscription: Subscription | any;
  statusText: string  | any;
  constructor(public db : DatabaseService,
    public apiService:ApiService,
    ) { }

     //start time counter for getting latest orders
     startcounter(){
      this.db.getNotificationTime().then(res => {
        console.log("user timer : ", res);
        this.subscription = timer(0, res).pipe(
          switchMap(async () => {
            this.db.getOrderIDS().then(res => {
              this.getLatestOrder(res)})
              
          })
          
        ).subscribe(result =>{console.log("timer started");
        }
        );
      })
     
    
    }
     //unsubscribe timer
    destroyCounter(){
      this.subscription.unsubscribe();
    }
    getLatestOrder(orderData:any) {
      this.db.setOrderIDS(orderData)
      this.apiService.postData("picker-latestorders/", orderData).subscribe((data: any) => {
        console.log("latestorders : ", data);
        // this.appcom.setbadge(data.response.no_of_latest_order)
      })
    }
}
