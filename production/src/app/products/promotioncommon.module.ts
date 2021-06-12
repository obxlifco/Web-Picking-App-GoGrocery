import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PromotionAddEditComponent, PromotionPreviewComponent, ImportFileComponent, ExportFileComponent, FreeProductListComponent } from './promotion/products.promotion.addedit.component';
import { PromotionConditionsComponent, CategoryListComponent, ProductListComponent, CustomerListComponent, CustomerGroupListComponent, WeekListComponent } from './promotion/products.promotion.conditions.component';
import { BmscommonModule } from '../bmscommon.module';
import { DialogsService } from '../global/dialog/confirm-dialog.service';
import { CookieService } from 'ngx-cookie';
import { RouterModule } from '@angular/router';
import { OwlDateTimeModule, OwlNativeDateTimeModule } from 'ng-pick-datetime';
import { NgSelectModule } from '@ng-select/ng-select';
@NgModule({
  declarations: [
    PromotionAddEditComponent,
    PromotionConditionsComponent,
    PromotionPreviewComponent,
    ImportFileComponent,
    ExportFileComponent,
    CategoryListComponent,
    ProductListComponent,
    CustomerListComponent,
    CustomerGroupListComponent,
    WeekListComponent,
    CategoryListComponent,
    FreeProductListComponent
  ],
  imports: [
    CommonModule,
    BmscommonModule,
    RouterModule,
    OwlDateTimeModule, 
    OwlNativeDateTimeModule,
    NgSelectModule
  ],
  entryComponents: [
    ProductListComponent,
    CustomerListComponent,
    WeekListComponent,
    CustomerGroupListComponent,
    ImportFileComponent,
    CategoryListComponent,
    FreeProductListComponent
  ],
  exports:[
    BmscommonModule,
    PromotionAddEditComponent,
    PromotionConditionsComponent,
    PromotionPreviewComponent,
    ImportFileComponent,
    ExportFileComponent,
    CategoryListComponent,
    ProductListComponent,
    CustomerListComponent,
    CustomerGroupListComponent,
    WeekListComponent,
    FreeProductListComponent
  ],
  providers: [
    DialogsService, CookieService
],
})
export class PromotioncommonModule { }
