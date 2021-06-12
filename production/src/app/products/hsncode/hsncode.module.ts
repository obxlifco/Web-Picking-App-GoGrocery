import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HsncodeRoutingModule } from './hsncode-routing.module';
import { BmscommonModule } from '../../bmscommon.module';
// import { GloballistComponent } from '../../globallist/globallist.component';
import { HsnCodeComponent } from './products.hsncode.component';
import { HsnCodeAddEditComponent, HsnCodeImportComponent } from './products.hsncode.addedit.component';

@NgModule({
  declarations: [
  // GloballistComponent,
  HsnCodeComponent,
  HsnCodeAddEditComponent,
  HsnCodeImportComponent,
  ],
  imports: [
    CommonModule,
    HsncodeRoutingModule,
    BmscommonModule
  ],
  entryComponents: [
    HsnCodeImportComponent
  ],

})
export class HsncodeModule { }