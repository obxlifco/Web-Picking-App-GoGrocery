import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { OrderhistoryComponent } from './orderhistory.component';
import { OrderdetailsComponent } from './orderdetails.component';
import { PaymentoptionComponent } from '../paymentoption/paymentoption.component';
import { ThankyouComponent } from './thankyou/thankyou.component';
import { WishlistComponent } from './wishlist/wishlist.component';
import { MyprofileComponent } from './myprofile/myprofile.component';
import {DeliveryaddressComponent} from './deliveryaddress/deliveryaddress.component';
import { ChangepasswordComponent } from './changepassword/changepassword.component';
import {MyWalletComponent} from './my-wallet/my-wallet.component';
import {SaveListComponent} from './save-list/save-list.component';
import {FailedorderComponent} from './failedorder/failedorder.component';
const routes: Routes = [
  {path : 'order-history',component :OrderhistoryComponent},
  {path : 'place-order',component :OrderdetailsComponent},
  {path : 'place-order/:slug',component :OrderdetailsComponent, data: { view_order:0 }},
  {path : 'view-order/:slug',component :OrderdetailsComponent, data: { view_order:1 }},
  {path : 'payment-options/:slug',component :PaymentoptionComponent, data:{page:'profile'}},
  {path : 'payment-options-approved/:order_id',component :PaymentoptionComponent, data:{page:'approved'}},
  {path : 'thank-you',component :ThankyouComponent},
  {path : 'thank-you/:order_id',component :ThankyouComponent},
  {path : 'failed-order/:order_id',component : FailedorderComponent},
  {path : 'wishlist',component :WishlistComponent},
  {path : 'my-wallet',component :MyWalletComponent},
  {path : 'profiledetails',component :MyprofileComponent},
  {path : 'delivery-address',component :DeliveryaddressComponent},
  {path : 'change-password',component :ChangepasswordComponent},
  {path : 'change-password',component :OrderdetailsComponent},
  {path : 'save-list',component : SaveListComponent}
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class OrderhistoryRoutingModule { }
