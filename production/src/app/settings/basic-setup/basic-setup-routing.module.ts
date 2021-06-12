import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { BasicSetupAddEditComponent, BasicSetupTemplateComponent, BasicSetupPaymentGatewayComponent, BasicSetupTaxRateComponent, ChannelSetupAddEditComponent } from '../../settings/basic-setup/settings.basic-setup.addedit.component';
import { BasicSetupComponent, BasicSetupShippingComponent } from '../../settings/basic-setup/settings.basic-setup.component';
const routes: Routes = [
  { path: '', component: BasicSetupComponent },
  { path: 'add', component: BasicSetupAddEditComponent },
  { path: 'edit/:id', component: BasicSetupAddEditComponent },
  { path: 'edit/:id/template', component: BasicSetupTemplateComponent },
  { path: 'edit/:id/payment_gateway', component: BasicSetupPaymentGatewayComponent },
  { path: 'edit/:id/shipping', component: BasicSetupShippingComponent, data: { ship_type:1 }}, //1=flat ship,2=free shipping
  { path: 'edit/:id/free_shipping', component: BasicSetupShippingComponent, data: { ship_type:2 }},
  { path: 'edit/:id/tax', component: BasicSetupTaxRateComponent},
  { path: 'edit/:id/channel_setup', component: ChannelSetupAddEditComponent}
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class BasicSetupRoutingModule { }
