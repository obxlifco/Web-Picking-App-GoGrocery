import { Injectable } from '@angular/core';
import { DatabaseService } from 'src/app/services/database/database.service';

@Injectable({
  providedIn: 'root'
})
export class CommonfunctionService {
 counter = 0;
  constructor(public db: DatabaseService) { }
  public warehouse_id: any = ''
  public website_id: any = ''
  data = {
    warehouse_id: '',
    website_id: ''
  }

  set setWarehouseIDS(val: any) {
    this.db.getUserData().then(res => {
      // console.log("user data inside dashboard : ", res);
      this.data.warehouse_id = res.warehouse_id,
        this.data.website_id = res.website_id
    })
  }
  get getWarehouseIDS(): any {
    return this.data;
  }

  getcompletedOrders(completeorderdata: any,paymentid:any): any {
    this.counter++
    // console.log("incoming data from page : ",completeorderdata, "Api counter : ",this.counter);
    
   
    let temarray: any = []
    let shpcost: any = 0;
    let subtotal: any = 0;
    let grandtotal: any = 0;
    // for (var i = 0; i < completeorderdata.length; i++) {
    //   // counter++;
    //   // if (completeorderdata[i].order_status === 4) {
    //   //   temarray.push(completeorderdata[i])
    //   // }
    //   if (completeorderdata.length === counter) {
    //     console.log("length is correct", temarray);
    //     if (temarray.length !== 0) {
    //       // this.completelist["data"] = temarray

    //       for (var i = 0; i < completeorderdata.length; i++) {
    //         shpcost += temarray[i].shipping_cost
    //         subtotal += temarray[i].net_amount
    //         grandtotal += temarray[i].gross_amount
    //       }
    //       // this.completelist["data"]["shippingcost"] = this.precise_round(shpcost, 2)
    //       // this.completelist["data"]["subtotal"] = this.precise_round(subtotal, 2)
    //       // this.completelist["data"]["grandtotal"] = this.precise_round(grandtotal, 2)
    //     } else {
    //       // this.setfieldvalue()
    //     }
    //     return 
    //   } else {
    //     // console.log("length is not correct");
    //   }
    // }
    for (var i = 0; i < completeorderdata.length; i++) {
      shpcost += completeorderdata[i].shipping_cost
      subtotal += completeorderdata[i].net_amount
      grandtotal += completeorderdata[i].gross_amount
      // console.log("shpcost : ",shpcost," subtotal:",subtotal," grandtotal: ",grandtotal);
      
    }
    let data={
      shpcost:shpcost,
      subtotal:subtotal,
      grandtotal:grandtotal,
    }
    return data
  }

  //round off price
  precise_round(num: any, decimals: any) {
    var t = Math.pow(10, decimals);
    return (Math.round((num * t) + (decimals > 0 ? 1 : 0) * (Math.sign(num) * (10 / Math.pow(100, decimals)))) / t).toFixed(decimals);
  }

  //download csv file
  
  //convert json to csv and download it
  downloadFile(data:any, filename='picker list',dataparams:any) {
    console.log("data : ",data,"params : ",dataparams);
    
    let csvData = this.ConvertToCSV(data, dataparams);
    console.log("csvData",csvData)
    let blob = new Blob(['\ufeff' + csvData], { type: 'text/csv;charset=utf-8;' });
    let dwldLink = document.createElement("a");
    let url = URL.createObjectURL(blob);
    let isSafariBrowser = navigator.userAgent.indexOf('Safari') != -1 && navigator.userAgent.indexOf('Chrome') == -1;
    if (isSafariBrowser) {  //if Safari open in new window to save file with random filename.
        dwldLink.setAttribute("target", "_blank");
    }
    dwldLink.setAttribute("href", url);
    dwldLink.setAttribute("download", filename + ".csv");
    dwldLink.style.visibility = "hidden";
    document.body.appendChild(dwldLink);
    dwldLink.click();
    document.body.removeChild(dwldLink);
}
ConvertToCSV(objArray:any, headerList:any) {
     let array = typeof objArray != 'object' ? JSON.parse(objArray) : objArray;
     let str = '';
     let row = 'S.No,';
for (let index in headerList) {
         row += headerList[index] + ',';
     }
     row = row.slice(0, -1);
     str += row + '\r\n';
     for (let i = 0; i < array.length; i++) {
         let line = (i+1)+'';
         for (let index in headerList) {
            let head = headerList[index];
line += ',' + array[i][head];
         }
         str += line + '\r\n';
     }
     return str;
 }


}
