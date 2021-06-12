import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BasicSetupRoutingModule } from './basic-setup-routing.module';
import { BmscommonModule } from '../../bmscommon.module';

import { BasicSetupComponent, BasicSetupShippingComponent } from '../../settings/basic-setup/settings.basic-setup.component';
import { BasicSetupAddEditComponent, BasicSetupTemplateComponent, BasicSetupPaymentGatewayComponent, BasicSetupTaxRateComponent, ChannelSetupAddEditComponent } from '../../settings/basic-setup/settings.basic-setup.addedit.component';
import { FlatShipAddEditComponent, AmazonAuthenticationComponent, FlipkartAuthenticationComponent, SnapdealAuthenticationComponent, PaytmAuthenticationComponent, EbayAuthenticationComponent, TableRateAddEditComponent ,FreeShippingComponent , CODZipcodeComponent} from '../../settings/basic-setup/settings.basic-setup.addedit.component';
import { NgSelectModule } from '@ng-select/ng-select';

@NgModule({
  imports: [
    CommonModule,
    BasicSetupRoutingModule,
    BmscommonModule,
    NgSelectModule
  ],
  declarations: [
      BasicSetupAddEditComponent,
      BasicSetupComponent,
      BasicSetupTemplateComponent,
      BasicSetupPaymentGatewayComponent,
      BasicSetupTaxRateComponent,
      ChannelSetupAddEditComponent,
      BasicSetupShippingComponent,
      FlatShipAddEditComponent,
      AmazonAuthenticationComponent,
      FlipkartAuthenticationComponent,
      SnapdealAuthenticationComponent,
      PaytmAuthenticationComponent,
      EbayAuthenticationComponent,
      TableRateAddEditComponent,
      FreeShippingComponent,
      CODZipcodeComponent
      
  ],
  entryComponents: [
      FlatShipAddEditComponent,
      BasicSetupTemplateComponent,
      BasicSetupPaymentGatewayComponent,
      BasicSetupTaxRateComponent,
      ChannelSetupAddEditComponent,
      AmazonAuthenticationComponent,
      FlipkartAuthenticationComponent,
      SnapdealAuthenticationComponent,
      PaytmAuthenticationComponent,
      EbayAuthenticationComponent,
      TableRateAddEditComponent,
      FreeShippingComponent,
      CODZipcodeComponent
      
  ]
})
export class BasicSetupModule { }
