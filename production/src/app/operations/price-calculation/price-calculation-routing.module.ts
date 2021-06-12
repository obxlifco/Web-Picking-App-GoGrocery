import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { PriceCalculationComponent } from './price-calculation.component';
import { PriceAddeditComponent } from './price.addedit.component';


const routes: Routes = [
  {
    path:'',component:PriceCalculationComponent
  },
  {
    path:'add',component:PriceAddeditComponent
  },
  {
    path:'edit/:id',component:PriceAddeditComponent
  },

];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class PriceCalculationRoutingModule { }
