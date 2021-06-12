import { Component,OnInit,Inject} from '@angular/core';
import {MatDialog, MatDialogRef, MAT_DIALOG_DATA} from '@angular/material/dialog';
import { CookieService } from 'ngx-cookie';
import { WarehouseService } from '../../service/warehouse.service';
import { CartService } from '../../service/cart.service';
import { GlobalVariable } from '../../service/global';
import { ActivatedRoute, Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-warehouselist',
  templateUrl: './warehouselist.component.html',
  styleUrls: ['./warehouselist.component.css']
})
export class WarehouselistComponent implements OnInit {

	public selectedWareHouseDatails = {};
  public showConformationBox=0;
  public wareHouseData:any;
  public warehouse_logo_url:any;
  public ipAddress;
  public cartCount = 0;
  constructor(
    public dialogRef: MatDialogRef<WarehouselistComponent>,
    public dialogRefConform: MatDialogRef<WarehouselistComponent>,
		private _wareHouseService : WarehouseService,
		private _cookieService: CookieService,
    public cartService:CartService,
    private router: Router,
    private http: HttpClient,
    @Inject(MAT_DIALOG_DATA) public warehouseList
    ) {
  	 console.log("*************** Warehouse list data *****************");
  	 console.log(this.warehouseList);


  }

  ngOnInit() {
		this.selectedWareHouseDatails = this._cookieService.getObject('current_user_location') ? this._cookieService.getObject('current_user_location') : {};
    this.warehouse_logo_url = GlobalVariable.S3_URL+"warehouselogo/800x800/";
    this.getCartData();
  }

  getCartData(){
    this.cartService.initiateCartData();
    this.http.get<{ip:string}>('https://api6.ipify.org?format=json')
    .subscribe( data => {
      this.ipAddress = data && data['ip'] ? data['ip'] : '';
      this._cookieService.put('client_ip',this.ipAddress);
      console.log("*************** Client ip address ***************");
      console.log(this.ipAddress);
      this.fetchCardDetails(this.ipAddress);
    })
  }

  fetchCardDetails(requestedIp){
    this.cartService.requestedIp = requestedIp;

    this.cartService.getCartDetails().subscribe(response => {
      if (response && response['status'] == 200) {
        console.log(response,'Cart Response')
        this.cartCount = response.cart_count;
      }
    });
  }

  onWareHouseSelect(warehouseId,warehouseName) {
    if(warehouseId) {
    	this.wareHouseData = {
    		 warehouseId : warehouseId,
    		 warehouseName : warehouseName
      }
      console.log('this.selectedWareHouseDatails');
      console.log(this.selectedWareHouseDatails['selected_warehouse_name']);
      console.log('this.selectedWareHouseDatails');
      if(this.selectedWareHouseDatails['selected_warehouse_name']!=undefined){

        if(this.selectedWareHouseDatails['selected_warehouse_name']==warehouseName){
          this.dialogRef.close(this.wareHouseData);
          this.router.navigate(['/']);
        }else{
          // alert('Warehouse changed');
          console.log(this.cartCount,'cartCount')
          if(this.cartCount > 0 ){
            this.showConformationBox=1;
          } else{
            this.isWarehouseChange(1);
          }
        }
      }else{
        this.dialogRef.close(this.wareHouseData);
        console.log('First time');
        this.router.navigate(['/']);
      }
    }
  }

  isWarehouseChange(type:number=0){
    if(type==1){
      // alert('Empty cart');
      this.cartService.emptyCart();
      this.dialogRef.close(this.wareHouseData);
      this.router.navigate(['/']);      
    }else{
      this.dialogRef.close();
    }
  }
  close_dialog(){
    this.dialogRef.close();
  }
}
