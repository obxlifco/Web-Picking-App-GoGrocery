import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { OrdersComponent } from 'src/app/dashboard/pages/orders/orders.component';
import { environment } from '../../../../src/environments/environment'
import { DatabaseService } from '../database/database.service';
import { GlobalitemService } from '../globalitem/globalitem.service';
@Injectable({
  providedIn: 'root'
})
export class ApiService {


  apiUrl: any = "http://www.gogrocery.ae:8062/api/"
  constructor(private httpClient: HttpClient
  ) {
  }

  getData(subUrl: any): any {
    const headers = {
      'content-type': 'application/json',
      'Authorization': 'Token 09c3b932ba526c5038c54a6c4995a229b9606cb6',
      // 'Accept': 'form-data' 
    };
    return this.httpClient.get(this.apiUrl + subUrl, { headers });
  }

  postData(subUrl: string = "", data: any = []): any {
    // console.log("api url is : ",this.apiUrl+subUrl);
    //  this.httpClient.post(this.apiUrl+subUrl,tempdata,
    //   {
    //     headers: {
    //       'content-type': 'application/json',
    //       'Authorization': 'Token 09c3b932ba526c5038c54a6c4995a229b9606cb6',
    //       'Accept': 'form-data',
    //       // 'data-raw' : 
    //   }
    // });

    const headers = {
      'content-type': 'application/json',
      'Authorization': 'Token 09c3b932ba526c5038c54a6c4995a229b9606cb6',
      // 'Accept': 'form-data' 
    };
    return this.httpClient.post<any>(this.apiUrl + subUrl, data, { headers });
  }

  //test for bulk data
  postbulkData(subUrl: string = "", data: any = [], file: File, event: any): any {
    const headers = {
      // 'content-type': 'application/json',
      'Authorization': 'Token 09c3b932ba526c5038c54a6c4995a229b9606cb6',
      // 'Content-Disposition': 'form-data; name="import_file"; filename="filename.xls"',
      //  'Content-Type': 'multipart/form-data',
      // 'Content-Type': 'multipart/form-data'
      // 'Content-Type': 'application/x-www-form-urlencoded;form-data; charset=UTF-8',      
      'Accept': 'text/plain, */*',
      'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryQ8kMlckU3idkYjqk'
    };
    let tempdata={
      import_file:event,
      website_id: '1',
      with_category: '0',
      import_file_type: 'product',
    }
    // const formData = new FormData();
    // let formData: FormData = new FormData(); 
    // formData.append("import_file_type", data.import_file_type);
    // formData.append("import_file", file,file.name);
    // formData.append("website_id", data.website_id);
    // formData.append("with_category", data.with_category);
    // console.log(formData.get("with_category"))
    // return this.httpClient.post<any>(this.apiUrl + subUrl, formData, { headers });

    // var FormData = require('form-data');
    // var request = require('request');
    var form = new FormData();
    form.append("import_file_type", data.import_file_type);
    form.append("import_file", file,file.name);
    form.append("website_id", data.website_id);
    form.append("with_category", data.with_category);
    return this.httpClient.post<any>(this.apiUrl + subUrl, form, { headers });
  }

  public getIPAddress() {
    return this.httpClient.get("https://api.ipify.org/?format=json");
  }

  // tst
  
public upload(subUrl:any,formData:any) {
  const headers = {
    // 'content-type': 'application/json',
    'Authorization': 'Token 09c3b932ba526c5038c54a6c4995a229b9606cb6',
    // 'Content-Disposition': 'form-data; name="import_file"; filename="filename.xls"',
    //  'Content-Type': 'multipart/form-data',
    // 'Content-Type': 'multipart/form-data'
    // 'Content-Type': 'application/x-www-form-urlencoded;form-data; charset=UTF-8',      
    'Accept': 'text/plain, */*',
    // 'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryQ8kMlckU3idkYjqk'
  };
      // return this.httpClient.post<any>(this.apiUrl + subUrl, formData, {
      //   reportProgress: true,
      //   observe: 'events',
      //   headers
      // });
      return this.httpClient.post<any>(this.apiUrl + subUrl, formData, { headers });
  }
}
