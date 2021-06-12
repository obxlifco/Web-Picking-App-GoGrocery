import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import {FormsModule,ReactiveFormsModule} from '@angular/forms';
import { OrderhistoryRoutingModule } from './orderhistory-routing.module';
import { OrderhistoryComponent } from './orderhistory.component';
import { OrderdetailsComponent } from './orderdetails.component';
import { PaymentoptionComponent } from '../paymentoption/paymentoption.component';
import { MaterialModule } from '../../../global/modules/material.module';
import { PipeModule } from '../../../global/pipes/pipe.module';
import { ThankyouComponent } from './thankyou/thankyou.component';
import { WishlistComponent } from './wishlist/wishlist.component';
import { MyprofileComponent } from './myprofile/myprofile.component';
import { CancelreasonComponent } from './cancelreason/cancelreason.component';
import { DeliveryaddressComponent } from './deliveryaddress/deliveryaddress.component';
import {CheckoutModule} from '../../checkout/checkout.module';
import { ChangepasswordComponent } from './changepassword/changepassword.component';
import { MyWalletComponent } from './my-wallet/my-wallet.component';
import { LeftPanelProfileComponent } from './left-panel-profile/left-panel-profile.component';
import { SaveListComponent } from './save-list/save-list.component';
import { CreditCardDirectivesModule } from 'angular-cc-library';
import { NgSelectModule } from '@ng-select/ng-select';
import { FailedorderComponent } from './failedorder/failedorder.component';

@NgModule({
  declarations: [
    OrderhistoryComponent,
    OrderdetailsComponent, 
    PaymentoptionComponent,
    ThankyouComponent,WishlistComponent,
    MyprofileComponent,
    CancelreasonComponent,
    DeliveryaddressComponent,
    PaymentoptionComponent, 
    WishlistComponent, 
    MyprofileComponent, 
    CancelreasonComponent, 
    ChangepasswordComponent,
     MyWalletComponent, 
     LeftPanelProfileComponent, 
     SaveListComponent, FailedorderComponent,
  ],
  imports: [
    CommonModule,
    OrderhistoryRoutingModule,
    MaterialModule,
    PipeModule,
    FormsModule,
    ReactiveFormsModule,
    CheckoutModule,
    CreditCardDirectivesModule,
    NgSelectModule

  ],
  entryComponents: [
    CancelreasonComponent,
  ]
})
export class OrderhistoryModule { }
