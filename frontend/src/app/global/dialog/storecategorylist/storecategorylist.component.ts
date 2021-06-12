import { Component, OnInit, Inject } from '@angular/core';
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { CookieService } from 'ngx-cookie';
import { WarehouseService } from '../../service/warehouse.service';
import { CartService } from '../../service/cart.service';
import { GlobalVariable } from '../../service/global';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
  selector: 'app-storecategorylist',
  templateUrl: './storecategorylist.component.html',
  styleUrls: ['./storecategorylist.component.css']
})
export class storecategorylistComponent implements OnInit {

  public selectedStoreCategoryDatails = {};
  public showConformationBox = 0;
  public storecategoryData: any;
  public storecategory_logo_url: any;
  public store_category_group_list = [];
  public sliderChecked: Boolean = true;
  public categoryID: any = [];
  all: boolean = false;
  constructor(
    public dialogRef: MatDialogRef<storecategorylistComponent>,
    public dialogRefConform: MatDialogRef<storecategorylistComponent>,
    private _wareHouseService: WarehouseService,
    private _cookieService: CookieService,
    public cartService: CartService,
    private router: Router,
    @Inject(MAT_DIALOG_DATA) public storecategorylist
  ) {
    console.log("*************** Store Categorylist list data *****************");
    console.log(this.storecategorylist);
    this.storecategorylist.map(item => item['checked'] = true);
    this.storecategorylist.forEach(element => {
      this.categoryID.push(element.id)
    });
    this.all = true;

  }

  ngOnInit() {
    this.selectedStoreCategoryDatails = this._cookieService.getObject('current_user_location') ? this._cookieService.getObject('current_user_location') : {};
    this.storecategory_logo_url = GlobalVariable.S3_URL + "storecategorylogo/800x800/";
    console.log(this.storecategorylist);
    let clone_header_list = this.storecategorylist.slice(0);
    console.log(clone_header_list)
    this.store_category_group_list = this.groupingArray(clone_header_list, 3);
    console.log(this.store_category_group_list);
  }

  groupingArray(array = [], chunk) {

    var i, j, temparray, groupedArray = [];
    if (array.length == 0) {
      return array;
    }
    for (i = 0, j = array.length; i < j; i += chunk) {
      temparray = array.slice(i, i + chunk);
      groupedArray.push(temparray);
    }
    return groupedArray;
  }

  // onStoreCategorySelect(storecategoryID,storecategoryName,hasError) {
  //   console.log(hasError,'hasError')
  //   if(storecategoryID) {
  //     console.log(hasError,'hasError')
  //   	this.storecategoryData = {
  //   		 storecategoryID : storecategoryID,
  //   		 storecategoryName : storecategoryName
  //     }
  //     console.log(this.selectedStoreCategoryDatails);
  //     this.dialogRef.close(this.storecategoryData);
  //   }
  // }
  selectAll(ev) {
    this.categoryID = [];
    if (ev.checked) {
      this.storecategorylist.forEach(element => {
        this.categoryID.push(element.id)
      });
    }

    this.storecategorylist.map(item => item['checked'] = ev.checked);
  }
  onChange(storecategoryID, checked) {
    this.storecategorylist.map(item => {
      if (item.id === storecategoryID) {
        item['checked'] = !item['checked'];
      }
    });
    if (checked) {
      this.categoryID.push(storecategoryID);
    }
    else {
      let index = this.categoryID.indexOf((storecategoryID));
      if (index !== -1) {
        this.categoryID.splice(index, 1);
      }
    }
    let uncheckedval = this.storecategorylist.find(x => (x.checked == false));
    if (uncheckedval) {
      this.all = false;
    }
    else {
      this.all = true
    }



  }
  startShopping() {
    this.storecategoryData={
      storecategoryID:this.categoryID
    }
  
    if (this.sliderChecked = true) {
      this.dialogRef.close(this.storecategoryData);
    }
  }
  // isStoreCategoryChange(type:number=0){
  //   if(type==1){
  //     // alert('Empty cart');
  //     this.cartService.emptyCart();
  //     this.dialogRef.close(this.wareHouseData);
  //     this.router.navigate(['/']);      
  //   }else{
  //     this.dialogRef.close();
  //   }
  // }
  close_dialog() {
    this.dialogRef.close();
  }
}
