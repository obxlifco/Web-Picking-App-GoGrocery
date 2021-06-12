import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AuthGuard } from '../../global/service/auth-guard.service';

import { ShipmentComponent, PicklistComponent }  from '../../order/shipment/order.shipment.component';
import { ShipmentAddEditComponent, ShipmentInvoiceComponent,ShipmentLabelComponent,DeliveryPlannerComponent,ShipmentManifestComponent,}  from '../../order/shipment/order.shipment.addedit.component';
const routes: Routes = [	
    // picklist
    { path: '', component:PicklistComponent },
    { path: 'picklist', component:ShipmentAddEditComponent },
    { path: 'picklist/:id', component:ShipmentAddEditComponent },
    { path: 'grn/:id', component:ShipmentLabelComponent },
    { path: 'invoice/:id', component:ShipmentInvoiceComponent },
    // shipment
    { path: 'shipment', component:ShipmentComponent },
    { path: 'manifest/:id', component:ShipmentManifestComponent },
    { path: 'delivery_planner/:id', component:DeliveryPlannerComponent },
 ];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [
      RouterModule
  ]
})
export class ShipmentRoutingModule { }