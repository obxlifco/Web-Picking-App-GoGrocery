import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { HsnCodeComponent } from '../../products/hsncode/products.hsncode.component';
import { HsnCodeAddEditComponent } from '../../products/hsncode/products.hsncode.addedit.component';

const routes: Routes = [
  {
    path:'',
    component:HsnCodeComponent
  },
  {
    path:'add',
    component:HsnCodeAddEditComponent
  },
  {
    path:'edit/:id',
    component:HsnCodeAddEditComponent
  },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class HsncodeRoutingModule { }
