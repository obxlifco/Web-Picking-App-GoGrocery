import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {CheckoutComponent} from './checkout.component';
import {SuccessComponent} from './pages/success/success.component';

const routes: Routes = [
 {path : '',component : CheckoutComponent},
 {path : 'success/:id',component : SuccessComponent}


];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class CheckoutRoutingModule { }
