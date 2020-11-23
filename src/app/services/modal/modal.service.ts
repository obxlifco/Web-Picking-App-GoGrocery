import { Injectable } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { AddnewproductComponent } from 'src/app/components/addnewproduct/addnewproduct.component';
import { AddproductcategoryComponent } from 'src/app/components/addproductcategory/addproductcategory.component';
import { EditproductweightComponent } from 'src/app/components/editproductweight/editproductweight.component';
import { MapmodalComponent } from 'src/app/components/mapmodal/mapmodal.component';

@Injectable({
  providedIn: 'root'
})
export class ModalService {

  dialogRef: any;
  constructor(public dialog: MatDialog) { }

  async openCategoryModal(data: any) {
    this.dialogRef = this.dialog.open(AddnewproductComponent, {
      width: '500px',
      data: { data: data }
    });
  }

  async openSubCategoryModal(data: any) {
    this.dialogRef = this.dialog.open(AddproductcategoryComponent, {
      width: '500px',
      data: { data: data }
    });
  }

  async openModal(data: any,modalname:any) {
    this.dialogRef = this.dialog.open(modalname, {
      width: '50%',
      data: { data: data }
    });
  }

  async closeCategoryModal() {
    return this.dialogRef.afterClosed().subscribe((result: any) => {
      console.log('The dialog was closed in service page', result);
      return result;
    });
  }
}