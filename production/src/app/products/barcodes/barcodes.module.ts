import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BarcodesRoutingModule } from './barcodes-routing.module';
import { BarcodesComponent, BarcodeImportFileComponent, BarcodePreviewComponent } from './barcodes.component';
import { BarcodeaddeditComponent } from './barcodeaddedit.component';
import { ReactiveFormsModule} from '@angular/forms';
import { BmscommonModule } from '../../bmscommon.module';

@NgModule({
  declarations: [
  	BarcodesComponent, 
  	BarcodeaddeditComponent,
  	BarcodeImportFileComponent,
  	BarcodePreviewComponent,
  ],
  imports: [
    CommonModule,
    BarcodesRoutingModule,
    BmscommonModule,
    ReactiveFormsModule,
  ],
  entryComponents: [BarcodeImportFileComponent],
  
})
export class BarcodesModule { }
