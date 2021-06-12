import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { BarcodesComponent, BarcodePreviewComponent } from './barcodes.component';
import { BarcodeaddeditComponent } from './barcodeaddedit.component';

const routes: Routes = [
  {
    path:'',
    component:BarcodesComponent
  },
  {
    path:'add',
    component:BarcodeaddeditComponent
  },
  {
    path:'edit/:id',
    component:BarcodeaddeditComponent
  },
  {
    path:'preview_barcodes',
    component:BarcodePreviewComponent
  },

];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class BarcodesRoutingModule { }
