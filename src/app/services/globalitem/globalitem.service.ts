import { Injectable } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { AddnewproductComponent } from 'src/app/components/addnewproduct/addnewproduct.component';
import { AddproductcategoryComponent } from 'src/app/components/addproductcategory/addproductcategory.component';
import { ToastrService } from 'ngx-toastr';
import { NgxSpinnerService } from "ngx-spinner";
import { OrdersComponent } from 'src/app/dashboard/pages/orders/orders.component';
import { DatabaseService } from '../database/database.service';
export enum ToasterPosition {
  topRight = 'toast-top-right',
  topLeft = 'toast-top-left',
  bottomRight = 'toast-bottom-right',
  bottomLeft= 'toast-bottom-left',
  // Other positions you would like
}

@Injectable({
  providedIn: 'root'
})
export class GlobalitemService {

  dialogRef: any;
  toasterpositions:any='toast-bottom-right';


  constructor(public dialog: MatDialog,
    private toastr: ToastrService,
    private spinner: NgxSpinnerService,
    public db:DatabaseService
  ) { }

  // async openCategoryModal(data: any) {
  //   this.dialogRef = this.dialog.open(AddnewproductComponent, {
  //     width: '500px',
  //     data: { data: data }
  //   });
  // }

  // async openSubCategoryModal(data: any) {
  //   this.dialogRef = this.dialog.open(AddproductcategoryComponent, {
  //     width: '500px',
  //     data: { data: data }
  //   });
  // }

  // async closeCategoryModal() {
  //   return this.dialogRef.afterClosed().subscribe((result: any) => {
  //     console.log('The dialog was closed in service page', result);
  //     return result;
  //   });
  // }

  // spinner
  showSuccess(message:any, title:any) {
    this.toastr.success(message, title, {positionClass: this.toasterpositions})
  }

  showError(message:any, title:any) {
    this.toastr.error(message, title, { positionClass: this.toasterpositions })
  }

  showSpinner() {
    this.spinner.show();
  }
  hideSpinner() {
    this.spinner.hide();
  }
   
}
 