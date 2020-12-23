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

  headerlist:any
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

  getcompletedOrders(completeorderdata: any, paymentid: any): any {
    let shpcost: any = 0;
    let subtotal: any = 0;
    let grandtotal: any = 0;
    let shippingdiscount:any=0;
    let coupendiscount:any=0;
    let counters:any=0
    for (var i = 0; i < completeorderdata.length; i++) {
      if(!completeorderdata[i]?.customer?.first_name?.includes("Test") && !completeorderdata[i]?.customer?.first_name?.includes("test")&& 
      !completeorderdata[i]?.customer?.last_name?.includes("Test") && !completeorderdata[i]?.customer?.last_name?.includes("test")){
        // console.log("name entered is : ",completeorderdata[i].customer.first_name);
        
        shpcost += completeorderdata[i].shipping_cost
        subtotal += completeorderdata[i].net_amount
        grandtotal += completeorderdata[i].gross_amount
        shippingdiscount += completeorderdata[i].cart_discount
        coupendiscount += completeorderdata[i].gross_discount_amount 
      }else{
        counters++
        // console.log("test name entered is : ",completeorderdata[i].customer.first_name);
      }
      // console.log("shpcost : ",shpcost," subtotal:",subtotal," grandtotal: ",grandtotal);
    }
    let data = {
      shpcost: shpcost,
      subtotal: subtotal,
      grandtotal: grandtotal,
      totalList: completeorderdata,
      testorderFound:counters,
      shippingdiscount:shippingdiscount,
      coupendiscount:coupendiscount
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
  downloadFile(data: any, filename = 'picker list', dataparams: any,footerdata:any) {
    // console.log("data : ", data, "params : ", dataparams);
    let csvData = this.ConvertToCSV(data, dataparams);
    // console.log("csvData", csvData + '\r\n'+" Total Amount,"+"ordernum,"+"orderdate,"+"cname,"+"pmethod,"+"122323,"+"123,"+"0,"+"11,"+"333432211" ," header list :",this.headerlist)
    if(filename === "order products"){
      csvData = csvData + '\r\n'+" Total Amount,"+","+","+","+","+footerdata.Subtotal+","+footerdata.ShippingCost+","+footerdata.ShippingDiscount+","+footerdata.OtherDiscount+","+footerdata.GrandTotal
    }
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
  ConvertToCSV(objArray: any, headerList: any) {
    let array = typeof objArray != 'object' ? JSON.parse(objArray) : objArray;
    let str = '';
    let row = 'S.No,';
    for (let index in headerList) {
      row += headerList[index] + ',';
    }
    row = row.slice(0, -1);
    this.headerlist=row
    str += row + '\r\n';
    for (let i = 0; i < array.length; i++) {
      let line = (i + 1) + '';
      for (let index in headerList) {
        let head = headerList[index];
        line += ',' + array[i][head];
      }
      str += line + '\r\n';
    }
    return str;
  }

  monthname: any = [
    {
      "abbreviation": "Jan",
      "name": "January"
    },
    {
      "abbreviation": "Feb",
      "name": "February"
    },
    {
      "abbreviation": "Mar",
      "name": "March"
    },
    {
      "abbreviation": "Apr",
      "name": "April"
    },
    {
      "abbreviation": "May",
      "name": "May"
    },
    {
      "abbreviation": "Jun",
      "name": "June"
    },
    {
      "abbreviation": "Jul",
      "name": "July"
    },
    {
      "abbreviation": "Aug",
      "name": "August"
    },
    {
      "abbreviation": "Sep",
      "name": "September"
    },
    {
      "abbreviation": "Oct",
      "name": "October"
    },
    {
      "abbreviation": "Nov",
      "name": "November"
    },
    {
      "abbreviation": "Dec",
      "name": "December"
    }
  ]

  filterArray(array: any = []): any {
    return array.filter(function (elem: any, index: any, self: string | any[]) {
      return index === self.indexOf(elem);
    })
  }
}
