import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { BmscommonModule } from '../../bmscommon.module';

import { CategoryComponent, ExportCategoryFile }  from '../../products/category/products.category.component';
import { CategoryAddEditComponent,CategoryCustomFieldComponent, }  from '../../products/category/products.category.addedit.component';
import { CategoryAddEditCustomFieldComponent, CategoryImportCustomFieldComponent, CategoryImportPreviewComponent, MarketplaceCategoryChooseComponent } from '../../products/category/products.category.addedit.component';
import { CategoryRoutingModule } from './category-routing.module';
import {FormsModule,ReactiveFormsModule} from '@angular/forms';
import { NgSelectModule } from '@ng-select/ng-select';

@NgModule({
  declarations: [
      CategoryComponent,
      CategoryAddEditComponent,
      CategoryCustomFieldComponent,
      CategoryAddEditCustomFieldComponent,
      CategoryAddEditCustomFieldComponent, 
      CategoryImportCustomFieldComponent,
      CategoryImportPreviewComponent, 
      MarketplaceCategoryChooseComponent,
      ExportCategoryFile,
  ],
  imports: [
    CommonModule,
    CategoryRoutingModule,
    BmscommonModule,
    FormsModule,
    ReactiveFormsModule,
    NgSelectModule
  ],
    entryComponents: [
      CategoryCustomFieldComponent,
      CategoryAddEditCustomFieldComponent,
      CategoryAddEditCustomFieldComponent, 
      CategoryImportCustomFieldComponent,
      CategoryImportPreviewComponent, 
      MarketplaceCategoryChooseComponent,
      ExportCategoryFile
    ]
})
export class CategoryModule { }
