import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BmscommonModule } from '../../bmscommon.module';
import { PurchaseOrderRoutingModule } from './purchaseorder-routing.module';
import { PurchaseOrderComponent }  from '../../inventory/purchase-order/inventory.purchase-order.component';
import { PurchaseOrderAddEditComponent,PurchaseOrderViewComponent,PurchaseOrderGrnComponent }  from '../../inventory/purchase-order/inventory.purchase-order.addedit.component';
import { SupplierProductsComponent, ScanItemComponent } from '../../inventory/purchase-order/inventory.purchase-order.addedit.component';
import { PoSentComponent, ShipTrackComponent, PoReceivedComponent } from '../../inventory/purchase-order/inventory.purchase-order.component';
@NgModule({
  imports: [
    CommonModule,
    BmscommonModule,
    PurchaseOrderRoutingModule,
  ],
  declarations: [
    PurchaseOrderComponent,
    PurchaseOrderAddEditComponent,
    PurchaseOrderViewComponent,
    PurchaseOrderGrnComponent,
    SupplierProductsComponent,
    ScanItemComponent,
    PoSentComponent,
    ShipTrackComponent,
    PoReceivedComponent
  ],
  entryComponents: [ 
  	PurchaseOrderComponent,
    PurchaseOrderAddEditComponent,
    PurchaseOrderViewComponent,
    PurchaseOrderGrnComponent,
    SupplierProductsComponent,
    ScanItemComponent,
    PoSentComponent,
    ShipTrackComponent,
    PoReceivedComponent
  ]
})
export class PurchaseOrderModule { }