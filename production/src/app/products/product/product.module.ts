import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BmscommonModule } from '../../bmscommon.module';
import { ProductRoutingModule } from './product-routing.module';
import { NgxBarcodeModule } from 'ngx-barcode';
import { ChartsModule } from 'ng2-charts';
import { DndModule } from 'ng2-dnd';
import { ProductComponent, ProductDetailsComponent,ProductPreviewComponent }  from '../../products/product/products.product.component';
import { ImageReorderDialog, ProductPriceComponent, AddPriceTypeMasterComponent, SupplierList, VariantProductComponent, ImportProductPriceImportComponent, ProductPricePreviewComponent  } from '../../products/product/products.product.addedit.component';
import { ImportProductComponent, ShowMapFieldsComponent, ExportProductComponent } from '../../products/product/products.product.component';
import { ProductBasicInfoComponent,ProductAdvanceInfoComponent,ProductDefaultPriceComponent,ProductRelatedComponent,ProductSubstituteComponent,ProductSupplierComponent, ProductPriceSetupComponent,ProductVariantListComponent} from '../../products/product/products.product.addedit.component';
import { OwlDateTimeModule, OwlNativeDateTimeModule } from 'ng-pick-datetime';
import { NgxDaterangepickerMd } from 'ngx-daterangepicker-material';
import { NgxMatSelectSearchModule } from 'ngx-mat-select-search';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
// Import angular-fusioncharts
import { FusionChartsModule } from 'angular-fusioncharts';
// Import FusionCharts library
import * as FusionCharts from 'fusioncharts';
// Load FusionCharts Individual Charts
import * as Charts from 'fusioncharts/fusioncharts.charts';
import * as FusionTheme from 'fusioncharts/themes/fusioncharts.theme.fusion';
import { NgSelectModule } from '@ng-select/ng-select';
FusionChartsModule.fcRoot(FusionCharts, Charts,FusionTheme)
@NgModule({
  declarations: [
    ProductComponent,
    ProductDetailsComponent,
    ProductPreviewComponent,
    ImageReorderDialog,
    ProductPriceComponent,
    ImportProductComponent,
    ShowMapFieldsComponent,
    ProductBasicInfoComponent,
    ProductAdvanceInfoComponent,
    ProductDefaultPriceComponent,
    ProductSupplierComponent,
    ProductPriceSetupComponent,
    ProductRelatedComponent,
    ProductSubstituteComponent,
    AddPriceTypeMasterComponent,
    VariantProductComponent,
    SupplierList,
    ProductVariantListComponent,
    ExportProductComponent,
    ImportProductPriceImportComponent,
    ProductPricePreviewComponent,
  ],
  imports: [
    CommonModule,
    ProductRoutingModule,
    FormsModule,
    BmscommonModule,
    NgxBarcodeModule,
    ChartsModule,
    DndModule.forRoot(),
    OwlDateTimeModule,
    OwlNativeDateTimeModule,
    NgxMatSelectSearchModule,
    ReactiveFormsModule,
    FusionChartsModule,
    NgxDaterangepickerMd,
    NgSelectModule
  ],
  entryComponents: [
    AddPriceTypeMasterComponent,
    ProductPriceComponent,
    ImageReorderDialog,
    ImportProductComponent,
    ShowMapFieldsComponent,
    ProductPreviewComponent,
    ProductSupplierComponent,
    SupplierList,
    ProductVariantListComponent,
    ExportProductComponent,
    ImportProductPriceImportComponent
  ]
})
export class ProductModule { }