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
    const headers = {
      'content-type': 'application/json',
      'Authorization': 'Token 09c3b932ba526c5038c54a6c4995a229b9606cb6',
      // 'Accept': 'form-data'
    };
    return this.httpClient.post<any>(this.apiUrl + subUrl, data, { headers });
  }
  
  //post without token
  postwithoutTokenData(subUrl: string = "", data: any = []): any {
    const headers = {
      'content-type': 'application/json',
      // 'Accept': 'form-data' 
    };
    return this.httpClient.post<any>(this.apiUrl + subUrl, data, { headers });
  }


  public getIPAddress() {
    return this.httpClient.get("https://api.ipify.org/?format=json");
  }

  // tst
  
public upload(subUrl:any,formData:any) {
  const headers = {
    'Authorization': 'Token 09c3b932ba526c5038c54a6c4995a229b9606cb6',
    'Accept': 'text/plain, */*',
  };
      return this.httpClient.post<any>(this.apiUrl + subUrl, formData, { headers });
  }

  public updateData(subUrl:any,data:any) {
    const headers = {
      'Authorization': 'Token 09c3b932ba526c5038c54a6c4995a229b9606cb6',
      'content-type': 'application/json',
      'Accept':'application/json, text/plain, */*'
    };
        return this.httpClient.put<any>(this.apiUrl + subUrl, data, { headers });
    }
    
    // getfile
  getfileData() :any{
    let url ='http://www.gogrocery.ae:8062/media/importfile/sample/product_import_sheet.xls'
    const headers = {
      'content-type': 'application/json',
      // 'Authorization': 'Token 09c3b932ba526c5038c54a6c4995a229b9606cb6',
      // 'Accept': 'form-data' 
    };
    return this.httpClient.get(url, { headers });
  }
}
